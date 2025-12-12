from pathlib import Path
from typing import Annotated, Literal, Optional, List
from box import ConfigBox
from pydantic import BaseModel, computed_field, Field, field_validator
from fastapi import HTTPException, status
from ..utils.load_update_data import read_yaml
from sqlmodel import SQLModel, Field as DBField
from typing_extensions import Self

user_constants: ConfigBox = read_yaml(Path(__file__).parent.parent / 'user_input_literals.yaml')

gender_list: List[str] = user_constants.gender
occupations_list: List[str] = user_constants.occupations
tier_1_cities: List[str] = user_constants.tier_1_cities
tier_2_cities: List[str] = user_constants.tier_2_cities


class CommonModel(BaseModel):
   height: Annotated[float, Field(...,
                                 gt=0,
                                 description='Height of the patient in meters')]
   weight: Annotated[float, Field(...,
                                gt=0,
                                description='Weight of the patient in kgs')]
   
   @computed_field
   def bmi(self) -> float:
    return round(self.weight / (self.height ** 2), 2)
   
   @computed_field               
   def verdict(self) -> str:

    if self.bmi < 18.5:                   # type: ignore
       return 'Underweight'
    
    elif self.bmi <= 25:
        return 'Normal'
    
    elif self.bmi <= 30:
        return 'Overweight'
    
    else:
        return 'Obese'
   

# extends 'CommonModel' class for common fields
class Patient(CommonModel):
   id: Annotated[str, Field(...,
                           description='ID of the patient',
                           examples=['P007'])]
   name: Annotated[str, Field(...,
                              min_length=2,
                              max_length=50,
                              title='Patient name',
                              description='Name of the patient greater than 2 characters but less than 50 characters',
                              examples=['Josh', 'Sarah'])]
   city: Annotated[str, Field(...,
                             description='Residing city of the patient')]
   age: Annotated[int, Field(...,
                            gt=0,
                            lt=120,
                             description='Age of the patient')]
   gender: Annotated[Literal['male', 'female', 'others'], Field(...,
                                                            description='Gender of the patient')]        # type: ignore
   
    

class PatientUpdate(BaseModel):
   name: Annotated[Optional[str], Field(default=None)]
   city: Annotated[Optional[str], Field(default=None)]
   age: Annotated[Optional[int], Field(default=None,
                            gt=0,
                            lt=120)]
   gender: Annotated[Optional[str], Field(default=None)]
   height: Annotated[Optional[float], Field(default=None,
                                 gt=0)]
   weight: Annotated[Optional[float], Field(default=None,
                                gt=0)]
   
   @field_validator('gender')
   @classmethod
   def validate_gender(cls, value: str) -> str:
      if value not in gender_list:
        #  raise ValueError(f'Gender must be one of {gender_list}')             # ValueError generates 422 Unprocessable Entity
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Invalid gender, has to be from the list: {occupations_list}')
      
      return value


class UserInputFeatures(BaseModel):
   age: Annotated[int, Field(default=None,
                            gt=0,
                            lt=120)]
   height: Annotated[float, Field(...,
                                gt=0,
                                lt=2.5,           # any input not within this range of 'Field' fn. would trigger 422 Unprocessable Entity 
                                description='Height of the patient in meters')]
   weight: Annotated[float, Field(...,
                                gt=0,
                                description='Weight of the patient in kgs')]
   income_lpa: Annotated[float, Field(...,
                                      gt=0,
                                      description='Annual salary of the user in LPA')]
   smoker: Annotated[bool, Field(...,
                                    description='Is user a smoker?')]   
   city: Annotated[str, Field(...,
                              description='The residing city of the user/patient')]
   occupation: Annotated[str, Field(...,
                               description='Occupation of the user')]
   
   @field_validator('city')
   @classmethod
   def normalize_city_name(cls, value: str) -> str:
      return value.strip().title()                  # so that "new york" becomes "New York"
   
   @field_validator('occupation')
   @classmethod
   def validate_occupation(cls, value: str) -> str:
      if value not in occupations_list:
        #  raise ValueError(f'Occupations list has to be from {occupations_list}')        # ValueError generates 422 Unprocessable Entity
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Invalid occupation, has to be from the list: {occupations_list}')
      
      return value


   @computed_field
   def bmi(self) -> float:
      return round(self.weight/(self.height**2), 2)   
   
   @computed_field
   def lifestyle_risk(self) -> str:
      
      if self.smoker and self.bmi > 30:
         return 'high'
      
      elif self.smoker and self.bmi > 27:
         return 'medium'
      
      else:
         return 'low'
      
   @computed_field
   def city_tier(self) -> int:
      
      if self.city in tier_1_cities:
         return 1
      
      elif self.city in tier_2_cities:
         return 2
      
      else:
         return 3
      

   @computed_field
   def age_group(self) -> str:
      
      if self.age < 25:
         return 'young'
      
      elif self.age < 45:
         return 'adult'
      
      elif self.age < 60:
         return 'middle_aged'
      
      else:
         return 'senior'
   
    
# for working with SQLModel & DB
class PatientDB(SQLModel, table=True):
   __tablename__='patients'

   # NOTE: 
   # 1- SQLModel sometimes struggles to detect the primary_key=True flag when it's buried inside Annotated combined with Optional in older versions or specific configurations.
   # 2- Pydantic's "Field" does not understand primary_key=True, so SQLAlchemy would never see a primary key defined, used "Field" from SQLModel

   id: Optional[int] = DBField(default=None,
                             primary_key=True)     # type: ignore
   patient_id: str = DBField(index=True,
                           unique=True)            # type: ignore
   name: str
   city: str
   age: int
   gender: str
   height: float
   weight: float

   @classmethod
   def from_patient(cls, patient: Patient) -> Self:      # Self denotes 'PatientDB' return type
      
      # Convert Pydantic Patient to DB model
      # 1. Dump all data from patient
      # 2. Exclude 'id' (because it's 'P007' string, but DB needs 'id' as int)
      # 3. Pass 'patient_id' explicitly
      # 4. Unpack the rest (**data) automatically
      return cls(
         patient_id = patient.id,
        **patient.model_dump(exclude={
                  'id',
                  'bmi',
                  'verdict'
        })
      )