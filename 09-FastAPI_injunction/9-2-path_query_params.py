import json
from pathlib import Path
from fastapi import FastAPI, Response, status, Path as PathParam, HTTPException, Query
from typing import Annotated, Dict, List, Any, Optional

app: FastAPI = FastAPI()

json_file_path: Path = Path(__file__).parent / 'patient_data.json'

# load data
def load_patient_data():        # Dict[str, str] | Response
    try:
        with open(json_file_path, 'r') as json_file:
            return json.load(json_file)

    except FileNotFoundError as err:
        return Response(status_code=status.HTTP_404_NOT_FOUND,
                        content={
                            'error': f'Patient data file not found: {err}'
                        },
                        media_type='application/json')
    
        # better to use 'HTTPException' than 'Response' - should be inside 'except' block
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        #                     detail=f'Patient data file not found: {err}')


patient_data: Dict[str, Dict[str, Any]] | Response = load_patient_data()      # replaced 'object' type to 'Dict[str, Any]'


# route with path-parameter:
@app.get('/patients/{patient_id}',
         response_model=None)
def get_patient_by_id(patient_id: Annotated[str, PathParam(...,
                                                           description='The patient ID',
                                                           example='P001')
                                                        ]):

    if isinstance(patient_data, Response):
        return patient_data                     # returns the error response directly
    
    # better ready prod code
    if patient_id in patient_data:
         return patient_data[patient_id]  
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Patient {patient_id} not found')
     

    """
    if patient_id in patient_data:
        return patient_data[patient_id]
    
    return {
        'error': f'{patient_id} not found'              # avoid normaal JSON
    }
    """

    

# route with query-parameter to sort patients:
@app.get('/sort')
def sort_patients(sort_by: Annotated[str, Query(...,
                                                description='Sort patients on the basis of height, weight & bmi')],
                order_by: Optional[str] = Query(default=None,
                                                description='Sort either in asc or desc. order')
                                                ):
    
    valid_sorted_fields: List[str] = ['height', 'weight', 'bmi']
    valid_order_fields: List[str] = ['asc', 'desc']

    if sort_by not in valid_sorted_fields:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Invalid sort field, select from {valid_sorted_fields}')

    if order_by not in valid_order_fields:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Invalid order field, select from {valid_order_fields}')
    
    if isinstance(patient_data, Response):
        return patient_data
    
    sorted_data: List[Dict[str, Any]] = sorted(patient_data.values(),         # extract all "<Values>" from json file
                         key=lambda x: x.get(sort_by, 0),
                         reverse=True if order_by=='desc' else False)      # means desc order
    
    """
        *  x.get(sort_by, 0): this calls the dictionary's get() method on each item (weight, height, bmi). It attempts to retrieve the value associated with the key stored in the variable `sort_by`. If that key doesn't exist in the dictionary, it returns 0 as a default value instead of raising a KeyError.
        
        * Why use .get() with a default? Default value of 0 is safety mechanism. If any dictionary in the list is missing the sort_by key, the code won't crash—it will treat that item as having a value of 0 for sorting purposes.
    """

    return sorted_data