import pymongo
from fastapi import FastAPI, Path
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

#############################
mongo_host = '127.0.0.1'  # :8000
mongo_port = 27017
#############################

client = pymongo.MongoClient(host=mongo_host, port=mongo_port)
db = client.names

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Assassin's creed"}


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

# if __name__ == "__main__":
#     uvicorn.run(app, host='127.0.0.1', port=3001)
