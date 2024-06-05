import numpy as np
from PIL import Image, ImageEnhance
import os

import numpy as np

def fourier_sampling(T, C=3, amplitude_range=(0, 1), frequency_range=(0.2, 1.5)):
    """
    Generates a temporal array M for augmentation using Fourier Sampling.

    Parameters:
    - T: Total number of frames.
    - C: Number of sinusoidal basis functions.
    - amplitude_range: Range of amplitudes.
    - frequency_range: Range of frequencies.
    
    Returns:
    - M: Temporal array representing augmentation magnitudes over time.
    """
    M = np.zeros(T)
    for _ in range(C):
        weight = np.random.random()  # Changed to a single weight for each basis.
        frequency = np.random.uniform(*frequency_range)
        amplitude = np.random.uniform(*amplitude_range)
        offset = np.random.uniform(0, 2*np.pi)  # Changed to a phase offset in radians.
        
        # Generating a sinusoidal signal for this basis function
        t = np.arange(T)
        signal = np.sin(2 * np.pi * frequency * t / T + offset)
        
        # Normalizing and scaling the signal
        signal = (signal - np.min(signal)) / (np.max(signal) - np.min(signal))
        signal = signal * amplitude * weight  # Apply weight here.
        
        M += signal  # Add the weighted signal to M.
    
    # Normalize M to the desired range, e.g., [0.5, 1.5] to ensure reasonable augmentation levels.
    M = 0.5 + (M - np.min(M)) / (np.max(M) - np.min(M))
    
    return M


def adjust_brightness(image, enhancement_factor):
    """
    Adjusts the brightness of an image.
    
    Parameters:
    - image: PIL.Image object
    - enhancement_factor: A number specifying the adjustment factor.
    
    Returns:
    - Enhanced image with adjusted brightness.
    """
    enhancer = ImageEnhance.Brightness(image)
    enhanced_image = enhancer.enhance(enhancement_factor)
    return enhanced_image

# # Assuming the frames are stored in a folder named 'video_frames'
# folder_path = '6_action_4460_1631_1636 copy'
# frame_files = sorted(os.listdir(folder_path))  # Ensure the frames are in the correct order

# # Generate the temporal array M for 5 frames
# T = 6  # Total number of frames
# M = fourier_sampling(T)

# # Loop through each frame, adjust brightness, and save the modified frame
# for i, frame_file in enumerate(frame_files):
#     frame_path = os.path.join(folder_path, frame_file)
#     with Image.open(frame_path) as img:
#         # Adjust brightness based on M[i]. Assuming M values between 0.5 and 1.5 for demonstration.
#         modified_img = adjust_brightness(img, 0.5 + M[i])
#         modified_img.save(os.path.join(folder_path, f'modified_{frame_file}'))  # Save modified frame

# print("Brightness adjustment completed for all frames.")

def process_folder(input_folder, output_folder, T):
    for image_name in os.listdir(input_folder):
        image_path = os.path.join(input_folder, image_name)
        with Image.open(image_path) as img:
            M = fourier_sampling(T)
            for i in range(T):
                # Assuming the enhancement factor to be in the range [0.5, 1.5]
                factor = 0.5 + M[i]  # Adjust based on your augmentation needs
                enhanced_img = adjust_brightness(img, factor)
                enhanced_img.save(os.path.join(output_folder, f"{image_name}"))

def process_dataset(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for folder in os.listdir(input_dir):
        input_folder = os.path.join(input_dir, folder)
        output_folder = os.path.join(output_dir, folder)
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        # Assume T is equal to the number of images in the folder
        T = len([name for name in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, name))])
        
        process_folder(input_folder, output_folder, T)

# Paths to your input and output directories
input_dir = '../CholecT45/CholecT45/data_split'
output_dir = '../CholecT45/CholecT45/data_split_aug'

process_dataset(input_dir, output_dir)