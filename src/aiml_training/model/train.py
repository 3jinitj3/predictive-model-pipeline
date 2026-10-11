from src.aiml_training import preprocessing
from .models import LinearRegression

preprocessing.final_col_order.append('Next_year_cases')
preprocessing.final_col_order.remove('State')
preprocessing.final_col_order.remove('Year')
def abalation(removed_column:str):
    # def train_main():
    preprocessing.model_df['ad_rate'] = preprocessing.model_df['Next_year_cases'] / preprocessing.model_df['State_pop_by_year']
    training_df = preprocessing.model_df.drop(columns=[removed_column])
    if len(training_df.columns) == 2:
        print('Down to group indexes')
        return
    train_df = training_df[training_df['Year'] <= 2018].groupby(['Year', 'State']).mean(numeric_only=True)
    X_train = train_df.drop(columns='ad_rate')
    y_train = train_df['ad_rate']
    test_df = training_df[training_df['Year'] == 2019].groupby(['Year', 'State']).mean(numeric_only=True)
    X_test = test_df.drop(columns='ad_rate')
    y_test = test_df['ad_rate']
    # training_df = training_df.groupby(['Year', 'State']).mean(numeric_only=True)
    # training_df_2018 = training_df[training_df['Year'] <=2018]
    # training_df_2019 = training_df[training_df['Year'] == 2019]
    # test_2019 = training_df_2019.drop(columns='ad_rate')
    # test_key_2019 = test_2019['ad_rate']
    # prepared_data = preprocessing.prepare_pipeline_data(training_df_2018, 'ad_rate')
    linear_regression = LinearRegression()
    linear_regression.build_pipeline(X_train.select_dtypes(include='category').columns.tolist(), X_train.select_dtypes(exclude='category').columns.tolist())
    linear_regression.pipeline.fit(X_train, y_train)
    y_prediction = linear_regression.pipeline.predict(X_test)
    linear_regression.evaluate(y_test, y_prediction)


for column in preprocessing.final_col_order:
    print(f"{'=' * 50}")
    print(f"{f'R2 Result With The Removal Of Column {column}':^50}")
    print(f"{'=' * 50}")
    abalation(column)
    print(f"{'=' * 50}")
    print(f"{'End of R2 Report For Column ':^50}")
    print(f"{'=' * 50}")

# if __name__ == "__main__":
#     train_main()