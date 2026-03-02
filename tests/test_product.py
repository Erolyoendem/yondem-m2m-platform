from app.models.product import Product

def test_create_product(db_session):
    product = Product(name='Test Laptop', price=999.99, shop_id=1)
    db_session.add(product)
    db_session.commit()
    assert product.id is not None
    assert product.name == 'Test Laptop'
    assert product.price == 999.99

def test_product_currency(db_session):
    product = Product(name='Phone', price=599.99, shop_id=1, currency='USD')
    db_session.add(product)
    db_session.commit()
    assert product.currency == 'USD'
