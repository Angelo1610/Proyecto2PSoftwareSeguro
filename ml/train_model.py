import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score

df = pd.read_csv("dataset.csv")

X = df["code"]
y = df["label"]

pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(max_features=5000)),
    ("rf", RandomForestClassifier(n_estimators=100, random_state=21))
])

scores = cross_val_score(pipeline, X, y, cv=5)
print("Accuracy promedio:", scores.mean())

pipeline.fit(X, y)

joblib.dump(pipeline, "model.pkl")
print("Modelo guardado exitosamente en model.pkl")
