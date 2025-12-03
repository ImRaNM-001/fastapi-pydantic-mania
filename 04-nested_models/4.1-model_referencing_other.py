from pydantic import BaseModel

class Address(BaseModel):
    street: str
    city: str
    postal_code: str

class User(BaseModel):
    id: int
    name: str
    addr: Address


# create object of 'Address' model
addr_blr: Address = Address(street='ritchie street',
                            city='blr',
                            postal_code='uxiu-97')


# create object of 'User' model
user_vicks: User = User(id=456,
                        name='Vick Dawg',
                        addr=addr_blr)

print(f'User created {user_vicks}')