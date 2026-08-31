from flask import Blueprint, request, jsonify
from models.user_model import users
from models.session_model import sessions
from models.review_model import reviews
from utils.jwt_utils import generate_token, token_required
from bson import ObjectId
import bcrypt
import datetime
import re

# -------- AI Models -------- #
from ai_models.badge_prediction      import predict_badge
from ai_models.fraud_detection       import check_rating_fraud, log_fraud_event
from ai_models.recommendation_model  import get_tutor_recommendations, get_similar_tutors

auth_bp = Blueprint("auth", __name__)


# ================================================================
# VALIDATION HELPERS
# ================================================================

def validate_email(email):
    """Proper email format check using regex."""
    pattern = r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """
    Password rules:
    - Min 8 characters
    - At least 1 uppercase letter
    - At least 1 lowercase letter
    - At least 1 digit
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    return True, "OK"

def validate_name(name):
    """
    Name rules:
    - Min 2 characters
    - Only letters, spaces, dots, hyphens allowed
    - No numbers or special characters
    """
    if len(name.strip()) < 2:
        return False, "Name must be at least 2 characters"
    if not re.match(r'^[a-zA-Z\s.\-]+$', name.strip()):
        return False, "Name can only contain letters, spaces, dots, and hyphens"
    return True, "OK"


# ================================================================
# RANKING FUNCTION
# ================================================================

def calculate_score(tutor, current_user):

    rating        = tutor.get("rating", 0)
    sessions_done = tutor.get("sessions_completed", 0)
    response_time = tutor.get("response_time")

    badge_map = {"Beginner": 1, "Intermediate": 2, "Expert": 3}
    badge     = badge_map.get(tutor.get("badge"), 1)

    if response_time is None:
        response_score = 0
    else:
        response_score = 1 / (response_time + 1)

    score = (
        (rating        * 0.3) +
        (sessions_done * 0.2) +
        (badge         * 0.2) +
        (response_score* 0.3)
    )
    return score


# ================================================================
# REGISTER
# ================================================================

@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.json or {}

    name     = (data.get("name") or "").strip()
    email    = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    role     = data.get("role") or ""
    location = (data.get("location") or "").strip()

    skills_teach = [s.strip().lower() for s in data.get("skills_i_can_teach", [])]
    skills_learn = [s.strip().lower() for s in data.get("skills_i_want_to_learn", [])]

    # -------- TYPE CHECK -------- #
    if not isinstance(skills_teach, list) or not isinstance(skills_learn, list):
        return jsonify({"error": "Skills must be in list format"}), 400

    # -------- REQUIRED FIELDS -------- #
    if not name or not email or not password or not role or not location:
        return jsonify({"error": "All fields required"}), 400

    # -------- NAME VALIDATION -------- #
    name_ok, name_msg = validate_name(name)
    if not name_ok:
        return jsonify({"error": name_msg}), 400

    # -------- EMAIL VALIDATION -------- #
    if not validate_email(email):
        return jsonify({"error": "Invalid email format. Example: user@gmail.com"}), 400

    # -------- PASSWORD VALIDATION -------- #
    pw_ok, pw_msg = validate_password(password)
    if not pw_ok:
        return jsonify({"error": pw_msg}), 400

    # -------- ROLE VALIDATION -------- #
    if role not in ["tutor", "learner"]:
        return jsonify({"error": "Invalid role"}), 400

    if role == "tutor" and len(skills_teach) == 0:
        return jsonify({"error": "Tutor must add at least one skill"}), 400

    if len(skills_learn) == 0:
        return jsonify({"error": "At least one learning skill required"}), 400

    # -------- DUPLICATE CHECK -------- #
    if users.find_one({"email": email}):
        return jsonify({"error": "User already exists"}), 400

    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    user = {
        "name":     name,
        "email":    email,
        "password": hashed.decode("utf-8"),
        "location": location,

        "role":    role,
        "credits": 0,

        "is_verified":    False,
        "verified_skill": None,
        "verified_level": None,

        "skills_i_can_teach":    skills_teach if role == "tutor" else [],
        "skills_i_want_to_learn": skills_learn,

        "rating":             0,
        "rating_count":       0,
        "sessions_completed": 0,
        "response_time":      None,

        "badge":    "Beginner",
        "progress": [],
        "bio":      "",

        "created_at":   datetime.datetime.utcnow(),
        "last_login":   None,
        "last_active":  None,
        "updated_at":   datetime.datetime.utcnow()
    }

    users.insert_one(user)
    return jsonify({"message": "User registered successfully"})


# ================================================================
# LOGIN
# ================================================================

@auth_bp.route("/login", methods=["POST"])
def login():

    data     = request.json or {}
    email    = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    user = users.find_one({"email": email})

    if not user:
        return jsonify({"error": "User not found"}), 404

    # -------- BAN CHECK (login pe bhi) -------- #
    if user.get("is_banned"):
        return jsonify({
            "error":   "Your account has been banned",
            "reason":  user.get("ban_reason", "Violation of platform rules"),
            "contact": "Contact support to appeal this ban"
        }), 403

    if bcrypt.checkpw(password.encode("utf-8"), user["password"].encode("utf-8")):

        token = generate_token(user["_id"])

        # -------- TRACK last_login + last_active -------- #
        now = datetime.datetime.utcnow()
        users.update_one(
            {"_id": user["_id"]},
            {"$set": {
                "last_login":  now,
                "last_active": now
            }}
        )

        return jsonify({
            "message": "Login successful",
            "token":   token,
            "role":    user.get("role"),
            "name":    user.get("name"),
            "email":   user.get("email")
        })

    else:
        return jsonify({"error": "Invalid password"}), 401


# ================================================================
# PROFILE (PROTECTED)
# ================================================================

@auth_bp.route("/profile", methods=["GET"])
@token_required
def profile(user_id):

    # -------- UPDATE last_active -------- #
    users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"last_active": datetime.datetime.utcnow()}}
    )

    user = users.find_one(
        {"_id": ObjectId(user_id)},
        {"_id": 0, "password": 0}
    )

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify(user)


# ================================================================
# GET ALL USERS
# ================================================================

@auth_bp.route("/users", methods=["GET"])
def get_users():
    all_users = list(users.find({}, {"_id": 0, "password": 0}))
    return jsonify(all_users)


# ================================================================
# GET USER BY EMAIL
# ================================================================

@auth_bp.route("/profile/<email>", methods=["GET"])
def get_profile(email):

    user = users.find_one(
        {"email": email.lower()},
        {"_id": 0, "password": 0}
    )

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify(user)


# ================================================================
# GET ALL TUTORS
# ================================================================

@auth_bp.route("/tutors", methods=["GET"])
def get_tutors():
    tutors = list(users.find(
        {"role": "tutor"},
        {"_id": 0, "password": 0}
    ))
    return jsonify(tutors)


# ================================================================
# GET ALL LEARNERS
# ================================================================

@auth_bp.route("/learners", methods=["GET"])
def get_learners():
    learners = list(users.find(
        {"role": "learner"},
        {"_id": 0, "password": 0}
    ))
    return jsonify(learners)


# ================================================================
# SEARCH ROUTES
# ================================================================

@auth_bp.route("/search_tutor/<skill>", methods=["GET"])
def search_tutor(skill):
    tutors = list(users.find(
        {"role": "tutor", "skills_i_can_teach": {"$regex": skill, "$options": "i"}},
        {"_id": 0, "password": 0}
    ))
    return jsonify(tutors)


@auth_bp.route("/search_learner/<skill>", methods=["GET"])
def search_learner(skill):
    learners = list(users.find(
        {"role": "learner", "skills_i_want_to_learn": {"$regex": skill, "$options": "i"}},
        {"_id": 0, "password": 0}
    ))
    return jsonify(learners)


@auth_bp.route("/search_all/<skill>", methods=["GET"])
def search_users(skill):
    result = list(users.find(
        {"$or": [
            {"skills_i_can_teach":    {"$regex": skill, "$options": "i"}},
            {"skills_i_want_to_learn":{"$regex": skill, "$options": "i"}}
        ]},
        {"_id": 0, "password": 0}
    ))
    return jsonify(result)


@auth_bp.route("/search/<role>/<skill>", methods=["GET"])
def search_by_role(role, skill):

    if role not in ["tutor", "learner"]:
        return jsonify({"error": "Invalid role"}), 400

    query = {"role": role}
    if role == "tutor":
        query["skills_i_can_teach"] = {"$regex": skill, "$options": "i"}
    else:
        query["skills_i_want_to_learn"] = {"$regex": skill, "$options": "i"}

    result = list(users.find(query, {"_id": 0, "password": 0}))
    return jsonify(result)


# ================================================================
# UPDATE SKILLS (PROTECTED)
# ================================================================

@auth_bp.route("/update_skills", methods=["PUT"])
@token_required
def update_skills(user_id):

    data = request.json or {}
    user = users.find_one({"_id": ObjectId(user_id)})

    skills_learn = data.get("skills_i_want_to_learn", [])
    if not isinstance(skills_learn, list):
        return jsonify({"error": "skills_i_want_to_learn must be a list"}), 400

    update_data = {
        "skills_i_want_to_learn": list(set(skills_learn)),
        "updated_at": datetime.datetime.utcnow()
    }

    if user["role"] == "tutor":
        skills_teach = data.get("skills_i_can_teach", [])
        if not isinstance(skills_teach, list):
            return jsonify({"error": "skills_i_can_teach must be a list"}), 400
        update_data["skills_i_can_teach"] = list(set(skills_teach))

    users.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})
    return jsonify({"message": "Skills updated successfully"})


# ================================================================
# UPDATE BIO (PROTECTED)
# ================================================================

@auth_bp.route("/update_bio", methods=["PUT"])
@token_required
def update_bio(user_id):

    data = request.json or {}
    bio  = (data.get("bio") or "").strip()

    if not bio:
        return jsonify({"error": "Bio required"}), 400

    if len(bio) < 10:
        return jsonify({"error": "Bio must be at least 10 characters"}), 400

    users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {
            "bio":        bio,
            "updated_at": datetime.datetime.utcnow()
        }}
    )
    return jsonify({"message": "Bio updated"})


# ================================================================
# REMOVE SKILL (PROTECTED)
# ================================================================

@auth_bp.route("/remove_skill", methods=["DELETE"])
@token_required
def remove_skill(user_id):

    data       = request.json or {}
    skill      = data.get("skill")
    skill_type = data.get("type")

    if not skill or not skill_type:
        return jsonify({"error": "Skill and type required"}), 400

    if skill_type not in ["teach", "learn"]:
        return jsonify({"error": "Invalid type"}), 400

    field = "skills_i_can_teach" if skill_type == "teach" else "skills_i_want_to_learn"

    users.update_one(
        {"_id": ObjectId(user_id)},
        {
            "$pull": {field: skill},
            "$set":  {"updated_at": datetime.datetime.utcnow()}
        }
    )
    return jsonify({"message": "Skill removed successfully"})


# ================================================================
# DELETE OWN ACCOUNT (PROTECTED)
# ================================================================

@auth_bp.route("/delete_me", methods=["DELETE"])
@token_required
def delete_me(user_id):
    users.delete_one({"_id": ObjectId(user_id)})
    return jsonify({"message": "Account deleted"})


# ================================================================
# ADMIN DELETE
# ================================================================

@auth_bp.route("/admin/delete/<email>", methods=["DELETE"])
def admin_delete_user(email):
    users.delete_one({"email": email.lower()})
    return jsonify({"message": "User removed by admin"})


# ================================================================
# TUTOR DASHBOARD (PROTECTED)
# ================================================================

@auth_bp.route("/tutor/dashboard", methods=["GET"])
@token_required
def tutor_dashboard(user_id):

    user = users.find_one({"_id": ObjectId(user_id)})

    if user["role"] != "tutor":
        return jsonify({"error": "Access denied"}), 403

    return jsonify({
        "name":                   user.get("name"),
        "badge":                  user.get("badge"),
        "is_verified":            user.get("is_verified"),
        "skills_i_can_teach":     user.get("skills_i_can_teach"),
        "skills_i_want_to_learn": user.get("skills_i_want_to_learn"),
        "rating":                 user.get("rating"),
        "rating_count":           user.get("rating_count"),
        "sessions_completed":     user.get("sessions_completed"),
        "response_time":          user.get("response_time"),
        "credits":                user.get("credits"),
        "bio":                    user.get("bio"),
        "last_login":             user.get("last_login"),
        "last_active":            user.get("last_active")
    })


# ================================================================
# LEARNER DASHBOARD (PROTECTED)
# ================================================================

@auth_bp.route("/learner/dashboard", methods=["GET"])
@token_required
def learner_dashboard(user_id):

    user = users.find_one({"_id": ObjectId(user_id)})

    if user["role"] != "learner":
        return jsonify({"error": "Access denied"}), 403

    return jsonify({
        "name":                   user.get("name"),
        "skills_i_want_to_learn": user.get("skills_i_want_to_learn"),
        "credits":                user.get("credits"),
        "progress":               user.get("progress"),
        "last_login":             user.get("last_login"),
        "last_active":            user.get("last_active")
    })


# ================================================================
# RATE TUTOR (PROTECTED)
# ================================================================

@auth_bp.route("/rate_tutor/<email>", methods=["POST"])
@token_required
def rate_tutor(user_id, email):

    data    = request.get_json() or {}
    rating  = data.get("rating")
    comment = (data.get("comment") or "").strip()

    if not isinstance(rating, (int, float)):
        return jsonify({"error": "Rating must be a number"}), 400

    if rating < 1 or rating > 5:
        return jsonify({"error": "Rating must be between 1 and 5"}), 400

    tutor = users.find_one({"email": email.lower()})
    if not tutor:
        return jsonify({"error": "User not found"}), 404

    current_user = users.find_one({"_id": ObjectId(user_id)})

    if tutor["email"] == current_user["email"]:
        return jsonify({"error": "You cannot rate yourself"}), 400

    if tutor["role"] != "tutor":
        return jsonify({"error": "You can only rate tutors"}), 400

    # -------- FIND LATEST UNRATED COMPLETED SESSION -------- #
    session_exists = sessions.find_one(
        {
            "learner_id": str(user_id),
            "tutor_id":   str(tutor["_id"]),
            "status":     "completed",
            "rated":      {"$ne": True}
        },
        sort=[("_id", -1)]
    )

    if not session_exists:
        return jsonify({"error": "No unrated completed session found"}), 403

    # -------- FRAUD CHECK -------- #
    fraud_result = check_rating_fraud(user_id, str(tutor["_id"]))
    if fraud_result["is_fraud"]:
        log_fraud_event(user_id, "rating_fraud", fraud_result)
        return jsonify({
            "error": "Suspicious rating activity detected. Rating blocked.",
            "flags": fraud_result["flags"]
        }), 403

    rating_count   = tutor.get("rating_count", 0)
    current_rating = tutor.get("rating", 0)
    new_rating     = ((current_rating * rating_count) + rating) / (rating_count + 1)

    users.update_one(
        {"email": email.lower()},
        {
            "$set": {"rating": round(new_rating, 2)},
            "$inc": {"rating_count": 1}
        }
    )

    reviews.insert_one({
        "tutor_id":   str(tutor["_id"]),
        "learner_id": str(user_id),
        "rating":     rating,
        "comment":    comment,
        "created_at": datetime.datetime.utcnow()
    })

    # -------- ML BADGE PREDICTION -------- #
    updated_user = users.find_one({"email": email.lower()})
    badge_result = predict_badge(
        sessions_completed = updated_user.get("sessions_completed", 0),
        rating             = updated_user.get("rating", 0),
        rating_count       = updated_user.get("rating_count", 0),
        response_time      = updated_user.get("response_time")
    )
    badge = badge_result["badge"]

    users.update_one(
        {"email": email.lower()},
        {"$set": {"badge": badge}}
    )

    sessions.update_one(
        {"_id": session_exists["_id"]},
        {"$set": {"rated": True}}
    )

    return jsonify({
        "message":          "Tutor rated successfully",
        "new_rating":       round(new_rating, 2),
        "badge":            badge,
        "badge_confidence": badge_result["confidence"]
    })


# ================================================================
# UPDATE PROGRESS (PROTECTED)
# ================================================================

@auth_bp.route("/update_progress", methods=["PUT"])
@token_required
def update_progress(user_id):

    data  = request.json or {}
    skill = data.get("skill")

    if not skill:
        return jsonify({"error": "Skill required"}), 400

    users.update_one(
        {"_id": ObjectId(user_id)},
        {"$push": {"progress": skill}}
    )
    return jsonify({"message": "Progress updated"})


# ================================================================
# SWITCH ROLE (PROTECTED)
# ================================================================

@auth_bp.route("/switch-role", methods=["PUT"])
@token_required
def switch_role(user_id):

    user     = users.find_one({"_id": ObjectId(user_id)})
    new_role = (request.json or {}).get("role")

    if new_role not in ["tutor", "learner"]:
        return jsonify({"error": "Invalid role"}), 400

    if new_role == "tutor" and not user.get("is_verified"):
        return jsonify({"error": "Pass skill test first to become a tutor"}), 403

    users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {
            "role":       new_role,
            "updated_at": datetime.datetime.utcnow()
        }}
    )
    return jsonify({"message": f"Role switched to {new_role}"})


# ================================================================
# GET CREDITS (PROTECTED)
# ================================================================

@auth_bp.route("/credits", methods=["GET"])
@token_required
def get_credits(user_id):
    user = users.find_one({"_id": ObjectId(user_id)})
    return jsonify({"credits": user.get("credits", 0)})


# ================================================================
# SMART MATCH (PROTECTED)
# ================================================================

@auth_bp.route("/smart_match", methods=["GET"])
@token_required
def smart_match(user_id):

    current_user = users.find_one({"_id": ObjectId(user_id)})

    if not current_user:
        return jsonify({"error": "User not found"}), 404

    if current_user.get("role") != "tutor":
        return jsonify({"error": "Only tutors can access smart match"}), 403

    user_learn = set(s.lower() for s in current_user.get("skills_i_want_to_learn", []))
    user_teach = set(s.lower() for s in current_user.get("skills_i_can_teach", []))

    tutors = list(users.find({
        "role":              "tutor",
        "is_verified":       True,
        "skills_i_can_teach":{"$in": list(user_learn)}
    }))

    high_priority = []
    low_priority  = []

    for tutor in tutors:
        if str(tutor["_id"]) == str(user_id):
            continue

        tutor_teach = set(s.lower() for s in tutor.get("skills_i_can_teach", []))
        tutor_learn = set(s.lower() for s in tutor.get("skills_i_want_to_learn", []))

        if user_learn & tutor_teach and tutor_learn & user_teach:
            high_priority.append(tutor)
        elif user_learn & tutor_teach:
            low_priority.append(tutor)

    def add_score(tutor):
        tutor["score"] = round(calculate_score(tutor, current_user), 2)
        return tutor

    scored_high = sorted(map(add_score, high_priority), key=lambda x: x["score"], reverse=True)
    scored_low  = sorted(map(add_score, low_priority),  key=lambda x: x["score"], reverse=True)

    result = scored_high + scored_low

    cleaned = []
    for rank, tutor in enumerate(result, start=1):
        tutor["_id"]  = str(tutor["_id"])
        tutor["rank"] = rank                   # ← rank number added
        tutor["match_type"] = "mutual" if tutor in scored_high else "one-sided"
        tutor.pop("password",     None)
        tutor.pop("test_answers", None)
        tutor.pop("test_meta",    None)
        cleaned.append(tutor)

    limit   = int(request.args.get("limit", 10))
    cleaned = cleaned[:limit]

    return jsonify(cleaned)


# ================================================================
# GET REVIEWS
# ================================================================

@auth_bp.route("/reviews/<tutor_email>", methods=["GET"])
def get_reviews(tutor_email):

    tutor = users.find_one({"email": tutor_email.lower()})
    if not tutor:
        return jsonify({"error": "Tutor not found"}), 404

    tutor_reviews = list(reviews.find({"tutor_id": str(tutor["_id"])}))

    result = []
    for r in tutor_reviews:
        learner = users.find_one({"_id": ObjectId(r["learner_id"])})
        result.append({
            "rating":       r.get("rating"),
            "comment":      r.get("comment"),
            "created_at":   r.get("created_at"),
            "learner_name": learner.get("name") if learner else "Unknown"
        })

    return jsonify(result)


# ================================================================
# TUTOR RECOMMENDATIONS — ML (PROTECTED)
# ================================================================

@auth_bp.route("/recommendations", methods=["GET"])
@token_required
def get_recommendations(user_id):

    top_n  = int(request.args.get("top_n", 5))
    result = get_tutor_recommendations(learner_id=user_id, top_n=top_n)

    if isinstance(result, dict) and "error" in result:
        return jsonify(result), 404

    return jsonify(result)


# ================================================================
# SIMILAR TUTORS — ML
# ================================================================

@auth_bp.route("/similar_tutors/<email>", methods=["GET"])
def similar_tutors(email):

    top_n  = int(request.args.get("top_n", 5))
    result = get_similar_tutors(tutor_email=email, top_n=top_n)

    if isinstance(result, dict) and "error" in result:
        return jsonify(result), 404

    return jsonify(result)