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


@app.get("/get_nickname")
async def get_nickname():
    pass


@app.post("/add_used")
async def add_used(data: AddUserData):
    data = dict(data)
    result = client.MainNamesDB.used.find_one({"UserId": data["UserId"]})
    if result:
        result["usedNames"].append(data["Name"])
        client.MainNamesDB.used.update_one({"_id": result["_id"]}, {"$set": result})
    else:
        if data["UserName"] == "":
            data["UserName"] = "Игрок"
        client.MainNamesDB.used.insert_one(
            {"UserId": data["UserId"], "UserName": data["UserName"], "usedNames": [data["Name"]]}
        )

    # print(result)
    last_right_letter = get_last_symbol(data["Name"]).upper()
    # print(last_right_letter)
    regx = re.compile(f"^{last_right_letter}", re.IGNORECASE)
    # regx = re.compile("^А", re.IGNORECASE)
    list_of_names = ""
    try:
        list_of_names = [name["Name"] for name in client.MainNamesDB.names.find({"Name": regx})]
        # print(list_of_names)
        shuffle(list_of_names)
    except TypeError:
        sleep(0.1)
    unused_names_list = [name for name in list_of_names if name not in result["usedNames"]]
    # print(result["usedNames"])
    # print(unused_names_list)
    if len(unused_names_list) != 0:
        # print(unused_names_list[0])
        result["usedNames"].append(unused_names_list[0])
        client.MainNamesDB.used.update_one({"_id": result["_id"]}, {"$set": result})
        return unused_names_list[0]

    return ""


@app.post("/clear_user_info")
async def clear_user_info(user_id: GetId):
    client.MainNamesDB.used.delete_one({"UserId": user_id.Id})


def get_last_symbol(new_name):
    key_letter = ""
    wrong_chars = "ъыь"
    for i in range(len(new_name)):
        is_correct = True
        for char in wrong_chars:
            if new_name[::-1][i] == char:
                is_correct = False
                break
        if is_correct:
            key_letter = new_name[::-1][i]
            break

    return key_letter
    # return [char for char in new_name[::-1] if char not in "ъыь"][0].upper()


if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=3001)
