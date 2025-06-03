import os

# --- Configuration ---
TARGET_FOLDER = "skin"
MIN_FILENAME_LENGTH = 4 # The desired minimum length for the numeric part (e.g., 4 for 0001)
# --- End Configuration ---

def pad_numeric_filenames_direct(folder_path, min_length):
    """
    Directly renames .skin and .hskin files in the folder so that their numeric
    filename part (before the extension) is at least min_length characters long,
    padded with leading zeros.
    e.g., 1.skin -> 0001.skin, 12.hskin -> 0012.hskin
    """
    if not os.path.isdir(folder_path):
        print(f"Error: Folder '{folder_path}' not found. Please check TARGET_FOLDER setting.")
        return

    print(f"Processing folder: {folder_path}")
    print(f"Padding numeric part of .skin/.hskin filenames to at least {min_length} digits.")
    print("-" * 30)

    renamed_count = 0
    skipped_count = 0
    error_count = 0
    already_padded_count = 0

    allowed_extensions = {".jpg", ".skin", ".hskin"}

    # Iterate directly, but be mindful if new names could match old names in subsequent iterations
    # For this specific operation (padding), it's generally safe as "1.skin" -> "0001.skin"
    # won't match "1.skin" again if "0001.skin" was processed first.
    # Sorting can make the order predictable but isn't strictly needed for correctness here.
    filenames = os.listdir(folder_path)
    filenames.sort() # Optional: for consistent processing order

    for filename in filenames:
        original_full_path = os.path.join(folder_path, filename)

        if not os.path.isfile(original_full_path):
            continue # Skip directories

        name_part, ext_part = os.path.splitext(filename)
        ext_lower = ext_part.lower()

        if ext_lower not in allowed_extensions:
            continue

        if not name_part.isdigit():
            print(f"Skipping '{filename}': Name part '{name_part}' is not purely numeric.")
            skipped_count += 1
            continue

        if len(name_part) >= min_length:
            already_padded_count +=1
            continue

        padded_name_part = name_part.zfill(min_length)
        new_filename = f"{padded_name_part}{ext_part}"
        new_full_path = os.path.join(folder_path, new_filename)

        if os.path.exists(new_full_path):
            # This could happen if "0001.skin" already exists and we are trying to pad "1.skin"
            # Or if the script is run multiple times by mistake on already partially padded files.
            # For this specific task, if new_full_path is the same as original_full_path,
            # it's already caught by len(name_part) >= min_length.
            # So this primarily catches conflicts with *other* pre-existing files.
            print(f"Warning: Target '{new_filename}' already exists. Skipping rename of '{filename}'.")
            skipped_count += 1
            continue

        try:
            os.rename(original_full_path, new_full_path)
            print(f"Renamed: '{filename}' -> '{new_filename}'")
            renamed_count += 1
        except Exception as e:
            print(f"Error renaming '{filename}' to '{new_filename}': {e}")
            error_count += 1

    print("-" * 30)
    print(f"Renaming process complete.")
    print(f"Successfully renamed: {renamed_count} files.")
    print(f"Already met length criteria: {already_padded_count} files.")
    print(f"Skipped (non-numeric, target exists, etc.): {skipped_count} files.")
    if error_count > 0:
        print(f"Errors encountered: {error_count} files.")

if __name__ == "__main__":
    if TARGET_FOLDER == "your_folder_path_here":
        print("Error: Please set the TARGET_FOLDER variable in the script before running.")
    else:
        pad_numeric_filenames_direct(TARGET_FOLDER, MIN_FILENAME_LENGTH)
