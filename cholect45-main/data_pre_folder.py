import os
import shutil
import pandas as pd

# Path to the CSV file containing the frame-to-action mappings
csv_file_path = 'continuous_verbs.csv'  # actual path to CSV file

# Load the dataset
data = pd.read_csv(csv_file_path, header=None)

# Base path where the action folders will be created
actions_base_path = '../CholecT45/CholecT45/data_split'

# Ensure the base action folders path exists
if not os.path.exists(actions_base_path):
    os.makedirs(actions_base_path)

# Process the CSV and organize frames into action folders
for index, row in data.iterrows():
    video_folder_path, start_frame, length, label = row[0], int(row[1]), int(row[2]), row[3]
    end_frame = start_frame + length - 1  # Calculate end frame

    # Create a unique folder for each continuous action including the label
    action_folder_name = f"{label}_action_{index}_{start_frame}_{end_frame}"
    action_folder_path = os.path.join(actions_base_path, action_folder_name)
    if not os.path.exists(action_folder_path):
        os.makedirs(action_folder_path)

    # Move the frames to the action folder
    for frame_number in range(start_frame, end_frame + 1):
        frame_filename = f"{frame_number:06d}.png"  # Frame filenames are zero-padded to 6 digits
        frame_path = os.path.join(video_folder_path, frame_filename)
        frame_destination_path = os.path.join(action_folder_path, frame_filename)


        # if os.path.exists(frame_path):
        #     frame_destination_path = os.path.join(action_folder_path, frame_filename)
        #     shutil.move(frame_path, frame_destination_path)  # Move the frame

                # Debugging output
        print(f"Trying to move: {frame_path} to {frame_destination_path}")
        
        if os.path.exists(frame_path):
            shutil.copy(frame_path, frame_destination_path)  # Change from move to copy
        else:
            print(f"Frame does not exist: {frame_path}")
print("Frames have been organized into action folders.")

