import pandas as pd
from dataclasses import dataclass
from sklearn.model_selection import train_test_split

@dataclass
class PreparedData:
    X_train: pd.DataFrame
    X_test: pd.DataFrame
    y_train: pd.Series
    y_test: pd.Series
    category_cols: list[str]
    numerical_cols: list[str]


def prepare_pipeline_data(data:pd.DataFrame, target_col:str) -> PreparedData:
    if not isinstance(data, pd.DataFrame):
        raise TypeError("Error: Data argument type must be 'pd.DataFrame'")
    if target_col not in data.columns:
        raise ValueError(f"Error: {target_col} is not a column name in the provided 'pd.DataFrame'")
    x = data.drop(columns=target_col)
    y = data[target_col]
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=.20, random_state=3)
    category_cols = X_train.select_dtypes(include='category').columns.tolist()
    numerical_cols = X_train.select_dtypes(include='number').columns.tolist()
    return PreparedData(
        X_train = X_train,
        X_test = X_test,
        y_train = y_train,
        y_test = y_test,
        category_cols = category_cols,
        numerical_cols = numerical_cols
    )