import os


def stage_corresponding_files(txt_dir, csv_dir, png_dir):
    """Stages matching .txt, .csv, and .png files based on names.

    Args:
        txt_dir: Path to the directory containing .txt files.
        csv_dir: Path to the directory containing .csv files.
        png_dir: Path to the directory containing .png files.
    """

    for txt_file in os.listdir(txt_dir):
        if txt_file.endswith(".txt"):
            base_name = os.path.splitext(txt_file)[0]  # Remove .txt extension

            txt_path = os.path.join(txt_dir, txt_file)
            csv_path = os.path.join(csv_dir, base_name + ".csv")
            png_path = os.path.join(png_dir, base_name + ".png")

            # Check if corresponding .csv and .png files exist
            if os.path.exists(csv_path) and os.path.exists(png_path):
                os.system(f"git add {txt_path} {csv_path} {png_path}")
            else:
                print(f"Warning: Corresponding files not found for {txt_file}")


# Example usage (replace with your actual directory paths)
stage_corresponding_files("txt", "csv", "png")
