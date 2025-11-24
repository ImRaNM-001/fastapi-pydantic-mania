from pydantic import BaseModel
from typing import Dict, TypedDict

class Address(BaseModel):
    """
        the idea is to extract fields of 'Address' model (ex: city/state/pin) easily from object of 'Patient' model directly
        ex: pq_patient.addr.city
            pq_patient.addr.state
    """
    city: str
    state: str
    zipcode: str

class Patient(BaseModel):
    name: str
    gender: str
    age: int
    addr: Address

pq_patient_data: Dict[str, object] = {
    'name': 'maven',
    'gender': 'male',
    'age': 42,
    'addr': Address(**{
        'city': '32 auburn st.',
        'state': 'wcn',
        'zipcode': 'x07Z5'
    })
}

pq_patient: Patient = Patient(**pq_patient_data)            # type: ignore

# export the patient object as a Dict
print(pq_patient.model_dump(), '\n')

included_fields: Dict[str, object] = pq_patient.model_dump(include={
                                                            'name',                 # set of values
                                                            'age'
                                                        })

print(included_fields, '\n', type(included_fields))             # prints  <class 'dict'>



excluded_fields= pq_patient.model_dump(exclude={
                                                        'age': True,                # dict of values
                                                        'addr': {'state'}
                                                        # 'addr': {'state', 'zipcode'}   # Exclude multiple nested fields:
                                                })

print('\n', excluded_fields)



class Bakery(BaseModel):
    name: str
    location: str
    items_available: int = 11

class InputData(TypedDict):
    name: str
    location: str

baking_data: InputData = {
    'name': 'Shelon\'s bake hot',
    'location': '54 auburn st.'
}

b1_bakery: Bakery = Bakery(**baking_data)

# export the object excluding the property not assigned a value during object creation
print(b1_bakery.model_dump(exclude_unset=True))
