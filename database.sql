CREATE TABLE IF NOT EXISTS urls (
    id int PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(255) UNIQUE,
    created_at DATE
);
CREATE TABLE IF NOT EXISTS url_checks (
    id int PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    url_id INT REFERENCES urls(id) NOT NULL,
    status_code int,
    h1 VARCHAR(255),
    title VARCHAR(255),
    description VARCHAR(255),
    created_at TIMESTAMP
);