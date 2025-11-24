from pydantic import BaseModel, EmailStr, field_validator
from typing import List

class Patient(BaseModel):
    name: str
    email: EmailStr
    age: int

    @field_validator('name')
    @classmethod
    def transform_name(cls, value) -> str:
        return value.upper()


    @field_validator('email')           # 'something@xyz.com'
    @classmethod
    def validate_email_domain(cls, value) -> EmailStr:
        valid_domains: List[str] = ['xyz.com', 'abc.com']        
        extracted_domain_name: str = value.split('@')[-1]
        
        if extracted_domain_name not in valid_domains:
            raise ValueError(f'{extracted_domain_name} is not a valid domain')
        return value


    @field_validator('age', mode='after')       # mode='before' will get value (age='90') before type coercion
    @classmethod
    def validate_age_limit(cls, value) -> int:
       if not (0 < value < 100):
           raise ValueError(f'Value = {value} is invalid, age should be in between 0 and 100')
       return value
                           

patient_daniel: Patient = Patient(name='DAniel',
                                  email='hKd@abc.com',
                                  age='90')             # mode='after' will convert '90' to 90

print(patient_daniel.model_dump())

# or, wrap inside a try-except block:
# try:
#     print(f'Passed: {patient_daniel.model_dump()}')
# except Exception as ex:
#     print(f'Failed: {ex}')    



