import os
from collections import Counter

directory_path = '../CholecT45/CholecT45/data_split'

# Ensuring we're only looking at directories
folders = [name for name in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, name))]

# Count the total number of folders
total_folders = len(folders)

# Initialize a counter for folders starting with each digit
digit_counter = Counter(folder[0] for folder in folders if folder[0].isdigit())

# Print the total number of folders
print(f"Total folders: {total_folders}")

# Print the count of folders for each initial digit
for digit in range(10):
    print(f"Folders starting with {digit}: {digit_counter[str(digit)]}")