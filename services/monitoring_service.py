import os
import time
import warnings
import numpy as np

warnings.filterwarnings("ignore", category=FutureWarning)

from services.embedding_service import (
    get_multiple_face_embeddings
)

from database.person_repository import (
    get_registered_persons
)

# ======================================================

MONITORING_FOLDER = r"C:\my_work\aiv22\Images"
SIMILARITY_THRESHOLD = 0.65

processed_files = set()

# 🔴 CONTROL FLAG (NEW)
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

def process_image(image_path):

    print("\n" + "=" * 60)
    print(f"Processing: {image_path}")

    detected_faces = get_multiple_face_embeddings(image_path)

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

        for person in registered_persons:

            stored_embedding = person["face_embedding"]

            similarity = cosine_similarity(
                detected_embedding,
                stored_embedding
            )

            # track best
            if similarity > best_similarity:
                second_best = best_person
                second_best_score = best_similarity

                best_similarity = similarity
                best_person = person

        print("\n----------------------------------------")
        print(f"FACE #{index + 1}")

        # ==================================================
        # MATCH FOUND
        # ==================================================

        if best_person and best_similarity >= SIMILARITY_THRESHOLD:

            print("MATCH FOUND")
            print(f"Name: {best_person['full_name']}")
            print(f"Similarity: {round(best_similarity, 4)}")
            print("Matched Registered Image:")
            print(best_person["image_path"])

        # ==================================================
        # UNKNOWN + NEAREST MATCH
        # ==================================================

        else:

            print("UNKNOWN PERSON")

            if best_person:

                print("\nNearest Match Suggestion:")
                print(f"Name: {best_person['full_name']}")
                print(f"Similarity: {round(best_similarity, 4)}")
                print(best_person["image_path"])

                if second_best:
                    print("\nSecond Best:")
                    print(f"Name: {second_best['full_name']}")
                    print(f"Similarity: {round(second_best_score, 4)}")


# ======================================================

def start_monitoring():

    global monitoring_active
    monitoring_active = True

    print("\nMonitoring Started")
    print(f"Monitoring Directory: {MONITORING_FOLDER}")
    print("\nPress STOP option in menu to end monitoring.\n")

    while monitoring_active:

        try:
            files = os.listdir(MONITORING_FOLDER)

            for file_name in files:

                if not monitoring_active:
                    break

                file_path = os.path.join(MONITORING_FOLDER, file_name)

                if not file_name.lower().endswith((".jpg", ".jpeg", ".png")):
                    continue

                if file_path in processed_files:
                    continue

                processed_files.add(file_path)

                process_image(file_path)

            time.sleep(2)

        except Exception as error:

            print("\nMonitoring Error:")
            print(error)

            time.sleep(5)


# ======================================================

def stop_monitoring():

    global monitoring_active
    monitoring_active = False

    print("\nMonitoring Stopped Successfully.\n")