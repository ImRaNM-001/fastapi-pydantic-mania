import json
import yaml
import joblib as jb
from pathlib import Path
from typing import Dict, Any
from fastapi import HTTPException, status
from box import ConfigBox
from box.exceptions import BoxValueError

json_file_path: Path = Path(__file__).parent.parent / 'patient_data.json'

# generic functions
def load_patient_data():
   try:
      with open(json_file_path, 'r') as json_file:
         return json.load(json_file)
  
   except FileNotFoundError as err:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                           detail=f'Patient data file not found: {err}')


def update_data_to_json(data_dict: Dict[str, Dict[str, Any]]) -> None:
  try:
     with open(json_file_path, 'w') as json_file:
       json.dump(data_dict, 
                 json_file,
                 indent=4)

  except Exception as exp:
     print(f'Error: {exp}')

"""
   **Other possible exceptions status codes:**
   | Exception                         | Status Code                       | Meaning |
   |-----------                        |-------------                      |---------|
   | `FileNotFoundError`               | 404                               | File not found |
   | `PermissionError`                 | 403                               | Forbidden (no access) |
   | `TypeError`                       | 422                               | Unprocessable entity (bad data) |
   | `JSONDecodeError`                 | 400                               | Bad request (invalid JSON) |
   | `OSError`                         | 503                               | Service unavailable (disk issue) |   
   """


model_file_path: Path = Path(__file__).parent.parent / 'insurance_premium_prediction_model.joblib'

def load_model():
   try:
      with open(model_file_path, 'rb') as model_file:
         return jb.load(model_file)

   except FileNotFoundError as err:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                           detail=f'Insurance premium classification model file not found: {err}')
   

def read_yaml(path_to_yaml: Path) -> ConfigBox:
   try:
      with open(path_to_yaml) as yaml_file:
         return ConfigBox(yaml.safe_load(yaml_file))
   
   except BoxValueError:
        raise ValueError('Yaml file is empty')

   except Exception as exception:
        raise exception




