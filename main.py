from argparse import ArgumentParser
import pandas as pd
import spawn.spawner as spawner

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-o', '--output_file', type=str, required=True)
    parser.add_argument('-t', '--simulation_time', type=float, required=True)

    return parser.parse_args()


def main():
    args = parse_args()

    spawn_data = spawner.simulate(args.simulation_time)

    pd.DataFrame(spawn_data, columns=[
        'spawn_time',
        'x_pos',
        'y_pos',
        'has_rotation',
        'period_between_rotation',
        'rotation_time',
    ]).to_csv(args.output_file, index=False, sep=';')


if __name__ == '__main__':
    main()