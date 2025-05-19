import mlflow
import os
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.ensemble import RandomForestRegressor
from dotenv import load_dotenv

load_dotenv()

df = load_diabetes()

X_train, X_test, y_train, y_test = train_test_split(df.data, df.target)

mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI"))

mlflow.set_experiment('Example Project')

mlflow.autolog()

print('Starting...')

with mlflow.start_run():
    rf = RandomForestRegressor(n_estimators=100, max_depth=6, max_features=3)
    rf.fit(X_train, y_train)
    prediction = rf.predict(X_test)
    mlflow.log_metric("my_metric", 0) 

print('The experiment was successfully completed')

