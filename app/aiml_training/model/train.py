from src.aiml_training import preprocessing
from .models import *
import pandas as pd
from datetime import datetime
from dataclasses import dataclass


@dataclass
class EvaluationData:
    model_df: pd.DataFrame
    model: Model
    prepared_data: type[preprocessing.PreparedData] | type[preprocessing.TimeSerisData]
    target_cols: str|list[str]
    time_series_col:str|None = None
    time_split: int|datetime|None = None
    grouping: str|list[str]|None = None
    

def train_model(model_df:pd.DataFrame, sklearn_model:Model, target_cols:str|list[str], time_series_col:str|None=None, time_split:int|datetime|None=None, grouping:str|list[str]|None = None, collect_dataclass:bool=False) -> type[EvaluationData]|None:
    """
    
    """

    if grouping:
        model_df = model_df.groupby(grouping).mean(numeric_only=True)

    if time_series_col:
        prepared_data = preprocessing.prepare_time_series_data(
            model_df=model_df,
            target_cols=target_cols,
            time_series_col=time_series_col,
            time_split=time_split)
        
    else:
        prepared_data = preprocessing.prepare_pipeline_data(
            model_df=model_df,
            target_cols=target_cols)

    sklearn_model.build_pipeline(prepared_data.category_cols, prepared_data.numerical_cols)
    sklearn_model.fit(X_train=prepared_data.X_train, y_train=prepared_data.y_train)
    y_prediction = sklearn_model.predict(prepared_data.X_test)
    sklearn_model.evaluate(y_test=prepared_data.y_test, y_prediction=y_prediction)

    if collect_dataclass:
        return EvaluationData(
            model_df = model_df,
            model = sklearn_model,
            prepared_data = prepared_data,
            target_cols = target_cols,
            time_series_col = time_series_col,
            time_split = time_split,
            grouping = grouping)
    return None

    

if __name__ == "__main__":
    evaluation_data = train_model()