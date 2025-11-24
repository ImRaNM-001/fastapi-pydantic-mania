from pydantic import BaseModel, model_validator
from typing import Dict
from typing_extensions import Self      # For Python < 3.11, using Self

class Patient(BaseModel):
    name: str
    age: int
    contact_details: Dict[str, str]

    @model_validator(mode='after')
    def validate_emergency_contact(self) -> Self:
        if self.age > 60 and 'emergency' not in self.contact_details:
            raise ValueError('Patients older than 60 years are required to have an Emergency contact')
        return self

    # primitive-style
    # @model_validator(mode='after')
    # @classmethod
    # def validate_emergency_contact(cls, model: 'Patient') -> 'Patient':
    #     if model.age > 60 and 'emergency' not in model.contact_details:
    #         raise ValueError('Patients older than 60 years are required to have an Emergency contact')
    #     return model


p1_patient: Patient = Patient(name='Ramu',                          # this passes
                              age=68,
                              contact_details={
                                  'relative': 'son',
                                  'emergency': '911' 
                              })


p2_patient: Patient = Patient(name='Divya',                         # this fails
                              age=72,
                              contact_details={
                                  'phone': '78676766897' 
                              })


