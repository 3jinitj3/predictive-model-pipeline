from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter, FuncFormatter
import seaborn as sns

# Creating a flexible path variable to execute file from any path.
project_root = Path(__file__).resolve().parents[2]
data_dir = project_root/"data"

# Data preprocessing, cleaning and normalizaton | etl (Extract, Transform, Load) | Load csv
Alzheimers_df = pd.read_csv(data_dir/"Alzheimers_Disease_dataset.csv")

# Import and structure question risk weights
question_risk_weights = pd.read_csv(data_dir/"question_risk_weights.csv")
question_weights = dict(zip(question_risk_weights["Question"], question_risk_weights["Weight"]))

# Import and structure state population data
state_populations = pd.read_csv(data_dir/"state_populations_2015-2025.csv")
state_populations = state_populations.drop(columns="Census_Vintage")
state_pop_lookup = dict(zip(zip(state_populations["State"], state_populations["Year"]), state_populations["Population"]))

# Import and structure state fifty plus data
fifty_plus = pd.read_csv(data_dir/"fifty_plus.csv")
fifty_plus_lookup = dict(zip(zip(fifty_plus["State"], fifty_plus["Year"]), fifty_plus["Age_50_Plus_Percentage"]))

# Import estimated cases by year (2015 - 2020)
estimated_cases = pd.read_csv(data_dir/"estimated_ad_cases_2015_2020.csv")
estimated_cases_lookup = dict(zip(zip(estimated_cases["State"], estimated_cases["Year"]), estimated_cases["Estimated_AD_Cases"]))

# Manipulation methods:
# columns(df.drop(column, axis=1)), rows(df.dropna()), drop_duplicate_rows(drop_duplicates())
# Count missing Valuess, isna().sum() or .isnull.sum()
# Fill missisng Valuess, it operates on the column before it df[column].fillna(Values, inplace=True)
# Other inputation technique: k-nearest neighbor, smote(synthetic minority oversampling technique)
# from sklearn.impute impot KNNImputer (k-nearest neighbor)
# inputer = KNNImputer(n_neighbors=2, weights="uniform")
# df[column] = imputer.fit_transform(df[same_column])

# Change dtype of str columns to category to reduce memory footprint
str_columns = Alzheimers_df.dtypes[Alzheimers_df.dtypes == "str"]
Alzheimers_df[str_columns.index] = Alzheimers_df[str_columns.index].astype('category')

# Order topic list
category_list = list(Alzheimers_df["Topic"].cat.categories)
Alzheimers_df["Topic"] = Alzheimers_df["Topic"].cat.set_categories(new_categories=category_list, ordered=True)

# List of columns to drop
columns_to_drop = [
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

# Rename columns
Alzheimers_df = Alzheimers_df.rename(columns={"Stratification1": "Age_Group", "Stratification2": "Race_Gender", "YearEnd": "Year", "LocationDesc": "State", "Data_Value": "Values"})

# Deal with empty rows, columns, and duplicates
# 1 .sum() shows na by columns, but two will show the df total
Alzheimers_df = (
    Alzheimers_df
    .drop(columns_to_drop, axis=1)
    .drop_duplicates()
    .dropna()
)

# Visualize the data to gain an understanding
# Helper notes for visualization.
#sns.set(font_scale=1.5)
#sns.set_style('example')
#sns.catplot(x='category', y='measure', data=df, kind='bar', hue='other_field')
#plt.show()





"""plt.figure(figsize=(10,6))
plt.hist(Alzheimers_df["Age_Group"], bins=4, alpha=.50, label="Original Age Group")
plt.legend(prop={'size': 16})
plt.title('Histogram of Age Group')
plt.xlabel('Age Groups'); plt.ylabel('Count')
plt.show()

plt.figure(figsize=(10,6))
plt.hist(Alzheimers_df["State"], bins=60, alpha=.50, label="Original State")
plt.legend(prop={'size': 16})
plt.title('Histogram of State')
plt.xlabel('States'); plt.ylabel('Counts')
plt.show()

plt.figure(figsize=(10,6))
plt.hist(Alzheimers_df["Race_Gender"], bins=15, alpha=.50, label="Original Race and Sex")
plt.legend(prop={'size': 16})
plt.title('Histogram of Race and Sex')
plt.xlabel('Race and Gender'); plt.ylabel('Counts')
plt.show()

data = Alzheimers_df["Values"]
plt.figure(figsize=(10,5))
plt.hist(data, bins=30, alpha=.5, label='Original Values')
plt.legend(prop={'size': 16})
plt.title('Histogram of Original Data Values')
plt.xlabel('Data Values (%)'); plt.ylabel('Counts')
plt.show()

# Using Catplot for visualization
sample_df = Alzheimers_df.sample(n=1000, replace=False, axis=0)
print(f"Sample DF info: \n{sample_df.info()}")
sns.set_style("darkgrid")
j = sns.catplot(x="Year", data=sample_df, kind="count", height=6, aspect=1.75,  palette=sns.color_palette("Paired"), legend=True)
j.figure.suptitle("EDA REPS")
j.set_axis_labels("Data from Years", "Average # of adults")
j.set_xticklabels(rotation=27.5, ha="right")
j.figure.subplots_adjust(bottom=.30, top=.90)
plt.show()"""

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

# Creating new features for risk weights
Alzheimers_df["Risk_By_Age_Group"] = Alzheimers_df["Age_Group"].map(age_ad_risk)
Alzheimers_df["Risk_By_State"] = Alzheimers_df["State"].map(state_ad_risk)
Alzheimers_df["Risk_By_Sex"] = Alzheimers_df["Race_Gender"].map(sex_ad_risk)
Alzheimers_df["Risk_By_Sex"] = Alzheimers_df["Risk_By_Sex"].fillna(0)
Alzheimers_df["Risk_By_Race"] = Alzheimers_df["Race_Gender"].map(race_ad_risk)
Alzheimers_df["Risk_By_Race"] = Alzheimers_df["Risk_By_Race"].fillna(0)
Alzheimers_df["Question_Risk_Weight"] = Alzheimers_df["Question"].map(question_weights)
Alzheimers_df["State_pop_by_year"] = Alzheimers_df[["State", "Year"]].apply(tuple, axis=1).map(state_pop_lookup)
Alzheimers_df["Fifty_plus_percentage"] = Alzheimers_df[["State", "Year"]].apply(tuple, axis=1).map(fifty_plus_lookup)
Alzheimers_df["Estimated_AD_state_cases"] = Alzheimers_df[["State", "Year"]].apply(tuple, axis=1).map(estimated_cases_lookup)
Alzheimers_df = Alzheimers_df[Alzheimers_df["Question_Risk_Weight"].notna()]

# Compare State Valuess with actual states and remove the difference
state_set = set(Alzheimers_df["State"].values)
state_set_check = set(state_ad_risk.keys())
state_rows_delete = list(state_set.difference(state_set_check))
Alzheimers_df = Alzheimers_df[~Alzheimers_df["State"].isin(state_rows_delete)]

# 1 in 9 people > 65 have Alzheimers Dementia, that 11% of americans
# Sex risk 21.1 male, 11.6 female
# Creating sex column to separate sex from the race_gender column
# Used weighted average formula to get risk metrics (female_risk * female_pop) + (male_risk * male_pop)/(total_pop)

# Separate sex demographic from Race_Gender column into its own column for risk metrics.
sex_mapping = [
    Alzheimers_df["Race_Gender"] == "Male",
    Alzheimers_df["Race_Gender"] == "Female"
]
sex_choices = ["Male", "Femle"]
Alzheimers_df["Sex"] = np.select(sex_mapping, sex_choices, default="Unknown")

# After separating sex, rename Race_Gender and clean up NaNs.
Alzheimers_df = Alzheimers_df.rename(columns={"Race_Gender": "Race"})
Alzheimers_df["Race"] = Alzheimers_df["Race"].cat.remove_categories(["Male", "Female"])
Alzheimers_df["Race"] = Alzheimers_df["Race"].cat.add_categories("Unknown").fillna("Unknown")

# Select optimal dtypes for columns below.
Alzheimers_df["Year"] = Alzheimers_df["Year"].astype('Int64')
Alzheimers_df["Sex"] = Alzheimers_df["Sex"].astype('category')
Alzheimers_df["Risk_By_Age_Group"] = Alzheimers_df["Risk_By_Age_Group"].astype('float64')
Alzheimers_df["State_pop_by_year"] = Alzheimers_df["State_pop_by_year"].astype('Int64')
Alzheimers_df["Estimated_AD_state_cases"] = Alzheimers_df["Estimated_AD_state_cases"].astype('Int64')

# Make sure float columns (risk metric columns) have only 2 decimals.
float_columns = Alzheimers_df.columns[Alzheimers_df.dtypes == "float64"]
Alzheimers_df[float_columns] = Alzheimers_df[float_columns].round(2)

# Set final order of df columns for organization.
final_col_order = ["Year", "State", "State_pop_by_year", "Fifty_plus_percentage", "Class", "Topic", "Question", "Age_Group", "Race", "Sex", "Values", "Risk_By_State", "Risk_By_Age_Group", "Risk_By_Race", "Risk_By_Sex", "Question_Risk_Weight", "Estimated_AD_state_cases"]
Alzheimers_df = Alzheimers_df[final_col_order]

# Output raw_processed df to csv
# Alzheimers_df.to_csv(data_dir/"Alzheimers_raw_processed_df.csv", index=False)

# Create target column next_year_cases.
targets = Alzheimers_df[
    ["State", "Year", "Estimated_AD_state_cases"]
].drop_duplicates().sort_values(["State", "Year"])

targets["Next_year_cases"] = targets.groupby("State")["Estimated_AD_state_cases"].shift(-1)
Alzheimers_df = Alzheimers_df.merge(
    targets[["State", "Year", "Next_year_cases"]],
    on=["State", "Year"],
    how="left"
)

train_data = Alzheimers_df[Alzheimers_df["Year"] <= 2018]
test_data = Alzheimers_df[
    (Alzheimers_df["Year"] <=2020) & (Alzheimers_df["Year"] > 2018)
]
test_data2 = Alzheimers_df[Alzheimers_df["Year"] > 2020]

# Output training and testing dataset to csv.
"""train_data.to_csv(data_dir/"train_dataset.csv", index=False)
test_data.to_csv(data_dir/"test_dataset.csv", index=False)
test_data2.to_csv(data_dir/"test2_dataset.csv", index=False)"""

"""print(Alzheimers_df.info())

ad_estimates = Alzheimers_df.groupby("Year")["Estimated_AD_state_cases"].agg(['mean', 'median', 'sum'])
print(ad_estimates)

# Theme
sns.set_theme(
    style='whitegrid',
    context='talk',
    palette='colorblind'
)

# Figure
plt.figure(figsize=(12,6))

# Plot data
plt.plot(
    ad_estimates.index,
    ad_estimates['mean'],
    label='Mean',
    linewidth=3,
    marker='o'
)
plt.plot(
    ad_estimates.index,
    ad_estimates['median'],
    linestyle='-.',
    linewidth=2.5,
    label='Median'
)

# Labels
plt.title(
    "Average Alzheimer's Cases Increased While Median Remained Relatively Stable",
    fontweight='bold',
    fontsize=16,
    pad=20
)
plt.xlabel("Year"); plt.ylabel("Estimated Alzheimer's Cases")
plt.tick_params(axis='both', labelsize=14)
plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda x, pos: f'{x/1000:,.0f}K'))
plt.ylim(50000, 130000)
for x, y in zip(ad_estimates.index, ad_estimates['mean']):
    if pd.notna(y):
        plt.annotate(
            f"{y:,.0f}",
            (x, y),
            textcoords='offset points',
            xytext=(0,-30),
            ha='center',
            fontsize=12
        )

# Extras
plt.legend(
    title='Statistic',
    title_fontsize=12,
    loc='upper left',
    bbox_to_anchor=(1,0.5),
    fontsize=10,
    frameon=False
)
sns.despine()
plt.grid(alpha=.20)
# Layout
plt.tight_layout()

# Display
plt.show()


"""
