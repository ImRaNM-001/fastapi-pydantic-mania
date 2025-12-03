import pandas as pd
from pandas import DataFrame
from typing import AsyncGenerator, Dict, Any
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from fastapi import FastAPI, status
from .models import UserInputFeatures   # type: ignore
from .utils import load_model            # type: ignore

# Skip loading model on every request each time (slow and inefficient), instead load once at startup
insurance_model = None

@asynccontextmanager
async def model_lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    
    global insurance_model
    insurance_model = load_model()
    print('Model loaded into memory!')

    yield                           # used to create generator functions to produce a sequence of values over time, pausing and resuming execution. 
    print('Model shutting down...')

app: FastAPI = FastAPI(lifespan=model_lifespan)


@app.post('/predict')
def predict_insurance_premium(user_input: UserInputFeatures) -> JSONResponse:

    input_df: DataFrame = pd.DataFrame([            # each List is a row
        {
            'income_lpa': user_input.income_lpa,
            'occupation': user_input.occupation,
            'bmi': user_input.bmi,
            'lifestyle_risk': user_input.lifestyle_risk,
            'city_tier': user_input.city_tier,
            'age_group': user_input.age_group,
        }
    ])

    prediction = load_model().predict(input_df)[0]

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={
                            'predicted_insurance_premium': prediction
                        },
                        media_type='application/json')


