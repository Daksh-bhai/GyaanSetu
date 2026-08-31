import datetime
from bson import ObjectId

# ================================================================
# FRAUD DETECTION MODULE
# ================================================================

def _get_collections():
    from models.session_model import sessions
    from models.review_model  import reviews
    from models.user_model    import users
    return sessions, reviews, users


# ================================================================
# CHECK 1: SESSION FRAUD
# ================================================================
def check_session_fraud(learner_id, tutor_id):
    sessions, reviews, users = _get_collections()

    flags      = []
    risk_score = 0

    now       = datetime.datetime.utcnow()
    last_hour = now - datetime.timedelta(hours=1)
    last_day  = now - datetime.timedelta(days=1)

    learner_id_str = str(learner_id)
    tutor_id_str   = str(tutor_id)

    # FLAG 1: Too many requests in 1 hour (>5 is suspicious)
    recent_requests = sessions.count_documents({
        "learner_id" : learner_id_str,
        "created_at" : {"$gte": last_hour}
    })
    if recent_requests >= 5:
        flags.append(f"⚠️  {recent_requests} requests in last 1 hour")
        risk_score += 35

    # FLAG 2: Repeated requests to same tutor today (>3)
    same_tutor_today = sessions.count_documents({
        "learner_id" : learner_id_str,
        "tutor_id"   : tutor_id_str,
        "created_at" : {"$gte": last_day}
    })
    if same_tutor_today >= 3:
        flags.append(f"⚠️  {same_tutor_today} requests to same tutor today")
        risk_score += 30

    # FLAG 3: High rejection rate (>80%, minimum 10 requests)
    total_requests = sessions.count_documents({"learner_id": learner_id_str})
    rejected_requests = sessions.count_documents({
        "learner_id" : learner_id_str,
        "status"     : "rejected"
    })
    if total_requests >= 10:
        rejection_rate = rejected_requests / total_requests
        if rejection_rate > 0.80:
            flags.append(f"⚠️  High rejection rate: {round(rejection_rate * 100)}%")
            risk_score += 20

    # FLAG 4: New account < 5 minutes old
    learner = users.find_one({"_id": ObjectId(learner_id)})
    if learner:
        account_age = (now - learner.get("created_at", now)).total_seconds()
        if account_age < 300:
            flags.append("⚠️  Account created < 5 minutes ago")
            risk_score += 20

    return {
        "is_fraud"   : risk_score >= 70,   # Raised threshold from 50 → 70
        "risk_score" : min(risk_score, 100),
        "flags"      : flags
    }


# ================================================================
# CHECK 2: RATING FRAUD
# ================================================================
def check_rating_fraud(learner_id, tutor_id):
    """
    FIXED: Less aggressive — legitimate test sessions were getting blocked.

    Main checks:
    - Already rated THIS specific session today (not all sessions)
    - Too many reviews in 1 hour (not 1 day)
    - Extreme pattern (all 1s or all 5s) — only soft flag
    - No completed session exists — this is already checked in auth_routes before calling this
    """
    sessions, reviews, users = _get_collections()

    flags      = []
    risk_score = 0

    now       = datetime.datetime.utcnow()
    last_hour = now - datetime.timedelta(hours=1)
    last_day  = now - datetime.timedelta(days=1)

    learner_id_str = str(learner_id)
    tutor_id_str   = str(tutor_id)

    # FLAG 1: Already rated same tutor in last HOUR (not day)
    # Using 1 hour instead of 1 day to avoid blocking legit multiple sessions
    already_rated_hour = reviews.count_documents({
        "learner_id" : learner_id_str,
        "tutor_id"   : tutor_id_str,
        "created_at" : {"$gte": last_hour}
    })
    if already_rated_hour >= 1:
        flags.append("⚠️  Already rated this tutor in last hour")
        risk_score += 40   # Reduced from 60 → 40

    # FLAG 2: Too many reviews in 1 hour (>3 in 1 hour is suspicious)
    reviews_last_hour = reviews.count_documents({
        "learner_id" : learner_id_str,
        "created_at" : {"$gte": last_hour}
    })
    if reviews_last_hour >= 3:
        flags.append(f"⚠️  {reviews_last_hour} reviews in last hour (spam pattern)")
        risk_score += 30

    # FLAG 3: Extreme rating pattern (soft flag only, +15)
    all_reviews = list(reviews.find({"learner_id": learner_id_str}))
    if len(all_reviews) >= 8:
        ratings = [r.get("rating", 3) for r in all_reviews]
        extreme = all(r == 1 or r == 5 for r in ratings)
        if extreme:
            flags.append("⚠️  All ratings are extreme (1 or 5)")
            risk_score += 15   # Reduced from 20 → 15, soft flag

    # NOTE: "No completed session" check REMOVED from here
    # It is already checked in auth_routes.py rate_tutor() BEFORE calling this function
    # So if we reach here, a valid unrated completed session exists

    return {
        "is_fraud"   : risk_score >= 60,   # Threshold 60
        "risk_score" : min(risk_score, 100),
        "flags"      : flags
    }


# ================================================================
# UTIL: LOG FRAUD
# ================================================================
def log_fraud_event(user_id, event_type, details):
    try:
        sessions, reviews, users = _get_collections()
        db = users.database
        db["fraud_logs"].insert_one({
            "user_id"    : str(user_id),
            "event_type" : event_type,
            "risk_score" : details.get("risk_score"),
            "flags"      : details.get("flags"),
            "timestamp"  : datetime.datetime.utcnow()
        })
    except Exception as e:
        print(f"⚠️  Fraud log failed: {e}")


if __name__ == "__main__":
    print("🧪 Fraud Detection Module Loaded")