import pymongo
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from schemas import *
import re
from random import shuffle
from time import sleep

with open(".env", "r") as f:
    mongo_link = f.read()

client = pymongo.MongoClient(mongo_link)
# collection in our database that is containing already used names for current user
used_col = client.MainNamesDB.used

app = FastAPI()

# a frontend running in a browser has JavaScript code that communicates with this Python backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def start_page():
    return "This is start page, add one of this parameters to the link: /get_nickname, /add_used, /clear_user_info"


@app.post("/get_nickname")
async def get_nickname(user_id: GetId):
    result = client.MainNamesDB.used.find_one({"UserId": user_id.Id, "UserName": {"$exists": True}})
    if result is None:
        client.MainNamesDB.used.insert_one({"UserId": user_id.Id})
        return ""
    else:
        return result["UserName"]


@app.post("/manage_nickname")
async def manage_nickname(data: ManageNickname):
    client.MainNamesDB.used.update_one({"UserId": data.UserId}, {"$set": {"UserName": data.Nickname}})


@app.post("/add_used")
async def add_used(data: AddUserData):
    data = dict(data)
    result = client.MainNamesDB.used.find_one({"UserId": data["UserId"]})
    if result:
        if client.MainNamesDB.names.find_one({"Name": data["Name"]}) is None:
            return "1"
        result["usedNames"].append(data["Name"])
        client.MainNamesDB.used.update_one({"_id": result["_id"]}, {"$set": result})

    last_right_letter = get_last_symbol(data["Name"])
    regx = re.compile(f"^{last_right_letter}", re.IGNORECASE)
    list_of_names = ""
    try:
        list_of_names = [name["text"] for name in client.MainNamesDB.names_table.find({"text": regx})]
        shuffle(list_of_names)
    except TypeError:
        print("Unable to upload data from MainNamesDB.names_table correctly")
        list_of_names = [name["text"] for name in client.MainNamesDB.names_table.find({"text": regx})]
        sleep(0.5)
        shuffle(list_of_names)
    except BufferError:
        print("Unable to upload any data from MainNamesDB.names_table")

    unused_names_list = [name for name in list_of_names if name not in result["usedNames"]]
    if len(unused_names_list) != 0:
        result["usedNames"].append(unused_names_list[0])
        client.MainNamesDB.used.update_one({"_id": result["_id"]}, {"$set": result})
        return unused_names_list[0]
    else:
        return "0"


@app.post("/clear_user_info")
async def clear_user_info(user_id: GetId):
    result = client.MainNamesDB.used.find_one({"UserId": user_id.Id})
    result["usedNames"] = []
    client.MainNamesDB.used.update_one({"UserId": user_id.Id}, {"$set": result})


def get_last_symbol(new_name):
    return [char for char in new_name[::-1] if char not in "ъыь"][0].upper()


if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=3001)
