import os

import pandas as pd
from PIL import Image


def filter_entities(data, entity_list):
    if not entity_list:
        return data
    return data[data["Entity"].isin(entity_list)]


def process_csv(
    file_name, entity_list, source_directory="plain_csv", destination_directory="csv"
):
    file_path = os.path.join(source_directory, file_name)
    data = pd.read_csv(file_path)

    filtered_data = filter_entities(data, entity_list)
    destination_file_path = os.path.join(destination_directory, file_name)

    os.makedirs(destination_directory, exist_ok=True)
    filtered_data.to_csv(destination_file_path, index=False)


def process_png(file_name, source_directory="plain_png", destination_directory="png"):
    max_width = 1000
    max_height = 1000

    source_path = os.path.join(source_directory, file_name)
    destination_path = os.path.join(destination_directory, file_name)

    try:
        with Image.open(source_path) as img:
            width, height = img.size

            if width > max_width or height > max_height:
                # Calculate aspect ratio and new sizes
                aspect_ratio = width / height
                if width > max_width:
                    new_width = max_width
                    new_height = round(new_width / aspect_ratio)
                else:
                    new_height = max_height
                    new_width = round(new_height * aspect_ratio)

                # Resize the image
                img = img.resize((new_width, new_height), Image.LANCZOS)

            # Save the compressed image (adjust quality if needed)
            os.makedirs(destination_directory, exist_ok=True)
            img.save(destination_path, optimize=True, quality=90)

    except OSError:
        print(f"Error processing image: {file_name}")
