from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class Cart(BaseModel):
    user_id: int
    items: List[str]
    quantities: Dict[str, int]


class BlogPost(BaseModel):
    title: str
    content: str
    image_url: Optional[str] = None


# Task: Create Employee model with properties,
# id, 
# name - min 3 chars
# department - Optional - default value as 'General', 
# salary - must be >=10000

class Employee(BaseModel):
    id: int
    name: str = Field(..., 
                      min_length=3, 
                      max_length=40, 
                      description='An Employee name', 
                      examples=['John', 'Doe'])
    dept: Optional[str] = 'General'
    sal: float = Field(..., ge=10000)



