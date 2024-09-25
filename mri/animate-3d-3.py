import os
import cv2
import pydicom
import numpy as np

def load_dicom_images_from_folder(folder_path):
    """Load all DICOM files from a folder and return the image slices as a 3D numpy array (volume)
       and the spacing information for correct proportions."""
    dicom_slices = []
    pixel_spacing = None
    slice_thickness = None

    for filename in sorted(os.listdir(folder_path)):
        dicom_path = os.path.join(folder_path, filename)
        ds = pydicom.dcmread(dicom_path)
        
        # Get pixel spacing and slice thickness from the DICOM metadata
        if pixel_spacing is None:
            pixel_spacing = ds.PixelSpacing  # [row spacing, column spacing]
        if slice_thickness is None:
            slice_thickness = ds.SliceThickness

        # Extract image and append to the list of slices
        image = ds.pixel_array
        dicom_slices.append(image)
    
    # Convert list of slices to a 3D numpy array (volume)
    volume = np.array(dicom_slices)
    return volume, pixel_spacing, slice_thickness

def resize_slices(slices, scale_x, scale_y):
    """Resize the 2D slices based on the scaling factors for correct proportions."""
    resized_slices = []
    for slice in slices:
        resized = cv2.resize(slice, (0, 0), fx=scale_x, fy=scale_y, interpolation=cv2.INTER_LINEAR)
        resized_slices.append(resized)
    return resized_slices

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

def get_sagittal_view(volume, pixel_spacing, slice_thickness):
    """Return slices in the sagittal view (side view) and rotate 270 degrees (90 degrees counterclockwise)."""
    sagittal_slices = np.transpose(volume, (2, 0, 1))  # Transpose to slice along the sagittal axis
    scale_x = pixel_spacing[0] / slice_thickness  # Adjust x-axis (columns) based on slice thickness
    resized_slices = resize_slices(sagittal_slices, scale_x=scale_x, scale_y=1)

    # Rotate each slice by 270 degrees (90 degrees counter-clockwise)
    rotated_slices = [cv2.rotate(slice, cv2.ROTATE_90_CLOCKWISE) for slice in resized_slices]
    return rotated_slices

def get_coronal_view(volume, pixel_spacing, slice_thickness):
    """Return slices in the coronal view (front view) and invert vertically."""
    coronal_slices = np.transpose(volume, (1, 0, 2))  # Transpose to slice along the coronal axis
    scale_x = pixel_spacing[0] / slice_thickness  # Adjust x-axis (columns) based on slice thickness
    resized_slices = resize_slices(coronal_slices, scale_x=scale_x, scale_y=1)

    # Flip each slice vertically
    flipped_slices = [cv2.flip(slice, 0) for slice in resized_slices]
    return flipped_slices

if __name__ == "__main__":
    # Specify the folder containing the DICOM files
    dicom_folder = "../69571325/"

    # Load DICOM slices as a 3D volume (numpy array) and retrieve spacing information
    volume, pixel_spacing, slice_thickness = load_dicom_images_from_folder(dicom_folder)

    # Generate axial view (default view: top to bottom)
    axial_slices = get_axial_view(volume)
    create_video_from_slices(axial_slices, "axial_view.mp4", fps=10)

    # Generate sagittal view (side view) with correct proportions and 270-degree rotation
    sagittal_slices = get_sagittal_view(volume, pixel_spacing, slice_thickness)
    create_video_from_slices(sagittal_slices, "sagittal_view.mp4", fps=10)

    # Generate coronal view (front view) with correct proportions and vertical flip
    coronal_slices = get_coronal_view(volume, pixel_spacing, slice_thickness)
    create_video_from_slices(coronal_slices, "coronal_view.mp4", fps=10)

