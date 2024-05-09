CREATE TABLE IF NOT EXISTS forms (
    form_id SERIAL PRIMARY KEY,
    user_id VARCHAR(32) UNIQUE, /* учтонить размер айдишника */
    lat DECIMAL(9,6),
    long DECIMAL(9,6),
    goal VARCHAR(32),
    city VARCHAR(32),
    gender VARCHAR(32),
    name VARCHAR(32),
    age INTEGER,
    preference VARCHAR(32),
    description VARCHAR(150),
    first_photo_id VARCHAR(83),
    second_photo_id VARCHAR(83),
    third_photo_id VARCHAR(83),
    created_at TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS likes (
    like_id SERIAL PRIMARY KEY,
    user_id_from VARCHAR(32) REFERENCES forms(user_id),
    user_id_to VARCHAR(32) REFERENCES forms(user_id),
    is_like BOOLEAN,
    created_at TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS matches (
    match_id SERIAL PRIMARY KEY,
    user_id_1 VARCHAR(32) REFERENCES forms(user_id),
    user_id_2 VARCHAR(32) REFERENCES forms(user_id),
    created_at TIMESTAMP NOT NULL
);
