CREATE TABLE products (
  id INT NOT NULL AUTO_INCREMENT,
  aliexpress_id BIGINT NOT NULL,
  link VARCHAR(1024) NOT NULL,
  title VARCHAR(1024),
  rating FLOAT,
  n_reviews INT,
  n_orders INT,
  category_id INT NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE categories (
  id INT NOT NULL AUTO_INCREMENT,
  link VARCHAR(1024) NOT NULL,
  title varchar(255),
  PRIMARY KEY (id)
);

CREATE TABLE prices (
  id INT NOT NULL AUTO_INCREMENT,
  product_id int NOT NULL,
  price_usd float,
  price_ils float,
  date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id)
);

ALTER TABLE products ADD FOREIGN KEY(category_id) REFERENCES categories(id);
ALTER TABLE prices ADD FOREIGN KEY(product_id) REFERENCES products(id);
