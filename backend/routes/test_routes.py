from flask import Blueprint, request, jsonify
from utils.jwt_utils import token_required
from models.user_model import users
from bson import ObjectId
from data.question_bank import question_bank
import random
import datetime

test_bp = Blueprint("test", __name__)

# ================================================================
# CONSTANTS
# ================================================================

MAX_ATTEMPTS  = 3          # kitni baar fail ho sakta hai
COOLDOWN_MINS = 60         # fail ke baad kitne minute wait karna padega


# ================================================================
# START TEST
# ================================================================

@test_bp.route("/start", methods=["POST"])
@token_required
def start_test(user_id):

    data   = request.json or {}
    domain = data.get("domain")
    field  = data.get("field")
    level  = data.get("level")

    if not domain or not field or not level:
        return jsonify({"error": "domain, field, level — teeno required hain"}), 400

    user = users.find_one({"_id": ObjectId(user_id)})

    # -------- PREVENT MULTIPLE CONCURRENT TESTS -------- #
    if user.get("test_answers"):
        return jsonify({"error": "Pehle wala test pehle submit karo"}), 400

    # -------- ATTEMPT LIMIT CHECK -------- #
    # test_meta mein attempts aur last_attempt_at track hoga
    test_meta = user.get("test_meta") or {}
    attempts  = test_meta.get("attempts", 0)
    last_fail = test_meta.get("last_failed_at")

    if attempts >= MAX_ATTEMPTS:
        return jsonify({
            "error":        f"Maximum {MAX_ATTEMPTS} attempts limit reach ho gayi",
            "attempts_used": attempts,
            "suggestion":   "Ek lower level try karo ya admin se contact karo"
        }), 429

    # -------- COOLDOWN CHECK -------- #
    if last_fail:
        if isinstance(last_fail, str):
            last_fail = datetime.datetime.fromisoformat(last_fail)
        elapsed_mins = (datetime.datetime.utcnow() - last_fail).total_seconds() / 60
        if elapsed_mins < COOLDOWN_MINS:
            wait_mins = int(COOLDOWN_MINS - elapsed_mins) + 1
            return jsonify({
                "error":          f"Cooldown active — {wait_mins} minute baad try karo",
                "wait_minutes":   wait_mins,
                "attempts_used":  attempts,
                "attempts_left":  MAX_ATTEMPTS - attempts
            }), 429

    # -------- GET QUESTIONS -------- #
    try:
        questions = question_bank[domain][field][level]
    except KeyError:
        return jsonify({"error": f"Invalid domain/field/level — '{domain}/{field}/{level}' nahi mila"}), 400

    if len(questions) == 0:
        return jsonify({"error": "Is topic ke liye questions available nahi hain"}), 400

    selected = random.sample(questions, min(10, len(questions)))

    # -------- SAVE IN DB -------- #
    users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {
            "test_answers": selected,
            "test_meta": {
                "domain":         domain,
                "field":          field,
                "level":          level,
                "attempts":       attempts,       # purana count save raho — submit pe increment hoga
                "last_failed_at": last_fail,
                "started_at":     datetime.datetime.utcnow().isoformat()
            }
        }}
    )

    # Answers strip karke bhejo
    questions_to_send = [
        {"question": q["question"], "options": q["options"]}
        for q in selected
    ]

    return jsonify({
        "message":       "Test shuru ho gaya",
        "total":         len(questions_to_send),
        "questions":     questions_to_send,
        "attempts_used": attempts,
        "attempts_left": MAX_ATTEMPTS - attempts
    })


# ================================================================
# SUBMIT TEST
# ================================================================

@test_bp.route("/submit", methods=["POST"])
@token_required
def submit_test(user_id):

    data    = request.json or {}
    answers = data.get("answers")
    level   = data.get("level")
    field   = data.get("field")

    if not answers or not level or not field:
        return jsonify({"error": "answers, level, field — teeno required hain"}), 400

    user      = users.find_one({"_id": ObjectId(user_id)})
    questions = user.get("test_answers", [])

    if not questions:
        return jsonify({"error": "Koi active test nahi mila — pehle /test/start call karo"}), 400

    # -------- SCORE CALCULATE -------- #
    option_map = {"A": 0, "B": 1, "C": 2, "D": 3}
    score      = 0

    for i, q in enumerate(questions):
        if i >= len(answers):
            continue
        user_ans = answers[i]
        if isinstance(user_ans, str) and user_ans.upper() in option_map:
            idx       = option_map[user_ans.upper()]
            actual    = q["options"][idx] if idx < len(q["options"]) else ""
        else:
            actual = user_ans
        if actual == q["answer"]:
            score += 1

    total     = len(questions)
    test_meta = user.get("test_meta") or {}
    attempts  = test_meta.get("attempts", 0) + 1    # yahan increment karo

    # ================================================================
    # PASS (score >= 7)
    # ================================================================
    if score >= 7:

        already_verified = user.get("is_verified", False)

        # -------- UPDATE USER -------- #
        users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {
                "is_verified":    True,
                "verified_skill": field,
                "verified_level": level,
                "updated_at":     datetime.datetime.utcnow()
            }}
        )

        # 5 credits sirf pehli baar
        credits_awarded = 0
        if not already_verified:
            users.update_one(
                {"_id": ObjectId(user_id)},
                {"$inc": {"credits": 5}}
            )
            credits_awarded = 5
            bonus_msg = " Tumhe 5 bonus credits mile hain!"
        else:
            bonus_msg = ""

        # -------- CLEANUP TEST DATA (pass pe reset attempts bhi) -------- #
        users.update_one(
            {"_id": ObjectId(user_id)},
            {"$unset": {
                "test_answers": "",
                "test_meta":    ""
            }}
        )

        return jsonify({
            "result":          "PASS",
            "score":           score,
            "total":           total,
            "message":         "Congratulations! Ab tum verified ho." + bonus_msg,
            "credits_awarded": credits_awarded
        })

    # ================================================================
    # FAIL (score < 7)
    # ================================================================
    else:

        suggestion = get_next_level(level)

        # -------- CLEANUP + SAVE FAIL META -------- #
        # test_answers hata do, lekin attempt count + last_failed_at save karo
        users.update_one(
            {"_id": ObjectId(user_id)},
            {
                "$unset": {"test_answers": ""},
                "$set": {
                    "test_meta": {
                        "domain":         test_meta.get("domain"),
                        "field":          field,
                        "level":          level,
                        "attempts":       attempts,
                        "last_failed_at": datetime.datetime.utcnow().isoformat()
                    }
                }
            }
        )

        attempts_left = MAX_ATTEMPTS - attempts

        response = {
            "result":         "FAIL",
            "score":          score,
            "total":          total,
            "attempts_used":  attempts,
            "suggestion":     suggestion
        }

        if attempts_left > 0:
            response["message"]       = f"Fail! {COOLDOWN_MINS} minute baad retry kar sakte ho."
            response["attempts_left"] = attempts_left
            response["cooldown_mins"] = COOLDOWN_MINS
        else:
            response["message"]       = f"Saari {MAX_ATTEMPTS} attempts khatam — level change karo."
            response["attempts_left"] = 0

        return jsonify(response)


# ================================================================
# LEVEL SUGGESTION HELPER
# ================================================================

def get_next_level(level):
    if level == "expert":
        return "Intermediate level try karo"
    elif level == "intermediate":
        return "Beginner level try karo"
    else:
        return "Abhi learner raho aur zyada practice karo"


# ================================================================
# TEST STATUS — kitne attempts bache hain
# GET /api/test/status
# ================================================================

@test_bp.route("/status", methods=["GET"])
@token_required
def test_status(user_id):

    user      = users.find_one({"_id": ObjectId(user_id)})
    test_meta = user.get("test_meta") or {}
    attempts  = test_meta.get("attempts", 0)
    last_fail = test_meta.get("last_failed_at")

    cooldown_active  = False
    wait_minutes     = 0

    if last_fail:
        if isinstance(last_fail, str):
            last_fail = datetime.datetime.fromisoformat(last_fail)
        elapsed_mins = (datetime.datetime.utcnow() - last_fail).total_seconds() / 60
        if elapsed_mins < COOLDOWN_MINS:
            cooldown_active = True
            wait_minutes    = int(COOLDOWN_MINS - elapsed_mins) + 1

    return jsonify({
        "is_verified":    user.get("is_verified", False),
        "verified_skill": user.get("verified_skill"),
        "verified_level": user.get("verified_level"),
        "attempts_used":  attempts,
        "attempts_left":  max(0, MAX_ATTEMPTS - attempts),
        "max_attempts":   MAX_ATTEMPTS,
        "cooldown_active":cooldown_active,
        "wait_minutes":   wait_minutes if cooldown_active else 0,
        "active_test":    bool(user.get("test_answers"))
    })