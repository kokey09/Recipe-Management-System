CREATE USER 'dashboard'@'localhost' IDENTIFIED BY 'dashboard';

GRANT ALL PRIVILEGES ON recipedb.* TO 'dashboard'@'localhost';

CREATE DATABASE recipedb;

USE recipedb;

CREATE TABLE recipes (
    recipe_id INT(11) AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    instructions TEXT NOT NULL,
    image_url VARCHAR(512)
);

CREATE TABLE ingredients (
     ingredient_id INT(11) AUTO_INCREMENT PRIMARY KEY,
     name VARCHAR(255) NOT NULL,
     description TEXT
);

CREATE TABLE account (
    id INT(11) AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50),
    email VARCHAR(120),
    password VARCHAR(60),
    date_created TIMESTAMP,
    type VARCHAR(255)
    is_deleted TINYINT(1)
);

CREATE TABLE recipe_ingredients (
     recipe_id INT(11),
     ingredient_id INT(11),
     FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id),
     FOREIGN KEY (ingredient_id) REFERENCES ingredients(ingredient_id)
);

CREATE TABLE reviews (
    review_id INT(11) AUTO_INCREMENT PRIMARY KEY,
    recipe_id INT(11),
    account_id INT(11),
    review_text TEXT,
    rating INT(5),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES account(id),
    FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id)
);
