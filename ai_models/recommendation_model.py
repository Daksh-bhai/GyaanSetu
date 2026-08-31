import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# ================================================================
# RECOMMENDATION MODEL
# Skill-based cosine similarity se tutors recommend karta hai
# Smart Match se better — ML scoring + similarity combined
# ================================================================
#
# get_tutor_recommendations(learner_id, top_n=5)
#   → Learner ke learning skills se tutors match karo
#
# get_learner_recommendations(tutor_id, top_n=5)
#   → Tutor ke teaching skills se learners match karo
#
# get_similar_tutors(tutor_email, top_n=5)
#   → Ek tutor jaisi skills wale doosre tutors dhundo
# ================================================================


# -------- HELPER: Skill vector banana -------- #
def _skill_vector(user_skills, all_skills):
    """Binary vector: 1 if skill present, 0 if not"""
    return [1 if skill in user_skills else 0 for skill in all_skills]


# -------- HELPER: All skills vocabulary banana -------- #
def _build_skill_vocab(users_list):
    all_skills = set()
    for u in users_list:
        for skill in u.get("skills_i_can_teach", []):
            all_skills.add(skill.lower().strip())
        for skill in u.get("skills_i_want_to_learn", []):
            all_skills.add(skill.lower().strip())
    return sorted(list(all_skills))


# -------- HELPER: Tutor scoring (rating + badge + similarity) -------- #
def _compute_tutor_score(tutor, similarity_score):
    badge_map = {"Beginner": 0.33, "Intermediate": 0.66, "Expert": 1.0}

    rating          = tutor.get("rating", 0) / 5.0
    badge_score     = badge_map.get(tutor.get("badge", "Beginner"), 0.33)
    sessions_norm   = min(tutor.get("sessions_completed", 0) / 50.0, 1.0)

    # Response time score (lower time = better)
    resp_time = tutor.get("response_time")
    if resp_time:
        resp_score = 1.0 / (1.0 + resp_time / 3600)   # normalize by hour
    else:
        resp_score = 0.5   # neutral

    # Weighted final score
    final = (
        similarity_score * 0.40 +
        rating           * 0.25 +
        badge_score      * 0.15 +
        sessions_norm    * 0.10 +
        resp_score       * 0.10
    )

    return round(final, 4)


# ================================================================
# MAIN FUNCTION 1: LEARNER → TUTOR RECOMMENDATIONS
# ================================================================
def get_tutor_recommendations(learner_id, top_n=5):
    """
    Learner ke liye best tutors recommend karo.

    Args:
        learner_id (str): Learner ka MongoDB ObjectId (string)
        top_n      (int): Kitne results chahiye

    Returns:
        list of dicts: Sorted tutor list with scores
    """

    from models.user_model import users
    from bson import ObjectId

    # -------- Learner fetch -------- #
    learner = users.find_one({"_id": ObjectId(learner_id)})

    if not learner:
        return {"error": "Learner not found"}

    learner_skills = set(
        s.lower().strip() for s in learner.get("skills_i_want_to_learn", [])
    )

    if not learner_skills:
        return {"error": "No learning skills set by learner"}

    # -------- Verified tutors fetch -------- #
    tutors = list(users.find(
        {"role": "tutor", "is_verified": True},
        {"password": 0, "test_answers": 0, "test_meta": 0}
    ))

    if not tutors:
        return {"error": "No verified tutors found"}

    # -------- Build vocabulary -------- #
    all_skills = _build_skill_vocab(tutors + [learner])

    if not all_skills:
        return {"error": "No skills in system"}

    # -------- Learner vector -------- #
    learner_vec = [_skill_vector(learner_skills, all_skills)]

    # -------- Score each tutor -------- #
    results = []

    for tutor in tutors:

        # Skip self
        if str(tutor["_id"]) == str(learner_id):
            continue

        tutor_skills = set(
            s.lower().strip() for s in tutor.get("skills_i_can_teach", [])
        )

        if not tutor_skills:
            continue

        # Cosine similarity
        tutor_vec      = [_skill_vector(tutor_skills, all_skills)]
        similarity     = cosine_similarity(learner_vec, tutor_vec)[0][0]

        # No overlap → skip
        if similarity == 0:
            continue

        final_score = _compute_tutor_score(tutor, similarity)

        results.append({
            "name"               : tutor.get("name"),
            "email"              : tutor.get("email"),
            "badge"              : tutor.get("badge"),
            "rating"             : tutor.get("rating"),
            "sessions_completed" : tutor.get("sessions_completed"),
            "skills_i_can_teach" : tutor.get("skills_i_can_teach"),
            "location"           : tutor.get("location"),
            "bio"                : tutor.get("bio"),
            "similarity_pct"     : round(similarity * 100, 1),
            "final_score"        : final_score
        })

    # -------- Sort & return -------- #
    results.sort(key=lambda x: x["final_score"], reverse=True)
    return results[:top_n]


# ================================================================
# MAIN FUNCTION 2: TUTOR → LEARNER RECOMMENDATIONS
# ================================================================
def get_learner_recommendations(tutor_id, top_n=5):
    """
    Tutor ke liye potential learners recommend karo.
    (Tutor ki teaching skills se learner match)

    Args:
        tutor_id (str): Tutor ka MongoDB ObjectId (string)
        top_n    (int): Kitne results chahiye

    Returns:
        list of dicts: Sorted learner list
    """

    from models.user_model import users
    from bson import ObjectId

    tutor = users.find_one({"_id": ObjectId(tutor_id)})

    if not tutor:
        return {"error": "Tutor not found"}

    tutor_skills = set(
        s.lower().strip() for s in tutor.get("skills_i_can_teach", [])
    )

    if not tutor_skills:
        return {"error": "Tutor has no teaching skills"}

    # All learners
    learners = list(users.find(
        {"role": "learner"},
        {"password": 0}
    ))

    if not learners:
        return {"error": "No learners found"}

    all_skills = _build_skill_vocab(learners + [tutor])

    tutor_vec = [_skill_vector(tutor_skills, all_skills)]

    results = []

    for learner in learners:
        if str(learner["_id"]) == str(tutor_id):
            continue

        learner_skills = set(
            s.lower().strip() for s in learner.get("skills_i_want_to_learn", [])
        )

        if not learner_skills:
            continue

        learner_vec = [_skill_vector(learner_skills, all_skills)]
        similarity  = cosine_similarity(tutor_vec, learner_vec)[0][0]

        if similarity == 0:
            continue

        results.append({
            "name"                  : learner.get("name"),
            "email"                 : learner.get("email"),
            "skills_i_want_to_learn": learner.get("skills_i_want_to_learn"),
            "location"              : learner.get("location"),
            "similarity_pct"        : round(similarity * 100, 1)
        })

    results.sort(key=lambda x: x["similarity_pct"], reverse=True)
    return results[:top_n]


# ================================================================
# MAIN FUNCTION 3: SIMILAR TUTORS
# ================================================================
def get_similar_tutors(tutor_email, top_n=5):
    """
    Ek tutor jaisi skills wale doosre tutors dhundo.
    (Profile page pe "Similar Tutors" section ke liye)

    Args:
        tutor_email (str): Tutor ka email
        top_n       (int): Kitne results chahiye

    Returns:
        list of dicts
    """

    from models.user_model import users

    tutor = users.find_one({"email": tutor_email.lower()})

    if not tutor:
        return {"error": "Tutor not found"}

    all_tutors = list(users.find(
        {"role": "tutor", "is_verified": True},
        {"password": 0, "test_answers": 0}
    ))

    all_skills = _build_skill_vocab(all_tutors)

    if not all_skills:
        return {"error": "No skills in system"}

    tutor_skills = set(
        s.lower().strip() for s in tutor.get("skills_i_can_teach", [])
    )
    tutor_vec = [_skill_vector(tutor_skills, all_skills)]

    results = []

    for t in all_tutors:
        if t["email"] == tutor_email.lower():
            continue

        t_skills = set(
            s.lower().strip() for s in t.get("skills_i_can_teach", [])
        )
        t_vec      = [_skill_vector(t_skills, all_skills)]
        similarity = cosine_similarity(tutor_vec, t_vec)[0][0]

        if similarity == 0:
            continue

        results.append({
            "name"               : t.get("name"),
            "email"              : t.get("email"),
            "badge"              : t.get("badge"),
            "rating"             : t.get("rating"),
            "skills_i_can_teach" : t.get("skills_i_can_teach"),
            "similarity_pct"     : round(similarity * 100, 1)
        })

    results.sort(key=lambda x: x["similarity_pct"], reverse=True)
    return results[:top_n]


# -------- DIRECT RUN → Quick test -------- #
if __name__ == "__main__":
    print("🧪 Recommendation Model Loaded")
    print("Functions available:")
    print("  get_tutor_recommendations(learner_id, top_n=5)")
    print("  get_learner_recommendations(tutor_id, top_n=5)")
    print("  get_similar_tutors(tutor_email, top_n=5)")