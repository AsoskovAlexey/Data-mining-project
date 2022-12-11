def add_product(product):
    """Returns a query to add a product"""
    return f'REPLACE INTO products (aliexpress_id, link, title, rating, n_reviews, n_orders, category_id) VALUES ({product.aliexpress_id}, "{product.link}", "{product.title}", {product.rating}, {product.n_reviews}, {product.n_orders}, {product.category_id});'


def get_category_id(url, title):
    """Returns a query to SELECT a category id"""
    return f'SELECT id FROM categories WHERE link = "{url}" and title = "{title}";'


def add_category(url, title):
    """Returns a query to INSERT a new category"""
    return f'REPLACE INTO categories (link, title) VALUES ("{url}", "{title}");'


def get_product_id(aliexpress_id):
    """Returns a query to SELECT a product id"""
    return f"SELECT id FROM products WHERE aliexpress_id = {aliexpress_id};"


def add_price(product):
    """Returns a query to add prices to the database"""
    return f"REPLACE INTO prices (product_id, price_usd, price_ils) VALUES ({product.id}, {product.price_usd}, {product.price_ils});"
