from abc import ABC, abstractmethod
import requests
import json
from time import time

from entities import *

TOKEN = '66912b6a10f7166912b6a10f75'


class Api(ABC):
    @abstractmethod
    def participate(self) -> ParticipateResponse: ...

    @abstractmethod
    def command(self, cmd: Command) -> CommandResponse: ...

    @abstractmethod
    def units(self) -> UnitResponse: ...

    @abstractmethod
    def world(self) -> WorldResponse: ...

    @abstractmethod
    def rounds(self) -> RoundsResponse: ...


class ServerApi(Api):
    def __init__(self, base_url: str, log: bool = False) -> None:
        self.base_url = base_url
        self.log = log

    def request(self, method, endpoint, body=None) -> dict:
        if body is None:
            body = {}
        url = self.base_url + endpoint
        headers = {
            'X-Auth-Token': TOKEN
        }
        r = requests.request(method, url, json=body, headers=headers)
        if r.status_code != 200:
            data = json.dumps(r.json(), indent=2)
            raise Exception('Got %d status code from server, server returned\n %s' % (r.status_code, data))
        return r.json()

    def participate(self) -> ParticipateResponse:
        data = self.request('put', '/play/zombidef/participate')
        return ParticipateResponse.deserialize(data)

    def command(self, cmd: Command) -> CommandResponse:
        body = cmd.serialize()
        data = self.request('post', '/play/zombidef/command', body)
        if self.log:
            now = str(int(time()))
            filename = now + '-command-request.json'
            json.dump(body, open('command/%s' % filename, 'w'))
            filename = now + '-command-response.json'
            json.dump(data, open('command/%s' % filename, 'w'))

        return CommandResponse.deserialize(data)

    def units(self) -> UnitResponse:
        data = self.request('get', '/play/zombidef/units')
        if self.log:
            filename = str(int(time())) + '-units.json'
            json.dump(data, open('units/%s' % filename, 'w'))
        return UnitResponse.deserialize(data)

    def world(self) -> WorldResponse:
        data = self.request('get', '/play/zombidef/world')
        if self.log:
            filename = str(int(time())) + '-world.json'
            json.dump(data, open('world/%s' % filename, 'w'))
        return WorldResponse.deserialize(data)

    def rounds(self) -> RoundsResponse:
        data = self.request('get', '/rounds/zombidef')
        return RoundsResponse.deserialize(data)

testServerApi = ServerApi('https://games-test.datsteam.dev', log=True)
mainServerApi = ServerApi('https://games.datsteam.dev')


class MockApi(Api):
    def __init__(self) -> None:
        pass

    def participate(self) -> ParticipateResponse:
        return ParticipateResponse(1)

    def command(self, cmd: Command) -> CommandResponse:
        return CommandResponse([], [])

    def units(self) -> UnitResponse:
        resp = json.load(open('sample-responses/unit-response.json'))
        return UnitResponse.deserialize(resp)

    def world(self) -> WorldResponse: 
        resp = {
            "realmName": "map1",
            "zpots": [
                {
                    "x": 1,
                    "y": 1,
                    "type": "default"
                }
            ]
        }
        return WorldResponse.deserialize(resp)

    def rounds(self) -> RoundsResponse:
        resp = {
            "gameName": "defense",
            "now": "2021-01-01T00:00:00Z",
            "rounds": [
                {
                    "duration": 60,
                    "endAt": "2021-01-01T00:00:00Z",
                    "name": "Round 1",
                    "repeat": 1,
                    "startAt": "2021-01-01T00:00:00Z",
                    "status": "active"
                }
            ]
        }
        return RoundsResponse.deserialize(resp)
