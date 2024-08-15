from decimal import Decimal

def calculate_discount(cart):
    total_price = sum(item.get_cost() for item in cart.items.all())
    total_quantity = sum(item.quantity for item in cart.items.all())

    if not isinstance(total_price, Decimal):
        total_price = Decimal(total_price)

    if total_quantity == 2:
        discount = Decimal('0.30')  # 30% discount for 2 courses
    elif total_quantity >= 3:
        discount = Decimal('0.35')  # 35% discount for 3 or more courses
    else:
        discount = Decimal('0')

    discounted_total = total_price - (total_price * discount)
    return discounted_total, discount * 100
