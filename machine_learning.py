import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import pickle
import os

# Load dataset
df = pd.read_csv('C:\\Users\\hp\\Regex\\data files\\Car Sell Dataset.csv')

# Label Encoding
le_dict = {}
categorical_cols = ['Brand', 'Model Name', 'Model Variant', 'Car Type',
                    'Transmission', 'Fuel Type', 'Owner', 'State', 'Accidental']

for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    le_dict[col] = le

# Manually fit Owner encoder (for consistent order)
all_owner_values = ['First', 'Second', 'Third', 'Fourth & Above']
le_owner = LabelEncoder()
le_owner.fit(all_owner_values)
le_dict['Owner'] = le_owner

# Split data
X = df.drop(columns='Price')
y = df['Price']

x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Random Forest
rf = RandomForestRegressor()
rf.fit(x_train, y_train)

# Save model and encoders
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, 'rf_model.pkl')
encoder_path = os.path.join(BASE_DIR, 'le_dict.pkl')

with open(model_path, 'wb') as f:
    pickle.dump(rf, f)

with open(encoder_path, 'wb') as f:
    pickle.dump(le_dict, f)

print("✅ Model and encoders saved successfully!")
