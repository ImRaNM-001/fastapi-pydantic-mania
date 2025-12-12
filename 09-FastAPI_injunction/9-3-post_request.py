from typing import Dict, Any
from fastapi.responses import JSONResponse
from fastapi import FastAPI, HTTPException, status
from .models import Patient                  # type: ignore
from .utils import load_patient_data, update_data_to_json                  # type: ignore

app: FastAPI = FastAPI()  

@app.post('/create_patient')
def create_patient(patient_obj: Patient) -> JSONResponse:

  # load existing data from json file
  patient_data: Dict[str, Dict[str, Any]] = load_patient_data()

  # verify if patient already exists
  if patient_obj.id in patient_data:
     raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                         detail=f'Patient already exists for this id')

  # add new patient to the json schema and save in file
  patient_data[patient_obj.id] = patient_obj.model_dump(exclude={
                                                        'id'
                                                      })
  update_data_to_json(patient_data)

  return JSONResponse(status_code=status.HTTP_201_CREATED,
                      content={
                         'message' : 'Patient added successfully'
                      })

