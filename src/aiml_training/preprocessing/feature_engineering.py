import numpy as np
import pandas as pd
from  typing import Literal
from src.aiml_training.eda.analysis import datasets
from src.aiml_training import eda



def columns_to_categories(data:pd.DataFrame|list[pd.DataFrame], by_dtypes:Literal["object", "str", "both"]| None = None) -> pd.DataFrame |  list[pd.DataFrame]:
    """
    
    """
    def dtypes_to_categories(data):
        if by_dtypes == 'both':
            cat_data = data.select_dtypes(exclude='number').columns
            data[cat_data] = data[cat_data].astype('category')
        else:
            cat_data = data.select_dtypes(include=by_dtypes).columns
            data[cat_data] = data[cat_data].astype('category')
        return data
    
    if not isinstance(data, list):
        return dtypes_to_categories(data)
    df_list = []
    for df in data:
        df_list.append(dtypes_to_categories(df))
    return df_list


def drop_columns(data:pd.DataFrame|list[tuple[pd.DataFrame, str|list]], column_name:str|list|None = None) -> pd.DataFrame | list[pd.DataFrame]:
    """
    
    """
    if not isinstance(data, list):
        return data.drop(column_name, axis=1)
    df_list = []
    for df, cols_to_drop in data:
        df_list.append(df.drop(cols_to_drop, axis=1))
    return df_list


def rename_columns(data:pd.DataFrame|list[tuple[pd.DataFrame, dict[str:str]]], old_new:dict[str:str]|None = None) -> pd.DataFrame | list[pd.DataFrame]:
    """
    
    """
    if not isinstance(data, list):
        return data.rename(columns=old_new)
    df_list = []
    for df, rename_values in data:
        df_list.append(df.rename(columns=rename_values))
    return df_list


def clean_df(data:pd.DataFrame|list[pd.DataFrame]) -> pd.DataFrame|list[pd.DataFrame]:
    """
    
    """
    def drop_columns_na_duplicates(data):
        data = data.dropna()
        data = data.drop_duplicates()
        return data
    if not isinstance(data, list):
        return drop_columns_na_duplicates(data)
    df_list = []
    for df in data:
        df_list.append(drop_columns_na_duplicates(df))
    return df_list


def add_column_map_fill(data:pd.DataFrame, new_column:str|None = None, ref_column:str|None = None, mapping:dict|None = None, multiple_entry:tuple[tuple[str, str, dict],...]|None = None, fill:bool=False) -> pd.DataFrame:
    """
    
    """
    if multiple_entry is not None:
        for new_col, ref_col, ref_map in multiple_entry:
            data[new_col] = data[ref_col].map(ref_map)
            if fill:
                data[new_col] = data[new_col].fillna(0)
        return data
    data[new_column] = data[ref_column].map(mapping)
    if fill:
        data[new_column] = data[new_column].fillna(0)
    return data


# List of columns to drop
ad_columns_to_drop = [
    "RowId",
    "YearStart",
    "LocationAbbr",
    "Datasource",
    "Data_Value_Unit", 
    "DataValueTypeID",
    "Data_Value_Type",
    "Data_Value_Alt", 
    "Data_Value_Footnote_Symbol",
    "Data_Value_Footnote",
    "Low_Confidence_Limit",
    "High_Confidence_Limit",
    "StratificationCategory1",
    "StratificationCategory2",
    "ClassID",
    "TopicID",
    "QuestionID",
    "LocationID",
    "StratificationCategoryID1",
    "StratificationID1",
    "StratificationCategoryID2",
    "StratificationID2",
    "Geolocation"
]


datasets = {
    name: columns_to_categories(df, 'both')
    for name, df in datasets.items()
}

datasets['alzheimers_df'] = drop_columns(datasets['alzheimers_df'], ad_columns_to_drop)
datasets['state_populations_df'] = drop_columns(datasets['state_populations_df'], 'Census_Vintage')
datasets['alzheimers_df'] = rename_columns(
    datasets['alzheimers_df'],
    {"Stratification1": "Age_Group",
     "Stratification2": "Race_Gender",
     "YearEnd": "Year",
     "LocationDesc": "State",
     "Data_Value": "Question_Weight"
    }
)

alzheimers_df = datasets['alzheimers_df']
questions_df = datasets['questions_df']
state_populations_df = datasets['state_populations_df']
fifty_plus_df = datasets['fifty_plus_df']
estimated_cases_df = datasets['estimated_cases_df']


# Establish risk weights
# Age
age_ad_risk = {
    "50-64 years": .026,
    "65 years or older": .052,
    "Overall": .038
}

# State
state_ad_risk = {
    "Alabama": 0.118,
    "Alaska": 0.088,
    "Arizona": 0.110,
    "Arkansas": 0.113,
    "California": 0.120,
    "Colorado": 0.104,
    "Connecticut": 0.119,
    "Delaware": 0.113,
    "District of Columbia": 0.168,
    "Florida": 0.125,
    "Georgia": 0.120,
    "Hawaii": 0.113,
    "Idaho": 0.098,
    "Illinois": 0.120,
    "Indiana": 0.109,
    "Iowa": 0.110,
    "Kansas": 0.112,
    "Kentucky": 0.104,
    "Louisiana": 0.124,
    "Maine": 0.101,
    "Maryland": 0.129,
    "Massachusetts": 0.113,
    "Michigan": 0.112,
    "Minnesota": 0.107,
    "Mississippi": 0.125,
    "Missouri": 0.112,
    "Montana": 0.098,
    "Nebraska": 0.110,
    "Nevada": 0.106,
    "New Hampshire": 0.101,
    "New Mexico": 0.118,
    "New York": 0.127,
    "North Carolina": 0.116,
    "North Dakota": 0.111,
    "Ohio": 0.113,
    "Oklahoma": 0.108,
    "Oregon": 0.100,
    "Pennsylvania": 0.115,
    "Rhode Island": 0.114,
    "South Carolina": 0.115,
    "South Dakota": 0.105,
    "Tennessee": 0.109,
    "Utah": 0.100,
    "Vermont": 0.099,
    "Virginia": 0.117,
    "Washington": 0.102,
    "West Virginia": 0.102,
    "Wisconsin": 0.106,
    "Wyoming": 0.099
}

# Sex age 50 - 64
sex_ad_risk = {
    "Female": .112,
    "Male": .206
}

# Race
race_ad_risk = {
    "White": .10,
    "Hispanic": .14,
    "Black": .19,
    "Native Am/Alaskin Native": .17,
    "Asian/Pacific Islander": .10,
}

# Question
question_risk = eda.combine_columns(questions_df, 2, ['Question', 'Weight'])


# Creating new features for risk weights
alzheimers_df = add_column_map_fill(
    data=alzheimers_df,
    multiple_entry=(
        ('Risk_By_Age_Group', 'Age_Group', age_ad_risk),
        ('Risk_By_State', 'State', state_ad_risk),
        ('Risk_By_Sex', 'Race_Gender', sex_ad_risk),
        ('Risk_By_Race', 'Race_Gender', race_ad_risk),
        ('Risk_By_Question_Weight', 'Question', question_risk)
    )
)


alzheimers_df["State_pop_by_year"] = alzheimers_df[["State", "Year"]].apply(tuple, axis=1).map(eda.combine_columns(state_populations_df, 3, ['State', 'Year', 'Population']))
alzheimers_df["Fifty_plus_percentage"] = alzheimers_df[["State", "Year"]].apply(tuple, axis=1).map(eda.combine_columns(fifty_plus_df, 3, ['State', 'Year', 'Age_50_Plus_Percentage']))
alzheimers_df["Estimated_AD_state_cases"] = alzheimers_df[["State", "Year"]].apply(tuple, axis=1).map(eda.combine_columns(estimated_cases_df, 3, ['State', 'Year', 'Estimated_AD_Cases']))
# alzheimers_df = alzheimers_df[alzheimers_df["Risk_By_Question_Weight"].notna()]


# Separate sex demographic from Race_Gender column into its own column for risk metrics.
sex_mapping = [
    alzheimers_df["Race_Gender"] == "Male",
    alzheimers_df["Race_Gender"] == "Female"
]
sex_choices = ["Male", "Femle"]
alzheimers_df["Sex"] = np.select(sex_mapping, sex_choices, default="Unknown")

# After separating sex, rename Race_Gender and clean up NaNs.
alzheimers_df = alzheimers_df.rename(columns={"Race_Gender": "Race"})
alzheimers_df["Race"] = alzheimers_df["Race"].cat.remove_categories(["Male", "Female"])
alzheimers_df["Race"] = alzheimers_df["Race"].cat.add_categories("Unknown").fillna("Unknown")

# Select optimal dtypes for columns below.
alzheimers_df["Year"] = alzheimers_df["Year"].astype('Int64')
alzheimers_df["Sex"] = alzheimers_df["Sex"].astype('category')
alzheimers_df["Risk_By_Age_Group"] = alzheimers_df["Risk_By_Age_Group"].astype('float64')
alzheimers_df["State_pop_by_year"] = alzheimers_df["State_pop_by_year"].astype('Int64')
alzheimers_df["Estimated_AD_state_cases"] = alzheimers_df["Estimated_AD_state_cases"].astype('Int64')

# Make sure float columns (risk metric columns) have only 2 decimals.
float_columns = alzheimers_df.columns[alzheimers_df.dtypes == "float64"]
alzheimers_df[float_columns] = alzheimers_df[float_columns].round(2)

# Set final order of df columns for organization.
final_col_order = ["Year", "State", "State_pop_by_year", "Fifty_plus_percentage", "Class", "Topic", "Question", "Age_Group", "Race", "Sex", "Question_Weight", "Risk_By_State", "Risk_By_Age_Group", "Risk_By_Race", "Risk_By_Sex", "Risk_By_Question_Weight", "Estimated_AD_state_cases"]
alzheimers_df = alzheimers_df[final_col_order]


# Output raw_processed df to csv
alzheimers_df.to_csv("data/alzheimers_raw_processed_df.csv", index=False)

# Create target column next_year_cases.
targets = alzheimers_df[
    ["State", "Year", "Estimated_AD_state_cases"]
].drop_duplicates().sort_values(["State", "Year"])


targets["Next_year_cases"] = targets.groupby("State")["Estimated_AD_state_cases"].shift(-1)
alzheimers_df = alzheimers_df.merge(
    targets[["State", "Year", "Next_year_cases"]],
    on=["State", "Year"],
    how="left"
)

num_cols = alzheimers_df[['Risk_By_Sex', 'Risk_By_Race', 'Question_Weight', 'Risk_By_Question_Weight', 'Risk_By_State', 'Fifty_plus_percentage']].columns
alzheimers_df[num_cols] = alzheimers_df[num_cols].fillna(alzheimers_df[num_cols].median())
alzheimers_df['State_pop_by_year'] = alzheimers_df.groupby('Year')['State_pop_by_year'].transform(lambda x: x.fillna(x.median()))
alzheimers_df['Estimated_AD_state_cases'] =alzheimers_df.groupby('State')["Estimated_AD_state_cases"].transform(lambda x: x.fillna(x.median()))
alzheimers_df = alzheimers_df.dropna(subset='Next_year_cases').copy()

model_df = alzheimers_df.copy()
model_df.to_csv("data/alzheimers_model_ready.csv", index=False)