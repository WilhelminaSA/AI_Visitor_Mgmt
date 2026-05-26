CREATE EXTENSION IF NOT EXISTS vector;

-- =====================================================
-- PERSONS
-- =====================================================

CREATE TABLE persons (

    person_id SERIAL PRIMARY KEY,

    full_name VARCHAR(100) NOT NULL,

    gender VARCHAR(20),

    age INT,

    person_type VARCHAR(50),

    mobile_number VARCHAR(20),

    notes TEXT,

    is_vip BOOLEAN DEFAULT FALSE,

    is_blacklisted BOOLEAN DEFAULT FALSE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- PERSON REFERENCE IMAGES
-- =====================================================

CREATE TABLE person_reference_images (

    image_id SERIAL PRIMARY KEY,

    person_id INT REFERENCES persons(person_id),

    image_path TEXT NOT NULL,

    face_embedding vector(512),

    clip_embedding vector(512),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- DETECTION EVENTS
-- =====================================================

CREATE TABLE detection_events (

    event_id BIGSERIAL PRIMARY KEY,

    detected_time TIMESTAMP
    DEFAULT CURRENT_TIMESTAMP,

    detected_person_id INT
    REFERENCES persons(person_id),

    detected_name VARCHAR(100),

    confidence_score FLOAT,

    is_known_person BOOLEAN,

    snapshot_path TEXT,

    created_at TIMESTAMP
    DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- MONITORING CONTROL
-- =====================================================

CREATE TABLE monitoring_control (

    id INT PRIMARY KEY,

    monitoring_running BOOLEAN DEFAULT FALSE,

    monitoring_interval_sec INT DEFAULT 30,

    updated_at TIMESTAMP
    DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO monitoring_control (
    id
)
VALUES (1);

-- =====================================================
-- VECTOR INDEXES
-- =====================================================

CREATE INDEX face_embedding_idx
ON person_reference_images
USING hnsw (
    face_embedding vector_cosine_ops
);

CREATE INDEX clip_embedding_idx
ON person_reference_images
USING hnsw (
    clip_embedding vector_cosine_ops
);