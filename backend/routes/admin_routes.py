from flask import Blueprint, request, jsonify
from models.user_model import users, db
from models.session_model import sessions
from bson import ObjectId
import datetime

admin_bp = Blueprint("admin", __name__)

# ============================================================ #
#   ADMIN KEY VERIFICATION                                      #
#   Har admin route isse check karta hai pehle                  #
#   .env mein store karo production mein:                       #
#   ADMIN_KEY = os.getenv("ADMIN_KEY", "gyaansetu_admin_2025") #
# ============================================================ #

ADMIN_KEY = "gyaansetu_admin_2025"

def verify_admin(req):
    """Returns True if request has valid admin key header."""
    return req.headers.get("X-Admin-Key") == ADMIN_KEY


# ============================================================ #
#   GET /api/admin/stats                                        #
#   Platform ka full dashboard — user counts, session stats     #
#   BUG FIX: `if db` → removed, PyMongo db bool() crash karta  #
# ============================================================ #

@admin_bp.route("/stats", methods=["GET"])
def get_stats():

    if not verify_admin(request):
        return jsonify({"error": "Unauthorized — invalid admin key"}), 403

    try:
        total_users      = users.count_documents({})
        total_tutors     = users.count_documents({"role": "tutor"})
        total_learners   = users.count_documents({"role": "learner"})
        verified_tutors  = users.count_documents({"role": "tutor", "is_verified": True})
        banned_users     = users.count_documents({"is_banned": True})

        total_sessions     = sessions.count_documents({})
        completed_sessions = sessions.count_documents({"status": "completed"})
        pending_sessions   = sessions.count_documents({"status": "pending"})
        accepted_sessions  = sessions.count_documents({"status": "accepted"})
        cancelled_sessions = sessions.count_documents({"status": "cancelled"})

        # -------- SAFE COLLECTION ACCESS -------- #
        # BUG FIX: Never use `if db` — PyMongo Database objects don't support bool()
        # Always use try/except or direct access
        fraud_logs_count = db["fraud_logs"].count_documents({})
        reports_count    = db["reports"].count_documents({})
        open_reports     = db["reports"].count_documents({"status": "open"})

        return jsonify({
            "users": {
                "total":    total_users,
                "tutors":   total_tutors,
                "learners": total_learners,
                "verified_tutors": verified_tutors,
                "banned":   banned_users
            },
            "sessions": {
                "total":     total_sessions,
                "completed": completed_sessions,
                "pending":   pending_sessions,
                "accepted":  accepted_sessions,
                "cancelled": cancelled_sessions
            },
            "reports": {
                "total": reports_count,
                "open":  open_reports
            },
            "fraud_logs": fraud_logs_count
        })

    except Exception as e:
        return jsonify({"error": f"Stats fetch failed: {str(e)}"}), 500


# ============================================================ #
#   GET /api/admin/users                                        #
#   Optional query params: role, is_banned, is_verified         #
# ============================================================ #

@admin_bp.route("/users", methods=["GET"])
def get_users():

    if not verify_admin(request):
        return jsonify({"error": "Unauthorized"}), 403

    query = {}

    role       = request.args.get("role", "").strip().lower()
    is_banned  = request.args.get("is_banned", "").strip().lower()
    is_verified = request.args.get("is_verified", "").strip().lower()

    if role in ["tutor", "learner"]:
        query["role"] = role

    if is_banned == "true":
        query["is_banned"] = True
    elif is_banned == "false":
        query["is_banned"] = {"$ne": True}

    if is_verified == "true":
        query["is_verified"] = True

    all_users = list(users.find(query, {"password": 0, "test_answers": 0}))

    for u in all_users:
        u["_id"] = str(u["_id"])

    return jsonify({
        "total": len(all_users),
        "users": all_users
    })


# ============================================================ #
#   GET /api/admin/user/<email>                                 #
#   Single user ka full profile (no password)                   #
# ============================================================ #

@admin_bp.route("/user/<email>", methods=["GET"])
def get_user(email):

    if not verify_admin(request):
        return jsonify({"error": "Unauthorized"}), 403

    user = users.find_one(
        {"email": email.lower()},
        {"password": 0, "test_answers": 0}
    )

    if not user:
        return jsonify({"error": "User not found"}), 404

    user["_id"] = str(user["_id"])

    # Fetch their sessions too
    user_sessions = list(sessions.find(
        {"$or": [
            {"learner_id": str(user["_id"])},
            {"tutor_id":   str(user["_id"])}
        ]},
        {"_id": 0}
    ))

    return jsonify({
        "user": user,
        "session_count": len(user_sessions),
        "sessions": user_sessions
    })


# ============================================================ #
#   PUT /api/admin/ban/<email>                                  #
#   Body: { "reason": "Harassment" }                           #
# ============================================================ #

@admin_bp.route("/ban/<email>", methods=["PUT"])
def ban_user(email):

    if not verify_admin(request):
        return jsonify({"error": "Unauthorized"}), 403

    data   = request.json or {}
    reason = data.get("reason", "Admin action")

    user = users.find_one({"email": email.lower()})

    if not user:
        return jsonify({"error": "User not found"}), 404

    if user.get("is_banned"):
        return jsonify({"error": "User is already banned"}), 400

    users.update_one(
        {"email": email.lower()},
        {"$set": {
            "is_banned":   True,
            "banned_at":   datetime.datetime.utcnow().isoformat(),
            "ban_reason":  reason
        }}
    )

    return jsonify({
        "message": f"{user.get('name')} has been banned",
        "email":   email,
        "reason":  reason,
        "banned_at": datetime.datetime.utcnow().isoformat()
    })


# ============================================================ #
#   PUT /api/admin/unban/<email>                                #
# ============================================================ #

@admin_bp.route("/unban/<email>", methods=["PUT"])
def unban_user(email):

    if not verify_admin(request):
        return jsonify({"error": "Unauthorized"}), 403

    user = users.find_one({"email": email.lower()})

    if not user:
        return jsonify({"error": "User not found"}), 404

    if not user.get("is_banned"):
        return jsonify({"error": "User is not banned"}), 400

    users.update_one(
        {"email": email.lower()},
        {"$set": {
            "is_banned":  False,
            "ban_reason": None,
            "banned_at":  None,
            "unbanned_at": datetime.datetime.utcnow().isoformat()
        }}
    )

    return jsonify({"message": f"{user.get('name')} has been unbanned"})


# ============================================================ #
#   GET /api/admin/sessions                                     #
#   Optional: ?status=completed/pending/accepted/cancelled      #
# ============================================================ #

@admin_bp.route("/sessions", methods=["GET"])
def get_sessions():

    if not verify_admin(request):
        return jsonify({"error": "Unauthorized"}), 403

    query  = {}
    status = request.args.get("status", "").strip().lower()

    valid_statuses = ["pending", "accepted", "completed", "cancelled", "rejected"]
    if status and status in valid_statuses:
        query["status"] = status

    all_sessions = list(sessions.find(query))

    for s in all_sessions:
        s["_id"] = str(s["_id"])

    return jsonify({
        "total": len(all_sessions),
        "sessions": all_sessions
    })


# ============================================================ #
#   GET /api/admin/fraud_logs                                   #
# ============================================================ #

@admin_bp.route("/fraud_logs", methods=["GET"])
def get_fraud_logs():

    if not verify_admin(request):
        return jsonify({"error": "Unauthorized"}), 403

    logs = list(db["fraud_logs"].find({}, {"_id": 0}))

    return jsonify({
        "total": len(logs),
        "logs":  logs
    })


# ============================================================ #
#   GET /api/admin/reports                                      #
#   All user-submitted reports                                  #
# ============================================================ #

@admin_bp.route("/reports", methods=["GET"])
def get_reports():

    if not verify_admin(request):
        return jsonify({"error": "Unauthorized"}), 403

    status = request.args.get("status", "").strip().lower()
    query  = {}

    if status in ["open", "reviewed", "dismissed"]:
        query["status"] = status

    reports = list(db["reports"].find(query, {"_id": 0}))

    return jsonify({
        "total":   len(reports),
        "reports": reports
    })


# ============================================================ #
#   PUT /api/admin/reports/<report_id>/review                   #
#   Mark a report as reviewed or dismissed                      #
#   Body: { "action": "reviewed" | "dismissed" }               #
# ============================================================ #

@admin_bp.route("/reports/<report_id>/review", methods=["PUT"])
def review_report(report_id):

    if not verify_admin(request):
        return jsonify({"error": "Unauthorized"}), 403

    data   = request.json or {}
    action = data.get("action", "reviewed").strip().lower()

    if action not in ["reviewed", "dismissed"]:
        return jsonify({"error": "action must be 'reviewed' or 'dismissed'"}), 400

    result = db["reports"].update_one(
        {"report_id": report_id},
        {"$set": {
            "status":      action,
            "reviewed_at": datetime.datetime.utcnow().isoformat()
        }}
    )

    if result.matched_count == 0:
        return jsonify({"error": "Report not found"}), 404

    return jsonify({"message": f"Report marked as {action}"})


# ============================================================ #
#   PUT /api/admin/credits/add/<email>                          #
#   Body: { "amount": 10 }                                      #
# ============================================================ #

@admin_bp.route("/credits/add/<email>", methods=["PUT"])
def admin_add_credits(email):

    if not verify_admin(request):
        return jsonify({"error": "Unauthorized"}), 403

    data   = request.json or {}
    amount = data.get("amount")

    if amount is None or not isinstance(amount, (int, float)) or amount <= 0:
        return jsonify({"error": "Valid positive amount required"}), 400

    user = users.find_one({"email": email.lower()})

    if not user:
        return jsonify({"error": "User not found"}), 404

    users.update_one(
        {"email": email.lower()},
        {"$inc": {"credits": amount}}
    )

    updated = users.find_one({"email": email.lower()})

    return jsonify({
        "message": f"{amount} credits added to {email}",
        "new_balance": updated.get("credits", 0)
    })


# ============================================================ #
#   PUT /api/admin/credits/deduct/<email>                       #
#   Body: { "amount": 5 }                                       #
# ============================================================ #

@admin_bp.route("/credits/deduct/<email>", methods=["PUT"])
def admin_deduct_credits(email):

    if not verify_admin(request):
        return jsonify({"error": "Unauthorized"}), 403

    data   = request.json or {}
    amount = data.get("amount")

    if amount is None or not isinstance(amount, (int, float)) or amount <= 0:
        return jsonify({"error": "Valid positive amount required"}), 400

    user = users.find_one({"email": email.lower()})

    if not user:
        return jsonify({"error": "User not found"}), 404

    if user.get("credits", 0) < amount:
        return jsonify({"error": "User does not have enough credits"}), 400

    users.update_one(
        {"email": email.lower()},
        {"$inc": {"credits": -amount}}
    )

    updated = users.find_one({"email": email.lower()})

    return jsonify({
        "message": f"{amount} credits deducted from {email}",
        "new_balance": updated.get("credits", 0)
    })


# ============================================================ #
#   DELETE /api/admin/user/<email>                              #
#   Permanently delete user                                     #
# ============================================================ #

@admin_bp.route("/user/<email>", methods=["DELETE"])
def delete_user(email):

    if not verify_admin(request):
        return jsonify({"error": "Unauthorized"}), 403

    user = users.find_one({"email": email.lower()})

    if not user:
        return jsonify({"error": "User not found"}), 404

    users.delete_one({"email": email.lower()})

    return jsonify({"message": f"User {email} permanently deleted"})