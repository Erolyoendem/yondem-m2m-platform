from app.models.deal import Deal

def test_create_deal(db_session):
    deal = Deal(title='50% Rabatt', discount_value=50.0, discount_type='percent', shop_id=1)
    db_session.add(deal)
    db_session.commit()
    assert deal.id is not None
    assert deal.title == '50% Rabatt'

def test_deal_with_code(db_session):
    deal = Deal(title='10 EUR Rabatt', discount_value=10.0, discount_type='fixed', code='SAVE10', shop_id=1)
    db_session.add(deal)
    db_session.commit()
    assert deal.code == 'SAVE10'
