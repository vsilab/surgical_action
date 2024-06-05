import os
import csv

actions_base_path = '../CholecT45/CholecT45/data_split_aug'  # Update with new path
new_csv_file_path = 'new_continuous_actions_aug_summary.csv'  # The new CSV file to create

with open(new_csv_file_path, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=' ')

    for folder_name in os.listdir(actions_base_path):
        folder_path = os.path.join(actions_base_path, folder_name)
        if os.path.isdir(folder_path):
            total_frames = sum(1 for f in os.listdir(folder_path) if f.endswith('.png'))
            # Assuming the label is the first part of the folder name
            label = folder_name.split('_')[0]
            csvwriter.writerow([folder_path, total_frames, label])

print("New CSV file has been created.")

import pandas as pd
from sklearn.model_selection import train_test_split

# Path to the original CSV file
csv_file_path = 'new_continuous_actions_aug_summary.csv'  

# Load the dataset
data = pd.read_csv(csv_file_path)

# Splitting the dataset into train, validation, and test sets
# Adjust the test_size and random_state as needed
train, test = train_test_split(data, test_size=0.2, random_state=42)  # 70% training, 30% test
val, test = train_test_split(test, test_size=0.5, random_state=42)  # Split the 30% into two 15% sets for val and test

# Specify the paths for the output CSV files
train_csv_path = 'data_aug/train.csv'
val_csv_path = 'data_aug/val.csv'
test_csv_path = 'data_aug/test.csv'

# Save the splits to new CSV files
train.to_csv(train_csv_path, index=False)
val.to_csv(val_csv_path, index=False)
test.to_csv(test_csv_path, index=False)

print("New train/test/validation file has been created.")