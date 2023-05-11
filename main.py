from enum import Enum

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from typing_extensions import Annotated
from pydantic import BaseModel, Field
from random import choice

app = FastAPI()

class Slots(str, Enum):
    RR = 'rr'
    RA = 'ra'
    RS = 'rs'
    RD = 'rd'
    AA = 'aa'
    AS = 'as'
    AD = 'ad'
    SS = 'ss'
    DS = 'ds'
    DD = 'dd'

class JoinModel(BaseModel):
    name: str
    public: Slots
    private_aa: Slots
    private_as: Slots
    private_ad: Slots
    private_ss: Slots
    private_ds: Slots
    private_dd: Slots


class HandModel(JoinModel):
    wins: int = 0
    losses: int = 0
    battles: int = 0

def battle(a, b):
    choices = ['a', 'd', 's']
    a["public"] = a["public"].replace('r', choice(choices), 1)
    a["public"] = a["public"].replace('r', choice(choices), 1)
    b["public"] = b["public"].replace('r', choice(choices), 1)
    b["public"] = b["public"].replace('r', choice(choices), 1)
    a["public"] = ''.join(sorted(a["public"]))
    b["public"] = ''.join(sorted(b["public"]))
    a_hand = a["public"] + a["private_" + b["public"]]
    b_hand = b["public"] + b["private_" + a["public"]]
    a_hand = a_hand.replace('r', choice(choices), 1)
    a_hand = a_hand.replace('r', choice(choices), 1)
    b_hand = b_hand.replace('r', choice(choices), 1)
    b_hand = b_hand.replace('r', choice(choices), 1)

    a_dmg, b_dmg = 0, 0

    print(a_hand, b_hand)
        
    # Star attacks
    if (a_hand.count("s") - b_hand.count("s") >= 3):
        return 1
    if (b_hand.count("s") - a_hand.count("s") >= 3):
        return 2

    # A attacking B
    b_dmg += 2 * max(0, a_hand.count("a") - b_hand.count("d")) + a_hand.count("a")
    if b_hand.count("d") >= 1:
        b_dmg = max(b_dmg, 0)

    # B attacking A
    a_dmg += 2 * max(0, b_hand.count("a") - a_hand.count("d")) + b_hand.count("a")
    if a_hand.count("d") == 1:
        a_dmg = max(a_dmg, 0)

    # # A attacking B
    # if (b_hand.count("d") >= a_hand.count("a")):
    #     a_dmg += a_hand.count("a")
    # if (b_hand.count("d") < a_hand.count("a")):
    #     a_dmg += b_hand.count("d")
    #     b_dmg += 2 * max(0, a_hand.count("a") - b_hand.count("d"))

    # #  B attacking A
    # if (a_hand.count("d") >= b_hand.count("a")):
    #     b_dmg += b_hand.count("a")
    # if (a_hand.count("d") < b_hand.count("a")):
    #     b_dmg += a_hand.count("d")
    #     a_dmg += 2 * max(0, b_hand.count("a") - a_hand.count("d"))

    print(a["name"], a_dmg, b["name"], b_dmg)
    if a_dmg < b_dmg:
        return 1
    elif a_dmg > b_dmg:
        return 2
    else:
        return 0
    
players = [
        HandModel(
            name="attack andy",
            public=Slots.AA,
            private_aa=Slots.AA,
            private_as=Slots.AA,
            private_ad=Slots.AA,
            private_ds=Slots.AA,
            private_dd=Slots.AA,
            private_ss=Slots.AA,
            wins=0),
        HandModel(
            name="defense darrel",
            public=Slots.DD,
            private_aa=Slots.DD,
            private_as=Slots.DD,
            private_ad=Slots.DD,
            private_ds=Slots.DD,
            private_dd=Slots.DD,
            private_ss=Slots.DD,
            wins=0),
        HandModel(
            name="random ron",
            public=Slots.RR,
            private_aa=Slots.RR,
            private_as=Slots.RR,
            private_ad=Slots.RR,
            private_ds=Slots.RR,
            private_dd=Slots.RR,
            private_ss=Slots.RR,
            wins=0),
        HandModel(
            name="smart random randy",
            public=Slots.RR,
            private_aa=Slots.RR,
            private_as=Slots.RS,
            private_ad=Slots.RR,
            private_ds=Slots.RS,
            private_dd=Slots.RR,
            private_ss=Slots.SS,
            wins=0),
        HandModel(
            name="super smart random rohan",
            public=Slots.RR,
            private_aa=Slots.RD,
            private_as=Slots.DS,
            private_ad=Slots.RD,
            private_ds=Slots.RS,
            private_dd=Slots.RR,
            private_ss=Slots.SS,
            wins=0),
        HandModel(
            name="Smart Defense Dan",
            public=Slots.DD,
            private_aa=Slots.DD,
            private_as=Slots.DS,
            private_ad=Slots.DD,
            private_ds=Slots.DS,
            private_dd=Slots.DD,
            private_ss=Slots.SS,
            wins=0),
        HandModel(
            name="Star Stewart",
            public=Slots.SS,
            private_aa=Slots.SS,
            private_as=Slots.SS,
            private_ad=Slots.SS,
            private_ds=Slots.SS,
            private_dd=Slots.SS,
            private_ss=Slots.AD,
            wins=0),
        HandModel(
            name="Attack Defense Adam",
            public=Slots.AA,
            private_aa=Slots.AD,
            private_as=Slots.AD,
            private_ad=Slots.AD,
            private_ds=Slots.AS,
            private_dd=Slots.AA,
            private_ss=Slots.AD,
            wins=0),
        HandModel(
            name="Star Faker Sean",
            public=Slots.SS,
            private_aa=Slots.AD,
            private_as=Slots.AD,
            private_ad=Slots.AD,
            private_ds=Slots.AA,
            private_dd=Slots.AA,
            private_ss=Slots.AA,
            wins=0),
        ]

def play_round():
    for i in range(len(players)):
        for j in range(i + 1, len(players)):
            result = battle(players[i].dict(), players[j].dict())
            if result == 1:
                players[i].wins += 1
                players[j].losses += 1
            elif result == 2:
                players[j].wins += 1
                players[i].losses += 1
            players[i].battles += 1
            players[j].battles += 1

@app.post("/api/join")
def join(request: JoinModel):
    hand = HandModel.parse_obj(request.dict())
    hand.wins = 0
    players.append(hand)
    return { 'room_code': 0 }

@app.get("/api/leaderboard")
def leaderboard():
    response = {}
    play_round()
    for player in players:
        response[player.name] = player.wins - player.losses 
    return response


app.mount("/", StaticFiles(directory="static", html=True), name="static")
