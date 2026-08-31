from flask import Blueprint, request, jsonify
from models.user_model import users
from models.session_model import sessions
from utils.jwt_utils import token_required
from bson import ObjectId
import datetime

session_bp = Blueprint("sessions", __name__)

# ================================================================
# ESCROW FLOW SUMMARY
#
# send_request   → credits LOCK from learner (escrow_credits in session)
# accept_request → status change + accepted_at timestamp set
# reject_request → escrow_credits RETURN to learner
# cancel_session → only ACCEPTER (tutor_id) can cancel after accept
#                  escrow_credits RETURN to requester
# complete       → ONLY ACCEPTER can complete
#                  IF before duration → refund to requester, NO credits to accepter
#                  IF after duration  → credits RELEASE to accepter
# ================================================================


def _utc_iso():
    """Return UTC datetime as ISO string WITH 'Z' suffix so browsers parse correctly."""
    return datetime.datetime.utcnow().isoformat() + "Z"


def _update_response_time(tutor_id, session_created_at):
    try:
        now           = datetime.datetime.utcnow()
        response_secs = (now - session_created_at).total_seconds()

        tutor    = users.find_one({"_id": ObjectId(tutor_id)})
        if not tutor:
            return

        old_rt   = tutor.get("response_time")
        rt_count = tutor.get("response_time_count", 0)

        if old_rt is None:
            new_rt = response_secs
        else:
            new_rt = ((old_rt * rt_count) + response_secs) / (rt_count + 1)

        users.update_one(
            {"_id": ObjectId(tutor_id)},
            {"$set": {
                "response_time":       round(new_rt, 1),
                "response_time_count": rt_count + 1
            }}
        )
    except Exception:
        pass


# ================================================================
# SEND REQUEST
# ================================================================

@session_bp.route("/send_request/<receiver_email>", methods=["POST"])
@token_required
def send_request(user_id, receiver_email):

    sender   = users.find_one({"_id": ObjectId(user_id)})
    receiver = users.find_one({"email": receiver_email.lower()})

    if not sender:
        return jsonify({"error": "Sender not found"}), 404

    if not receiver:
        return jsonify({"error": "Tutor not found"}), 404

    if receiver.get("is_banned"):
        return jsonify({"error": "Yeh user platform se ban hai"}), 403

    if receiver.get("role") == "tutor" and not receiver.get("is_verified"):
        return jsonify({"error": "Sirf verified tutors hi sessions le sakte hain"}), 403

    if not receiver.get("bio") or len(receiver.get("bio", "").strip()) < 10:
        return jsonify({"error": "Is tutor ka profile complete nahi hai (bio missing)"}), 403

    skill = (request.json or {}).get("skill", "").lower().strip()

    if not skill:
        return jsonify({"error": "Skill required"}), 400

    if skill not in [s.lower() for s in receiver.get("skills_i_can_teach", [])]:
        return jsonify({"error": f"Yeh tutor '{skill}' nahi padhata"}), 400

    if sender["email"] == receiver_email.lower():
        return jsonify({"error": "Aap khud ko request nahi bhej sakte"}), 400

    if receiver["role"] == "learner" and sender["role"] == "learner":
        return jsonify({"error": "Learner doosre learner ko request nahi bhej sakta"}), 400

    existing = sessions.find_one({
        "learner_id": str(user_id),
        "tutor_id":   str(receiver["_id"]),
        "status":     "pending"
    })
    if existing:
        return jsonify({"error": "Request already bheji ja chuki hai"}), 400

    active = sessions.find_one({
        "learner_id": str(user_id),
        "status":     {"$in": ["pending", "accepted"]}
    })
    if active:
        return jsonify({"error": "Aapki ek session already active hai"}), 400

    pending_count = sessions.count_documents({
        "tutor_id": str(receiver["_id"]),
        "status":   "pending"
    })
    if pending_count >= 50:
        return jsonify({"error": "Is tutor ke paas bahut zyada pending requests hain"}), 400

    duration = (request.json or {}).get("duration", 60)
    if duration not in [30, 60, 120, 180]:
        return jsonify({"error": "Duration 30, 60, 120, ya 180 minutes hona chahiye"}), 400

    credits_required = duration / 60

    if sender.get("credits", 0) < credits_required:
        return jsonify({
            "error":    "Credits insufficient",
            "required": credits_required,
            "current":  sender.get("credits", 0)
        }), 400

    scheduled_time_raw = (request.json or {}).get("scheduled_time", None)
    scheduled_time     = None

    if scheduled_time_raw is not None:
        try:
            parsed = datetime.datetime.fromisoformat(str(scheduled_time_raw))
            if parsed <= datetime.datetime.utcnow():
                return jsonify({"error": "scheduled_time future mein honi chahiye"}), 400

            session_end = parsed + datetime.timedelta(minutes=duration)

            conflict = sessions.find_one({
                "tutor_id": str(receiver["_id"]),
                "status":   {"$in": ["pending", "accepted"]},
                "scheduled_time": {"$ne": None},
                "$and": [
                    {"scheduled_time": {"$lt":  session_end.isoformat()}},
                    {"scheduled_time": {"$gte": parsed.isoformat()}}
                ]
            })

            if conflict:
                return jsonify({
                    "error":          "Is tutor ki us time slot pe already ek session hai",
                    "conflict_time":  conflict.get("scheduled_time")
                }), 409

            scheduled_time = parsed.isoformat() + "Z"

        except ValueError:
            return jsonify({
                "error": "Invalid scheduled_time format. ISO 8601 use karo"
            }), 400

    users.update_one(
        {"_id": ObjectId(user_id)},
        {"$inc": {"credits": -credits_required}}
    )

    now     = datetime.datetime.utcnow()
    session = {
        "learner_id":     str(user_id),
        "tutor_id":       str(receiver["_id"]),
        "skill":          skill,
        "duration":       duration,
        "credits_used":   credits_required,
        "escrow_credits": credits_required,
        "status":         "pending",
        "escrow_status":  "held",
        "scheduled_time": scheduled_time,
        "created_at":     now,
        "accepted_at":    None,
        "rated":          False,
        "early_complete": False,
        "session_started_at": None   # ← set only when BOTH users join the room
    }

    result     = sessions.insert_one(session)
    session_id = str(result.inserted_id)

    return jsonify({
        "message":        "Request bheji gayi",
        "session_id":     session_id,
        "escrow_credits": credits_required,
        "note":           f"{credits_required} credit(s) escrow mein lock hain"
    })


# ================================================================
# VIEW REQUESTS — Enriched with learner/tutor name + email
# ================================================================

@session_bp.route("/requests", methods=["GET"])
@token_required
def get_requests(user_id):

    user = users.find_one({"_id": ObjectId(user_id)})
    if not user:
        return jsonify({"error": "User not found"}), 404

    query = {
        "$or": [
            {"learner_id": str(user_id)},
            {"tutor_id":   str(user_id)}
        ]
    }

    result = list(sessions.find(query))

    output = []
    for r in result:
        learner = users.find_one(
            {"_id": ObjectId(r["learner_id"])},
            {"name": 1, "email": 1}
        )
        tutor = users.find_one(
            {"_id": ObjectId(r["tutor_id"])},
            {"name": 1, "email": 1}
        )

        r["_id"] = str(r["_id"])
        r["learner"] = {
            "name":  learner.get("name")  if learner else "?",
            "email": learner.get("email") if learner else "?"
        }
        r["tutor"] = {
            "name":  tutor.get("name")  if tutor else "?",
            "email": tutor.get("email") if tutor else "?"
        }
        # Serialize session_started_at with Z suffix if it's a datetime object
        if "session_started_at" in r:
            sat = r["session_started_at"]
            if isinstance(sat, datetime.datetime):
                r["session_started_at"] = sat.isoformat() + "Z"
        output.append(r)

    return jsonify(output)


# ================================================================
# ACCEPT REQUEST
# ================================================================

@session_bp.route("/accept-request/<id>", methods=["PUT"])
@token_required
def accept_request(user_id, id):

    user = users.find_one({"_id": ObjectId(user_id)})
    if not user:
        return jsonify({"error": "User not found"}), 404

    if user["role"] != "tutor":
        return jsonify({"error": "Sirf tutors accept kar sakte hain"}), 403

    session = sessions.find_one({"_id": ObjectId(id)})
    if not session:
        return jsonify({"error": "Session nahi mili"}), 404

    if session.get("escrow_status") != "held":
        return jsonify({"error": "Escrow held state mein nahi"}), 400

    now = datetime.datetime.utcnow()
    # FIX: store with Z suffix so browsers parse as UTC
    accepted_at_str = now.isoformat() + "Z"

    result = sessions.update_one(
        {
            "_id":      ObjectId(id),
            "tutor_id": str(user_id),
            "status":   "pending"
        },
        {"$set": {
            "status":      "accepted",
            "accepted_at": accepted_at_str
        }}
    )

    if result.matched_count == 0:
        return jsonify({"error": "Request nahi mili ya already handle ho chuki"}), 404

    _update_response_time(
        tutor_id           = str(user_id),
        session_created_at = session.get("created_at", now)
    )

    escrow = session.get("escrow_credits", session.get("credits_used", 1))

    return jsonify({
        "message":        "Request accept ho gayi — session timer start!",
        "escrow_credits": escrow,
        "accepted_at":    accepted_at_str,
        "note":           f"{escrow} credit(s) escrow mein — full duration ke baad release honge"
    })


# ================================================================
# REJECT REQUEST
# ================================================================

@session_bp.route("/reject-request/<id>", methods=["PUT"])
@token_required
def reject_request(user_id, id):

    user = users.find_one({"_id": ObjectId(user_id)})
    if not user:
        return jsonify({"error": "User not found"}), 404

    if user["role"] != "tutor":
        return jsonify({"error": "Sirf tutors reject kar sakte hain"}), 403

    session = sessions.find_one({
        "_id":      ObjectId(id),
        "tutor_id": str(user_id),
        "status":   "pending"
    })

    if not session:
        return jsonify({"error": "Request nahi mili ya already handle ho chuki"}), 404

    escrow = session.get("escrow_credits", session.get("credits_used", 1))

    users.update_one(
        {"_id": ObjectId(session["learner_id"])},
        {"$inc": {"credits": escrow}}
    )

    sessions.update_one(
        {"_id": ObjectId(id)},
        {"$set": {
            "status":        "rejected",
            "escrow_status": "refunded",
            "refunded_at":   _utc_iso()
        }}
    )

    return jsonify({
        "message":         "Request reject ho gayi",
        "escrow_refunded": escrow,
        "note":            f"{escrow} credit(s) requester ko wapas gaye"
    })


# ================================================================
# CANCEL SESSION
# ================================================================

@session_bp.route("/cancel/<id>", methods=["PUT"])
@token_required
def cancel_session(user_id, id):

    session = sessions.find_one({"_id": ObjectId(id)})
    if not session:
        return jsonify({"error": "Session nahi mili"}), 404

    if str(user_id) not in [session["tutor_id"], session["learner_id"]]:
        return jsonify({"error": "Aap is session ka hissa nahi hain"}), 403

    if session["status"] in ["completed", "cancelled", "rejected"]:
        return jsonify({"error": f"'{session['status']}' session cancel nahi ho sakta"}), 400

    if session["status"] == "accepted":
        if str(user_id) == session["learner_id"]:
            return jsonify({
                "error": "Session accept ho chuki hai — requester cancel nahi kar sakta. Sirf accepter (tutor) cancel kar sakta hai."
            }), 403

    cancelled_by = "tutor" if str(user_id) == session["tutor_id"] else "learner"
    escrow       = session.get("escrow_credits", session.get("credits_used", 1))

    if session.get("escrow_status") == "held":
        users.update_one(
            {"_id": ObjectId(session["learner_id"])},
            {"$inc": {"credits": escrow}}
        )
        escrow_status = "refunded"
        refund_note   = f"{escrow} credit(s) requester ko wapas gaye"
    else:
        escrow_status = session.get("escrow_status", "unknown")
        refund_note   = "Escrow held nahi tha — refund nahi hua"

    sessions.update_one(
        {"_id": ObjectId(id)},
        {"$set": {
            "status":        "cancelled",
            "escrow_status": escrow_status,
            "cancelled_by":  cancelled_by,
            "cancelled_at":  _utc_iso()
        }}
    )

    return jsonify({
        "message":       "Session cancel ho gayi",
        "cancelled_by":  cancelled_by,
        "refund_note":   refund_note,
        "escrow_status": escrow_status
    })


# ================================================================
# COMPLETE SESSION
# ================================================================

@session_bp.route("/complete-session/<id>", methods=["PUT"])
@token_required
def complete_session(user_id, id):

    session = sessions.find_one({"_id": ObjectId(id)})
    if not session:
        return jsonify({"error": "Session nahi mili"}), 404

    if str(user_id) != session["tutor_id"]:
        return jsonify({"error": "Sirf accepter (tutor) hi session complete kar sakta hai"}), 403

    if session["status"] == "completed":
        return jsonify({"error": "Session already complete hai"}), 400

    if session["status"] != "accepted":
        return jsonify({"error": "Session accept nahi hui abhi tak"}), 400

    if session.get("escrow_status") != "held":
        return jsonify({"error": "Escrow already settle ho chuka hai"}), 400

    escrow       = session.get("escrow_credits", session.get("credits_used", 1))
    duration_min = session.get("duration", 60)
    now          = datetime.datetime.utcnow()

    elapsed_min = None
    is_early    = False

    timer_ref = session.get("session_started_at") or session.get("accepted_at")

    if timer_ref:
        if isinstance(timer_ref, str):
            # Handle both "Z" and non-Z suffixed strings
            timer_ref_clean = timer_ref.replace("Z", "+00:00") if timer_ref.endswith("Z") else timer_ref
            try:
                timer_ref_dt = datetime.datetime.fromisoformat(timer_ref_clean)
                # Make naive if aware
                if timer_ref_dt.tzinfo is not None:
                    timer_ref_dt = timer_ref_dt.replace(tzinfo=None)
            except ValueError:
                timer_ref_dt = datetime.datetime.fromisoformat(timer_ref.rstrip("Z"))
        else:
            timer_ref_dt = timer_ref

        elapsed_min = (now - timer_ref_dt).total_seconds() / 60
        is_early    = elapsed_min < duration_min

    if is_early:
        users.update_one(
            {"_id": ObjectId(session["learner_id"])},
            {"$inc": {"credits": escrow}}
        )

        sessions.update_one(
            {"_id": ObjectId(id)},
            {"$set": {
                "status":         "completed",
                "escrow_status":  "refunded_early",
                "completed_at":   _utc_iso(),
                "early_complete": True,
                "elapsed_min":    round(elapsed_min, 1)
            }}
        )

        return jsonify({
            "message":               "Session early complete — credits accepter ko nahi mile",
            "credits_to_accepter":   0,
            "refunded_to_requester": escrow,
            "elapsed_minutes":       round(elapsed_min, 1),
            "required_minutes":      duration_min,
            "early_complete":        True,
            "note":                  f"Duration {duration_min} min tha, sirf {round(elapsed_min)} min mein complete kiya"
        })

    else:
        users.update_one(
            {"_id": ObjectId(session["tutor_id"])},
            {"$inc": {
                "credits":            escrow,
                "sessions_completed": 1
            }}
        )

        sessions.update_one(
            {"_id": ObjectId(id)},
            {"$set": {
                "status":         "completed",
                "escrow_status":  "released",
                "completed_at":   _utc_iso(),
                "early_complete": False
            }}
        )

        return jsonify({
            "message":          "Session complete! 🎉",
            "credits_released": escrow,
            "early_complete":   False,
            "note":             f"{escrow} credit(s) accepter ko mil gaye"
        })


# ================================================================
# DELETE SESSION (completed / cancelled / rejected only)
# ================================================================

@session_bp.route("/delete/<id>", methods=["DELETE"])
@token_required
def delete_session(user_id, id):
    """
    Allows a user to remove a session from their view.
    Only completed, cancelled, or rejected sessions can be deleted.
    """
    try:
        session = sessions.find_one({"_id": ObjectId(id)})
    except Exception:
        return jsonify({"error": "Invalid session ID"}), 400

    if not session:
        return jsonify({"error": "Session not found"}), 404

    # Must be a participant
    if str(user_id) not in [session["tutor_id"], session["learner_id"]]:
        return jsonify({"error": "Unauthorized — you are not part of this session"}), 403

    # Only allow deleting inactive sessions
    deletable_statuses = ["completed", "cancelled", "rejected"]
    if session["status"] not in deletable_statuses:
        return jsonify({
            "error": f"Cannot delete a '{session['status']}' session. Only completed/cancelled/rejected sessions can be deleted."
        }), 400

    sessions.delete_one({"_id": ObjectId(id)})

    return jsonify({"message": "Session deleted successfully"})


# ================================================================
# GET MY ACTIVE REQUESTS
# ================================================================

@session_bp.route("/my_requests", methods=["GET"])
@token_required
def get_my_requests(user_id):

    my_sessions = list(sessions.find({
        "$or": [
            {"learner_id": str(user_id)},
            {"tutor_id":   str(user_id)}
        ],
        "status": {"$in": ["pending", "accepted"]}
    }))

    result = []
    for r in my_sessions:
        learner = users.find_one({"_id": ObjectId(r["learner_id"])})
        tutor   = users.find_one({"_id": ObjectId(r["tutor_id"])})

        sat = r.get("session_started_at")
        if isinstance(sat, datetime.datetime):
            sat = sat.isoformat() + "Z"

        result.append({
            "session_id":        str(r["_id"]),
            "skill":             r.get("skill"),
            "duration":          r.get("duration"),
            "status":            r.get("status"),
            "escrow_credits":    r.get("escrow_credits"),
            "escrow_status":     r.get("escrow_status"),
            "scheduled_time":    r.get("scheduled_time"),
            "accepted_at":       r.get("accepted_at"),
            "session_started_at": sat,
            "created_at":        str(r.get("created_at", "")),
            "learner": {
                "name":  learner.get("name")  if learner else "?",
                "email": learner.get("email") if learner else "?"
            },
            "tutor": {
                "name":  tutor.get("name")  if tutor else "?",
                "email": tutor.get("email") if tutor else "?"
            }
        })

    return jsonify(result)