CREATE TABLE IF NOT EXISTS urls (
    id int PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(255) UNIQUE,
    created_at DATE
);

CREATE TABLE IF NOT EXISTS checks (
    check_id int PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    url_id int REFERENCES urls(id)
    response_code int,
    h1 VARCHAR(255)
    title VARCHAR(255),
    description VARCHAR(255),
    created_at DATE
    );