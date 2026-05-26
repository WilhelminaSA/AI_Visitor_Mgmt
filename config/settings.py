import os

# ======================================================
# DATABASE
# ======================================================

DB_HOST = "localhost"

DB_PORT = "5432"

DB_NAME = "ai_visitor_db"

DB_USER = "postgres"

DB_PASSWORD = "snehaa_p"

# ======================================================
# REGISTERED PERSON IMAGE STORAGE
# ======================================================

REGISTERED_PERSON_DIR = (
    r"C:\data\registered_persons"
)

# ======================================================
# CREATE DIRECTORY IF NOT EXISTS
# ======================================================

os.makedirs(
    REGISTERED_PERSON_DIR,
    exist_ok=True
)

# ======================================================
# MONITORING
# ======================================================

MONITORING_DIR = (
    r"C:\my_work\aiv22\Images"
)

MONITORING_INTERVAL = 30

# ======================================================
# AI SETTINGS
# ======================================================

MATCH_THRESHOLD = 0.58
