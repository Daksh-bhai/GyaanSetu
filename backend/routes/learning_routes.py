from flask import Blueprint, request, jsonify
from utils.jwt_utils import token_required
from models.user_model import users
from bson import ObjectId

# -------- AI Learning Module -------- #
from ai_models.learning_module import get_learning_roadmap, get_available_skills

learning_bp = Blueprint("learning", __name__)


# ================================================================
# GET LEARNING ROADMAP
# GET /api/learn/roadmap?skill=python&level=beginner
# ================================================================
@learning_bp.route("/roadmap", methods=["GET"])
@token_required
def roadmap(user_id):

    skill = request.args.get("skill", "").strip()
    level = request.args.get("level", "beginner").strip()

    if not skill:
        return jsonify({"error": "skill parameter required. e.g. ?skill=python&level=beginner"}), 400

    result = get_learning_roadmap(skill, level)

    if "error" in result:
        return jsonify(result), 404

    return jsonify(result)


# ================================================================
# GET ALL AVAILABLE SKILLS
# GET /api/learn/skills
# ================================================================
@learning_bp.route("/skills", methods=["GET"])
def available_skills():
    return jsonify(get_available_skills())


# ================================================================
# GET PERSONALIZED ROADMAP (based on user's learning skills)
# GET /api/learn/my_roadmap?level=beginner
# ================================================================
@learning_bp.route("/my_roadmap", methods=["GET"])
@token_required
def my_roadmap(user_id):

    level = request.args.get("level", "beginner").strip()

    user = users.find_one({"_id": ObjectId(user_id)})

    if not user:
        return jsonify({"error": "User not found"}), 404

    skills_to_learn = user.get("skills_i_want_to_learn", [])

    if not skills_to_learn:
        return jsonify({"error": "No learning skills set on your profile"}), 400

    results = []

    for skill in skills_to_learn:
        roadmap_data = get_learning_roadmap(skill, level)

        # Only add if roadmap found (skip errors)
        if "error" not in roadmap_data:
            results.append(roadmap_data)

    if not results:
        return jsonify({
            "error"            : "No roadmaps found for your skills",
            "your_skills"      : skills_to_learn,
            "available_skills" : get_available_skills()["skills"]
        }), 404

    return jsonify({
        "user"     : user.get("name"),
        "level"    : level,
        "roadmaps" : results,
        "total"    : len(results)
    })
