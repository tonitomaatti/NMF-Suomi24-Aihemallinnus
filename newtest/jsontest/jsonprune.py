import json
import os

path = "./aineisto/"
for filename in os.listdir(path):
    with open(path + filename, 'r', encoding='UTF-8') as json_file:
        data = json.load(json_file)