from src.aiml_training.eda.aquisition import  multiple_dataframes
import pandas as pdload_data,
import numpy as np
from pathlib import Path


# Creating a flexible path variable to execute file from any path.
project_root = Path(__file__).resolve().parents[3]
data_dir = project_root/"data"


# Load datasets
alzheimers_df, questions_df, state_populations_df, fifty_plus_df, estimated_cases_df = multiple_dataframes([
    ("csv", f"{data_dir}/Alzheimers_Disease_dataset.csv", None),
    ("csv", f"{data_dir}/question_risk_weights.csv", None),
    ("csv", f"{data_dir}/state_populations_2015-2025.csv", None),
    ("csv", f"{data_dir}/fifty_plus.csv", None),
    ("csv", f"{data_dir}/estimated_ad_cases_2015_2020.csv", None)
])


# Store datasets in order to reference the dataframe and variable name.
datasets = {
    "alzheimers_df": alzheimers_df,
    "questions_df": questions_df,
    "state_populations_df": state_populations_df,
    "fifty_plus_df": fifty_plus_df,
    "estimated_cases_df": estimated_cases_df
}


# Report header
def header(report:str, df_name:str) -> None:
    """
    Create header for formatted reports.

    Args:
        report: Name of the report.
        df_name: Name of DataFrame.

    Returns:
        None: Prints formatted header banner.
    """
    title = f"{report.title()} Report for {df_name}"
    print(f"{'=' * 100}")
    print(f"{title:^100}")
    print(f"{'=' * 100}\n")


# Report footer
def footer(report:str, df_name:str) -> None:
    """
    Create footer for formatted reports.

    Args:
        report: Name of the report.
        df_name: Name of DataFrame.

    Returns:
        None: Prints formatted footer banner.
    """
    title = f"End of {report.title()} Report for {df_name}"
    print(f"{'=' * 100}")
    print(f"{title:^100}")
    print(f"{'=' * 100}\n")


# Function to print out descriptive statistics for each dataframe
def descriptive_stats(df_dict:dict[str:pd.DataFrame]) -> None: # Later return dict for reports.
    """
    Print descriptive statistics for each DataFrame.

    Args:
        df_dict: Dictionary of DataFrames. Dictionary key is the DataFrame name and its value is the DataFrame.

    Returns:
        None: Prints formatted descriptive statistics report.
    """
    for name, dataset in df_dict.items():
        print(f"{'=' * 100}")
        print(f"{name:^100}")
        print(f"{'=' * 100}\n")
        print(f"{dataset.head(10)}")
        print(f"{'=' * 100}\n")
        print(f"{name}\n{dataset.info()}")
        print(f"{'=' * 100}\n")
        print(f"{name}\n{dataset.describe()}")
        print(f"{'=' * 100}\n")
        print(f"{name}\n{dataset.isna().sum()}")
        print(f"{'=' * 100}")
        print(f"{'End of Summary Stats':^100}")
        print(f"{'=' * 100}\n")


# Print missing values form each dataframe
def missing_value_summary(df_dict:dict[str:pd.DataFrame]) -> None: # Later return dict for reports.
    """
    Print summary of missing values.

    Args:
        df_dict: Dictionary of DataFrames. Dictionary key is the DataFrame name and its value is the DataFrame.

    Returns:
        None: Prints formatted missing values report.
    """
    for name, dataset in df_dict.items():
        missing_values_series = dataset.isna().sum()
        series_filter = missing_values_series[missing_values_series.values > 0]
        if series_filter.empty:
            continue
        else:
            print(f"{'=' * 100}")
            print(f"{name:^100}")
            print(f"{'=' * 100}\n")
            print(f"{series_filter}\n")
            print(f"{'=' * 100}")
            print(f"{'Total missing values:':<25}{series_filter.values.sum():,.0f}")
            print(f"{'=' * 100}\n")


# Change str and object dtypes to categorical for memory efficiency and prep for model encoding
def categorical_summary(df_dict:dict[str:pd.DataFrame]) -> None: # Later return dict for reports.
    """
    Prints columns with str data types as categorical data types to see the number of unique values for future encoding.

    Args:
        df_dict: Dictionary of DataFrames. Dictionary key is the DataFrame name and its value is the DataFrame.

    Returns:
        None: Prints formatted report on categorical values per string column in each DataFrame.
    """
    for name, dataset in df_dict.items():
        string_cols = dataset.select_dtypes(include=['object', 'str']).columns
        dataset[string_cols] = dataset[string_cols].astype('category')
        category_dict = {
            column_name: values.cat.categories.tolist() for column_name, values in dataset[string_cols].items()
        }
        title = f"List of {name} Column Categories"
        print(f"{'=' * 100}")
        print(f"{name:^100}")
        print(f"{'=' * 100}\n")
        print(f"{title:^100}\n")
        for column, categories in category_dict.items():
            print(f"{'Column Name:':<13}{column}")
            print(f"{'Categories':<13}{len(categories)}")
            if len(categories) <= 75:
                print(*[f"o {category}" for category in categories], sep='\n')
                print()
            else:
                print("Sample Categories")
                print(*[f"o {category}" for category in categories[:25]], sep='\n')
        print(f"{'=' * 100}\n")
        # Return a summary dict: "Question": {"n_categories": 39, "categories": [..]}


# Generate correlation report for each dataframe
def correlation_summary(df_dict:dict[str:pd.DataFrame]) -> None: # Later return dict for reports.
    """
    Print correlation summary for each DataFrame.

    Args:
        df_dict: Dictionary of DataFrames. Dictionary key is the DataFrame name and its value is the DataFrame.

    Returns:
        None: Prints formatted correlation summary report.
    """
    for name, dataset in df_dict.items():
        numerical_df = dataset.select_dtypes(include='number')
        corr_matrix = numerical_df.corr()
        if corr_matrix.shape[0] < 2:
            print(f"\n{name.title()} does not enough numerical columns for a correlation analysis.\n")
        else:
            title = f"Correlation Report for {name}"
            print(f"{'=' * 100}")
            print(f"{title:^100}")
            print(f"{'=' * 100}\n")
            print(f"{'Variable 1':^33}{'Variable 2':^33}{'Correlation':^33}")
            print(f"{'-' * 80:^100}")
            correlations = []
            for i, j in zip(*np.triu_indices_from(corr_matrix, k=1)):
                correlations.append(
                    (corr_matrix.columns[i],
                    corr_matrix.columns[j],
                    corr_matrix.iloc[i, j])
                )
            correlations.sort(key=lambda x: abs(x[2]), reverse=True)
            for var1, var2, corr in correlations:
                print(f"{var1:^33}{var2:^33}{corr:^33.3f}")
            print(f"{'-' * 80:^100}\n")
        # return dictionary for reporting


# Duplicate report for dataframes
def duplicate_summary(df_dict:dict[str:pd.DataFrame]) -> None: # Later return dict for reports.
    """
    Prints summary of DataFrame duplicates.

    Args:
        df_dict: Dictionary of DataFrames. Dictionary key is the DataFrame name and its value is the DataFrame.

    Returns:
        None: Prints formatted duplicate report.
    """
    for name, dataset in df_dict.items():
        raw_row_number = dataset.shape[0]
        dataset = dataset.drop_duplicates()
        duplicate_rows = raw_row_number - dataset.shape[0]
        if duplicate_rows == 0:
            header('duplicate', name)
            print(f"{'Number of rows:':<17}{raw_row_number}")

            print(f"{'Duplicate rows:':<17}{duplicate_rows}\n")
            footer('duplicate', name)
        else:
            footer('duplicate', name)
            print(f"{'Number of rows:':<17}{raw_row_number}")
            print(f"{'Duplicate rows:':<17}{duplicate_rows}\n")
            footer('duplicate', name)


# Get dtypes within dataframes
def dtypes_summary(df_dict:dict[str:pd.DataFrame]) -> None: # Later return dict for reports.
    """
    Prints a summary of DataFrame data types.

    Args:
        df_dict: Dictionary of DataFrames. Dictionary key is the DataFrame name and its value is the DataFrame.

    Returns:
        None: Prints formatted data types report.
    """
    for name, dataset in df_dict.items():
        dtypes = dataset.dtypes
        header('dtypes', name)
        print("Column Names and Data Types")
        print(dtypes,'\n')
        print("Data Types by Percentage")
        print(dataset.dtypes.value_counts(normalize=True))
        footer('dtypes', name)


# Generate report on numerical column outliers. Get IQR(Interquartile Range) and report values outside upper and lower limits.
def outlier_summary(df_dict:dict[str:pd.DataFrame]) -> None: # Later return dict for reports.
    """
    Prints a summary of DataFrame numerical column outliers.

    Args:
        df_dict: Dictionary of DataFrames. Dictionary key is the DataFrame name and its value is the DataFrame.

    Returns:
        None: Prints formatted numerical columns outlier report
    """
    for name, dataset in df_dict.items():
        numerical_df = dataset.select_dtypes(include='number')
        header('outlier', name)
        for column_name, data in numerical_df.items():
            q1 = round(data.quantile(.25), 2)
            q3 = round(data.quantile(.75), 2)
            iqr = round(q3 - q1, 2)
            upper_limit = round(q3 + (1.5 * iqr), 2)
            lower_limit = round(q1 - (1.5 * iqr), 2)
            upper_outliers = data[data > upper_limit]
            upper_count = upper_outliers.shape[0]
            lower_outliers = data[data < lower_limit]
            lower_count = lower_outliers.shape[0]
            print(f"{'Column Name:':<30}{column_name}")
            print(f"{f'Upper Outliers:':<30}{upper_count}")
            print(f"{f'Lower Outliers:':<30}{lower_count}\n")
            print(f"{'Q1 Quantile:':<30}{q1}")
            print(f"{'Q3 Quantile:':<30}{q3}")
            print(f"{'Inter Quartile Range (IQR):':<30}{iqr}")
            print(f"{'Upper Threshold:':<30}{upper_limit}")
            print(f"{'Lower Threshold:':<30}{lower_limit}\n")
            print(f"Upper Outlier Values\n{'=' * 20}")
            if upper_outliers.empty:
                print("No Upper Outliers")
            else:
                if len(upper_outliers) > 100:
                    print("Number of upper outliers is to large to print (>100)")
                    print(f"Sample\n{upper_outliers.values[:10]}")
                else:
                    print(*[f'o {value}' for value in upper_outliers], sep='\n')
            print()
            print(f"Lower Outlier Values\n{'=' * 20}")
            if lower_outliers.empty:
                print("No Lower Outliers")
            else:
                if len(lower_outliers) > 100:
                    print("Number of lower outliers is to large to print (>100)")
                    print(f"Sample\n{lower_outliers.values[:10]}")
                else:
                    print(*[f'o {value}' for value in lower_outliers], sep='\n')
            print()
            print(f"{'=' * 100}")
        footer('outlier', name)
        # add outlier pct count per column to see the distribution
