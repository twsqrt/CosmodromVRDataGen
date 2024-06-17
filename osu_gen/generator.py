import osu_gen.config as conf
from osu_gen.osu_data import OsuData


def get_distance_from_box_to_hit_zone(y_pos: int) -> float:
    parabola = (2 * (y_pos - conf.PLAYER_POSITION_Y) / conf.BOX_WIDTH) ** 2
    return conf.PLAYER_POSITINO_X - conf.HIT_DISTANCE + parabola


def generate(osu_data: OsuData) -> list:
    spawn_data = []

    for _, row in osu_data.hit_objects.iterrows():
        osu_timing = row['time']
        x = (row['x_pos'] - 0.5) * conf.BOX_WIDTH
        y = (row['y_pos'] - 0.5) * conf.BOX_HEIGHT

        distance = get_distance_from_box_to_hit_zone(x)
        time_offset = distance / conf.TARGET_SPEED

        if time_offset < osu_timing:
            spawn_time = osu_timing - time_offset
            row = [spawn_time, x, y, 'Linear', 1, 1, False, -1, -1]
            spawn_data.append(row)
            
    return spawn_data