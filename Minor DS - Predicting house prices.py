import pandas as pd
from IPython.core.display import display
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from sklearn.preprocessing import LabelEncoder


def print_results(data, actual, predictions):
    print("vraagprijs = ", lr.intercept_, " + ",
          " + ".join(["{} * {}".format(el[0], el[1])
                      for el in list(zip(lr.coef_, X_train.columns))]))
    print("MSR: ", mean_squared_error(actual, predictions) ** (1 / 2))
    print("R2", r2_score(actual, predictions))

    results = data.copy()
    results['predicted'] = predictions
    results['true'] = y_test
    results['difference'] = results['predicted'] - results['true']
    display(results.iloc[results['difference'].abs().argsort()])


if __name__ == '__main__':
    # Read the data.
    df = pd.read_json("nl_for_sale_all_anon.json")
    labelencoder = LabelEncoder()

    # Remove unacceptable values.
    df = df[df["bouwjaar"] != 1005]

    # Make sure the data is of the correct type.
    df["vraagprijs"] = pd.to_numeric(df["vraagprijs"].str.replace(".",
                                                                  ""))
    df["bouwjaar"] = pd.to_numeric(df["bouwjaar"].str.replace(r"\w+\s+",
                                                              ""))
    df["perceel"] = pd.to_numeric(df["perceel"])

    # Drop unknown data.
    df.dropna(subset=["vraagprijs"])

    # Transform the data.
    steden = df["stad"].unique()
    stad_df = pd.DataFrame(steden, columns=["stad"])
    stad_df["stad_nr"] = labelencoder.fit_transform(
        stad_df["stad"])
    df = pd.merge(df, stad_df, on="stad")

    # df[["woning", "gebouw"]] = df["item_type"].str.split(", ",
    #                                                      expand=True)
    # df["gebouw"] = df["gebouw"].str.replace(r"\s\(.*\)", "")

    # woningen = df["woning"].unique()
    # woning_df = pd.DataFrame(woningen, columns=["woning"])
    # woning_df["woning_nr"] = labelencoder.fit_transform(
    #     woning_df["woning"])
    # df = pd.merge(df, woning_df, on="woning")

    # gebouwen = df["gebouw"].unique()
    # gebouw_df = pd.DataFrame(gebouwen, columns=["gebouw"])
    # gebouw_df["gebouw_nr"] = labelencoder.fit_transform(
    #     gebouw_df["gebouw"])
    # df = pd.merge(df, gebouw_df, on="gebouw")

    # Determine the features.
    y = df['vraagprijs']
    X = df[["woonoppervlakte", "bouwjaar", "perceel", "stad_nr",
            "kamers", "vraagprijsm2"]]

    # Split the data.
    X = X.fillna(0)
    X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                        test_size=0.20,
                                                        random_state=1)

    # Create a model.
    lr = LinearRegression()

    # Train the model to calculate the coefficients.
    lr.fit(X_train, y_train)
    pd.set_option('display.float_format', lambda x: '%.2f' % x)
    predictions = lr.predict(X_test)

    # Show the results.
    print_results(X_test, y_test, predictions)
