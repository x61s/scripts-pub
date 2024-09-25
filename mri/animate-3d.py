import os
import cv2
import pydicom
import numpy as np

def load_dicom_images_from_folder(folder_path):
    """Load all DICOM files from a folder and return the image slices as a 3D numpy array (volume)."""
    dicom_slices = []
    for filename in sorted(os.listdir(folder_path)):
        dicom_path = os.path.join(folder_path, filename)
        ds = pydicom.dcmread(dicom_path)
        image = ds.pixel_array
        dicom_slices.append(image)
    return np.array(dicom_slices)

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
        # Normalize the slice to 8-bit (0-255)
        normalized_slice = cv2.normalize(slice, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
        video_writer.write(normalized_slice)

    video_writer.release()
    print(f"Video saved to {output_file}")

def get_axial_view(volume):
    """Return slices in the axial view (top-down view)."""
    return volume

def get_sagittal_view(volume):
    """Return slices in the sagittal view (side view)."""
    return np.transpose(volume, (2, 0, 1))  # Transpose to slice along a different axis

def get_coronal_view(volume):
    """Return slices in the coronal view (front view)."""
    return np.transpose(volume, (1, 0, 2))  # Transpose to slice along a different axis

if __name__ == "__main__":
    # Specify the folder containing the DICOM files
    dicom_folder = "../69571325/"

    # Load DICOM slices as a 3D volume (numpy array)
    volume = load_dicom_images_from_folder(dicom_folder)

    # Generate axial view (default view: top to bottom)
    axial_slices = get_axial_view(volume)
    create_video_from_slices(axial_slices, "axial_view.mp4", fps=10)

    # Generate sagittal view (side view)
    sagittal_slices = get_sagittal_view(volume)
    create_video_from_slices(sagittal_slices, "sagittal_view.mp4", fps=10)

    # Generate coronal view (front view)
    coronal_slices = get_coronal_view(volume)
    create_video_from_slices(coronal_slices, "coronal_view.mp4", fps=10)

