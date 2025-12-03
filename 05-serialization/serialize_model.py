from pydantic import BaseModel, EmailStr, field_serializer, Field
from datetime import datetime
from typing import List, Dict, Optional

class Address(BaseModel):
    street: str
    city: str
    zipcode: str

class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_active: bool = True
    # is_active: Optional[bool] = Field(default=True)
    created_at: datetime
    addr: Address
    tags: List[str] = []

    # further formatting the ISO format of "datetime":
    # @field_serializer('created_at', mode='plain')
    @field_serializer('created_at')
    def serialize_datetime(self, dt: datetime) -> str:
        return dt.strftime('%d-%m-%Y %H:%M:%S')

    # OLD CODE - "json_encoders" is deprecated in Pydantic v2. Used serializers instead
    # model_config: ConfigDict = ConfigDict(
    #     json_encoders={
    #         datetime: lambda val: val.strftime('%d-%m-%Y %H:%M:%S')
    #     }
    # )


# create a user
user_raju: User = User(
    id = 23,
    name = 'Raju',
    email = 'rk@kaju.com',
    created_at = datetime(2025, 3, 15, 14, 30),
    addr = Address(
        street= '23 milton st.',
        city = 'gift-city',
        zipcode = 'th676x'
    ),
    tags = ['premium', 'platinum']
)

user_raju_dict: Dict[str, object] = user_raju.model_dump()
print(type(user_raju_dict))                 # prints <class 'dict'>
print(user_raju_dict)

print('-------------\n')

user_raju_json = user_raju.model_dump_json()
print(type(user_raju_json))                  # prints <class 'str'>
print(user_raju_json)                       # prints "created_at":"2025-03-15T14:30:00" in json which is not readable format



