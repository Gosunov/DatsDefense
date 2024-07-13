from time import sleep, time

from entities import *
from api import mainServerApi, testServerApi, MockApi
from strategy import get_command


def print_status(data: UnitResponse, 
                 world: WorldResponse, 
                 cmd: Command, 
                 resp: CommandResponse):
    points = data.player.points
    base_size = len(data.base)
    zombie_kills = data.player.zombie_kills
    gold = data.player.gold
    attacks = len(cmd.attacks)
    builds = len(cmd.builds)
    rejected = len(resp.errors)
    print(
        "points=%d,base_size=%d,zombie_kills=%d,gold=%d,attacks=%d,builds=%d,rejected=%d" % 
        (points, base_size, zombie_kills, gold, attacks, builds, rejected)
    )


# API = MockApi()
API = testServerApi
# API = mainServerApi

try:
    starts_in_sec = API.participate().starts_in_sec
    print('Round is starting in %ds, waiting...' % starts_in_sec)
    sleep(starts_in_sec + 0.75)
except:
    pass

world = API.world()
while True:
    data = API.units()
    t1 = int(time() * 10**3)
    tleft = data.turn_ends_in_ms
    print("Turn ends in %dms" % tleft)

    cmd = get_command(data, world)

    resp = API.command(cmd)
    for error in resp.errors:
        if error == "you are dead":
            print("We are dead :(")
            exit(0)
        print(error)

    print_status(data, world, cmd, resp)
    t2 = int(time() * 10**3)
    tused = t2 - t1
    print("Finished turn %d in (%dms/%dms)" % (data.turn, tused, tleft))
    textra = tleft - tused
    if textra >= 0:
        sleep(textra / 10**3)
