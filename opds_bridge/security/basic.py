import base64
from fastapi import HTTPException, Request, Depends
from opds_bridge.config import get_settings

def basic_auth_guard(request: Request, settings=Depends(get_settings)):
    user = settings.OPDS_BASIC_USER
    pw = settings.OPDS_BASIC_PASS
    if not user and not pw:
        return

    auth = request.headers.get("authorization", "")
    if not auth.lower().startswith("basic "):
        raise HTTPException(
            status_code=401,
            detail="Auth required",
            headers={"WWW-Authenticate": 'Basic realm="OPDS"'},
        )
    try:
        decoded = base64.b64decode(auth.split(" ", 1)[1]).decode("utf-8")
        got_user, got_pw = decoded.split(":", 1)
    except Exception:
        raise HTTPException(status_code=400, detail="Malformed Authorization")

    if got_user != user or got_pw != pw:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": 'Basic realm="OPDS"'},
        )
