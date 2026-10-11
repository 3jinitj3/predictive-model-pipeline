import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression as SKLearnLinearRegression
from sklearn.ensemble import RandomForestRegressor as SKLearnRandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from abc import ABC, abstractmethod



class Model(ABC):
    def __init__(self):
        self.model: BaseEstimator | None = None
        self.pipeline: Pipeline | None = None


    @abstractmethod
    def build_pipeline(self, *args, **kwargs):
        pass


    @abstractmethod
    def build_model(self, *args, **kwargs):
        pass


    def fit(self, X_train:pd.DataFrame, y_train:pd.Series) -> None:
        if self.pipeline is None:
            raise ValueError("Error: Pipeline has not been built")
        self.pipeline.fit(X_train, y_train)


    def predict(self, X_test:pd.DataFrame) -> np.ndarray:
        if self.pipeline is None:
            raise ValueError("Error: Pipeline has not been built")
        return self.pipeline.predict(X_test)


    def evaluate(self, y_test:pd.Series, y_prediction:np.ndarray) -> None:
        mae = mean_absolute_error(y_test, y_prediction)
        rmse = mean_squared_error(y_test, y_prediction) ** 0.5
        r2 = r2_score(y_test, y_prediction)
        print(y_test.describe())
        print(f"MAE: {mae:,.6f}")
        print(f"RMSE: {rmse:,.6f}")
        print(f"R2: {r2:.4f}")


class LinearRegression(Model):

    def __init__(self,  fit_intercept:bool=True, copy_X:bool=True, tol:float=1e-06, n_jobs:int|None=None, positive:bool=False) -> None:
        super().__init__()
        self.fit_intercept = fit_intercept
        self.copy_X = copy_X
        self.tol = tol
        self.n_jobs = n_jobs
        self.positive = positive


    def build_model(self):
        self.model = SKLearnLinearRegression(
            fit_intercept = self.fit_intercept,
            copy_X = self.copy_X,
            tol = self.tol,
            n_jobs = self.n_jobs,
            positive = self.positive)

    
    def build_pipeline(self, category_cols:list[str], numerical_cols:list[str]) -> None:
        preprocessor = ColumnTransformer(transformers=[
                ('cat', OneHotEncoder(handle_unknown='ignore'), category_cols),
                ('num', StandardScaler(), numerical_cols)])
        self.pipeline = Pipeline([
            ('preprocessor', preprocessor),
            ('model', self.model)])


class RandomForestRegressor(Model):

    def __init__(self, n_estimators:int=100, max_depth:int|None=None, random_state:int|None=None, n_jobs:int|None=None) -> None:
        super().__init__()
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.random_state = random_state
        self.n_jobs = n_jobs


    def build_model(self):
        self.model = SKLearnRandomForestRegressor(
            n_estimators = self.n_estimators,
            max_depth = self.max_depth,
            random_state =self.random_state,
            n_jons = self.n_jobs)
        

    def build_pipeline(self, category_cols:list[str], numerical_cols:list[str]) -> None:
        preprocessor = ColumnTransformer(transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore'), category_cols),
            ('num', StandardScaler(), numerical_cols)])
        self.pipeline = Pipeline([
            ('preprocessor', preprocessor),
            ('model', self.model)])

        