from typing import Any

def turncache(f):
    ''' 
    DANGER: Use this decorator only with functions 
    that takes the same arguments, when turn is the same

    Usage:
    ```
    @turncache
    f(turn: int, data: UnitResponse, world: WorldResponse): ...
    ```
    '''

    def wrapper(*args, **kwargs):
        wrapper.last_turn: int
        wrapper.last_value: Any
        turn = args[0]
        if turn == wrapper.last_turn:
            return wrapper.last_value
        print('Call was made')
        value = f(*args, **kwargs)
        wrapper.last_turn = turn
        wrapper.last_value = value
        return value

    wrapper.last_turn  = -1
    wrapper.last_value = None
    return wrapper
