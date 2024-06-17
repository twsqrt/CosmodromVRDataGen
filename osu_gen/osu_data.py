import typing
import pandas as pd

class OsuData:
    def parse_general_data(self, index: int, lines: list):
        _, file_name = lines[index + 1].split(':')
        _, audio_lead_in = lines[index + 2].split(':')
        self.audio_file_name = file_name.strip()
        self.audio_lead_in = int(audio_lead_in) / 1000
    

    def parse_hit_object(self, parameters: list) -> list:
        x, y, time, _, _, _ = parameters
        return [int(time) / 1000, int(x) / 512, int(y) / 384]


    def parse_hit_objects_data(self, index: int, lines: list):
        line = ''
        hit_objects = []
        i = 1

        while line != '\n' and i < len(lines) - index: 
            line = lines[index + i]

            parameters = line.split(',')
            object_type = parameters[3]

            if object_type == '1':
                hit_object = self.parse_hit_object(parameters)
                hit_objects.append(hit_object)

            i += 1
        
        self.hit_objects = pd.DataFrame(hit_objects, columns=[
            'time',
            'x_pos',
            'y_pos'
        ])


    def __init__(self, file: typing.IO):
        lines = file.readlines()

        general_index = lines.index('[General]\n')
        self.parse_general_data(general_index, lines)

        hit_obj_index = lines.index('[HitObjects]\n')
        self.parse_hit_objects_data(hit_obj_index, lines)
        