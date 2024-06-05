import os
import csv
from sklearn.model_selection import train_test_split

# Function to gather data from video frame folders
def gather_data(folder_path):
    data = []
    # Iterate through each folder in the directory
    for folder in os.listdir(folder_path):
        full_path = os.path.join(folder_path, folder)
        # Check if the path is indeed a directory
        if os.path.isdir(full_path):
            # Count the number of frames (assuming files represent frames)
            num_frames = len([name for name in os.listdir(full_path) if os.path.isfile(os.path.join(full_path, name))])
            # Append the full path, an index of 0, and the number of frames to the data list
            data.append((full_path, 0, num_frames))
    return data

# Splitting the gathered data into training, validation, and testing sets
def split_data(data):
    # Adjust the test size to reflect the 70/15/15 split indirectly through train_test_split
    train_val, test = train_test_split(data, test_size=0.15, random_state=42)
    # Calculating validation size as a percentage of train_val size to maintain a 70/15/15 split overall
    train, val = train_test_split(train_val, test_size=0.1765, random_state=42)  # ~17.65% of 85% is ~15% of total
    return train, val, test

# Function to save data to a CSV file, ensuring no header is written
def save_to_csv(data, file_name):
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        # Write rows without including a header
        writer.writerows(data)

# Main execution block
if __name__ == "__main__":
    folder_path = '../CholecT45/CholecT45/data'  
    data = gather_data(folder_path)
    train, val, test = split_data(data)

    # Save the splits to CSV files
    save_to_csv(train, 'train.csv')
    save_to_csv(val, 'val.csv')
    save_to_csv(test, 'test.csv')
