from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import train_test_split
import pandas as pd
import joblib
import re
import os
# Load datasets with appropriate error handling
try:
    emails_df = pd.read_csv('dataset/Phishing_Email.csv', quoting=3, on_bad_lines='skip', encoding='utf-8')
    urls_df = pd.read_csv('dataset/phishing_site_urls.csv', quoting=3, on_bad_lines='skip', encoding='utf-8')
except pd.errors.ParserError as e:
    print(f"Error reading CSV files: {e}")
    exit()

# Display the first few rows and data types of emails_df
print(emails_df.head())
print(emails_df.dtypes)

# Clean the data by removing rows where 'Email Text' is NaN
emails_df = emails_df.dropna(subset=['Email Text'])

# Add labels to the datasets
emails_df['label'] = 1  # Assuming 1 is phishing
urls_df['label'] = 1    # Assuming 1 is phishing

# Feature extraction functions
def extract_features_email(df):
    features = pd.DataFrame()
    if 'Email Text' in df.columns:
        features['length'] = df['Email Text'].apply(len)
    else:
        print("Column 'Email Text' not found in emails_df")
        exit()
    # Add more sophisticated text-based features here
    return features

def extract_features_url(df):
    features = pd.DataFrame()
    if 'URL' in df.columns:
        features['length'] = df['URL'].apply(len)
        features['num_dots'] = df['URL'].apply(lambda x: x.count('.'))
        features['has_ip'] = df['URL'].apply(lambda x: bool(re.search(r'\d+\.\d+\.\d+\.\d+', x)))
    else:
        print("Column 'URL' not found in urls_df")
        exit()
    # Add more sophisticated URL-based features here
    return features

# Extract features
email_features = extract_features_email(emails_df)
url_features = extract_features_url(urls_df)

# Combine features with labels
email_data = pd.concat([email_features, emails_df['label']], axis=1)
url_data = pd.concat([url_features, urls_df['label']], axis=1)

# Combine both datasets
final_data = pd.concat([email_data, url_data], ignore_index=True)

# Prepare data for training
X = final_data.drop('label', axis=1)
y = final_data['label']

# Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the model with missing value handling
pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='mean')),  # Handle missing values by replacing with the mean
    ('scaler', StandardScaler()),
    ('model', RandomForestClassifier(n_estimators=100, random_state=42))
])
pipeline.fit(X_train, y_train)

# Make predictions
y_pred = pipeline.predict(X_test)

# Evaluate the model
print(f"Accuracy: {accuracy_score(y_test, y_pred)}")
print(classification_report(y_test, y_pred))
output_dir = 'backend/models'
os.makedirs(output_dir, exist_ok=True)

# Save the model
joblib.dump(pipeline, os.path.join(output_dir, 'phishing_model.pkl'))
print("Model saved as 'backend/models/phishing_model.pkl'")

# # Save the model
# joblib.dump(pipeline, 'backend/models/phishing_model.pkl')
# print("Model saved as 'backend/models/phishing_model.pkl'")
