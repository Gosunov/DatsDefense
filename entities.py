class Coordinates:
    def __init__(self,
                 x: int,
                 y: int) -> None:
        self.x = x
        self.y = y

    @classmethod
    def deserialize(cls, data: dict) -> "Coordinates":
        x = data.get('x', -1)
        y = data.get('y', -1)
        return cls(x, y)


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
                 wait_turns: str,
                 type: str,
                 speed: int,
                 id: str,
                 health: int,
                 direction: str, # TODO: Literal["normal" | ]
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
        for tower in data.get('base', []):
            base.append(Tower.deserialize(tower))
        enemy_towers = []
        for enemy_tower in data.get('enemyTowers', []):
            enemy_towers.append(EnemyTower.deserialize(enemy_tower))
        zombies = []
        for zombie in data.get('zombies', []):
            zombies.append(Zombie.deserialize(zombie))
        player = Player.deserialize(data.get('player', {}))
        realm_name = data.get('realmName', 'unknown-realm')
        turn = data.get('turn', 0)
        turn_ends_in_ms = data.get('turnEndsInMs', 0)
        return cls(base, enemy_towers, zombies, player, realm_name, turn, turn_ends_in_ms)
