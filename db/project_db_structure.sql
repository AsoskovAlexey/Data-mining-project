CREATE TABLE products (
  id BIGINT NOT NULL,
  link VARCHAR(1024) NOT NULL,
  title VARCHAR(1024),
  rating FLOAT,
  n_reviews INT,
  n_orders INT,
  price FLOAT,
  category_id INT NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE category_level_3 (
  id INT NOT NULL,
  title VARCHAR(255),
  parent_id INT NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE category_level_2 (
  id INT NOT NULL,
  title VARCHAR(255),
  parent_id INT NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE category_level_1 (
  id INT NOT NULL,
  title VARCHAR(255),
  PRIMARY KEY (id)
);

CREATE TABLE reviews (
  id INT NOT NULL,
  product_id INT NOT NULL,
  product_type VARCHAR(1024),
  comment TEXT,
  PRIMARY KEY (id)
);

#ALTER TABLE products ADD FOREIGN KEY(category_id) REFERENCES category_level_3(id);

#ALTER TABLE category_level_3 ADD FOREIGN KEY(parent_id) REFERENCES category_level_2(id);

#ALTER TABLE category_level_2 ADD FOREIGN KEY(parent_id) REFERENCES category_level_1(id);

#ALTER TABLE reviews ADD FOREIGN KEY(product_id) REFERENCES products(id);
