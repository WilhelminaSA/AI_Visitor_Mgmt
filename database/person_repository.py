from database.db_connection import (
    get_connection,
    get_dict_cursor
)

# ======================================================
# INSERT PERSON
# ======================================================

def insert_person(
    full_name,
    gender,
    age,
    person_type,
    image_path,
    face_embedding,
    clip_embedding
):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        # ==============================
        # INSERT PERSON
        # ==============================

        person_query = """
        INSERT INTO persons (
            full_name,
            gender,
            age,
            person_type
        )
        VALUES (%s, %s, %s, %s)
        RETURNING person_id;
        """

        cursor.execute(person_query, (
            full_name,
            gender,
            age,
            person_type
        ))

        person_id = cursor.fetchone()[0]

        # ==============================
        # CONVERT EMBEDDINGS
        # ==============================

        face_embedding_list = [float(x) for x in face_embedding.tolist()]
        clip_embedding_list = [float(x) for x in clip_embedding.tolist()]

        # ==============================
        # INSERT IMAGE TABLE
        # ==============================

        image_query = """
        INSERT INTO person_reference_images (
            person_id,
            image_path,
            face_embedding,
            clip_embedding
        )
        VALUES (%s, %s, %s, %s)
        """

        cursor.execute(image_query, (
            person_id,
            image_path,
            face_embedding_list,
            clip_embedding_list
        ))

        connection.commit()
        return person_id

    except Exception as e:
        connection.rollback()
        print("\n[ERROR] insert_person failed:", e)
        return None

    finally:
        cursor.close()
        connection.close()


# ======================================================
# GET ALL REGISTERED PERSONS (🔥 FIXED HERE)
# ======================================================

def get_registered_persons():

    connection = get_connection()
    cursor = get_dict_cursor(connection)

    try:

        # 🔥 FIX: LEFT JOIN instead of INNER JOIN
        query = """
        SELECT
            p.person_id,
            p.full_name,
            p.gender,
            p.age,
            p.person_type,
            pri.image_path,
            pri.face_embedding
        FROM persons p
        LEFT JOIN person_reference_images pri
        ON p.person_id = pri.person_id
        ORDER BY p.person_id;
        """

        cursor.execute(query)
        rows = cursor.fetchall()

        persons = []

        for row in rows:

            face_embedding = row["face_embedding"]

            # handle string vector case
            if isinstance(face_embedding, str):
                face_embedding = face_embedding.strip("[]")
                face_embedding = [
                    float(x) for x in face_embedding.split(",")
                    if x.strip()
                ]

            persons.append({
                "person_id": row["person_id"],
                "full_name": row["full_name"],
                "gender": row["gender"],
                "age": row["age"],
                "person_type": row["person_type"],
                "image_path": row["image_path"],
                "face_embedding": face_embedding
            })

        return persons

    except Exception as e:
        print("\n[ERROR] get_registered_persons failed:", e)
        return []

    finally:
        cursor.close()
        connection.close()


# ======================================================
# SEARCH BY ID
# ======================================================

def search_person_by_id(person_id):

    connection = get_connection()
    cursor = get_dict_cursor(connection)

    try:

        query = """
        SELECT *
        FROM persons
        WHERE person_id = %s;
        """

        cursor.execute(query, (person_id,))
        return cursor.fetchone()

    except Exception as e:
        print("\n[ERROR] search_person_by_id:", e)
        return None

    finally:
        cursor.close()
        connection.close()


# ======================================================
# SEARCH BY NAME
# ======================================================

def search_persons_by_name(name):

    connection = get_connection()
    cursor = get_dict_cursor(connection)

    try:

        query = """
        SELECT *
        FROM persons
        WHERE LOWER(full_name) LIKE LOWER(%s)
        ORDER BY person_id;
        """

        cursor.execute(query, (f"%{name}%",))
        return cursor.fetchall()

    except Exception as e:
        print("\n[ERROR] search_persons_by_name:", e)
        return []

    finally:
        cursor.close()
        connection.close()


# ======================================================
# DELETE PERSON
# ======================================================

def delete_person_by_id(person_id):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute(
            "DELETE FROM person_reference_images WHERE person_id=%s",
            (person_id,)
        )

        cursor.execute(
            "DELETE FROM persons WHERE person_id=%s",
            (person_id,)
        )

        deleted = cursor.rowcount > 0

        connection.commit()
        return deleted

    except Exception as e:
        connection.rollback()
        print("\n[ERROR] delete_person_by_id:", e)
        return False

    finally:
        cursor.close()
        connection.close()