import yaml
import argparse
import sys

def update_yaml(file_path, key, new_value):
  try:  
    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)

    # Update the value
    data["image"][key] = new_value

    with open(file_path, 'w') as f:
        yaml.dump(data, f, default_flow_style=False)
  except FileNotFoundError:
        print(f"File {file_path} not found.")
        sys.exit(1)

parser = argparse.ArgumentParser('My program')
parser.add_argument('-i', '--imagetag')


args = vars(parser.parse_args())
new_tag = args['imagetag']
print(new_tag)

file_path = 'values.yaml'
key_to_update = 'tag'


update_yaml(file_path, key_to_update, new_tag)
