def create_product_query(product):
    return f'REPLACE INTO products (id, link, title, rating, n_reviews, n_orders, price, category_id) VALUES ({product.id}, "{product.link}", "{product.title}", {product.rating}, {product.n_reviews}, {product.n_orders}, {product.price}, {product.category});'
                