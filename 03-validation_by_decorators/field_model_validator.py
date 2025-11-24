from pydantic import BaseModel, Field, field_validator, model_validator, computed_field

class User(BaseModel):
    username: str

    # perform validations on 'username' field/property
    @field_validator('username')
    @classmethod
    def username_length(cls, value):         # cls is the User class
        if len(value) < 4:
            raise ValueError('username must be at least 4 chars')
        return value


# --- Testing the validator ---
try:
    user_1 = User(username='Step')
    print(f'passed: {user_1}')

except Exception as ex:
    print(f'failed: {ex}')




class SignupData(BaseModel):
    passwd: str
    confirm_passwd: str

    @model_validator(mode='after')
    def passwd_match(cls, values) -> 'SignupData':
        if values.passwd != values.confirm_passwd:
            raise ValueError('Password do not match')
        return values


class Product(BaseModel):
    price: float
    quantity: int        
    
    @computed_field
    @property                               # Just use @computed_field alone—it already makes it a property:
    def total_price(self) -> float:
        return self.price * self.quantity

mob_phone: Product = Product(price=4.2, 
                             quantity=2)
print(mob_phone.total_price)                # prints 8.4 - Accessed as a property, not a method


# Task: Create Booking model with properties,
# user_id, room_id - int
# nights - must be >= 1
# rate_per_night - float,
#
# also add computed_field: total_amount = nights * rate_per_night

class Booking(BaseModel):
    user_id: int
    room_id: int
    nights: int = Field(..., ge=1)
    rate_per_night: float

    @computed_field
    @property
    def total_amount(self) -> float:
        return self.nights * self.rate_per_night
  



