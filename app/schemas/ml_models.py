from enum import Enum
from pydantic import BaseModel



class MLModels(str, Enum):
    linreg = 'LinearRegression'
    bridge = 'Ridge'
    lasso = 'Lasso'
    logreg = 'LogisticRegression'


class Model(BaseModel): # Deciding to use a model for each ML model and its args.
    pass