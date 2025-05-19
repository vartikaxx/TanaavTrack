import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.feature_selection import SelectFromModel
import joblib

# Load the dataset
df = pd.read_csv('Impact_of_Remote_Work_on_Mental_Health.csv')

# Drop Employee_ID as it's not relevant for prediction
df = df.drop('Employee_ID', axis=1)

# Convert Stress_Level to numeric
stress_level_map = {'Low': 25, 'Medium': 50, 'High': 75}  # Changed to more balanced values
df['Stress_Level'] = df['Stress_Level'].map(stress_level_map)

# Add interaction features
df['Work_Pressure'] = df['Hours_Worked_Per_Week'] * df['Number_of_Virtual_Meetings'] / 100
df['Support_Balance'] = df['Company_Support_for_Remote_Work'] * df['Work_Life_Balance_Rating'] / 10

# Separate features and target
X = df.drop(['Stress_Level', 'Mental_Health_Condition'], axis=1)  # Remove Mental_Health_Condition as it's an outcome
y = df['Stress_Level']

# Identify numeric and categorical columns
numeric_features = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
categorical_features = X.select_dtypes(include=['object']).columns.tolist()

# Create preprocessing pipelines for both numeric and categorical data
numeric_transformer = Pipeline(steps=[
    ('scaler', StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ('onehot', OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore'))
])

# Combine preprocessing steps
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ])

# Create a pipeline with preprocessing and model
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', GradientBoostingRegressor(random_state=42))
])

# Define parameter grid for GridSearchCV
param_grid = {
    'regressor__n_estimators': [100, 200],
    'regressor__learning_rate': [0.05, 0.1],
    'regressor__max_depth': [3, 4, 5],
    'regressor__min_samples_split': [2, 5],
    'regressor__min_samples_leaf': [1, 2]
}

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Perform grid search
grid_search = GridSearchCV(model, param_grid, cv=5, scoring='r2', n_jobs=-1)
grid_search.fit(X_train, y_train)

print("Best parameters:", grid_search.best_params_)
print("\nModel Performance:")
print(f"Train R² score: {grid_search.score(X_train, y_train):.4f}")
print(f"Test R² score: {grid_search.score(X_test, y_test):.4f}")

# Get feature importance
feature_names = (numeric_features + 
                [f"{feat}_{val}" for feat, vals in 
                 zip(categorical_features, 
                     grid_search.best_estimator_.named_steps['preprocessor']
                     .named_transformers_['cat'].named_steps['onehot'].categories_) 
                 for val in vals[1:]])

feature_importance = pd.DataFrame({
    'feature': feature_names,
    'importance': grid_search.best_estimator_.named_steps['regressor'].feature_importances_
})
feature_importance = feature_importance.sort_values('importance', ascending=False)

print("\nTop 10 Most Important Features:")
print(feature_importance.head(10))

# Save the best model
joblib.dump(grid_search.best_estimator_, 'models/stress_predictor.pkl')

# Save feature names and other metadata
metadata = {
    'numeric_features': numeric_features,
    'categorical_features': categorical_features,
    'feature_names': feature_names,
    'stress_level_map': stress_level_map
}
joblib.dump(metadata, 'models/metadata.pkl')

print("\nModel and metadata saved successfully!") 