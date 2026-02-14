from jwt import encode
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

def create_token(username: str) -> str: 
    if not SECRET_KEY or not ALGORITHM:
        raise ValueError("SECRET_KEY or ALGORITHM is not set")
    expire = datetime.utcnow() + timedelta(hours=1)
    payload = {"username": username, "exp": expire}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return encode(payload, SECRET_KEY, algorithm=ALGORITHM)

print(create_token("token_created_successfully"))