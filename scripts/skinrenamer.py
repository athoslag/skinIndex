import os
import shutil # Not strictly needed for rename, but good for other file ops

def sort_and_rename_files_combined(folder_path, dry_run=True):
    """
    Sorts all .skin and .hskin files in the given folder together and renames
    them sequentially (e.g., 1.skin, 2.hskin, 3.skin, ...), preserving original extensions.
    """
    if not os.path.isdir(folder_path):
        print(f"Error: Folder '{folder_path}' not found.")
        return

    print(f"Processing folder: {folder_path}")
    if dry_run:
        print("--- DRY RUN MODE --- (No files will actually be renamed)")
    else:
        print("--- LIVE MODE --- (Files WILL be renamed)")
    print("-" * 30)

    all_target_files = []
    allowed_extensions = {".skin", ".hskin"}

    # 1. Collect all .skin and .hskin files into a single list
    for filename in os.listdir(folder_path):
        full_path = os.path.join(folder_path, filename)
        if os.path.isfile(full_path):
            _ , ext = os.path.splitext(filename) # Get extension
            if ext.lower() in allowed_extensions:
                all_target_files.append(filename)

    if not all_target_files:
        print("No .skin or .hskin files found in the folder.")
        return

    # 2. Sort the combined list of files alphabetically
    all_target_files.sort()
    print(f"Found {len(all_target_files)} total .skin/.hskin files to process.")
    # for f in all_target_files: print(f"  - {f}") # Optional: print sorted list

    rename_operations = [] # List to store (old_path, temp_path, final_path)
    temp_suffix = "__temp_rename__"

    # 3. Plan renames for the combined sorted list: original -> temporary -> final
    for i, old_filename in enumerate(all_target_files):
        counter = i + 1 # Start numbering from 1
        original_base, original_ext = os.path.splitext(old_filename)
        old_path = os.path.join(folder_path, old_filename)

        # Temporary filename: original_base + temp_suffix + original_ext
        temp_filename = f"{original_base}{temp_suffix}{original_ext}"
        temp_path = os.path.join(folder_path, temp_filename)

        # Final filename: counter + original_ext
        final_filename = f"{counter}{original_ext}"
        final_path = os.path.join(folder_path, final_filename)

        rename_operations.append({
            "original_name": old_filename,
            "old_path": old_path,
            "temp_path": temp_path,
            "final_path": final_path,
            "final_name": final_filename
        })

    # --- Stage 1: Rename original files to temporary names ---
    print("\n--- Stage 1: Renaming to temporary names ---")
    successful_temp_renames = [] # List of (temp_path, old_path) for potential revert
    for op in rename_operations:
        if not os.path.exists(op["old_path"]):
            print(f"Warning: Original file '{op['old_path']}' seems to have disappeared. Skipping.")
            continue

        if os.path.exists(op["temp_path"]) and op["temp_path"] != op["old_path"]:
            is_another_original_target = any(
                other_op["old_path"] == op["temp_path"]
                for other_op in rename_operations if other_op["old_path"] != op["old_path"]
            )
            if is_another_original_target:
                print(f"CRITICAL ERROR: Temporary name '{op['temp_path']}' for '{op['original_name']}' conflicts with another file targeted for rename. Aborting to prevent data loss.")
                if not dry_run:
                    print("Attempting to revert Stage 1 renames...")
                    for R_temp_path, R_old_path in successful_temp_renames:
                        try:
                            os.rename(R_temp_path, R_old_path)
                            print(f"Reverted: '{os.path.basename(R_temp_path)}' -> '{os.path.basename(R_old_path)}'")
                        except Exception as e_revert:
                            print(f"Error reverting '{os.path.basename(R_temp_path)}': {e_revert}")
                return

        print(f"Plan (Stage 1): '{op['original_name']}' -> '{os.path.basename(op['temp_path'])}'")
        if not dry_run:
            try:
                os.rename(op["old_path"], op["temp_path"])
                successful_temp_renames.append((op["temp_path"], op["old_path"]))
            except Exception as e:
                print(f"Error renaming '{op['old_path']}' to '{op['temp_path']}': {e}")
                print("Attempting to revert Stage 1 renames due to error...")
                for R_temp_path, R_old_path in successful_temp_renames:
                    try:
                        os.rename(R_temp_path, R_old_path)
                        print(f"Reverted: '{os.path.basename(R_temp_path)}' -> '{os.path.basename(R_old_path)}'")
                    except Exception as e_revert:
                        print(f"Error reverting '{os.path.basename(R_temp_path)}': {e_revert}")
                return # Stop processing

    # --- Stage 2: Rename temporary files to final names ---
    print("\n--- Stage 2: Renaming temporary names to final names ---")
    for op in rename_operations:
        if not os.path.exists(op["temp_path"]):
            # This means either original didn't exist or stage 1 failed for this specific file
            # (if stage 1 had a global fail, we would have returned)
            print(f"Info: Temporary file '{os.path.basename(op['temp_path'])}' (for original '{op['original_name']}') not found. Skipping Stage 2 for this file.")
            continue

        if os.path.exists(op["final_path"]) and op["final_path"] != op["temp_path"]:
            print(f"Warning: Final target '{op['final_name']}' already exists and is not the temp file for '{op['original_name']}'. Skipping rename of '{os.path.basename(op['temp_path'])}'. Manual check needed.")
            continue

        print(f"Plan (Stage 2): '{os.path.basename(op['temp_path'])}' -> '{op['final_name']}'")
        if not dry_run:
            try:
                os.rename(op["temp_path"], op["final_path"])
            except Exception as e:
                print(f"Error renaming '{op['temp_path']}' to '{op['final_path']}': {e}")
                # File is left with its temporary name.

    print("-" * 30)
    if dry_run:
        print("Dry run finished. No files were changed.")
    else:
        print("Renaming process complete.")
        # Check for leftover temporary files
        any_temp_left = False
        for item in os.listdir(folder_path):
            if temp_suffix in item and (item.endswith(".skin") or item.endswith(".hskin")):
                print(f"Warning: Temporary file '{item}' may still exist in the folder.")
                any_temp_left = True
        if not any_temp_left and successful_temp_renames: # Check if any successful renames happened
             print("All processed temporary files seem to have been renamed to final names.")
        elif not successful_temp_renames and not any_temp_left:
             print("No files were actually renamed in Stage 1 (e.g. all skipped or empty list).")


if __name__ == "__main__":
    target_folder = input("Enter the path to the folder: ")

    # --- IMPORTANT ---
    # Set DRY_RUN to False to actually rename files.
    # It's highly recommended to run with DRY_RUN = True first!
    # --- ----------- ---
    is_dry_run = True
    # is_dry_run = False # UNCOMMENT THIS LINE TO PERFORM ACTUAL RENAMING

    confirm_action = ""
    if not is_dry_run:
        confirm_action = input(f"You are about to RENAME files in '{target_folder}'. This is NOT a dry run. Type 'YES' to proceed: ")

    if is_dry_run:
        print("Running in DRY RUN mode.")
        sort_and_rename_files_combined(target_folder, dry_run=True)
    elif confirm_action == "YES":
        print("Running in LIVE mode.")
        sort_and_rename_files_combined(target_folder, dry_run=False)
    else:
        print("Operation cancelled by user or invalid confirmation.")
