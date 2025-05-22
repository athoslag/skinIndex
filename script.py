import os

# --- Configuration ---
TARGET_FOLDER = "cropped_images"
INCREMENT_VALUE = 1
ALLOWED_EXTENSIONS = {".jpg"} # Add or remove as needed
# --- End Configuration ---

def rename_images_descending(folder_path, increment_by):
    """
    Renames image files in a folder by adding an increment_value to their
    numeric filename, processing from highest to lowest to avoid conflicts.
    Example: 0.png -> 1.png, 1.png -> 2.png (if increment_by is 1)
    """
    if not os.path.isdir(folder_path):
        print(f"Error: Folder '{folder_path}' not found. Please check TARGET_FOLDER setting.")
        return

    print(f"Processing folder: {folder_path}")
    print(f"Incrementing numeric filenames by: {increment_by}")
    print(f"Processing in descending order of current numeric value.")
    print("-" * 30)

    files_to_rename = []

    # 1. Collect and parse image files
    for filename in os.listdir(folder_path):
        original_full_path = os.path.join(folder_path, filename)
        if not os.path.isfile(original_full_path):
            continue

        name_part, ext_part = os.path.splitext(filename)
        ext_lower = ext_part.lower()

        if ext_lower not in ALLOWED_EXTENSIONS:
            continue

        try:
            current_number = int(name_part)
            files_to_rename.append({
                "original_filename": filename,
                "current_number": current_number,
                "extension": ext_part, # Preserve original case of extension
                "original_name_part_len": len(name_part) # To optionally preserve leading zeros
            })
        except ValueError:
            print(f"Skipping '{filename}': Name part '{name_part}' is not purely numeric.")
            continue

    if not files_to_rename:
        print("No suitable image files found to rename.")
        return

    # 2. Sort files by current_number in descending order
    files_to_rename.sort(key=lambda x: x["current_number"], reverse=True)

    renamed_count = 0
    error_count = 0

    # 3. Rename files from highest current number to lowest
    for file_info in files_to_rename:
        old_filename = file_info["original_filename"]
        old_full_path = os.path.join(folder_path, old_filename)

        new_number = file_info["current_number"] + increment_by
        
        # Decide if you want to preserve leading zeros.
        # If 0.png becomes 1.png, but 00.png should become 01.png, use zfill.
        # For the simple example "0.png -> 1.png", direct string conversion is fine.
        # If you want to keep the same number of digits as the original (e.g. 09 -> 10, not 9 -> 10)
        # you can use zfill with the original length.
        # For example `0.png` -> `1.png`, `9.png` -> `10.png`.
        # If `00.png` -> `01.png`, use:
        # new_name_part = str(new_number).zfill(file_info["original_name_part_len"])
        # For the basic request, direct string conversion is simpler:
        new_name_part = str(new_number)

        new_filename = f"{new_name_part}{file_info['extension']}"
        new_full_path = os.path.join(folder_path, new_filename)

        if old_full_path == new_full_path:
            print(f"Skipping '{old_filename}': New name is identical (increment might be 0 or name structure unexpected).")
            continue

        # This check is mostly a safeguard; descending sort should prevent overwriting
        # files that are *also* part of this renaming batch.
        if os.path.exists(new_full_path):
            print(f"Warning: Target '{new_filename}' already exists. Skipping rename of '{old_filename}'.")
            error_count +=1 # Count as an error/skip due to conflict
            continue

        try:
            os.rename(old_full_path, new_full_path)
            print(f"Renamed: '{old_filename}' -> '{new_filename}'")
            renamed_count += 1
        except Exception as e:
            print(f"Error renaming '{old_filename}' to '{new_filename}': {e}")
            error_count += 1

    print("-" * 30)
    print(f"Renaming process complete.")
    print(f"Successfully renamed: {renamed_count} files.")
    if error_count > 0:
        print(f"Skipped or errors: {error_count} files.")

if __name__ == "__main__":
    if TARGET_FOLDER == "your_image_folder_path_here" or not TARGET_FOLDER:
        print("Error: Please set the TARGET_FOLDER variable in the script before running.")
    else:
        rename_images_descending(TARGET_FOLDER, INCREMENT_VALUE)
