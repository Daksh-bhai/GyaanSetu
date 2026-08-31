from flask import Blueprint, request, jsonify
from models.user_model import users, db
from utils.jwt_utils import token_required
from bson import ObjectId
import datetime
import uuid

report_bp = Blueprint("report", __name__)

# ============================================================ #
#   REPORT SYSTEM — Phase 13 Extension                          #
#                                                               #
#   Flow:                                                       #
#   1. User reports another user via POST /api/report/user      #
#   2. Reports stored in `reports` collection                   #
#   3. Auto-ban triggers:                                       #
#      - 3+ fraud/harassment reports → immediate auto-ban       #
#      - 5+ any reports → auto-ban                              #
#   4. Admin can review/dismiss reports via admin panel         #
#                                                               #
#   Report Categories:                                          #
#   - harassment    → abusive/threatening behavior              #
#   - fraud         → fake skills, credit scam                  #
#   - violence      → threats of physical harm                  #
#   - spam          → repeated unwanted requests                #
#   - inappropriate → offensive content                         #
# ============================================================ #

REPORT_CATEGORIES = ["harassment", "fraud", "violence", "spam", "inappropriate"]

# Severe categories — 3 reports → auto-ban
SEVERE_CATEGORIES = ["harassment", "fraud", "violence"]

# Auto-ban thresholds
AUTO_BAN_SEVERE_THRESHOLD = 3   # 3 severe reports
AUTO_BAN_ANY_THRESHOLD    = 5   # 5 any reports


# ============================================================ #
#   POST /api/report/user/<reported_email>                      #
#   Body: {                                                     #
#     "category": "harassment",                                 #
#     "description": "Optional description"                     #
#   }                                                           #
#   Auth: Required                                              #
# ============================================================ #

@report_bp.route("/user/<reported_email>", methods=["POST"])
@token_required
def report_user(user_id, reported_email):

    reporter = users.find_one({"_id": ObjectId(user_id)})
    reported = users.find_one({"email": reported_email.lower()})

    if not reporter:
        return jsonify({"error": "Reporter not found"}), 404

    if not reported:
        return jsonify({"error": "Reported user not found"}), 404

    # Prevent self-report
    if reporter["email"] == reported_email.lower():
        return jsonify({"error": "You cannot report yourself"}), 400

    data     = request.json or {}
    category = data.get("category", "").strip().lower()
    description = data.get("description", "").strip()

    # Validate category
    if not category:
        return jsonify({
            "error": "Category required",
            "valid_categories": REPORT_CATEGORIES
        }), 400

    if category not in REPORT_CATEGORIES:
        return jsonify({
            "error": f"Invalid category '{category}'",
            "valid_categories": REPORT_CATEGORIES
        }), 400

    # -------- DUPLICATE REPORT CHECK -------- #
    # Same reporter cannot report same person for same category twice
    already_reported = db["reports"].find_one({
        "reporter_id":    str(user_id),
        "reported_email": reported_email.lower(),
        "category":       category,
        "status":         "open"
    })

    if already_reported:
        return jsonify({"error": "You already have an open report for this user with this category"}), 400

    # -------- CREATE REPORT -------- #
    report = {
        "report_id":      str(uuid.uuid4()),
        "reporter_id":    str(user_id),
        "reporter_email": reporter["email"],
        "reported_email": reported_email.lower(),
        "reported_name":  reported.get("name"),
        "category":       category,
        "description":    description,
        "status":         "open",       # open → reviewed / dismissed
        "created_at":     datetime.datetime.utcnow().isoformat()
    }

    db["reports"].insert_one(report)

    # -------- AUTO-BAN LOGIC -------- #
    auto_ban_result = check_auto_ban(reported_email.lower(), reported)

    response = {
        "message": "Report submitted successfully",
        "report_id": report["report_id"],
        "category": category
    }

    if auto_ban_result["banned"]:
        response["auto_ban"] = True
        response["ban_reason"] = auto_ban_result["reason"]

    return jsonify(response), 201


# ============================================================ #
#   GET /api/report/against_me                                  #
#   Tutor can see reports filed against them                    #
#   (summary only — not reporter identity)                      #
#   Auth: Required                                              #
# ============================================================ #

@report_bp.route("/against_me", methods=["GET"])
@token_required
def reports_against_me(user_id):

    user = users.find_one({"_id": ObjectId(user_id)})

    if not user:
        return jsonify({"error": "User not found"}), 404

    reports = list(db["reports"].find(
        {"reported_email": user["email"]},
        {"reporter_id": 0, "reporter_email": 0, "_id": 0}   # hide reporter identity
    ))

    return jsonify({
        "total_reports": len(reports),
        "reports": reports
    })


# ============================================================ #
#   GET /api/report/my_reports                                  #
#   Reports filed by the current user                           #
#   Auth: Required                                              #
# ============================================================ #

@report_bp.route("/my_reports", methods=["GET"])
@token_required
def my_reports(user_id):

    reports = list(db["reports"].find(
        {"reporter_id": str(user_id)},
        {"_id": 0}
    ))

    return jsonify({
        "total": len(reports),
        "reports": reports
    })


# ============================================================ #
#   AUTO-BAN HELPER                                             #
#   Called after every new report                               #
#   Returns: { "banned": True/False, "reason": "..." }         #
# ============================================================ #

def check_auto_ban(reported_email: str, reported_user: dict) -> dict:
    """
    Checks if the reported user should be auto-banned.

    Rules:
    - 3+ open reports in SEVERE categories (harassment, fraud, violence) → ban
    - 5+ open reports of ANY category → ban

    Returns dict with banned:True/False and reason.
    """

    # Skip if already banned
    if reported_user.get("is_banned"):
        return {"banned": False, "reason": None}

    # Count severe reports
    severe_count = db["reports"].count_documents({
        "reported_email": reported_email,
        "category":       {"$in": SEVERE_CATEGORIES},
        "status":         "open"
    })

    # Count total reports
    total_count = db["reports"].count_documents({
        "reported_email": reported_email,
        "status":         "open"
    })

    ban_reason = None

    if severe_count >= AUTO_BAN_SEVERE_THRESHOLD:
        ban_reason = f"Auto-banned: {severe_count} severe reports (harassment/fraud/violence)"

    elif total_count >= AUTO_BAN_ANY_THRESHOLD:
        ban_reason = f"Auto-banned: {total_count} total reports from multiple users"

    if ban_reason:
        # Execute ban
        users.update_one(
            {"email": reported_email},
            {"$set": {
                "is_banned":   True,
                "ban_reason":  ban_reason,
                "banned_at":   datetime.datetime.utcnow().isoformat(),
                "banned_by":   "system_auto"
            }}
        )

        # Log the auto-ban event
        db["fraud_logs"].insert_one({
            "event":          "auto_ban",
            "user_email":     reported_email,
            "reason":         ban_reason,
            "severe_reports": severe_count,
            "total_reports":  total_count,
            "timestamp":      datetime.datetime.utcnow().isoformat()
        })

        return {"banned": True, "reason": ban_reason}

    return {"banned": False, "reason": None}