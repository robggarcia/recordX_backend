from mongodb import db
import pandas as pd
import bcrypt

sheet_id = "1ZlsxceBGl1kIs5-OA-PRI9dW3S1FdNgOASq2mkMrZck"
sheet_name = "Sample_Record_Data"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}".format()

df = pd.read_csv(url)

# record_data = df.to_dict()
record_data = df.to_dict(orient="records")

for record in record_data:
    record['genre'] = record['genre'].split(", ")

try:
    db.drop_collection("record_collection")
    record_col = db["record_collection"]
    record_col.insert_many(record_data)
except:
    print("There was an error seeding record data")

# artist_list = df["artist"].to_list()
# devo = df[df.artist == "Devo"]
# genre = devo.genre
# genre[0] = genre[0].split(", ")

# print(genre)
# print(devo.cost)

user_data = [
    {
        "username": "stanley",
        "email": "stanley@gmail.com",
        "password": "stanley123"
    }, {
        "username": "oscar",
        "email": "oscar@gmail.com",
        "password": "oscar123"
    }, {
        "username": "tilly",
        "email": "tilly@gmail.com",
        "password": "tilly123"
    }, {
        "username": "rob",
        "email": "rob@gmail.com",
        "password": "rob123",
        "admin": True
    }
]

for user in user_data:
    user["password"] = bcrypt.hashpw(
        user["password"].encode('utf-8'), bcrypt.gensalt())

print(user_data)


try:
    db.drop_collection("user_collection")
    user_col = db["user_collection"]
    user_col.insert_many(user_data)
except:
    print("There was an error seeding user data")
