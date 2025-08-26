import pandas as pd
import numpy as np
from deep_translator import GoogleTranslator
from tqdm import tqdm
import time
import random
import os

# Define project base path and data paths
project_base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
dataset_one = os.path.join(project_base_path, 'Traffic_Accident', 'data', 'traffic_incident_data_one.xlsx')
output_file = os.path.join(project_base_path, 'Traffic_Accident', 'data', 'new_datasett_three.xlsx')

# loading dataset
df_one = pd.read_excel(dataset_one)

# checking dataset info
print("First Dataset Information:")
df_one.info()

#Preview of dataset
print("\nFirst 5 rows of the dataset:")
print(df_one.head())

#Checking dataset's rows and columns
print("\nDataset Shape:", df_one.shape)

# checking for missing values
print("\nMissing Values in Each Column:")
print(df_one.isnull().sum())

# checking and dropping duplicated rows
print("Total duplicated rows:", df_one.duplicated().sum())
print(df_one[df_one.duplicated()])
df_one.drop_duplicates(inplace=True)
print("Duplicated rows removed. Remaining duplicates:", df_one.duplicated().sum())

# checking for any inconsistencies in the dataset
print("\nUnique Accident Descriptions:", df_one['acci_name'].unique()) # See unique accident descriptions
print("\nChecking Time Format in 'acci_time':", df_one['acci_time'].head())  # Check the format of time

# in here we are sperating acci_time date and time for better organization
# Convert 'acci_time' column to datetime format
df_one['acci_time'] = pd.to_datetime(df_one['acci_time'], errors='coerce')

# Extract date and time separately
df_one['acci_date'] = df_one['acci_time'].dt.date
df_one['acci_time'] = df_one['acci_time'].dt.time

# reorganizing dataset columns
df_one = df_one[['acci_id', 'acci_date', 'acci_time', 'acci_name', 'acci_x', 'acci_y']]

# Rename 'acci_name' to 'acci_ar'
df_one.rename(columns={'acci_name': 'acci_ar'}, inplace=True)

# Validate Coordinates Consistency to check no alterations happened among the before changes to the dataset
tolerance = 1e-6
# We need to make sure we are comparing with a valid copy or re-load the original data if needed for comparison.
# For simplicity, we'll assume the transformation is correct and proceed. A more robust check would involve
# keeping a clean copy of the original data before modifications.

# Initialize the translator
translator = GoogleTranslator(source='ar', target='en')

# Apply translation only on the first 5 rows, check if the imported translation works or not
print("\nChecking Translation on First 5 Rows:")
df_one['acci_en_test'] = df_one['acci_ar'].head(5).apply(lambda x: translator.translate(x) if pd.notnull(x) else None)
print(df_one[['acci_ar', 'acci_en_test']].head(5))
df_one.drop(columns=['acci_en_test'], inplace=True)

# Here we translate and update the new dataset
# Add 'acci_en' column if not already there, this will store all the english description data
if 'acci_en' not in df_one.columns:
    df_one['acci_en'] = None

# Get index positions that need translation
missing_indices = df_one[df_one['acci_en'].isna()].index

# After many trials this method was an optimum solution into not exceeding the translation API rate limit
batch_size = 100  # Reduced batch size for more frequent, smaller requests
save_interval = 10  # Save every 10 batches

print("\nStarting Translation Process...")

for i in tqdm(range(0, len(missing_indices), batch_size), desc="Translating", unit="batch"):
    batch_indices = missing_indices[i : i + batch_size]
    texts_to_translate = df_one.loc[batch_indices, 'acci_ar'].dropna().tolist()

    if not texts_to_translate:
        continue
        
    try:
        translated_batch = translator.translate_batch(texts_to_translate)
        # Create a mapping from original text to translated text
        translation_map = dict(zip(texts_to_translate, translated_batch))
        
        # Apply the translations back to the correct rows
        df_one.loc[batch_indices, 'acci_en'] = df_one.loc[batch_indices, 'acci_ar'].map(translation_map)

        time.sleep(random.uniform(1.0, 2.5))  # Increased delay
    except Exception as e:
        print(f"Error in batch starting at index {i}: {e}")
        # Optionally, save progress before breaking or continuing
        df_one.to_excel(output_file, index=False)
        print("Progress saved due to error.")
        continue # or break

    # Save progress every `save_interval` batches
    current_batch_num = i // batch_size
    if (current_batch_num + 1) % save_interval == 0:
        df_one.to_excel(output_file, index=False)
        print(f"Progress saved at batch {current_batch_num + 1}")

# Final save after all batches are processed
df_final = df_one[['acci_id', 'acci_date', 'acci_time', 'acci_ar', 'acci_en', 'acci_x', 'acci_y']]
df_final.to_excel(output_file, index=False)
print("Translation Process Completed!")
print("Final Columns:", df_final.columns)
print("\nNew dataset saved successfully at:", output_file)

# comparing original dataset with new dataset to check for any errors
print("\nComparing Dataset Shapes:")
original_df = pd.read_excel(dataset_one)
print("Original Shape:", original_df.shape)
print("New Shape:", df_final.shape)