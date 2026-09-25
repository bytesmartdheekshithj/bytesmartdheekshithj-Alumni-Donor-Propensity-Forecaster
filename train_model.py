import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


DATA_PATH = "alumni_donor_dataset_2025.csv"
MODEL_PATH = "alumni_donor_propensity_model_2025.pkl"

data = pd.read_csv(DATA_PATH)
features = data.drop(columns=["Alumni_ID", "Is_Donor_2025"])
target = data["Is_Donor_2025"].map({"No": 0, "Yes": 1})

numeric_features = features.select_dtypes(include=["int64", "float64"]).columns.tolist()
categorical_features = features.select_dtypes(include=["object"]).columns.tolist()

numeric_transformer = Pipeline(
    steps=[("imputer", SimpleImputer(strategy="median"))]
)
categorical_transformer = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore")),
    ]
)
preprocessor = ColumnTransformer(
    transformers=[
        ("numerical", numeric_transformer, numeric_features),
        ("categorical", categorical_transformer, categorical_features),
    ]
)

model_pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        (
            "classifier",
            RandomForestClassifier(
                n_estimators=300,
                random_state=42,
                class_weight="balanced",
                n_jobs=-1,
            ),
        ),
    ]
)

model_pipeline.fit(features, target)
joblib.dump(model_pipeline, MODEL_PATH)
print(f"Saved trained model to {MODEL_PATH}")