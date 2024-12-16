import os
from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime

def get_exif_date_taken(image_path):
    """Retrieve the date the photo was taken from the image's EXIF metadata."""
    try:
        image = Image.open(image_path)
        exif_data = image._getexif()
        if exif_data:
            for tag, value in exif_data.items():
                tag_name = TAGS.get(tag, tag)
                if tag_name == "DateTimeOriginal":
                    return value
    except Exception as e:
        print(f"Error reading EXIF data from {image_path}: {e}")
    return None

def format_date(exif_date):
    """Convert EXIF date format to yyyymmdd_hhmmss."""
    try:
        date_obj = datetime.strptime(exif_date, "%Y:%m:%d %H:%M:%S")
        return date_obj.strftime("%Y%m%d_%H%M%S")
    except ValueError as e:
        print(f"Error parsing date: {e}")
        return None

def rename_images_in_folder(folder_path):
    """Iterate through a folder and rename JPEG files based on their EXIF date."""
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.jpg', '.jpeg')):
            full_path = os.path.join(folder_path, filename)
            exif_date = get_exif_date_taken(full_path)

            if exif_date:
                formatted_date = format_date(exif_date)
                if formatted_date:
                    new_filename = f"{formatted_date}.jpg"
                    new_full_path = os.path.join(folder_path, new_filename)

                    if not os.path.exists(new_full_path):
                        os.rename(full_path, new_full_path)
                        print(f"Renamed {filename} to {new_filename}")
                    else:
                        print(f"Skipped {filename}: {new_filename} already exists.")
                else:
                    print(f"Skipped {filename}: Could not format EXIF date.")
            else:
                print(f"Skipped {filename}: No EXIF date found.")

# Set the path to the folder containing your photos
folder_path = "path/to/your/folder"
rename_images_in_folder(folder_path)
