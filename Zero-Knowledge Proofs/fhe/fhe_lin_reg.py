import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from concrete.ml.sklearn import LinearRegression as FHELinearRegression
from time import perf_counter

def load_and_preprocess_data():
    df = pd.read_csv("insurance.csv")
    target_col = "charges"

    X_raw = df.drop(columns=[target_col])
    y_dollars = df[target_col].to_numpy()
    y_thousands = y_dollars / 1000.0

    X = pd.get_dummies(X_raw, drop_first=True)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y_thousands, test_size=0.2, random_state=42)

    x_scaler = StandardScaler()
    X_train_scaled = x_scaler.fit_transform(X_train)
    X_test_scaled = x_scaler.transform(X_test)

    X_all_scaled = x_scaler.transform(X)
    y_all = y_thousands

    y_train = y_train
    y_test = y_test

    return X_train_scaled, y_train, X_test_scaled, y_test, X_all_scaled, y_all


if __name__ == "__main__":
    X_train, y_train, X_test, y_test, X_all_scaled, y_all = load_and_preprocess_data()

    fhe_linear_model = FHELinearRegression(n_bits=12)

    fhe_linear_model.fit(X_train, y_train)
    X_calibration = X_train[:200]

    # kompajliramo model u FHE kolo
    fhe_linear_model.compile(X_calibration)

    from time import perf_counter

    # Poređenje clear, simulate i execute režima na celoj bazi

    # Clear predikcija
    start = perf_counter()
    linear_clear_all = fhe_linear_model.predict(X_all_scaled)
    linear_clear_time = perf_counter() - start

    # FHE simulacija
    start = perf_counter()
    linear_sim_all = fhe_linear_model.predict(X_all_scaled, fhe="simulate")
    linear_sim_time = perf_counter() - start

    # FHE execute
    start = perf_counter()
    linear_execute_all = fhe_linear_model.predict(X_all_scaled, fhe="execute")
    linear_execute_time = perf_counter() - start

    linear_summary = pd.DataFrame({
        "mode": ["clear", "simulate", "execute"],
        "MAE": [
            mean_absolute_error(y_all, linear_clear_all),
            mean_absolute_error(y_all, linear_sim_all),
            mean_absolute_error(y_all, linear_execute_all)],
        "time_seconds": [
            linear_clear_time,
            linear_sim_time,
            linear_execute_time]})

    linear_comparison = pd.DataFrame({
        "actual_dollars": np.ravel(y_all),
        "clear_prediction": np.ravel(linear_clear_all),
        "simulate_prediction": np.ravel(linear_sim_all),
        "execute_prediction": np.ravel(linear_execute_all)
    })

    print(linear_summary)
    print(linear_comparison.head(10))
