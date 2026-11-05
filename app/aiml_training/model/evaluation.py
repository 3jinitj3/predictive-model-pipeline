import pandas as pd
from src.aiml_training.preprocessing.feature_engineering import feature_engineering_main
from .models import LinearRegression
from .train import *
from collections.abc import Callable
import textwrap




def header(column_name:str|list[str]) -> None:
    """
    
    """
    def print_header():
        print(f"{'=' * 100}")
        print(f"{'R2 Result With The Removal Of Column(s)':^100}")

    if isinstance(column_name, str):
        column_name = column_name.replace('_', ' ').title()
        print_header()
        print(f"{column_name:^100}")
        print(f"{'=' * 100}\n")
    elif isinstance(column_name, list):
        formatted_cols = [col.replace('_', ' ').title() for col in column_name]
        remove_cols = ", ".join(formatted_cols)
        print_header()
        for line in textwrap.wrap(remove_cols, width=80):
            print(f"{line:^100}")
        print(f"{'=' * 100}\n")
    return None


def footer() -> None:
    """
    
    """
    print(f"{'=' * 100}")
    print(f"{'End of R2 Report For Column ':^100}")
    print(f"{'=' * 100}\n")
    return None


def report_base(evaluation_data:type[EvaluationData], remove_column:str|list[str]) -> None:
    """
    
    """
    evaluation_data.model_df = evaluation_data.model_df.drop(columns=remove_column)
    train_model(
        model_df=evaluation_data.model_df,
        sklearn_model=evaluation_data.model,
        target_cols=evaluation_data.target_cols,
        time_series_col=evaluation_data.time_series_col,
        time_split=evaluation_data.time_split,
        grouping=evaluation_data.grouping,)
    return None


def abalation(columns:list) -> None:
    """
    
    """
    for column in columns:
        header(column)
        report_base(remove_column=column)
        footer()
    return None


def sequential_elimination(columns:list) -> None:
    """
    
    """
    running_columns = []
    for column in columns:
        running_columns.append(column)
        header(running_columns)
        report_base(remove_column=running_columns)
        footer()
    return None


def evaluation_report(report_function:Callable, remove_columns:list) -> None:
    """
    
    """
    report_function(remove_columns)
    return None




if __name__ == "__main__":
    pass
