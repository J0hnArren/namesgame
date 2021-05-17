import pymongo
from fastapi import FastAPI, Path
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from schemas import *
import re
from random import shuffle

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


@app.post("/add_used")
async def add_used(data: AddUserData):
    data = dict(data)
    result = client.MainNamesDB.used.find_one({"UserId": data["UserId"]})
    if result:
        result["usedNames"].append(data["Name"])
        client.MainNamesDB.used.update_one({"_id": result["_id"]}, {"$set": result})
    else:
        client.MainNamesDB.used.insert_one({"UserId": data["UserId"], "usedNames": [data["Name"]]})

    last_right_letter = get_last_symbol(data["Name"]).upper()
    # regx = re.compile(f"^{last_right_letter}", re.IGNORECASE)
    regx = re.compile("^Д", re.IGNORECASE)
    list_of_names = [name["Name"] for name in client.MainNamesDB.names.find({"Name": regx})]
    shuffle(list_of_names)
    print(list_of_names[0])
    print(result["usedNames"])

    return ""


@app.post("/clear_user_info")
async def somewhat(pk: int = Path(..., gt=0, le=3)):
    message = "default text"
    if pk == 1:
        message = "Не позволяй клинку поразить невиновного"
    elif pk == 2:
        message = "Никогда не подставляй под удар Братство"
    else:
        message = "Скрывайся у всех на виду"
    return {"pk": message}


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


if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=3001)
