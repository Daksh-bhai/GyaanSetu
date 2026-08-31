import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pickle
import os

# ================================================================
# BADGE PREDICTION MODEL
# Predicts tutor badge: "Beginner" / "Intermediate" / "Expert"
# Features: sessions_completed, rating, rating_count, response_time
# ================================================================

MODEL_PATH = os.path.join(os.path.dirname(__file__), "badge_model.pkl")


# -------- STEP 1: SYNTHETIC TRAINING DATA -------- #
def generate_training_data(n=1000):
    """
    Synthetic data banata hai based on domain rules.
    Real data aane ke baad yahan MongoDB se fetch karke replace kar sakte ho.
    """

    np.random.seed(42)
    X = []
    y = []

    for _ in range(n):
        sessions   = np.random.randint(0, 60)
        rating     = round(np.random.uniform(0, 5), 2)
        r_count    = np.random.randint(0, 40)
        resp_time  = np.random.uniform(60, 7200)   # seconds

        # --- Ground truth labels (same logic as current rule-based) --- #
        if sessions > 10 and rating >= 4.0:
            badge = "Expert"
        elif sessions > 5 and rating >= 3.0:
            badge = "Intermediate"
        else:
            badge = "Beginner"

        # --- Noise inject (real world mein data clean nahi hota) --- #
        if np.random.random() < 0.05:
            badge = np.random.choice(["Beginner", "Intermediate", "Expert"])

        X.append([sessions, rating, r_count, resp_time])
        y.append(badge)

    return np.array(X), y


# -------- STEP 2: TRAIN & SAVE MODEL -------- #
def train_model():
    print("🔄 Training badge prediction model...")

    X, y = generate_training_data()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=150,
        max_depth=10,
        random_state=42,
        class_weight="balanced"   # handle class imbalance
    )
    model.fit(X_train, y_train)

    # --- Print accuracy report --- #
    y_pred = model.predict(X_test)
    print("\n📊 Model Performance:\n")
    print(classification_report(y_test, y_pred))

    # --- Save model --- #
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)

    print(f"✅ Badge model saved → {MODEL_PATH}")
    return model


# -------- STEP 3: LOAD (OR TRAIN IF NOT EXISTS) -------- #
def load_model():
    if os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, "rb") as f:
            return pickle.load(f)
    else:
        return train_model()


# -------- STEP 4: PREDICT FUNCTION (Routes mein use hoga) -------- #
def predict_badge(sessions_completed, rating, rating_count, response_time=None):
    """
    Tutor ka badge predict karta hai.

    Args:
        sessions_completed (int)  : Total sessions done
        rating             (float): Average rating (0-5)
        rating_count       (int)  : Number of ratings received
        response_time      (float): Avg response time in seconds (None = unknown)

    Returns:
        dict: {
            "badge"      : "Beginner" / "Intermediate" / "Expert",
            "confidence" : {"Beginner": 10.0, "Intermediate": 30.0, "Expert": 60.0}
        }
    """

    model = load_model()

    # Default response time if not available
    if response_time is None:
        response_time = 1800.0

    features = [[
        float(sessions_completed),
        float(rating),
        float(rating_count),
        float(response_time)
    ]]

    badge      = model.predict(features)[0]
    proba      = model.predict_proba(features)[0]
    classes    = model.classes_
    confidence = {cls: round(p * 100, 1) for cls, p in zip(classes, proba)}

    return {
        "badge"      : badge,
        "confidence" : confidence
    }


# -------- STEP 5: RETRAIN ON REAL DATA (Optional, future use) -------- #
def retrain_on_real_data(user_list):
    """
    MongoDB se real tutor data aane ke baad call karo.
    user_list: list of tutor dicts from MongoDB

    Example:
        from models.user_model import users
        tutors = list(users.find({"role": "tutor", "sessions_completed": {"$gt": 0}}))
        retrain_on_real_data(tutors)
    """

    if len(user_list) < 20:
        print("⚠️  Not enough real data (< 20). Using synthetic data.")
        return train_model()

    X = []
    y = []

    for u in user_list:
        sessions  = u.get("sessions_completed", 0)
        rating    = u.get("rating", 0)
        r_count   = u.get("rating_count", 0)
        resp_time = u.get("response_time", 1800)
        badge     = u.get("badge", "Beginner")

        if badge not in ["Beginner", "Intermediate", "Expert"]:
            continue

        X.append([sessions, rating, r_count, resp_time or 1800])
        y.append(badge)

    model = RandomForestClassifier(
        n_estimators=150,
        max_depth=10,
        random_state=42,
        class_weight="balanced"
    )
    model.fit(np.array(X), y)

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)

    print("✅ Model retrained on real data!")
    return model


# -------- DIRECT RUN → Train model -------- #
if __name__ == "__main__":
    train_model()

    # Quick test
    print("\n🧪 Quick Test:")
    print(predict_badge(15, 4.5, 20, 300))    # Expected: Expert
    print(predict_badge(7,  3.2, 10, 900))    # Expected: Intermediate
    print(predict_badge(2,  2.0, 3,  3600))   # Expected: Beginner