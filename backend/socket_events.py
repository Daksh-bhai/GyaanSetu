from flask_socketio import SocketIO, join_room, leave_room, emit
from flask import request as flask_request
from models.session_model import sessions
from models.user_model import users
from utils.jwt_utils import verify_token
from bson import ObjectId
import datetime

# ================================================================
# SOCKET EVENTS — Chat + WebRTC Signaling
#
# Flow:
# 1. User joins room via session_id
# 2. Both users in room → session_started_at recorded in DB
# 3. Chat messages broadcast to room
# 4. WebRTC: offer/answer/ice-candidate relayed via socket
#
# FIX: session_started_at is set when BOTH users join the room,
#      not when the tutor accepts the request (accepted_at).
#      This is the correct start time for the session timer.
# ================================================================

socketio = SocketIO(cors_allowed_origins="*", async_mode="threading")


def init_socketio(app):
    socketio.init_app(app)
    return socketio


# ── Active rooms tracker (in-memory) ─────────────────────────
# room_id → { user_id: { name, email, joined_at } }
active_rooms = {}

# sid (socket id) → { session_id, user_id }
# Used to clean up `active_rooms` on disconnect so stale entries don't
# prematurely start session timers.
active_sockets = {}


def _get_user_from_token(token):
    if not token:
        return None
    user_id = verify_token(token)
    if not user_id:
        return None
    user = users.find_one({"_id": ObjectId(user_id)}, {"name": 1, "email": 1})
    if not user:
        return None
    return {"user_id": user_id, "name": user.get("name"), "email": user.get("email")}


# ================================================================
# JOIN ROOM
# ================================================================
@socketio.on("join_session")
def handle_join(data):
    """
    data: { session_id, token }
    """
    token      = data.get("token")
    session_id = data.get("session_id")

    user = _get_user_from_token(token)
    if not user:
        emit("error", {"message": "Unauthorized"})
        return

    # Verify user is part of this session
    try:
        session = sessions.find_one({"_id": ObjectId(session_id)})
    except Exception:
        emit("error", {"message": "Invalid session id"})
        return

    if not session:
        emit("error", {"message": "Session not found"})
        return

    uid = user["user_id"]
    if uid not in [session["learner_id"], session["tutor_id"]]:
        emit("error", {"message": "You are not part of this session"})
        return

    if session["status"] != "accepted":
        emit("error", {"message": "Session is not active"})
        return

    # Join the socket room
    join_room(session_id)

    # Track in memory
    if session_id not in active_rooms:
        active_rooms[session_id] = {}
    active_rooms[session_id][uid] = {
        "name"      : user["name"],
        "email"     : user["email"],
        "joined_at" : datetime.datetime.utcnow().isoformat()
    }
    # Track socket so we can clean up on disconnect (tab close / refresh).
    active_sockets[flask_request.sid] = {"session_id": session_id, "user_id": uid}

    # Notify others in room
    emit("user_joined", {
        "user_id": uid,
        "name"   : user["name"],
        "message": f"{user['name']} joined the session"
    }, to=session_id)

    # Send room info back to joiner (include existing session_started_at if any)
    emit("room_info", {
        "session_id"        : session_id,
        "skill"             : session.get("skill"),
        "duration"          : session.get("duration"),
        "accepted_at"       : session.get("accepted_at"),
        "session_started_at": session.get("session_started_at"),   # ← FIX: send existing timer
        "participants"      : active_rooms[session_id]
    })

    # ── FIX: Start timer only when BOTH required participants are present ──────
    learner_uid = session.get("learner_id")
    tutor_uid   = session.get("tutor_id")
    participants = active_rooms.get(session_id, {})
    both_present = learner_uid in participants and tutor_uid in participants

    if both_present:
        def _parse_joined(val):
            try:
                return datetime.datetime.fromisoformat(val)
            except Exception:
                return datetime.datetime.utcnow()

        learner_join_dt = _parse_joined(participants[learner_uid].get("joined_at"))
        tutor_join_dt   = _parse_joined(participants[tutor_uid].get("joined_at"))
        latest_join_dt  = max(learner_join_dt, tutor_join_dt)

        started = session.get("session_started_at")
        should_reset = False

        if not started:
            should_reset = True
        else:
            # If `session_started_at` is much earlier than when BOTH users are
            # actually present (common when stale disconnects happen),
            # correct it once to the latest join time.
            if isinstance(started, datetime.datetime):
                started_dt = started
            elif isinstance(started, str):
                try:
                    # Support either "...Z" or "...+00:00" formats.
                    started_clean = started.replace("Z", "+00:00") if started.endswith("Z") else started
                    started_dt = datetime.datetime.fromisoformat(started_clean)
                    if started_dt.tzinfo is not None:
                        started_dt = started_dt.replace(tzinfo=None)
                except Exception:
                    started_dt = None
            else:
                started_dt = None

            if started_dt is None:
                should_reset = True
            else:
                if latest_join_dt > started_dt + datetime.timedelta(minutes=5):
                    should_reset = True

        if should_reset:
            sessions.update_one(
                {"_id": ObjectId(session_id)},
                {"$set": {"session_started_at": latest_join_dt}}
            )
            started_at_iso = latest_join_dt.isoformat()
        else:
            if isinstance(started, datetime.datetime):
                started_at_iso = started.isoformat()
            else:
                started_at_iso = str(started)

        # Emit both_ready to EVERYONE in room, including the start time.
        emit("both_ready", {
            "message": "Both participants are here. Session timer started!",
            "session_started_at": started_at_iso
        }, to=session_id)


# ================================================================
# CHAT MESSAGE
# ================================================================
@socketio.on("chat_message")
def handle_chat(data):
    """
    data: { session_id, token, message }
    """
    token      = data.get("token")
    session_id = data.get("session_id")
    message    = (data.get("message") or "").strip()

    user = _get_user_from_token(token)
    if not user or not message:
        return

    payload = {
        "user_id" : user["user_id"],
        "name"    : user["name"],
        "message" : message,
        "time"    : datetime.datetime.utcnow().strftime("%H:%M")
    }

    emit("chat_message", payload, to=session_id)


# ================================================================
# WEBRTC SIGNALING — Offer / Answer / ICE Candidate
# ================================================================
@socketio.on("webrtc_offer")
def handle_offer(data):
    """Relay SDP offer to other peer in room"""
    token      = data.get("token")
    session_id = data.get("session_id")
    offer      = data.get("offer")

    user = _get_user_from_token(token)
    if not user or not offer:
        return

    emit("webrtc_offer", {
        "offer"  : offer,
        "from_id": user["user_id"],
        "name"   : user["name"]
    }, to=session_id, include_self=False)


@socketio.on("webrtc_answer")
def handle_answer(data):
    """Relay SDP answer to other peer"""
    token      = data.get("token")
    session_id = data.get("session_id")
    answer     = data.get("answer")

    user = _get_user_from_token(token)
    if not user or not answer:
        return

    emit("webrtc_answer", {
        "answer" : answer,
        "from_id": user["user_id"]
    }, to=session_id, include_self=False)


@socketio.on("webrtc_ice")
def handle_ice(data):
    """Relay ICE candidate to other peer"""
    token      = data.get("token")
    session_id = data.get("session_id")
    candidate  = data.get("candidate")

    user = _get_user_from_token(token)
    if not user or not candidate:
        return

    emit("webrtc_ice", {
        "candidate": candidate,
        "from_id"  : user["user_id"]
    }, to=session_id, include_self=False)


# ================================================================
# VIDEO CALL EVENTS
# ================================================================
@socketio.on("call_started")
def handle_call_started(data):
    """Notify other peer that video call is starting"""
    token      = data.get("token")
    session_id = data.get("session_id")

    user = _get_user_from_token(token)
    if not user:
        return

    emit("call_started", {
        "from_id": user["user_id"],
        "name"   : user["name"],
        "message": f"{user['name']} started the video call"
    }, to=session_id)


@socketio.on("call_ended")
def handle_call_ended(data):
    """Notify other peer that call ended"""
    token      = data.get("token")
    session_id = data.get("session_id")

    user = _get_user_from_token(token)
    if not user:
        return

    emit("call_ended", {
        "from_id": user["user_id"],
        "name"   : user["name"],
        "message": f"{user['name']} ended the call"
    }, to=session_id)


# ================================================================
# LEAVE ROOM
# ================================================================
@socketio.on("leave_session")
def handle_leave(data):
    token      = data.get("token")
    session_id = data.get("session_id")

    user = _get_user_from_token(token)
    if not user:
        return

    leave_room(session_id)

    uid = user["user_id"]
    if session_id in active_rooms and uid in active_rooms[session_id]:
        del active_rooms[session_id][uid]
    # Cleanup socket tracking
    active_sockets.pop(flask_request.sid, None)

    emit("user_left", {
        "user_id": uid,
        "name"   : user["name"],
        "message": f"{user['name']} left the session"
    }, to=session_id)


@socketio.on("disconnect")
def handle_disconnect():
    # Clean up handled here as well so stale `active_rooms` entries
    # can't start timers when the other user is not really connected.
    meta = active_sockets.pop(flask_request.sid, None)
    if not meta:
        return

    session_id = meta.get("session_id")
    uid = meta.get("user_id")
    if not session_id or uid is None:
        return

    if session_id in active_rooms and uid in active_rooms[session_id]:
        user_info = active_rooms[session_id][uid]
        del active_rooms[session_id][uid]

        emit("user_left", {
            "user_id": uid,
            "name": user_info.get("name"),
            "message": f"{user_info.get('name')} left the session"
        }, to=session_id)

        if not active_rooms[session_id]:
            del active_rooms[session_id]