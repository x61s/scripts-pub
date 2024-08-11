import json
import pandas as pd

# Load JSON data from a file
with open('cleaned_converted_data_eur.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Convert the JSON data to a pandas DataFrame
df = pd.DataFrame.from_dict(data, orient='index', columns=[
    'url', 'description', 'size', 'apartment_type', 'price', 'date', 'location'
])

# # Group by apartment type and calculate the required statistics
# stats = df.groupby('apartment_type')['price'].agg(['min', 'max', 'mean', 'median']).reset_index()

# Group by apartment type and calculate the required statistics
stats = df.groupby('apartment_type').agg(
    count=('price', 'size'),
    min_price=('price', 'min'),
    max_price=('price', 'max'),
    avg_price=('price', 'mean'),
    median_price=('price', 'median')
).reset_index()

# Print the results
print(stats)

