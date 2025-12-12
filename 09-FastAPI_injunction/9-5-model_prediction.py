from typing import AsyncGenerator, Dict, Any
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from fastapi import FastAPI, status
from .models import UserInputFeatures   # type: ignore
from .utils import load_model, predict_output            # type: ignore
from sklearn.base import BaseEstimator

# Skip loading model on every request each time (slow and inefficient), instead load once at startup
insurance_model: BaseEstimator | None = None

@asynccontextmanager
async def model_lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    
    global insurance_model
    insurance_model = load_model()
    print('Model loaded into memory!')

    yield                           # used to create generator functions to produce a sequence of values over time, pausing and resuming execution. 
    print('Model shutting down...')

app: FastAPI = FastAPI(lifespan=model_lifespan)


@app.get('/health')                         # essential as a pre-requisite for cloud machine deployment
def health_check() -> Dict[str, str | bool]:
    return {
        'status': 'Ok',
        'version': 'extract from MLFlow - v_1.0',
        'model_load_status': insurance_model is not None
    }


@app.post('/predict')
def predict_insurance_premium(user_input: UserInputFeatures) -> JSONResponse:
    
    try:
        data_dict: Dict[str, Any] = {
                'income_lpa': user_input.income_lpa,
                'occupation': user_input.occupation,
                'bmi': user_input.bmi,
                'lifestyle_risk': user_input.lifestyle_risk,
                'city_tier': user_input.city_tier,
                'age_group': user_input.age_group,
            }

        prediction_output = predict_output(data_dict, insurance_model)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                'predicted_insurance_premium': prediction_output
            })    

    except Exception as ex:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                'Error': f'Temporary failure: Request cannot be processed right now, some exception occured: {str(ex)}'
            })


""" 
TODO: Data Science stuffs -->

1- add additional fields for output 'Response' body such as: 
    - predicted_class,
    - confidence, 
    - class_probabilities (dervied from probabilities)

ex:
            {
            "response": {
                "predicted_category": "Low",
                "confidence": 0.39,
                "class probabilities": {
                "High": 0.36,
                "Low": 0.39,
                "Medium": 0.25
                    }
                }
            }

2- add separate pydantic model for 'Response' fields output such as:
    - predicted_category: str, Field(...,)
    - confidence: float, Field(...,)
    - class_probabilities: Dict[str, float], Field(...,)

"""