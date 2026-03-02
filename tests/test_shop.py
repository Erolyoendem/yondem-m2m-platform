from app.models.shop import Shop

def test_create_shop(db_session):
    shop = Shop(name='Amazon', affiliate_network='amazon', commission_rate=5.0)
    db_session.add(shop)
    db_session.commit()
    assert shop.id is not None
    assert shop.name == 'Amazon'
    assert shop.cashback_rate is None

def test_shop_cashback(db_session):
    shop = Shop(name='eBay', affiliate_network='awin', commission_rate=3.0, cashback_rate=2.0)
    db_session.add(shop)
    db_session.commit()
    assert shop.cashback_rate == 2.0
