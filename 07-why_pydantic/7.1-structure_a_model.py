
from pydantic import BaseModel, EmailStr, AnyUrl
from typing import List, Dict, Optional

class Patient(BaseModel):
    name: str
    age: int
    weight: float
    married: bool
    email: EmailStr
    linkedin_url: AnyUrl
    allergies: List[str]
    contact_details: Dict[str, str]

# class InputData(TypedDict):
#     name: str
#     age: int
#     weight: float
#     married: bool
#     emaill: EmailStr
#     linkedin_url: AnyUrl        # problem: TypedDict cannot use Pydantic types like AnyUrl and EmailStr - it only supports standard Python types, so replace  'str' in the InputData definition.
#     allergies: List[str]
#     contact_details: Dict[str, str]

def insert_patient_data(patient: Patient) -> None:
    print('\n', patient, '\n')
    print(f'{patient.name} data inserted')

def update_patient_data(patient: Patient) -> None:
    print(f'{patient.name} data updated')

patient_data: Dict[str, object] = {
    'name': 'Rick',
    'age': 42,
    'weight': 78.98,
    'married': False,
    'email': 'rulerickki@hotmail.com',
    'linkedin_url': 'https://linkedin.com/ricksb2344',
    'allergies': ['Dust', 'Pollen'],
    'contact_details': {
        'phone': '4564564765'
    }
}

patient_rick: Patient = Patient(**patient_data)             # type: ignore

insert_patient_data(patient_rick)
print('----------\n')
update_patient_data(patient_rick)



   
