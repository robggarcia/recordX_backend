from dotenv import load_dotenv
import os
import jwt
import datetime

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")
print(JWT_SECRET)
email = 'test@gmail.com'
username = 'test_user'
_id = '63f15c6f456dcee722c7bd78'

token = jwt.encode({"email": email, "username": username},
                   JWT_SECRET, algorithm="HS256")

token = jwt.encode(
    {"_id": _id, "email": email, "username": username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=45)}, JWT_SECRET, algorithm="HS256")
data = jwt.decode(token, JWT_SECRET, algorithms="HS256")


print(token)
print(data)
