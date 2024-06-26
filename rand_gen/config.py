# Box size
BOX_HEIGHT = 200 
BOX_WIDTH = 400

NUMBER_OF_SPAWN_ATTEMPS = 10

# Targets
TARGET_SPEED = 300
COLLIDER_RADIUS = 30
COLIDER_LENGTH = 200

# Spawn time
SPAWN_TIME_INTERVAL = 0.5 
SPAWN_TIME_RANDOM_OFFSET = 0.2 

# Trajectory
TRAJECTORY_PROBABILITIES = [
    ('Linear', 0.5),
    ('HorizontalZigZag', 0.2),
    ('VerticalZigZag', 0.2),
    ('Spiral', 0.1),
]
TRAJECTORY_SCALE = 30
TRAJECTORY_PERIOD = 1

# Rotation
ADD_ROTATION_PROBABILITY = 0.3
ROTATION_TIME = 1.5
ROTATION_PERIOD = 0.2 