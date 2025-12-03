from typing import Dict, Any
from fastapi.responses import JSONResponse
from fastapi import FastAPI, HTTPException, status
from .models import Patient, PatientUpdate         # type: ignore
from .utils import load_patient_data, update_data_to_json                  # type: ignore

app: FastAPI = FastAPI() 

@app.put('/update/{patient_id}')
def update_patient(patient_id: str, patient_update_obj: PatientUpdate) -> JSONResponse:

   # load existing data from json file
   patient_data: Dict[str, Dict[str, Any]] = load_patient_data()

   if patient_id not in patient_data:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'Patient {patient_id} not found')
   

   existng_patient_dict: Dict[str, Any] = patient_data[patient_id]

   # convert the pydantic obj and exclude all fields not given by client during object update
   update_patient_dict: Dict[str, Any] = patient_update_obj.model_dump(exclude_unset=True)

   for key, val in update_patient_dict.items():    # taking <k,v> of from the obj what client submitted
      existng_patient_dict[key] = val              # getting into the same 'key' of existing data dict and replacing it's old value with new (client) one

   """
   in order to calculate the computed fields 'bmi' and 'verdict' from the newly supplied client data, recreate the pydantic object for 'Patient' class, the only class which got these fields
   
   also assign 'id' key of existing_patient_dict to the variable 'patient_id' coz Pydantic REQUIRES 'id' to create Patient object
    """
   patient_obj: Patient = Patient(id=patient_id,
                                  **existng_patient_dict)

   # convert above obj to dict and exclude 'id' field to match with 'PatientUpdate' schema (structure), add this dict to patient_data (json data)
   patient_data[patient_id] = patient_obj.model_dump(exclude={
                              'id'
                           })

   # finally update json file
   update_data_to_json(patient_data)

   return JSONResponse(status_code=status.HTTP_200_OK,
                       content={
                          'message' : 'Patient updated successfully'
                       },
                       media_type='application/json')


@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):

   patient_data = load_patient_data()
   
   if patient_id not in patient_data:
     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'Patient {patient_id} not found')
   
   del patient_data[patient_id]

   update_data_to_json(patient_data)

   return JSONResponse(status_code=status.HTTP_204_NO_CONTENT,
                       content={
                            'message' : 'Patient deleted successfully'
                       },
                       media_type='application/json')
    

