
CREATE TABLE users (
    id       BIGINT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(255) NOT NULL UNIQUE,
    name     VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE priority (
    id    BIGINT PRIMARY KEY AUTO_INCREMENT,
    level VARCHAR(50) NOT NULL
);

CREATE TABLE state_task (
    id    BIGINT PRIMARY KEY AUTO_INCREMENT,
    state VARCHAR(50) NOT NULL
);

CREATE TABLE tasks (
    id            BIGINT PRIMARY KEY AUTO_INCREMENT,
    title         VARCHAR(255) NOT NULL,
    description   VARCHAR(1000) NOT NULL,
    state_id      BIGINT NOT NULL DEFAULT 1,
    priority_id   BIGINT NOT NULL,
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id       BIGINT NOT NULL,
    CONSTRAINT fk_tasks_state    FOREIGN KEY (state_id)    REFERENCES state_task(id),
    CONSTRAINT fk_tasks_priority FOREIGN KEY (priority_id) REFERENCES priority(id),
    CONSTRAINT fk_tasks_user     FOREIGN KEY (user_id)     REFERENCES users(id)
);

INSERT INTO state_task (id, state) VALUES
    (1, 'pendiente'),
    (2, 'completado');

INSERT INTO priority (id, level) VALUES
    (1, 'baja'),
    (2, 'media'),
    (3, 'alta');