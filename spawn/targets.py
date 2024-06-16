import spawn.config as conf
import math


class Target:
    def __init__(self, spawn_time: float, start_pos_on_box: tuple, trajectory_function: callable) -> None:
        self.spawn_time = spawn_time
        self.trajectory_function = trajectory_function
        self.start_pos_on_box = start_pos_on_box

    
    def get_position_at(self, time: float) -> tuple:
        lifetime = time - self.spawn_time 

        if lifetime < 0:
            return None
        
        traj_x, traj_y = self.trajectory_function(lifetime)
        start_x, start_y = self.start_pos_on_box

        return (
            traj_x * conf.TRAJECTORY_SCALE + start_x,
            traj_y * conf.TRAJECTORY_SCALE + start_y, 
            lifetime * conf.TARGET_SPEED
        )
    

    def get_traveled_distance_at(self, time: float) -> float:
        lifetime = time - self.spawn_time
        return lifetime * conf.TARGET_SPEED if lifetime > 0 else 0


def __zig_zig(t: float) -> float:
    fraction = t % 1
    return 4 * abs(fraction - 0.5) - 1


def __spiral(t: float) -> float:
    angle = t * 2 * math.pi
    return (math.cos(angle), math.sin(angle))


def create_target(spawn_time: float, start_pos_on_box: tuple, trajectory: str) -> Target:
    trajectory_function = None

    match trajectory:
        case 'Linear':
            trajectory_function = lambda _: (0, 0)
        case 'HorizontalZigZag':
            trajectory_function = lambda t: (__zig_zig(t), 0)
        case 'VerticalZigZag':
            trajectory_function = lambda t: (0, __zig_zig(t))
        case 'Spiral':
            trajectory_function = __spiral
          
    return Target(spawn_time, start_pos_on_box, trajectory_function)


def is_overlaps(time: float, first: Target, second: Target) -> bool:
    x1, y1, z1 = first.get_position_at(time)
    x2, y2, z2 = second.get_position_at(time)

    square_distance = (x1 - x2) ** 2 + (y1 - y2) ** 2
    if square_distance > (2 * conf.COLLIDER_RADIUS) ** 2:
        return False

    return (abs(z1 - z2) < conf.COLIDER_LENGTH)


def has_overlaps_on_interval(start_time: float, 
    end_time: float, 
    first: Target, 
    second: Target,
    delta_time: float = 1 /30,
) -> bool:
    elapsed_time = start_time

    while elapsed_time < end_time:
        if is_overlaps(elapsed_time, first, second):
            return True
        elapsed_time += delta_time
    
    return False