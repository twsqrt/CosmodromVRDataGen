from argparse import ArgumentParser
import pandas as pd
import rand_gen.generator as generator

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-o', '--output_file', type=str, required=True)
    parser.add_argument('-t', '--simulation_time', type=float, required=True)

    return parser.parse_args()


def main():
    args = parse_args()

    spawn_data = generator.generate(args.simulation_time)

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