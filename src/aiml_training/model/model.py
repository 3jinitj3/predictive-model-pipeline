import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression as SKLearnLinearRegression
from sklearn.ensemble import RandomForestRegressor as SKLearnRandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from abc import ABC, abstractmethod



class Model(ABC):
    def __init__(self):
        self.pipeline = Pipeline | None = None


    @abstractmethod
    def build_pipeline(self, *args, **kwargs):
        pass


    def fit(self, X_train:pd.DataFrame, y_train:pd.Series) -> None:
        if self.pipeline is None:
            raise ValueError("Error: Pipeline has not been built")
        self.pipeline.fit(X_train, y_train)


    def predict(self, X_test:pd.DataFrame) -> np.ndarray:
        if self.pipeline is None:
            raise ValueError("Error: Pipeline has not been built")
        return self.pipeline.predict(X)


    def evaluate(self, y_test:pd.Series, y_prediction:np.ndarray) -> None:
        mae = mean_absolute_error(y_test, y_prediction)
        rmse = mean_squared_error(y_test, y_prediction) ** 0.5
        r2 = r2_score(y_test, y_prediction)
        print(y_test.describe())
        print(f"MAE: {mae:,.2f}")
        print(f"RMSE: {rmse:,.2f}")
        print(f"R2: {r2:.4f}")


class LinearRegression(Model):
    
    def build_pipeline(self, category_cols:list[str], numerical_cols:list[str]) -> None:
        preprocessor = ColumnTransformer(transformers=[
                ('cat', OneHotEncoder(handle_unknown='ignore'), category_cols),
                ('num', StandardScaler(), numerical_cols)])
        self.pipeline = Pipeline([
            ('preprocessor', preprocessor),
            ('model', SKLearnLinearRegression())])


class RandomForestRegressor(Model):

    def build_pipeline(self, category_cols:list[str], numerical_cols:list[str], n_estimators:int, random_state:int, n_jobs:int) -> None:
        preprocessor = ColumnTransformer(transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore'), category_cols),
            ('num', StandardScaler(), numerical_cols)])
        self.pipeline = Pipeline([
            ('preprocessor', preprocessor),
            ('model', SKLearnRandomForestRegressor(n_estimators=n_estimators, random_state=random_state, n_jobs=n_jobs))])

        
