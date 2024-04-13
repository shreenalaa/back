-- Create users table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    phone_number VARCHAR(20) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL
);

-- Create lost_items table
CREATE TABLE lost_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    category VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    date_lost DATE NOT NULL,
    location VARCHAR(255) NOT NULL,
    image_url VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Create found_items table
CREATE TABLE found_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    description TEXT NOT NULL,
    date_found DATE NOT NULL,
    location VARCHAR(255) NOT NULL,
    image_url VARCHAR(255)
);
