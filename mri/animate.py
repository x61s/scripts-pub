import os
import cv2
import pydicom
import numpy as np

def load_dicom_images_from_folder(folder_path):
    """Load all DICOM files from a folder and return the image slices as a list."""
    print(f"Loading DICOM files...")
    dicom_slices = []
    for filename in sorted(os.listdir(folder_path)):
        dicom_path = os.path.join(folder_path, filename)
        ds = pydicom.dcmread(dicom_path)
        # Assuming the image is grayscale
        image = ds.pixel_array
        # Normalize the image to the 8-bit range (0-255) if necessary
        image = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
        dicom_slices.append(image)
    return dicom_slices

def create_video_from_slices(slices, output_file, fps=10):
    """Create a video from a list of image slices."""
    if len(slices) == 0:
        print("No slices found to create a video.")
        return

    # Get dimensions of the first slice to set the video size
    height, width = slices[0].shape

    # Initialize video writer with filename, codec, fps, and frame size
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # For .mp4 files
    video_writer = cv2.VideoWriter(output_file, fourcc, fps, (width, height), isColor=False)

    for slice in slices:
        # Write each slice as a frame in the video
        video_writer.write(slice)

    video_writer.release()
    print(f"Video saved to {output_file}")

if __name__ == "__main__":
    # Specify the folder containing the DICOM files
    dicom_folder = "../69571325/"

    # Load DICOM slices from the folder
    slices = load_dicom_images_from_folder(dicom_folder)

    # Specify output video file path
    output_video_path = "output_video.mp4"

    # Create video from slices
    create_video_from_slices(slices, output_video_path, fps=10)

