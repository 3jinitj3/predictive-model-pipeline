











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

print(Alzheimers_df.info())

ad_estimates = Alzheimers_df.groupby("Year")["Estimated_AD_state_cases"].mean().sort_values()
print(ad_estimates)

"""# Theme
sns.set_theme(
    style='whitegrid',
    context='talk',
    palette='colorblind'
)

# Figure
fig = plt.figure(figsize=(12,6))

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

# Save and Dispay
fig.savefig(os.path.join("Charts", 'mean_vs_median.png'))
plt.show()"""

ad_cases = Alzheimers_df.groupby(["Year", "State"])["Estimated_AD_state_cases"].mean()

top_states = [
    "California",
    "Florida",
    "New York",
    "Pennsylvania",
    "Illinois"
]

filterd_states = Alzheimers_df[Alzheimers_df["State"].isin(top_states)]
filterd_states = filterd_states.copy()
filterd_states["State"] = filterd_states["State"].cat.remove_unused_categories()
print(filterd_states["State"].unique())
sns.set_theme(
    style='whitegrid',
    context='talk',
    palette='Set2'
)

top_five_fig = plt.figure(figsize=(12,6))
sns.lineplot(
    data=filterd_states,
    x="Year",
    y="Estimated_AD_state_cases",
    linewidth=2,
    marker='o',
    hue="State"
)

plt.title(
    "Top 5 Weighted States from 2015 - 2020 For Alzheimers Cases",
    fontsize=16,
    fontweight='bold',
    pad=20
)

plt.xlabel("Year"); plt.ylabel("Estimated AD Cases")
plt.tick_params(axis='both', labelsize=14)
plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda x, pos: f'{x/1000:,.0f}K'))
ca_cases = ad_cases.xs("California", level="State")
for x, y in zip(ca_cases.index, ca_cases):
    if pd.notna(y):
        plt.annotate(
            f"{y:,.0f}",
            (x, y),
            textcoords='offset points',
            xytext=(0, 10),
            ha='center',
            fontsize=12
        )
plt.legend(
    title="States",
    title_fontsize=12,
    loc= "upper left",
    bbox_to_anchor=(1,.50),
    fontsize=10,
    frameon=False
)
sns.despine()
plt.grid(alpha=.20)
plt.tight_layout()
top_five_fig.savefig(os.path.join("Charts", "top_five_states_by_cases.png"))
plt.show()



growth_pct = (((ad_cases.loc[2020] - ad_cases.loc[2015]) / ad_cases.loc[2015]) * 100).reset_index()
print(type(growth_pct))
print(growth_pct.sort_values(by="Estimated_AD_state_cases", ascending=False))
top_five_pct = growth_pct.sort_values(by="Estimated_AD_state_cases", ascending=False).head(5)
top_five_pct.columns = ["State", "Growth_Pct"]
top_five_pct["State"] = top_five_pct["State"].cat.remove_unused_categories()
top_five_pct = top_five_pct.sort_values(by="Growth_Pct", ascending=False)

growth_pct = growth_pct[growth_pct["State"].isin(filterd_states["State"])]
print(type(growth_pct))
print(growth_pct)
growth_pct = growth_pct.rename(columns={"Estimated_AD_state_cases":"Growth_Pct"})
print(type(growth_pct))
print(growth_pct)
print(len(growth_pct["State"]))
print(len(growth_pct["State"].cat.categories))
growth_pct["State"] = growth_pct["State"].cat.remove_unused_categories()
print(len(growth_pct["State"].cat.categories))

sns.set_theme(
    style='whitegrid',
    context='talk',
    palette='Set2'
)

growth_pct_fig = plt.figure(figsize=(12,6))

ax = sns.barplot(
        data=top_five_pct,
        x='State',
        y='Growth_Pct',
        width=.60,
        hue='State',
        dodge=False,
        palette="Set2"
    )
for container in ax.containers:
    ax.bar_label(
        container,
        fmt="%.2f%%",
        padding=3,
        fontsize=14,
        fontweight='400'
    )

plt.title(
    "Top 5 States By Percentage Increase in Alzheimers Cases",
    fontweight= 'bold',
    fontsize=16,
    pad=20
)

plt.xlabel("States"); plt.ylabel("Percentage Increase")
plt.tick_params(axis='both', labelsize=14)
plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda x, pos: f"{x:.2f}%"))

sns.despine()
plt.grid(alpha=.20)
plt.tight_layout()
growth_pct_fig.savefig(os.path.join("Charts", "top_five_by_pct.png"))
plt.show()

def create_figure(style_type:str, context_type:str, palette_type:str, **subplot_kwargs) -> tuple[Figure, Axes]:
    sns.set_theme(
        style=style_type,
        context=context_type,
        palette=palette_type
        )
    fig, ax = plt.subplots(**subplot_kwargs)
    return fig, ax

def chart_metadata(ax:Axes, ax_title:str, ax_xlabel:str, ax_ylabel:str, ax_fontsize:int) -> Axes:
    ax.set_title(title=ax_title, fontsize=ax_fontsize + 2, fontweight='bold')
    ax.set_xlabel(ax_xlabel, fontsize=ax_fontsize)
    ax.set_ylabel(ax_ylabel, fontisze=ax_fontsize)
    return ax

def style_ticks_grid(ax:Axes, grid_alpha:float, **tick_params_kwargs) -> Axes:
    ax.grid(alpha=grid_alpha)
    ax.tick_params(**tick_params_kwargs)
    return ax

def format_yaxis(ax:Axes, axis_type:Literal["%", "$", "K", "M"]) -> Axes:
    def formatter(func):
        ax.yaxis.set_major_formatter(FuncFormatter(func))
    match axis_type:
        case "%":
            formatter(lambda x, pos: f"{x:.2f}%")

        case "$":
            formatter(lambda x, pos: f"${x:.2f}")

        case "K":
            formatter(lambda x, pos: f"{x/1000:.0f}K")

        case "M":
            formatter(lambda x, pos: f"{x/1000000:.1f}M")
    return ax

def add_bar_labels(ax:Axes, label_type:Literal["%", "$", "K", "M"], **kwargs) -> Axes:
    for container in ax.containers:
        match label_type:
            case "%":
                formatter = lambda v: f"{v:.2f}%"
            case "$":
                formatter = lambda v: f"${v:,.2f}"
            case "K":
                formatter = lambda v: f"{v/1_000:.2f}K"
            case "M":
                formatter = lambda v: f"{v/1_000_000:.2f}M"
            case _:
                raise ValueError(f"Unsupported label type: {label_type}")
        labels = [formatter(value) for value in container.datavalues]
        ax.bar_label(container, labels=labels, padding=3, **kwargs)
    return ax

def clean_save_figure(fig:Figure, folder_name:str, png_name:str, show_plot:bool):
    sns.despine()
    fig.tight_layout()
    fig.savefig(os.path.join(folder_name, png_name))
    if show_plot:
        plt.show()

def hist_plot(data:pd.Series|pd.DataFrame, **kwargs) -> Axes:
    ax = sns.histplot(
        data=data,
        **kwargs
    )
    return ax

def bar_plot(data=pd.DataFrame, **kwargs) -> Axes:
    ax = sns.barplot(
        data=data,
        **kwargs
    )
    return ax

def box_plot(data=pd.DataFrame, **kwargs) -> Axes:
    ax = sns.boxenplot(
        data=data,
        **kwargs
    )
    return ax

def line_plot(data=pd.DataFrame, **kwargs) -> Axes:
    ax = sns.lineplot(
        data=data,
        **kwargs
    )
    return ax

def heatmap(data=pd.DataFrame, **kwargs) -> Axes:
    ax = sns.heatmap(
        data=data,
        **kwargs
    )
    return ax