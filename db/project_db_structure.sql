CREATE TABLE products (
  id int NOT NULL,
  link varchar(1024) NOT NULL,
  title varchar(1024),
  rating float,
  n_reviews int,
  n_orders int,
  price float,
  category_id int NOT NULL,
  PRIMARY KEY (ID)
);

CREATE TABLE category_level_3 (
  id int NOT NULL,
  title varchar(255),
  parent_id int NOT NULL,
  PRIMARY KEY (ID)
);

CREATE TABLE category_level_2 (
  id int NOT NULL,
  title varchar(255),
  parent_id int NOT NULL,
  PRIMARY KEY (ID)
);

CREATE TABLE category_level_1 (
  id int NOT NULL,
  title varchar(255),
  PRIMARY KEY (ID)
);

CREATE TABLE reviews (
  id int NOT NULL,
  product_id int NOT NULL,
  product_type varchar(1024),
  comment TEXT,
  PRIMARY KEY (ID)
);

ALTER TABLE products ADD FOREIGN KEY(category_id) REFERENCES category_level_3(id);

ALTER TABLE category_level_3 ADD FOREIGN KEY(parent_id) REFERENCES category_level_2(id);

ALTER TABLE category_level_2 ADD FOREIGN KEY(parent_id) REFERENCES category_level_1(id);

ALTER TABLE reviews ADD FOREIGN KEY(product_id) REFERENCES products(id);
