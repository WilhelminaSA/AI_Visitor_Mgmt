import sys
import os
import threading

# ======================================================
# ADD PROJECT ROOT TO PYTHON PATH
# ======================================================

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

PROJECT_ROOT = os.path.dirname(CURRENT_DIR)

if PROJECT_ROOT not in sys.path:

    sys.path.append(PROJECT_ROOT)

# ======================================================

from services.monitoring_service import (
    start_monitoring
)

# ======================================================

monitoring_running = False

# ======================================================

def start_monitoring_thread():

    global monitoring_running

    if monitoring_running:

        print()
        print("Monitoring already running.")

        return

    monitoring_running = True

    monitoring_thread = threading.Thread(
        target=start_monitoring,
        daemon=True
    )

    monitoring_thread.start()

    print()
    print("Monitoring thread started.")

# ======================================================

def show_menu():

    print()
    print("=================================")
    print(" AI Visitor Monitoring System ")
    print("=================================")

    print("1. Register Person")
    print("2. Delete Person")
    print("3. Search Person by ID")
    print("4. Search by Name")
    print("5. List All Persons")
    print("6. Start Monitoring")
    print("0. Exit")

# ======================================================

def start_menu():

    while True:

        show_menu()

        choice = input(
            "\nEnter choice: "
        ).strip()

        # ==========================================

        if choice == "6":

            start_monitoring_thread()

        # ==========================================

        elif choice == "0":

            print()
            print("Exiting...")

            break

        # ==========================================

        else:

            print()
            print(
                "Feature implementation pending."
            )
