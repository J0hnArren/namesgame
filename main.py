import pymongo
from bson.objectid import ObjectId
from fastapi import FastAPI, Path
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from schemas import *

#############################
mongo_host = '127.0.0.1'  # :8000
mongo_port = 27017
#############################

with open(".env", "r") as f:
    mongo_link = f.read()

client = pymongo.MongoClient(mongo_link)
used_doc = client.db.used

app = FastAPI()

# a frontend running in a browser has JavaScript code that communicates with this Python backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/{user_id}/")
async def root(id_: NewName):
    client.db.used.insertOne({"_id": NewName.id, "used_names": [""]})

    return 'client.db.used.find_one({"_id": NewName.id})'


@app.get("/game/{pk}")
async def somewhat(pk: int = Path(..., gt=0, le=3)):
    message = "default text"
    if pk == 1:
        message = "Не позволяй клинку поразить невиновного"
    elif pk == 2:
        message = "Никогда не подставляй под удар Братств"
    else:
        message = "Скрывайся у всех на виду"
    return {"pk": message}


if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=3001)
