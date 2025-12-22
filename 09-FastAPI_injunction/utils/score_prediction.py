import pandas as pd
from pandas import DataFrame
from typing import Dict, Any
from sklearn.base import BaseEstimator

def predict_output(data_dict: Dict[str, Any], sk_model: BaseEstimator) -> str:
    
    input_df: DataFrame = pd.DataFrame( [data_dict] )
    return sk_model.predict(input_df)[0]


"""
    • `input_df` is a single-row pandas DataFrame built from `data_dict` in 9-5-model_prediction.py file.

    • sk_model.predict(input_df) returns a 1D array-like of predictions, one prediction per row in input_df.

    • Since `input_df` has 1 row, predict(...) returns something like: array([pred_value]).

    • [0] grabs the first (and only) prediction, so [0] is the 0th element of the prediction output, not the 0th column of a DataFrame, which refers to: 
            • the first prediction in the array returned by sk_model.predict(...).

    • input_df is like `X_test` with exactly 1 sample (a single inference request).

"""