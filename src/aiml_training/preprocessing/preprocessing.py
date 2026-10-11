import pandas as pd
from dataclasses import dataclass
from datetime import datetime
from sklearn.model_selection import train_test_split



@dataclass
class PreparedData:
    X_train: pd.DataFrame
    X_test: pd.DataFrame
    y_train: pd.Series
    y_test: pd.Series
    category_cols: list[str]
    numerical_cols: list[str]


@dataclass
class TimeSerisData:
    X_train: pd.DataFrame
    X_test: pd.DataFrame
    y_train: pd.Series
    y_test: pd.Series
    category_cols: list[str]
    numerical_cols: list[str]


def function_exceptions_check(model_df:pd.DataFrame, target_cols:str|list[str]):
    """
    
    """
    if not isinstance(model_df, pd.DataFrame):
        raise TypeError("Error: Data argument type must be 'pd.DataFrame'")
    if target_cols not in model_df.columns:
        raise ValueError(f"Error: {target_cols} is not a column name in the provided 'pd.DataFrame'")

    
def prepare_pipeline_data(model_df:pd.DataFrame, target_cols:str|list[str]) -> PreparedData:
    """
    
    """
    function_exceptions_check(model_df=model_df, target_cols=target_cols)
    x = model_df.drop(columns=target_cols)
    y = model_df[target_cols]
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=.20, random_state=3)
    category_cols = X_train.select_dtypes(include='category').columns.tolist()
    numerical_cols = X_train.select_dtypes(include='number').columns.tolist()
    return PreparedData(
        X_train = X_train,
        X_test = X_test,
        y_train = y_train,
        y_test = y_test,
        category_cols = category_cols,
        numerical_cols = numerical_cols)


def prepare_time_series_data(model_df:pd.DataFrame, target_cols:str|list[str], time_series_col:str|None=None, time_split:int|float|datetime|None=None) -> TimeSerisData:
    """
    
    """
    function_exceptions_check(model_df=model_df, target_cols=target_cols)
    X_train_df = model_df[model_df[time_series_col] < time_split]
    X_test_df = model_df[model_df[time_series_col] >= time_split]
    X_train = X_train_df.drop(columns=target_cols)
    y_train = X_test_df[target_cols]
    X_test = X_test_df.drop(columss=target_cols)
    y_test = X_test_df[target_cols]
    category_cols = X_train.select_dtypes(include='category').columns.tolist()
    numerical_cols = X_train.select_dtypes(include='number').columns.tolist()
    return TimeSerisData(
        X_train = X_train,
        X_test = X_test,
        y_train = y_train,
        y_test = y_test,
        category_cols = category_cols,
        numerical_cols = numerical_cols) 