import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
file_path = "C:\\Users\\sasha\\Traffic_Accident_Analysis_Project\\Traffic_Accident\\data\\latest_dataset.xlsx"
df = pd.read_excel(file_path)

# Convert weather conditions to lowercase & remove extra spaces
df['condition'] = df['condition'].str.lower().str.strip()

# Fill missing values in the condition column
df['condition'].fillna('unknown', inplace=True)

# Get the total number of accidents
total_accidents = len(df)

# Plot the data without merging categories
plt.figure(figsize=(12, 5))
ax = sns.countplot(x='condition', data=df, order=df['condition'].value_counts().index, palette="viridis")

# Rotate labels for readability
plt.xticks(rotation=90)

# Update title with total count
plt.title(f"Accidents by Weather Condition (Total: {total_accidents})")

# Label the y-axis
plt.ylabel("Accident Count")

plt.show()

# Check if all accidents are counted
print("Total accident count in dataset:", total_accidents)
print("Total accidents counted in graph:", df['condition'].value_counts().sum())
