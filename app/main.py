import sys
import os
import threading

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)

if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

# ======================================================
from services.monitoring_service import start_monitoring, stop_monitoring

from services.embedding_service import (
    get_face_embedding,
    get_clip_embedding
)

from database.person_repository import (
    insert_person,
    get_registered_persons,
    delete_person_by_id,
    search_person_by_id,
    search_persons_by_name
)

from utils.image_storage import save_registered_person_image


# ======================================================
# GLOBAL FLAGS
# ======================================================

monitoring_thread = None
monitoring_running = False


# ======================================================
# MONITORING START
# ======================================================

def start_monitoring_thread():

    global monitoring_thread, monitoring_running

    if monitoring_running:
        print("\nMonitoring already running.")
        return

    monitoring_running = True

    monitoring_thread = threading.Thread(
        target=start_monitoring,
        daemon=True
    )

    monitoring_thread.start()

    print("\nMonitoring thread started.")


# ======================================================
# MONITORING STOP
# ======================================================

def stop_monitoring_thread():

    global monitoring_running

    if not monitoring_running:
        print("\nMonitoring is not running.")
        return

    stop_monitoring()

    monitoring_running = False

    print("\nMonitoring thread stopped.")


# ======================================================
# REGISTER PERSON
# ======================================================

def register_person():

    print("\n===== PERSON REGISTRATION =====")

    try:

        full_name = input("Enter Full Name: ").strip()
        gender = input("Enter Gender: ").strip()
        age = int(input("Enter Age: ").strip())
        person_type = input("Enter Person Type: ").strip()
        image_path = input("Enter Image Path: ").strip()

        if not os.path.exists(image_path):
            print("\nImage path does not exist.")
            return

        saved_image_path = save_registered_person_image(
            image_path,
            full_name
        )

        if not saved_image_path:
            print("\nFailed to save image.")
            return

        print("\nGenerating embeddings...")

        face_embedding = get_face_embedding(saved_image_path)
        clip_embedding = get_clip_embedding(saved_image_path)

        if face_embedding is None:
            print("\nNo face detected.")
            return

        person_id = insert_person(
            full_name,
            gender,
            age,
            person_type,
            saved_image_path,
            face_embedding,
            clip_embedding
        )

        if person_id:
            print("\nPerson registered successfully.")
            print("Person ID:", person_id)
            print("Image saved at:", saved_image_path)

        else:
            print("\nRegistration failed.")

    except Exception as e:
        print("\nError during registration:", e)


# ======================================================
# DELETE PERSON
# ======================================================

def delete_person():

    try:
        person_id = int(input("\nEnter Person ID to delete: "))

        if delete_person_by_id(person_id):
            print("\nPerson deleted successfully.")
        else:
            print("\nPerson not found.")

    except Exception as e:
        print("\nInvalid input or error:", e)


# ======================================================
# SEARCH BY ID
# ======================================================

def search_by_id():

    try:
        person_id = int(input("\nEnter Person ID: "))

        person = search_person_by_id(person_id)

        if person:
            print("\n--- PERSON FOUND ---")
            print(person)
        else:
            print("\nPerson not found.")

    except Exception as e:
        print("\nError:", e)


# ======================================================
# SEARCH BY NAME
# ======================================================

def search_by_name():

    name = input("\nEnter Name: ").strip()

    persons = search_persons_by_name(name)

    if persons:
        print("\n--- RESULTS ---")
        for p in persons:
            print(p)
    else:
        print("\nNo persons found.")


# ======================================================
# LIST ALL PERSONS (FIXED VERSION)
# ======================================================

def list_all_persons():

    try:

        persons = get_registered_persons()

        print("\nDEBUG COUNT:", len(persons))

        if not persons:
            print("\nNo persons registered.")
            return

        print("\n========== REGISTERED PERSONS ==========")

        for person in persons:

            print("\n--------------------------------")
            print(f"ID     : {person['person_id']}")
            print(f"Name   : {person['full_name']}")
            print(f"Gender : {person['gender']}")
            print(f"Age    : {person['age']}")
            print(f"Type   : {person['person_type']}")
            print(f"Image  : {person['image_path']}")

    except Exception as e:
        print("\nERROR in list_all_persons:", e)


# ======================================================
# MENU
# ======================================================

def show_menu():

    print("\n=================================")
    print(" AI Visitor Monitoring System ")
    print("=================================")

    print("1. Register Person")
    print("2. Delete Person")
    print("3. Search Person by ID")
    print("4. Search by Name")
    print("5. List All Persons")
    print("6. Start Monitoring")
    print("7. Stop Monitoring")
    print("0. Exit")


# ======================================================
# MAIN LOOP
# ======================================================

def start_menu():

    while True:

        show_menu()

        choice = input("\nEnter choice: ").strip()

        if choice == "1":
            register_person()

        elif choice == "2":
            delete_person()

        elif choice == "3":
            search_by_id()

        elif choice == "4":
            search_by_name()

        elif choice == "5":
            list_all_persons()

        elif choice == "6":
            start_monitoring_thread()

        elif choice == "7":
            stop_monitoring_thread()

        elif choice == "0":
            print("\nExiting...")
            break

        else:
            print("\nInvalid choice.")


# ======================================================

if __name__ == "__main__":
    start_menu()