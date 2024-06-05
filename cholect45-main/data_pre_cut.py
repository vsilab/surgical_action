import os
import csv

# Assume a base path for the video folders, needs to be specified
base_video_path = '../CholecT45/CholecT45/data'

# Placeholder for the path where the verb annotation files are located
annotation_folder_path = '../CholecT45/CholecT45/verb'
output_csv_path = 'continuous_verbs.csv'
output_csv_path_pretrian = 'continuous_verbs_pretrain.csv'

# Debugging: Check detected files in the directory
detected_files = os.listdir(annotation_folder_path)
print("Detected files:", detected_files)
print('number of files detexted', len(detected_files))


# # Debug function to process a single verb annotation file
# def debug_process_verb_file(file_name):
#     print(f"Processing file: {file_name}")
#     file_path = os.path.join(verb_annotation_path, file_name)
#     with open(file_path, 'r') as file:
#         for line in file:
#             print(f"Reading line: {line.strip()}")
#     print(f"Finished processing {file_name}")

# # Debug loop to check file reading
# for file_name in os.listdir(verb_annotation_path):
#     if file_name.endswith('.txt'):
#         debug_process_verb_file(file_name)

def process_annotation_file(file_path):
    continuous_sequences = []  # List to hold sequences: (verb_id, start_frame, sequence_length)
    with open(file_path, 'r') as file:
        last_frame_verbs = {}  # Dictionary to track the last frame where each verb was active
        for line in file:
            frame_index, *verbs = map(int, line.strip().split(','))
            for i, verb in enumerate(verbs):
                if verb:  # Verb is present in this frame
                    if i not in last_frame_verbs:  # Start of a new sequence for this verb
                        last_frame_verbs[i] = [frame_index, frame_index]  # [start_frame, last_frame]
                    else:
                        last_frame_verbs[i][1] = frame_index  # Update last frame for this verb
                else:  # Verb is not present in this frame
                    if i in last_frame_verbs:  # End of a sequence for this verb
                        # Record the sequence: verb_id, start_frame, sequence_length
                        continuous_sequences.append((i, last_frame_verbs[i][0], last_frame_verbs[i][1] - last_frame_verbs[i][0] + 1))
                        del last_frame_verbs[i]  # Remove verb from tracking

        # Check for any sequences that continue till the last frame processed
        for i, frames in last_frame_verbs.items():
            continuous_sequences.append((i, frames[0], frames[1] - frames[0] + 1))

    return continuous_sequences



# Dynamically discover and process annotation files
with open(output_csv_path, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    for file_name in os.listdir(annotation_folder_path):
        if file_name.endswith('.txt'):
            file_path = os.path.join(annotation_folder_path, file_name)
            print(f"Starting to process file: {file_name}")  # Print when a file starts processing
            sequences = process_annotation_file(file_path)
            video_id = file_name.replace('.txt', '')
            video_path = os.path.join(base_video_path, video_id)  # Combine base path with video ID
            for verb_id, start_frame, length in sequences:
                #csv_writer.writerow([video_path, verb_id, start_frame, length])
                csv_writer.writerow([video_path, start_frame, length, verb_id])
            print(f"Finished processing file: {file_name}")  # Print when a file finishes processing

# Dynamically discover and process annotation files
with open(output_csv_path_pretrian, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter= ' ')
    for file_name in os.listdir(annotation_folder_path):
        if file_name.endswith('.txt'):
            file_path = os.path.join(annotation_folder_path, file_name)
            print(f"Starting to process file: {file_name}")  # Print when a file starts processing
            sequences = process_annotation_file(file_path)
            video_id = file_name.replace('.txt', '')
            video_path = os.path.join(base_video_path, video_id)  # Combine base path with video ID
            for verb_id, start_frame, length in sequences:
                #csv_writer.writerow([video_path, verb_id, start_frame, length])
                csv_writer.writerow([video_path, start_frame, length])
            print(f"Finished processing file: {file_name}")  # Print when a file finishes processing

# import pandas as pd
# from sklearn.model_selection import train_test_split


# csv_file_path = 'continuous_verbs.csv'  

# # Load the dataset
# data = pd.read_csv(csv_file_path)

# # Splitting the dataset into train, validation, and test sets
# # Adjust the test_size and random_state as needed
# train, test = train_test_split(data, test_size=0.2, random_state=42)  # 70% training, 30% test
# val, test = train_test_split(test, test_size=0.5, random_state=42)  # Split the 30% into two 15% sets for val and test

# # Specify the paths for the output CSV files
# train_csv_path = 'train.csv'
# val_csv_path = 'val.csv'
# test_csv_path = 'test.csv'

# # Save the splits to new CSV files
# train.to_csv(train_csv_path, index=False)
# val.to_csv(val_csv_path, index=False)
# test.to_csv(test_csv_path, index=False)