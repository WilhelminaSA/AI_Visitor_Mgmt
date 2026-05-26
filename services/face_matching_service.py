import sys
import os
import numpy as np

# ======================================================
# ADD PROJECT ROOT TO PYTHON PATH
# ======================================================

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

PROJECT_ROOT = os.path.dirname(CURRENT_DIR)

if PROJECT_ROOT not in sys.path:

    sys.path.append(PROJECT_ROOT)

# ======================================================

from config.settings import MATCH_THRESHOLD

# ======================================================

def cosine_similarity(a, b):

    a = np.array(
        a,
        dtype=np.float32
    )

    b = np.array(
        b,
        dtype=np.float32
    )

    # ==================================================

    a_norm = np.linalg.norm(a)

    b_norm = np.linalg.norm(b)

    if a_norm == 0 or b_norm == 0:

        return 0.0

    # ==================================================

    similarity = np.dot(a, b) / (
        a_norm * b_norm
    )

    return float(similarity)

# ======================================================

def convert_embedding_to_list(
    embedding
):

    # ==================================================
    # HANDLE STRING FORMAT
    # ==================================================

    if isinstance(embedding, str):

        embedding = embedding.strip()

        embedding = embedding.strip("[")

        embedding = embedding.strip("]")

        embedding = [

            float(value.strip())

            for value in embedding.split(",")

            if value.strip() != ""
        ]

    # ==================================================

    return embedding

# ======================================================

def find_best_match(
    current_embedding,
    registered_persons
):

    best_match = None

    best_similarity = -1

    # ==================================================

    for person in registered_persons:

        db_embedding = person.get(
            "face_embedding"
        )

        if db_embedding is None:

            continue

        # ==============================================

        db_embedding = convert_embedding_to_list(
            db_embedding
        )

        # ==============================================

        try:

            similarity = cosine_similarity(
                current_embedding,
                db_embedding
            )

        except Exception as error:

            print()
            print(
                "Embedding comparison error:"
            )

            print(error)

            continue

        # ==============================================

        if similarity > best_similarity:

            best_similarity = similarity

            best_match = person

    # ==================================================

    if (
        best_match is not None
        and
        best_similarity >= MATCH_THRESHOLD
    ):

        best_match["similarity"] = (
            best_similarity
        )

        return best_match

    # ==================================================

    return None
