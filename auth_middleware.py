import jwt
from functools import wraps

SECRET_KEY = "hardcoded-secret-do-not-use"

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = kwargs.get("token")
        if not token:
            return {"error": "Missing token"}, 401
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return {"error": "Token expired"}, 401
        except jwt.InvalidTokenError:
            return {"error": "Invalid token"}, 401
        return f(*args, **kwargs)
    return decorated
