import pandas as pd
import requests
from typing import Literal
from sqlalchemy.engine import Connection


# Extract data from csv or url and load into a df
def load_data(fetch_type:Literal["csv", "requests"], path_url:str, **kwargs) -> pd.DataFrame:
    """
    Fetch csv or json data and load to DataFrame.

    Args:
        fetch_type: Data source type ('csv' or 'requests').
        path_url: CSV file path or API URL.
        **kwargs: Additional arguments passed to the data source.

    Returns:
        DataFrame containing loaded data.

    Raises:
        FileNotFoundError: If CSV file not found.
        TimeoutError: If request exceeds timeout limit.
        ConnectionError: If connection to server could not be established.
        ValueError: If unsupported fetch_type is provided.
    """
    match fetch_type.lower().strip():
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
    Fetch data from database.

    Args:
        query: SQL query clauses.
        conn: Connection arguments for database.

    Returns:
        DataFrame containing loaded data.

    Raises:
        RuntimeError: If database query fails
    """
    try:
        return pd.read_sql(query, conn)
    except RuntimeError as error:
        raise RuntimeError(
            f"Database query failed:\n{query}"
        ) from error


# Create dictionary lookup for datasets to be used later in apply functions
def combine_columns(data:pd.DataFrame, number_of_columns:int, ordered_columns:list) -> dict:
    """
    Zip columns together to form a dictionary with a single key or tuple-based keys.

    Args:
        data: DataFrame
        number_of_columns: Determines whether the output uses a single key or tuple-based keys (2 or 3).
        ordered_columns: A List of column names in priority order. Place key column(s) first.

    Returns:
        Dictionary that can be used with mapping and apply functions.

    Raises:
        ValueError: If unsupported number_of_columns value is provided.
    """
    if number_of_columns == 2:
        return dict(zip(data[ordered_columns[0]], data[ordered_columns[1]]))
    elif number_of_columns == 3:
        return dict(zip(zip(data[ordered_columns[0]], data[ordered_columns[1]]), data[ordered_columns[2]]))
    else:
        raise ValueError(f"Number of columns must be 2 or 3 at the max, forming a dictionar")


# Create funciton to process multiple DataFrames
def multiple_dataframes(fetch_path_kwargs:list[tuple[str, str, dict]]) -> list[pd.DataFrame]:
    """
    Takes a list tuples, fetches data and converts it into DataFrames.

    Args:
        fetch_path_kwargs:
            List of tuples:
                fetch = Data source type ('csv' or 'requests')
                path = CSV file path or API URL
                kwargs = Additional arguments passed to the data source

    Returns:
        A list of loaded DataFrames.
    """
    df_list = []
    for fetch, path, kwargs in fetch_path_kwargs:
        kwargs = kwargs or {}
        df_list.append(load_data(fetch, path, **kwargs))
        
    return df_list
