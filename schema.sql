CREATE DATABASE IF NOT EXISTS skillsakhi;
USE skillsakhi;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    teaches TEXT, -- Comma separated: "Python, Cooking"
    learns TEXT,  -- Comma separated: "Yoga, Marketing"
    availability VARCHAR(100),
    credits INT DEFAULT 5, -- Give 5 starter credits
    rating FLOAT DEFAULT 0,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE matches (
    id INT AUTO_INCREMENT PRIMARY KEY,
    requester_id INT,
    receiver_id INT,
    skill_offered VARCHAR(100),
    skill_requested VARCHAR(100),
    session_hours INT DEFAULT 1,
    status ENUM('pending', 'accepted', 'completed', 'rejected') DEFAULT 'pending',
    requester_confirmed BOOLEAN DEFAULT FALSE,
    receiver_confirmed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (requester_id) REFERENCES users(id),
    FOREIGN KEY (receiver_id) REFERENCES users(id)
);

CREATE TABLE reviews (
    id INT AUTO_INCREMENT PRIMARY KEY,
    match_id INT,
    reviewer_id INT,
    reviewee_id INT,
    rating INT CHECK (rating BETWEEN 1 AND 5),
    feedback TEXT,
    FOREIGN KEY (match_id) REFERENCES matches(id)
);