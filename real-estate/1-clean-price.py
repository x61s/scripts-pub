import json

# Exchange rate from TL to EUR
exchange_rate = 0.033

# Function to clean and convert price
def clean_and_convert_price(price, rate):
    try:
        tl_price = int(price.replace(" TL", "").replace(",", "").replace(" ", ""))
        return round(tl_price * rate, 2)
    except ValueError:
        return None

# Load JSON data from a file
with open('data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Create a new dictionary to store the cleaned and converted data
cleaned_data = {}

# Iterate through the dataset and update the prices
for key, value in data.items():
    cleaned_price = clean_and_convert_price(value[4], exchange_rate)
    if cleaned_price is not None:
        value[4] = cleaned_price
        cleaned_data[key] = value

# Save the cleaned and converted data back to a file
with open('cleaned_converted_data_eur.json', 'w', encoding='utf-8') as file:
    json.dump(cleaned_data, file, indent=4, ensure_ascii=False)

print("Cleaned and converted data saved to 'cleaned_converted_data_eur.json'")

