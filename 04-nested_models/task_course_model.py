# Task: Create 'Course' model with atributes:
# 'Modules' - each 'Course' has many 'Modules'
# and 'Lessons' - each 'Modules' has many 'Lessons'

from pydantic import BaseModel
from typing import List

class Lesson(BaseModel):
    lesson_id: int
    topic: str


class Module(BaseModel):
    module_id: int
    name: str
    lessons: List[Lesson]


class Course(BaseModel):
    course_id: int
    course_title: str
    modules: List[Module]


# create objects of above models
data_govr_lesson: Lesson = Lesson(lesson_id=23, topic='Data Governance lessons')
data_lineage_lesson: Lesson = Lesson(lesson_id=44, topic='Data Lineage issues')
model_building_lesson: Lesson = Lesson(lesson_id=67, topic='How to train a model?')


data_module: Module = Module(module_id=2, 
                             name='Module related to Data and it\'s pillars',
                            lessons=[data_govr_lesson, data_lineage_lesson])

model_lifecycle_module: Module = Module(module_id=3,
                                 name='Module depicting complete model lifecycle',
                                 lessons=[model_building_lesson])


mlOps_course: Course = Course(course_id=1,
                              course_title='MLOps zero to Hero',
                              modules=[data_module, model_lifecycle_module])

print(mlOps_course)