import cv2
import numpy as np

from PIL import Image

from insightface.app import FaceAnalysis

from sentence_transformers import (
    SentenceTransformer
)

# ======================================================
# LOAD INSIGHTFACE
# ======================================================

print("Loading InsightFace...")

face_app = FaceAnalysis(
    name="buffalo_l",
    providers=["CPUExecutionProvider"]
)

face_app.prepare(
    ctx_id=0,
    det_size=(640, 640)
)

print("InsightFace Loaded")

# ======================================================
# LOAD CLIP
# ======================================================

print("Loading CLIP...")

clip_model = SentenceTransformer(
    "sentence-transformers/clip-ViT-B-32"
)

print("CLIP Loaded")

# ======================================================
# NORMALIZE EMBEDDING
# ======================================================

def normalize_embedding(embedding):

    embedding = np.array(
        embedding,
        dtype=np.float32
    )

    norm = np.linalg.norm(
        embedding
    )

    if norm == 0:

        return embedding

    return embedding / norm

# ======================================================
# REGISTRATION
# EXACTLY ONE FACE REQUIRED
# ======================================================

def get_face_embedding(image_path):

    image = cv2.imread(image_path)

    if image is None:

        print("Unable to read image")

        return None

    faces = face_app.get(image)

    # ==============================================
    # REGISTRATION REQUIRES EXACTLY ONE FACE
    # ==============================================

    if len(faces) != 1:

        print()
        print(
            "Registration image must contain exactly one face"
        )

        return None

    embedding = faces[0].embedding

    embedding = normalize_embedding(
        embedding
    )

    return embedding

# ======================================================
# MONITORING
# MULTIPLE FACES ALLOWED
# ======================================================

def get_multiple_face_embeddings(
    image_path
):

    image = cv2.imread(image_path)

    if image is None:

        print("Unable to read image")

        return []

    faces = face_app.get(image)

    # ==============================================

    if len(faces) == 0:

        print("No face detected")

        return []

    # ==============================================

    all_embeddings = []

    for face in faces:

        embedding = face.embedding

        embedding = normalize_embedding(
            embedding
        )

        all_embeddings.append(
            embedding
        )

    return all_embeddings

# ======================================================
# CLIP EMBEDDING
# ======================================================

def get_clip_embedding(image_path):

    image = Image.open(
        image_path
    ).convert("RGB")

    embedding = clip_model.encode(
        image,
        convert_to_numpy=True
    )

    embedding = normalize_embedding(
        embedding
    )

    return embedding
