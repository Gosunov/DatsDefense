def dict_get_not_none(d: dict, key, default):
    v = d.get(key, default)
    if v is None:
        v = default
    return v

class Coordinates:
    def __init__(self,
                 x: int,
                 y: int) -> None:
        self.x = x
        self.y = y

    @classmethod
    def deserialize(cls, data: dict) -> "Coordinates":
        if data is None:
            data = {}
        x = data.get('x', -1)
        y = data.get('y', -1)
        return cls(x, y)

    def serialize(self) -> dict:
        return {
            "x": self.x,
            "y": self.y
        }

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other) -> bool:
        return (self.x, self.y) == (other.x, other.y)


class Tower:
    def __init__(self,
                 x: int,
                 y: int,
                 r: int,
                 last_attack: Coordinates,
                 is_head: bool,
                 id: str,
                 health: int,
                 attack: int) -> None:
        self.x = x
        self.y = y
        self.r = r
        self.last_attack = last_attack
        self.id = id
        self.is_head = is_head
        self.health = health
        self.attack = attack

    @classmethod
    def deserialize(cls, data: dict) -> "Tower":
        x = data.get('x', -1)
        y = data.get('y', -1)
        r = data.get('range', 5)
        last_attack = Coordinates.deserialize(data.get('lastAttack', {}))
        is_head = data.get('isHead', False)
        id = data.get('id', 'unknown-id')
        health = data.get('health', 100)
        attack = data.get('attack', 10)
        return cls(x, y, r, last_attack, is_head, id, health, attack)


class EnemyTower:
    def __init__(self,
                 x: int,
                 y: int,
                 last_attack: Coordinates,
                 is_head: bool,
                 health: int,
                 attack: int) -> None:
        self.x = x
        self.y = y
        self.last_attack = last_attack
        self.id = id
        self.is_head = is_head
        self.health = health
        self.attack = attack

    @classmethod
    def deserialize(cls, data: dict) -> "EnemyTower":
        x = data.get('x', -1)
        y = data.get('y', -1)
        last_attack = Coordinates.deserialize(data.get('lastAttack', {}))
        is_head = data.get('isHead', False)
        health = data.get('health', 100)
        attack = data.get('attack', 10)
        return cls(x, y, last_attack, is_head, health, attack)


class Zombie:
    def __init__(self,
                 x: int,
                 y: int,
                 wait_turns: int,
                 type: str, # TODO: Literal["normal" | ...]
                 speed: int,
                 id: str,
                 health: int,
                 direction: str, # TODO: Literal["up" | ...]
                 attack: int)-> None:
        self.x = x
        self.y = y
        self.wait_turns = wait_turns
        self.type = type
        self.speed = speed
        self.id = id
        self.health = health
        self.direction = direction
        self.attack = attack

    @classmethod
    def deserialize(cls, data: dict) -> "Zombie":
        x = data.get('x', -1)
        y = data.get('y', -1) 
        wait_turns = data.get('waitTurns', -1)
        type = data.get('type', 'normal') 
        speed = data.get('speed', 10) 
        id = data.get('id', 'unknow-id') 
        health = data.get('health', 100) 
        direction = data.get('direction', 'up') 
        attack = data.get('attack', 10)
        return cls(x, y, wait_turns, type, speed, id, health, direction, attack) 


class Player:
    def __init__(self,
                 name: str,
                 gold: int,
                 points: int,
                 zombie_kills: int, 
                 enemy_tower_kills: int, 
                 ) -> None:
        self.name = name
        self.gold = gold
        self.points = points
        self.zombie_kills = zombie_kills
        self.enemy_tower_kills = enemy_tower_kills

    @classmethod
    def deserialize(cls, data: dict) -> "Player":
        name = data.get('name', 'unknown-player')
        gold = data.get('gold', 0)
        points = data.get('points', 0)
        zombie_kills = data.get('zombieKills', 0)
        enemy_tower_kills = data.get('enemyBlockKills', 0)
        return cls(name, gold, points, zombie_kills, enemy_tower_kills)


class UnitResponse:
    def __init__(self,
                 base: list[Tower],
                 enemy_towers: list[EnemyTower],
                 zombies: list[Zombie],
                 player: Player,
                 realm_name: str,
                 turn: int,
                 turn_ends_in_ms: int) -> None:
        self.base = base
        self.enemy_towers = enemy_towers
        self.zombies = zombies
        self.player = player
        self.realm_name = realm_name
        self.turn = turn
        self.turn_ends_in_ms = turn_ends_in_ms

    @classmethod
    def deserialize(cls, data: dict) -> "UnitResponse":
        base = []
        for tower in dict_get_not_none(data, 'base', []):
            base.append(Tower.deserialize(tower))
        enemy_towers = []
        for enemy_tower in dict_get_not_none(data, 'enemyBlocks', []):
            enemy_towers.append(EnemyTower.deserialize(enemy_tower))
        zombies = []
        for zombie in dict_get_not_none(data, 'zombies', []):
            zombies.append(Zombie.deserialize(zombie))
        player = Player.deserialize(data.get('player', {}))
        realm_name = data.get('realmName', 'unknown-realm')
        turn = data.get('turn', 0)
        turn_ends_in_ms = data.get('turnEndsInMs', 0)
        return cls(base, enemy_towers, zombies, player, realm_name, turn, turn_ends_in_ms)


class AttackCommand:
    def __init__(self, id: str, target: Coordinates) -> None:
        self.id = id
        self.target = target

    @classmethod
    def deserialize(cls, data: dict) -> "AttackCommand":
        id = data.get('id', 'unknown')
        target = Coordinates.deserialize(data.get('target', {}))
        return cls(id, target)

    def serialize(self) -> dict:
        return {
            "blockId": self.id,
            "target": self.target.serialize()
        }


class BuildCommand:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    @classmethod
    def from_coordinates(cls, coords: Coordinates) -> "BuildCommand":
        return cls(coords.x, coords.y)

    @classmethod
    def deserialize(cls, data: dict) -> "BuildCommand":
        x = data.get('x', -1)
        y = data.get('y', -1)
        return cls(x, y)

    def serialize(self) -> dict:
        return {
            "x": self.x,
            "y": self.y
        }


class Command:
    def __init__(self, 
                 attacks: list[AttackCommand], 
                 builds: list[BuildCommand], 
                 move_base: Coordinates) -> None:
        self.attacks = attacks
        self.builds = builds
        self.move_base = move_base

    @classmethod
    def deserialize(cls, data: dict) -> "Command":
        attacks = []
        for attack in data.get('attack', []):
            attacks.append(AttackCommand.deserialize(attack))
        builds = []
        for build in data.get('build', []):
            builds.append(BuildCommand.deserialize(build))
        move_base = Coordinates.deserialize(data.get('moveBase', {}))
        return cls(attacks, builds, move_base)

    def serialize(self) -> dict:
        attacks = []
        for attack in self.attacks:
            attacks.append(attack.serialize())
        builds = []
        for build in self.builds:
            builds.append(build.serialize())
        return {
            'attack': attacks,
            'build': builds,
            'moveBase': self.move_base.serialize()
        }


class Zpot:
    def __init__(self, x: int, y: int, type: str) -> None:
        self.x = x
        self.y = y
        self.type = type

    @classmethod
    def deserialize(cls, data: dict) -> "Zpot":
        x = data.get('x', -1)
        y = data.get('y', -1)
        type = data.get('type', 'default')
        return cls(x, y, type)


class WorldResponse:
    def __init__(self, realm_name: str, zpots: list[Zpot]) -> None:
        self.realm_name = realm_name
        self.zpots = zpots

    @classmethod
    def deserialize(cls, data: dict) -> "WorldResponse":
        realm_name = data.get('realmName', 'unknown-realm')
        zpots = []
        for zpot in data.get('zpots', []):
            zpots.append(Zpot.deserialize(zpot))
        return cls(realm_name, zpots)


class Round:
    def __init__(self,
                duration: int,
                end_at: str,
                name: str, 
                repeat: int,
                start_at: str,
                status: str) -> None:
        self.duration = duration 
        self.end_at = end_at 
        self.name = name 
        self.repeat = repeat 
        self.start_at = start_at 
        self.status = status 

    @classmethod
    def deserialize(cls, data: dict) -> "Round":
        duration = data.get('duration', 0)
        end_at = data.get('endAt', '2021-01-01T00:00:00Z')
        name = data.get('name', 'unknown-round')
        repeat = data.get('repeat', 1)
        start_at = data.get('startAt', '2021-01-01T00:00:00Z')
        status = data.get('status', 'unknown')
        return cls(duration, end_at, name, repeat, start_at, status)


class RoundsResponse:
    def __init__(self, game_name: str, now: str, rounds: list[Round]) -> None:
        self.game_name = game_name
        self.now = now
        self.rounds = rounds

    @classmethod
    def deserialize(cls, data: dict) -> "RoundsResponse":
        game_name = data.get('gameName', 'unknown')
        now = data.get('now', '2021-01-01T00:00:00Z')
        rounds = []
        for round in data.get('rounds', []):
            rounds.append(Round.deserialize(round))
        return cls(game_name, now, rounds)


class ParticipateResponse:
    def __init__(self, starts_in_sec: int) -> None:
        self.starts_in_sec = starts_in_sec

    @classmethod
    def deserialize(cls, data: dict) -> "ParticipateResponse":
        starts_in_sec = data.get('startsInSec', 0)
        return cls(starts_in_sec)


class CommandResponse:
    def __init__(self, accepted_commands: list[AttackCommand | BuildCommand | Coordinates], errors: list[str]):
        self.accepted_commands = accepted_commands
        self.errors = errors

    @classmethod
    def deserialize(cls, data: dict) -> "CommandResponse":
        accepted_commands = []
        commands = data.get('acceptedCommands', {})
        for attack in commands.get('attacks', []):
            accepted_commands.append(AttackCommand.deserialize(attack))
        for build in commands.get('builds', []):
            accepted_commands.append(AttackCommand.deserialize(build))
        accepted_commands.append(Coordinates.deserialize(commands.get('moveBase')))
        errors = dict_get_not_none(data, 'errors', [])
        return cls(accepted_commands, errors)
