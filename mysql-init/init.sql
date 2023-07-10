USE your-database-name;

CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    firstname VARCHAR(50) NOT NULL,
    lastname VARCHAR(50) NOT NULL,
    birthday DATE NOT NULL,
    state VARCHAR(50) NOT NULL,
    city VARCHAR(50) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(100) NOT NULL,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL
);

INSERT INTO users (firstname, lastname, birthday, state, city, phone, email, username, password)
VALUES ('Admin', 'User', '2000-01-01', 'State', 'City', '1234567890', 'admin@example.com', 'admin', 'admin_password')
ON DUPLICATE KEY UPDATE firstname = 'Admin', lastname = 'User', birthday = '2000-01-01', state = 'State', city = 'City', phone = '1234567890', email = 'admin@example.com', password = 'admin_password';
