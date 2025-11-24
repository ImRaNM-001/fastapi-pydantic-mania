from pydantic import BaseModel, computed_field

class Patient(BaseModel):
    weight: float           # in kg
    height: float           # in meters

    @computed_field
    # @property                 # no longer needed in mordern pydantic_v2
    def calculate_bmi(self) -> float:
        return round(self.weight/(self.height**2), 2)           # or, f'{self.weight/(self.height**2):.2f}'


p1_patient: Patient = Patient(weight=78.2,
                              height=2.8)

print('BMI is', p1_patient.calculate_bmi)             # prints 9.97




