from argparse import ArgumentParser
import pandas as pd
import osu_gen.generator as generator
from osu_gen.osu_data import OsuData

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-i', '--input_file', type=str, required=True)
    parser.add_argument('-o', '--output_file', type=str, required=True)

    return parser.parse_args()


def main():
    args = parse_args()

    osu_data = None
    with open(args.input_file, 'r') as f:
        osu_data = OsuData(f)

    spawn_data = generator.generate(osu_data)

    pd.DataFrame(spawn_data, columns=[
        'spawn_time',
        'x_pos',
        'y_pos',
        'trajectory_type',
        'trajectory_scale',
        'trajectory_period',
        'has_rotation',
        'rotation_period',
        'rotation_time',
    ]).to_csv(args.output_file, index=False, sep=';')


if __name__ == '__main__':
    main()