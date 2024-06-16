import config as conf
import random


__targets_buffer = []


def update_targets(elapsed_time: float) -> None:
    for i, position in enumerate(__targets_buffer):
        x, y, z = position
        z += elapsed_time * conf.TARGET_SPEED
        if z > 2 * conf.TARGET_RADIUS:
            del __targets_buffer[i] 
        else:
            __targets_buffer[i] = x, y, z
         

def try_find_free_position():
    for _ in range(0, conf.NUMBER_OF_SPAWN_ATTEMPS):
        x = random.uniform(-1, 1) * conf.BOX_HEIGHT / 2
        y = random.uniform(-1, 1) * conf.BOX_WIDTH / 2

        overlaps = False

        for other_x, other_y, other_z in __targets_buffer:
            square_dist = (other_x - x) ** 2 + (other_y - y) ** 2 + other_z ** 2
            if square_dist < (2 * conf.TARGET_RADIUS) ** 2:
                overlaps = True
                break
        
        if not overlaps:
            return x, y

    return None


def get_spawn_time():
    offset = random.uniform(-1, 1) * conf.SPAWN_TIME_RANDOM_OFFSET
    return conf.SPAWN_TIME_INTERVAL + offset


def simulate(simulation_time: float, reset_targets_buffer: bool = False) -> list:
    elapsed_time = 0
    spawn_data = []

    if reset_targets_buffer:
        __targets_buffer.clear()

    while elapsed_time < simulation_time:
        spawn_time = get_spawn_time()
        elapsed_time += spawn_time
        
        update_targets(spawn_time)
        position = try_find_free_position()

        if position is not None:
            x, y = position
            __targets_buffer.append((x, y, 0))
            spawn_data.append([elapsed_time, x, y, False, 0, 0])
    
    return spawn_data
        