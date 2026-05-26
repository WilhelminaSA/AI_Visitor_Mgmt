import os
import time
import cv2
import warnings
import numpy as np

warnings.filterwarnings("ignore", category=FutureWarning)

from services.embedding_service import (
    get_multiple_face_embeddings
)

from database.person_repository import (
    get_registered_persons
)

from config.settings import (
    MONITORING_INTERVAL
)

# ======================================================

TEMP_CAPTURE_DIR = r"C:\my_work\aiv22\temp_monitoring"

SIMILARITY_THRESHOLD = 0.65

# ======================================================

if not os.path.exists(TEMP_CAPTURE_DIR):

    os.makedirs(TEMP_CAPTURE_DIR)

# ======================================================

monitoring_active = False

# ======================================================

def cosine_similarity(vec1, vec2):

    vec1 = np.array(vec1)

    vec2 = np.array(vec2)

    dot = np.dot(vec1, vec2)

    norm1 = np.linalg.norm(vec1)

    norm2 = np.linalg.norm(vec2)

    if norm1 == 0 or norm2 == 0:

        return 0.0

    return float(dot / (norm1 * norm2))

# ======================================================

def capture_camera_image():

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():

        print("\nUnable to access camera")

        return None

    success, frame = camera.read()

    camera.release()

    if not success:

        print("\nFailed to capture image")

        return None

    timestamp = int(time.time())

    image_path = os.path.join(
        TEMP_CAPTURE_DIR,
        f"capture_{timestamp}.jpg"
    )

    cv2.imwrite(image_path, frame)

    return image_path

# ======================================================

def process_image(image_path):

    print("\n" + "=" * 60)

    print(f"Processing: {image_path}")

    detected_faces = get_multiple_face_embeddings(
        image_path
    )

    if not detected_faces:

        print("No valid faces found")

        return

    print(f"\nDetected Faces: {len(detected_faces)}")

    registered_persons = get_registered_persons()

    for index, detected_embedding in enumerate(detected_faces):

        best_similarity = -1

        best_person = None

        second_best = None

        second_best_score = -1

        # ==================================================

        for person in registered_persons:

            stored_embedding = person["face_embedding"]

            if stored_embedding is None:

                continue

            similarity = cosine_similarity(
                detected_embedding,
                stored_embedding
            )

            # ==============================================

            if similarity > best_similarity:

                second_best = best_person

                second_best_score = best_similarity

                best_similarity = similarity

                best_person = person

        # ==================================================

        print("\n----------------------------------------")

        print(f"FACE #{index + 1}")

        # ==================================================
        # MATCH FOUND
        # ==================================================

        if (
            best_person
            and
            best_similarity >= SIMILARITY_THRESHOLD
        ):

            print("MATCH FOUND")

            print(
                f"Person ID: {best_person['person_id']}"
            )

            print(
                f"Name: {best_person['full_name']}"
            )

            print(
                f"Similarity: {round(best_similarity, 4)}"
            )

            print("Matched Registered Image:")

            print(
                best_person["image_path"]
            )

        # ==================================================
        # UNKNOWN
        # ==================================================

        else:

            print("UNKNOWN PERSON")

            if best_person:

                print("\nNearest Match Suggestion:")

                print(
                    f"Name: {best_person['full_name']}"
                )

                print(
                    f"Similarity: {round(best_similarity, 4)}"
                )

                print(
                    best_person["image_path"]
                )

                if second_best:

                    print("\nSecond Best:")

                    print(
                        f"Name: {second_best['full_name']}"
                    )

                    print(
                        f"Similarity: {round(second_best_score, 4)}"
                    )

# ======================================================

def start_monitoring():

    global monitoring_active

    monitoring_active = True

    print("\nMonitoring Started")

    print(
        f"\nCapturing image every {MONITORING_INTERVAL} seconds"
    )

    print(
        "\nPress STOP option in menu to end monitoring.\n"
    )

    # ==================================================

    while monitoring_active:

        try:

            image_path = capture_camera_image()

            print(
                f"monitoring: captured image path: {image_path}\n"
            )

            if image_path:

                process_image(image_path)

            # ==============================================

            for _ in range(MONITORING_INTERVAL):

                if not monitoring_active:

                    break

                time.sleep(1)

        except Exception as error:

            print("\nMonitoring Error:")

            print(error)

            time.sleep(5)

# ======================================================

def stop_monitoring():

    global monitoring_active

    monitoring_active = False

    print("\nMonitoring Stopped Successfully.\n")