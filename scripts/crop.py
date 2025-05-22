from PIL import Image
import os

# --- Configuration ---
INPUT_FOLDER = "new_images"  # Folder containing your original BMP images
OUTPUT_FOLDER = "cropped_images" # Folder where cropped JPG images will be saved
# Define the crop rectangle: (left, upper, right, lower)
# These are pixel coordinates.
CROP_RECTANGLE = (755, 345, 940, 625)  # (left, upper, right, lower) Example
JPEG_QUALITY = 90  # Quality for JPEG saving (0-100, higher is better quality but larger file)
# 185 x 280
# 755 x 345

# --- Script Logic ---

def crop_images_in_folder(input_dir, output_dir, crop_box, jpeg_quality):
    """
    Iterates over BMP images in input_dir, crops them using crop_box,
    converts them to JPG, and saves them to output_dir.
    """
    if not os.path.exists(input_dir):
        print(f"Error: Input folder '{input_dir}' does not exist.")
        return

    if not os.path.exists(output_dir):
        print(f"Creating output folder: '{output_dir}'")
        os.makedirs(output_dir)

    # Validate crop box (basic check)
    if not (len(crop_box) == 4 and
            crop_box[0] < crop_box[2] and  # left < right
            crop_box[1] < crop_box[3] and  # upper < lower
            crop_box[0] >= 0 and crop_box[1] >= 0):
        print(f"Error: Invalid CROP_RECTANGLE: {crop_box}. Ensure left < right, upper < lower, and coordinates are non-negative.")
        return

    if not (0 <= jpeg_quality <= 100):
        print(f"Error: Invalid JPEG_QUALITY: {jpeg_quality}. Must be between 0 and 100.")
        return


    print(f"Starting image cropping and conversion...")
    print(f"Input folder: {input_dir} (Expecting BMP files)")
    print(f"Output folder: {output_dir} (Saving as JPG files)")
    print(f"Crop rectangle (L, U, R, L): {crop_box}")
    print(f"JPEG Quality: {jpeg_quality}")
    print("-" * 30)

    processed_count = 0
    error_count = 0

    for filename in os.listdir(input_dir):
        if filename.lower().endswith(".bmp"):
            input_path = os.path.join(input_dir, filename)
            
            # Create output filename with .jpg extension
            base_filename, _ = os.path.splitext(filename)
            output_filename = f"{base_filename}.jpg"
            output_path = os.path.join(output_dir, output_filename)

            try:
                with Image.open(input_path) as img:
                    # Ensure the crop box is within the image dimensions
                    img_width, img_height = img.size
                    actual_crop_box = (
                        max(0, crop_box[0]),
                        max(0, crop_box[1]),
                        min(img_width, crop_box[2]),
                        min(img_height, crop_box[3])
                    )

                    if actual_crop_box[0] >= actual_crop_box[2] or actual_crop_box[1] >= actual_crop_box[3]:
                        print(f"Skipping '{filename}': Crop box is outside or results in zero-size image.")
                        error_count += 1
                        continue
                    
                    if actual_crop_box != crop_box:
                         print(f"Warning for '{filename}': Original crop box {crop_box} was adjusted to {actual_crop_box} to fit image dimensions ({img_width}x{img_height}).")

                    cropped_img = img.crop(actual_crop_box)

                    # Convert to RGB before saving as JPEG
                    # This handles various modes (like P, LA, RGBA) and removes alpha channel
                    if cropped_img.mode != 'RGB':
                        print(f"Info: Converting '{filename}' from mode '{cropped_img.mode}' to 'RGB' for JPEG saving.")
                        cropped_img = cropped_img.convert("RGB")
                    
                    cropped_img.save(output_path, "JPEG", quality=jpeg_quality)
                    print(f"Successfully cropped and converted '{filename}' -> '{output_filename}'")
                    processed_count += 1

            except FileNotFoundError:
                print(f"Error: File not found '{input_path}' (should not happen if os.listdir worked).")
                error_count += 1
            except Exception as e:
                print(f"Error processing '{filename}': {e}")
                error_count += 1
        else:
            # Only print if it's not a hidden file or directory
            if not filename.startswith('.'):
                print(f"Skipping non-BMP file: '{filename}'")


    print("-" * 30)
    print(f"Processing complete.")
    print(f"Successfully processed: {processed_count} images.")
    print(f"Errors/Skipped: {error_count} images.")

if __name__ == "__main__":
    # --- Run the script ---
    crop_images_in_folder(INPUT_FOLDER, OUTPUT_FOLDER, CROP_RECTANGLE, JPEG_QUALITY)
