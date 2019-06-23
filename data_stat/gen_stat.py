import json
import numpy


def get_num_to_gen(minimum: int):
    with open("sg_weights.json", "r") as file:
        json_data = json.load(file)
    sg_weights = json_data["sg_weights"]
    num_to_gen = [[number[0], minimum - min(number[1], minimum)] for number in sg_weights]
    return numpy.array(num_to_gen)[:, 1]


print(get_num_to_gen(10).sum())
