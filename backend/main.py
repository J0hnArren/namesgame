import pymongo
from fastapi import FastAPI, Path
from fastapi.middleware.cors import CORSMiddleware
import unicorn

#############################
mongo_host = '127.0.0.1'  # :8000
mongo_port = 27017
#############################

client = pymongo.MongoClient(host=mongo_host, port=mongo_port)
db = client.HabbitsDB

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
    return {"message": "My fellow brothers, I, Billy Herrington, stand here today, humbled by the task before us, "
                       "mindful of the sacrifices born by our nico Nico ancestors. We are in the midst of crisis. "
                       "Nico Nico Doga is at war against a far reaching storm of disturbance and of leash. Nico "
                       "Nico's economy is badly weakened, a consequence of carelessness and irresponsibility of the "
                       "part of management, but also on the collective failure to make hard choices and prepare for a "
                       "new, mad age. Today, I say to you that the challenge is real, they are serious, and there are "
                       "many. They will not be easily met or in a short span of time, but know that at Nico Nico, "
                       "they will be met. In reaffirming the greatness of our site, we understand that greatness is "
                       "never given, our journey has never been one of shortcuts. It has not been for the path, "
                       "for the feint hearted, or seek only the fleshly pleasures. Rather, it has been the risk "
                       "takers, the wasted genie, the creators of mad things. For us, they toiled in sweatshops, "
                       "endured the lash of the spanking, time and time again. These men struggled and sacrificed so "
                       "that we might LIVE BETTER. We remain the most powerful sight on the Internet and minds are no "
                       "less inventive and services were no less needed, that they were last week, or yesterday, "
                       "or the day before the day after tomorrow. Starting today, we must pull up our pants, "
                       "dust ourselves off, and begin again the work of remaking Nico Nico Doga. Now, there are some "
                       "who question the scale of our ambitions, who suggest that out service system cannot tolerate "
                       "to many movies. There memories are short, for they have forgotten what Nico Nico already has "
                       "done, what free men can achieve when imagination is joined to common purpose. And so, "
                       "to all of the people that are watching this video, from the grandest cities to the small "
                       "villages where Exile was born, know that Nico Nico is a friend of every man who seeks a "
                       "future of love and peace. Now we will begin to leave authorized common materials to Nico Nico "
                       "people and forge a hard, earned piece in this mad world. What is required of us now is a new "
                       "era of responsibility. This is the price and the promise of Nico nicommon's citizenship. Nico "
                       "Nico Doga in the face of are common dangers in this winter of our hardship, let us remember "
                       "these timeless words: ASS WE CAN. Let it be said by our children's children that when we were "
                       "tested by doss attacks, and refused by Youtube, we did not turn back, nor did we falter. And "
                       "we were carried forth that the great gift of freedom be delivered and is safely to future "
                       "generations. Thank You. God Bless. And God Bless Nico Nico Doga. "}


@app.get("/game/{pk}")
async def somewhat(pk: int = Path(..., gt=0, le=3)):
    return {"pk": pk}

# def main():
#     pass
#
#
# if __name__ == '__main__':
#     main()
