import pandas as pd
from pandas import DataFrame
from typing import Dict, Any
from sklearn.base import BaseEstimator

def predict_output(data_dict: Dict[str, Any], sk_model: BaseEstimator) -> str:
    
    input_df: DataFrame = pd.DataFrame( [data_dict] )
    return sk_model.predict(input_df)[0]
