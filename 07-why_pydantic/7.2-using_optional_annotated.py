
from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):
    name: str = Field(...,
                      max_length=50,
                      description='name of the patient less than 50 chars',
                      examples=['John', 'Jhonny'])
    age: int = Field(...,
                     gt=0,
                     lt=110)
    weight: Annotated[float, Field(...,
                                   gt=0)]
    
    # weight: Annotated[float, Field(...,
    #                                gt=0,
    #                                strict=True)]            # enforced 'type coercion'   i.e string '75.2' do not convert to 75.2 automatically
    

    married: Optional[bool] = False
    email: Annotated[EmailStr, Field(...,
                                     title='email address....')]
    linkedin_url: AnyUrl
    # allergies: Optional[List[str]] = Field(default=None,
    #                                        max_length=5)                # without using 'Annotated'

    allergies: Annotated[Optional[List[str]], Field(default=None,
                                           max_length=5)]                  # used 'Annotated'
    # allergies: Annotated[
    #         Optional[List[
    #             Annotated[str, Field(max_length=5)]
    #             ]],
    #             Field(default=None,
    #                   max_length=5)
    #             ]                               # validate both "List items" length and "each str" item length is 5
    contact_details: Dict[str, str]


def insert_patient_data(patient: Patient) -> None:
    print('\n', patient, '\n')
    print(f'{patient.name} data inserted')


patient_sammy: Patient = Patient(
    name='sally',
    age=35,
    weight=70.245,                      # '70.245' will also be allowed & converted automatically by pydantic - "type coercion" allowed
    email='sayk@outlook.com',
    linkedin_url=AnyUrl('https://linkedin.com/slysV67'),        
    allergies=['dusty', 'pollen', 'noise'],
    contact_details={
        'cell_no': '889787789898'
    }
)

insert_patient_data(patient_sammy)





   

