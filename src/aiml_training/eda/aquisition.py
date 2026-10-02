import pandas as pd
import requests
from pathlib import Path
from typing import Literal
from sqlalchemy.engine import Connection


# Extract data from csv or url and load into a df
def load_data(fetch_type:Literal["csv", "request"], path_url:str, **kwargs) -> pd.DataFrame:
    """
    
    """
    match fetch_type:
        case "csv":
            try:
                return pd.read_csv(path_url, **kwargs)
            except FileNotFoundError as error:
                raise FileNotFoundError(
                    f"CSV file not found, check your absolute path to csv: {path_url}"
                ) from error
        case "request":
            try:
                kwargs.setdefault("timeout", 10)
                response = requests.get(path_url, **kwargs)
                response.raise_for_status()
                return pd.DataFrame(response.json())
            except requests.Timeout as error:
                raise TimeoutError(
                    f"Timed out while requesting {path_url}\nMake sure url is valid"
                ) from error
            except requests.ConnectionError as error:
                raise ConnectionError(
                    f"Unable to connect to {path_url}\nMake sure url is valid"
                ) from error
            except requests.RequestException as error:
                raise RuntimeError(
                    f"Request failed for url: {path_url}"
                ) from error
        case _:
            raise ValueError(f"Unsupported fetch type: {fetch_type}")
    

# Connect and load data from db
def load_db_data(query:str, conn:Connection) -> pd.DataFrame:
    """
    
    """
    try:
        return pd.read_sql(query, conn)
    except Exception as error:
        raise RuntimeError(
            f"Database query failed:\n{query}"
        ) from error


# Create dictionary lookup for datasets to be used later in apply functions
def combine_columns(data:pd.DataFrame, number_of_columns:int, ordered_columns:list) -> dict:
    """
    
    """
    if number_of_columns == 2:
        return dict(zip(data[ordered_columns[0]], data[ordered_columns[1]]))
    elif number_of_columns == 3:
        return dict(zip(zip(data[ordered_columns[0]], data[ordered_columns[1]]), data[ordered_columns[2]]))
    else:
        raise ValueError(f"Number of columns must be 2 or 3 at the max, forming a dictionar")


def multiple_dataframes(fetch_path_kwargs:list[tuple]) -> list[pd.DataFrame]:
    """
    Takes a list tuples ("method", "path", "**kwargs"), fetches data and transforms into dataframes.

    Args:
        method_path_kwargs List[tuple]: [(
            method = same as load_data function ['csv', 'requests', 'db'],
            path = absolute_path/*.csv | url,
            kwargs = additional **kwargs associated with the fetch type
        )]

    Returns:
        A list of dataframes.
    """
    df_list = []
    for fetch, path, kwargs in fetch_path_kwargs:
        kwargs = kwargs or {}
        df_list.append(load_data(fetch, path, **kwargs))
        
    return df_list
