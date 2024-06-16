import spawn.config as conf
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


def get_spawn_time() -> float:
    offset = random.uniform(-1, 1) * conf.SPAWN_TIME_RANDOM_OFFSET
    return conf.SPAWN_TIME_INTERVAL + offset


def get_random_trajectory() -> str:
    random_value = random.uniform(0, 1)
    threshold = 0

    for name, prob in conf.TRAJECTORY_PROBABILITIES:
        threshold += prob
        if random_value < threshold:
            return name
         

def create_data_row(spawn_time: float, x_pos: float, y_pos: float) -> list:
    trajectory = get_random_trajectory()
    has_rotation = (random.uniform(0, 1) < conf.ADD_ROTATION_PROBABILITY)

    return [
        spawn_time, 
        x_pos, 
        y_pos, 
        trajectory, 
        conf.TRAJECTORY_SCALE,
        conf.TRAJECTORY_PERIOD,
        has_rotation,
        conf.ROTATION_PERIOD,
        conf.ROTATION_TIME
    ]


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
            row = create_data_row(elapsed_time, x, y)
            spawn_data.append(row)
    
    return spawn_data