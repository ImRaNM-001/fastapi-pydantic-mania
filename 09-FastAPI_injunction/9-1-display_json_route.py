import json
from fastapi import FastAPI, Response, status
from typing import Dict
from pathlib import Path

app: FastAPI = FastAPI()

json_file_path: Path = Path(__file__).parent / 'patient_data.json'

"""
Ensure the json file exists, but
Problem with this approach: if no try-except, the 'FileNotFoundError' crashes the server (500 error) instead of returning any custom status code 404.

    if not os.path.exists(json_file_path):
        raise FileNotFoundError(f'Patient data file not found')
"""


# create a GET route to display a json file
@app.get('/patients',
         response_model=None)           # use response_model=None coz 'Response' is not a valid Pydantic type.
def view_patients() -> Dict[str, object] | Response:
    try:
        with open(json_file_path, 'r') as json_file:
            # data = json.load(json_file)
            # print(type(data))
            return json.load(json_file)
    
    except FileNotFoundError as err:
         return Response(
             status_code=status.HTTP_404_NOT_FOUND,
             content=json.dumps({                           # json.dumps returns an ugly json
             'error': f'Patient data file not found: {err}'
            }),
            media_type='application/json')
    
    except json.JSONDecodeError as err:
        return Response(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=json.dumps({
                'error': f'Invalid JSON: {err}'
            }),
            media_type='application/json')

