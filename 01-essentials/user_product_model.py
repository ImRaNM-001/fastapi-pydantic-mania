from pydantic import BaseModel
from typing import Optional, TypedDict           

class User(BaseModel):
    id: int
    name: str
    is_active: bool


# created a custom type 'InputData' compatible with the types of variables of 'User' class 
class InputData(TypedDict):
    id: int
    name: str
    is_active: bool

# create user dict of type 'InputData' class
user_input_data: InputData = {         
    'id': 4,
    'name': 'Sehar',
    'is_active': True
}

# way1 of creating an class-object by dict unpacking
user_1: User = User(**user_input_data)      

print(f'User name is {user_1.name} and emp id is {user_1.id}')
print('------------\n')


# Task: Create Product model with 
# id, 
# name, 
# price, 
# in_stock properties


class Product(BaseModel):
    id: int
    name: str
    price: float
    in_stock: bool = True               # assigned a default value
    gold_plated_available: Optional[bool] = None    # Optional values must be assigned with a default value always to avoid errors


# create a product (object of 'Product' class) - way2 of creating an class-object
phone: Product = Product(
    id = 2,
    name = 'Tango',
    price = 4234.56,
    in_stock = False,
    # gold_plated_available = True
)

print(phone.in_stock)                   # prints False
print(phone.gold_plated_available)           # prints None




