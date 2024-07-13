from abc import ABC, abstractmethod
import requests
import json

from entities import *

TOKEN = '66912b6a10f7166912b6a10f75'


class Api(ABC):
    @classmethod
    @abstractmethod
    def participate(cls) -> ParticipateResponse: ...

    @classmethod
    @abstractmethod
    def command(cls, cmd: Command) -> CommandResponse: ...

    @classmethod
    @abstractmethod
    def units(cls) -> UnitResponse: ...

    @classmethod
    @abstractmethod
    def world(cls) -> WorldResponse: ...

    @classmethod
    @abstractmethod
    def rounds(cls) -> RoundsResponse: ...


class ServerApi(Api):
    @classmethod
    @property
    @abstractmethod
    def BASE_URL(cls) -> str: ...

    @classmethod
    @abstractmethod
    def request(cls, method, endpoint, body=None) -> dict:
        if body is None:
            body = {}
        url = cls.BASE_URL + endpoint
        headers = {
            'X-Auth-Token': TOKEN
        }
        r = requests.request(method, url, json=body, headers=headers)
        if r.status_code != 200:
            data = json.dumps(r.json(), indent=2)
            raise Exception('Got %d status code from server, server returned\n %s' % (r.status_code, data))
        return r.json()

    @classmethod
    def participate(cls) -> ParticipateResponse:
        data = cls.request('put', '/play/zombidef/participate')
        return ParticipateResponse.deserialize(data)

    @classmethod
    def command(cls, cmd: Command) -> CommandResponse:
        body = cmd.serialize()
        data = cls.request('post', '/play/zombidef/command', body)
        return CommandResponse.deserialize(data)

    @classmethod
    def units(cls) -> UnitResponse:
        data = cls.request('get', '/play/zombidef/units')
        return UnitResponse.deserialize(data)

    @classmethod
    def world(cls) -> WorldResponse:
        data = cls.request('get', '/play/zombidef/world')
        return WorldResponse.deserialize(data)

    @classmethod
    def rounds(cls) -> RoundsResponse:
        data = cls.request('get', '/rounds/zombidef')
        return RoundsResponse.deserialize(data)


class TestServerApi(ServerApi):
    @classmethod
    @property
    def BASE_URL(cls) -> str: return 'https://games-test.datsteam.dev'


class MainServerApi(ServerApi):
    @classmethod
    @property
    def BASE_URL(cls) -> str: return 'https://games.datsteam.dev'


class MockApi(Api):
    @classmethod
    def participate(cls) -> ParticipateResponse:
        return ParticipateResponse(1)

    @classmethod
    def command(cls, cmd: Command) -> CommandResponse:
        return CommandResponse([], [])

    @classmethod
    def units(cls) -> UnitResponse:
        resp = json.load(open('sample-responses/unit-response.json'))
        return UnitResponse.deserialize(resp)

    @classmethod
    def world(cls) -> WorldResponse: 
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

    @classmethod
    def rounds(cls) -> RoundsResponse:
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