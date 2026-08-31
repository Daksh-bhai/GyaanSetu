import jwt
import datetime
from functools import wraps
from flask import request, jsonify
import os
from dotenv import load_dotenv
from bson import ObjectId

load_dotenv()
SECRET_KEY = os.getenv("JWT_SECRET", "fallback_secret")


# -------- Generate JWT Token -------- #
def generate_token(user_id):

    payload = {
        "user_id": str(user_id),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    if isinstance(token, bytes):
        token = token.decode('utf-8')

    return token


# -------- Verify JWT Token -------- #
def verify_token(token):

    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded["user_id"]

    except jwt.ExpiredSignatureError:
        return None

    except jwt.InvalidTokenError:
        return None


# -------- JWT Decorator -------- #
# ============================================================ #
#   BAN CHECK yahan hota hai — ek jagah, poora system cover    #
#                                                               #
#   Banned user kya nahi kar sakta:                             #
#   - Session request bhejna                                    #
#   - Session accept/reject/complete/cancel karna               #
#   - Tutor ko rate karna                                       #
#   - Skills update karna                                       #
#   - Kisi ko report karna                                      #
#   - Dashboard access karna                                    #
#   - Smart match use karna                                     #
#                                                               #
#   Banned user kya kar sakta hai (token_required nahi lagta):  #
#   - Login (auth/login)                                        #
#   - Public profiles dekhna (auth/profile/<email>)             #
#   - Tutors list dekhna (auth/tutors)                          #
# ============================================================ #

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({"error": "Token missing"}), 401

        parts = auth_header.split(" ")

        if len(parts) != 2 or parts[0] != "Bearer":
            return jsonify({"error": "Invalid token format"}), 401

        token = parts[1]
        user_id = verify_token(token)

        if not user_id:
            return jsonify({"error": "Invalid or expired token"}), 401

        # -------- BAN CHECK -------- #
        # Import yahan karo — circular import se bachne ke liye
        from models.user_model import users

        user = users.find_one(
            {"_id": ObjectId(user_id)},
            {"is_banned": 1, "ban_reason": 1}   # sirf zarori fields fetch karo
        )

        if user and user.get("is_banned"):
            return jsonify({
                "error": "Your account has been banned",
                "reason": user.get("ban_reason", "Violation of platform rules"),
                "contact": "Contact support to appeal this ban"
            }), 403

        return f(user_id, *args, **kwargs)

    return decorated