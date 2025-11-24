from pydantic import BaseModel
from typing import Optional, List

class Comment(BaseModel):
    id: int
    content: str
    replies: Optional[ List['Comment'] ] = None       # self replication or forward referencing

# object of Comment class
my_comment: Comment = Comment(id=1,
                              content='YT 1st comment',
                              replies=[Comment(id=11, content='replied comment 11'),
                                       Comment(id=111, content='replied comment 111')                                      
                            ])

# print(my_comment)

nested_replies_comment: Comment = Comment(id=2,
                                          content='Complex comment structure',
                                          replies=[Comment(id=22, 
                                                           content='2nd comment started', 
                                                           replies=[Comment(id=221, content='nested comment inside 2nd comment')]
                                                           )])

print(nested_replies_comment)

Comment.model_rebuild()

