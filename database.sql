CREATE DATABASE ecommerce_chatbot;
USE ecommerce_chatbot;
CREATE TABLE complaints (

    id INT AUTO_INCREMENT PRIMARY KEY,

    customer_message TEXT,

    predicted_intent VARCHAR(100),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

CREATE TABLE orders (

    order_id INT PRIMARY KEY,

    customer_name VARCHAR(100),

    status VARCHAR(50)

);

INSERT INTO orders VALUES

(101, 'Ateeb', 'Shipped'),

(102, 'Sadiya', 'Delivered'),

(103, 'Anas', 'Processing');

CREATE TABLE chat_history (

    id INT AUTO_INCREMENT PRIMARY KEY,

    user_message TEXT,

    bot_response TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

SELECT * FROM complaints;

SHOW TABLES;
SELECT * FROM complaints;
SELECT * FROM chat_history;
SELECT * FROM complaints;