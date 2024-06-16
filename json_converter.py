from argparse import ArgumentParser
import spawn.config as conf
import json
import pandas as pd

def converte_target(row: pd.Series) -> dict:
    json = {}

    json['spawnTimeInSeconds'] = row['spawn_time']
    json['spawnPosition'] = {
        'x' : 0,
        'y' : row['y_pos'],
        'z' : row['x_pos'],
    }

    trajectory = row['trajectory_type']
    if trajectory != 'linear':
        json['trajectoryType'] = trajectory
    
    if row['has_rotation']:
        json['rotation'] = {
            'peridoInSeconds' : row['rotation_period'],
            'rotationTimeInSeconds' : row['rotation_time']
        }
    
    return json


def converte(data: pd.DataFrame) -> dict:
    json = {}
    targets = []

    for _, row in data.iterrows():
        targets.append(converte_target(row))
    
    json['targetsSpeed'] = conf.TARGET_SPEED
    json['targetsData'] = targets
    return json


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-o', '--output_file', type=str, required=True)
    parser.add_argument('-i', '--input_file', type=str, required=True)

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    df = pd.read_csv(args.input_file, sep=';')
    result = converte(df)

    with open(args.output_file, 'w') as f:
        json.dump(result, f)
     

if __name__ == '__main__':
    main()