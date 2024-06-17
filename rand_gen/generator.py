import rand_gen.config as conf
import rand_gen.targets as targets
import random


__targets_buffer = []


def update_targets_buffer(elapsed_time: float) -> None:
    for i, target in enumerate(__targets_buffer):
        traveled_distance = target.get_traveled_distance_at(elapsed_time)
        if traveled_distance > conf.COLIDER_LENGTH:
            del __targets_buffer[i]


def try_find_free_position(spawn_time: float, trajectory: str):
    for _ in range(0, conf.NUMBER_OF_SPAWN_ATTEMPS):
        position = get_random_position()

        new_target = targets.create_target(spawn_time, position, trajectory)
        overlaps = False

        for target in __targets_buffer:
            if targets.has_overlaps_on_interval(
                spawn_time,
                spawn_time + conf.TRAJECTORY_PERIOD,
                new_target,
                target,
            ):
                overlaps = True
                break
        
        if not overlaps:
            x, y = position
            return (x, y, new_target)

    return None


def get_spawn_time() -> float:
    offset = random.uniform(-1, 1) * conf.SPAWN_TIME_RANDOM_OFFSET
    return conf.SPAWN_TIME_INTERVAL + offset


def get_random_position() -> tuple:
    x = random.uniform(-1, 1) * conf.BOX_WIDTH / 2
    y = random.uniform(-1, 1) * conf.BOX_HEIGHT / 2

    return (x, y)


def get_random_trajectory() -> str:
    random_value = random.uniform(0, 1)
    threshold = 0

    for name, prob in conf.TRAJECTORY_PROBABILITIES:
        threshold += prob
        if random_value < threshold:
            return name
         

def create_data_row(
    spawn_time: float, 
    x_pos: float, 
    y_pos: float, 
    trajectory: str
) -> list:
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


def generate(time: float) -> list:
    elapsed_time = 0
    spawn_data = []

    min_time = conf.SPAWN_TIME_INTERVAL - conf.SPAWN_TIME_RANDOM_OFFSET 
    should_use_buffer = min_time < 0 or min_time * conf.TARGET_SPEED < conf.COLIDER_LENGTH

    while elapsed_time < time:
        spawn_time = get_spawn_time()
        elapsed_time += spawn_time
        
        trajectory = get_random_trajectory()

        if should_use_buffer:
            update_targets_buffer(elapsed_time)
            position = try_find_free_position(elapsed_time, trajectory)

            if position is not None:
                x, y, target = position
                __targets_buffer.append(target)
                row = create_data_row(elapsed_time, x, y, trajectory)
                spawn_data.append(row)
        else:
            x, y = get_random_position()
            row = create_data_row(elapsed_time, x, y, trajectory)
            spawn_data.append(row)
    
    return spawn_data