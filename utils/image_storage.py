import os
import shutil

# ======================================================
# STRICT DIRECTORY RULES
# ======================================================

INPUT_IMAGE_DIR = r"C:\my_work\aiv22\Images"
OUTPUT_DIR = r"C:\my_work\aiv22\data\registered_persons"


def ensure_dir_exists():
    """Ensure output folder exists"""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)


def get_next_image_number():
    """
    Get next incremental number from OUTPUT_DIR
    Format: img_001_name.jpg
    """

    ensure_dir_exists()

    existing_files = os.listdir(OUTPUT_DIR)

    max_num = 0

    for file in existing_files:
        try:
            if not file.startswith("img_"):
                continue

            parts = file.split("_")
            num = int(parts[1])

            if num > max_num:
                max_num = num

        except:
            continue

    return max_num + 1


def sanitize_name(name):
    """Make name safe for filename"""
    return name.strip().lower().replace(" ", "_")


def save_registered_person_image(source_image_path, full_name):
    """
    Save image in format:
    img_001_baseName.jpg
    """

    ensure_dir_exists()

    # ==================================================
    # FORCE INPUT ONLY FROM ALLOWED FOLDER
    # ==================================================

    if not source_image_path.startswith(INPUT_IMAGE_DIR):
        print("\n[ERROR] Invalid image source!")
        print("You can only use images from:")
        print(INPUT_IMAGE_DIR)
        return None

    img_num = get_next_image_number()
    base_name = sanitize_name(full_name)

    filename = f"img_{img_num:03d}_{base_name}.jpg"
    destination_path = os.path.join(OUTPUT_DIR, filename)

    try:
        shutil.copy(source_image_path, destination_path)

        print(f"\nImage saved successfully:")
        print(destination_path)

        return destination_path

    except Exception as e:
        print("\n[ERROR] Failed to save image:")
        print(e)
        return None