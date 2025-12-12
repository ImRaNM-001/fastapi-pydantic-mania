from .models.patient_models import Patient, PatientUpdate, PatientDB
from typing import Any, Generator, List
from fastapi import Depends, FastAPI, HTTPException, status
from sqlmodel import Session, SQLModel, create_engine, select

app: FastAPI = FastAPI()

# Create the SQLite database engine
engine = create_engine('sqlite:///patient_database.db',
                                echo=True)

SQLModel.metadata.create_all(engine)

# Dependency: Get the session
def get_session() -> Generator[Session, Any, None]:    

    with Session(engine) as session:
        yield session


# Get all patients
@app.get('/patients',
        response_model=List[PatientDB],
        status_code=status.HTTP_200_OK)
def read_patient(skip: int=0,
                limit: int=5,
                session: Session = Depends(get_session)):
    
    return session.exec(
        select(PatientDB)
        .offset(skip)              # OFFSET clause allows to skip a specified number of rows before starting to return the results
        .limit(limit)              # LIMIT clause is used to specify the number of records to return
        ).all()


# Get a patient by ID
@app.get('/patients/{patient_id}',
        response_model=PatientDB,
        status_code=status.HTTP_200_OK)
def get_patient_by_id(patient_id: str,
                    session: Session = Depends(get_session)) -> PatientDB:
    
    patient_info: PatientDB | None = session.exec(
        select(PatientDB)
        .where(PatientDB.patient_id == patient_id)
    ).first()                                       # .first() returns the 1st matching record or None if the table is empty/no match found.

    if not patient_info:            # patient not found
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Patient {patient_id} not found'
        )
    
    return patient_info


# Create new patient - uses existing Patient model for validation
@app.post('/create_patient',
         response_model=PatientDB,
         status_code=status.HTTP_201_CREATED)
def create_patient(patient: Patient,
                   session: Session = Depends(get_session)) -> PatientDB:
    
    existing_patient = session.exec(
        select(PatientDB)
        .where(PatientDB.patient_id == patient.id)
    ).first()

    if existing_patient:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'Patient with ID {patient.id} already exists'
        )
    
    # call classmethod of PatientDB model
    add_patient: PatientDB = PatientDB.from_patient(patient)
    session.add(add_patient)
    session.commit()
    session.refresh(add_patient)    # .commit() expires the object (clears its data) and .refresh() reloads the data from DB immediately so the updated object can be returned with all fields populated.

    return add_patient

    """
    Sample payload to insert:
        {
            "id": "P007",
            "name": "James Bond",
            "city": "London",
            "age": 40,
            "gender": "male",
            "height": 1.83,
            "weight": 85
        }
    """


# Update new patient - uses existing PatientUpdate model for validation
@app.patch('/update_patient/{patient_id}',
        response_model=PatientDB,
        status_code=status.HTTP_200_OK)
def update_patient(patient_id: str,
                patient_update_obj: PatientUpdate,
                session: Session = Depends(get_session)) -> PatientDB:

    update_patient = session.exec(
        select(PatientDB)
        .where(PatientDB.patient_id == patient_id)
    ).first()

    if not update_patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Patient: {patient_id} not found'
        )

    # Update the PatientDB's attributes
    for field, value in patient_update_obj\
                        .model_dump(exclude_unset=True)\
                        .items():
        if value is not None:
            setattr(update_patient, field, value)         # equivalent to     "existng_patient_dict[key] = val"

    session.add(update_patient)
    session.commit()
    session.refresh(update_patient)
    return update_patient


# Delete a patient by ID
@app.delete('/delete_patient/{patient_id}',
            status_code=status.HTTP_204_NO_CONTENT)
            # description=f'Patient deleted successfully')
def delete_patient(patient_id: str,
                   session: Session = Depends(get_session)) -> None:

    existing_patient: PatientDB = session.exec(
        select(PatientDB)
        .where(PatientDB.patient_id == patient_id)
    ).first()

    if not existing_patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Patient: {patient_id} not found'
        )
    
    session.delete(existing_patient)
    session.commit()

