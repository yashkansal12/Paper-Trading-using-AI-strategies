from decimal import Decimal

from trading.models import Trade
from portfolio.models import Portfolio, Position



#BUy
def buy_stock(user, stock, quantity, price):
    """
    Execute a BUY order.

    quantity -> int
    price -> float or Decimal
    """

    # Convert price to Decimal
    price = Decimal(str(price))

    # Ensure quantity is an integer
    quantity = int(quantity)

    total = Decimal(quantity) * price

    # Get or create portfolio
    portfolio, _ = Portfolio.objects.get_or_create(user=user)

    # Check balance
    if portfolio.cash_balance < total:
        return False, "Insufficient Balance"

    # Update portfolio cash
    portfolio.cash_balance -= total
    portfolio.invested_amount += total
    portfolio.save()

    # Record trade
    Trade.objects.create(
        user=user,
        stock=stock,
        trade_type="BUY",
        quantity=quantity,
        price=price,
        total_amount=total,
    )

    # Update/Create Position
    position, created = Position.objects.get_or_create(
        portfolio=portfolio,
        stock=stock,
        defaults={
            "quantity": quantity,
            "average_price": price,
            "current_price": price,
            "market_value": total,
            "unrealized_pnl": Decimal("0.00"),
        },
    )

    if not created:

        old_qty = position.quantity
        new_qty = quantity

        total_qty = old_qty + new_qty

        total_cost = (
            position.average_price * Decimal(old_qty)
        ) + (
            price * Decimal(new_qty)
        )

        avg_price = total_cost / Decimal(total_qty)

        position.quantity = total_qty
        position.average_price = avg_price

        position.current_price = price
        position.market_value = Decimal(total_qty) * price
        position.unrealized_pnl = (
            price - avg_price
        ) * Decimal(total_qty)

        position.save()

    return True, "Order Executed"



#Sell


def sell_stock(user, stock, quantity, price):

    price = Decimal(str(price))
    quantity = int(quantity)
    portfolio = Portfolio.objects.get(user=user)
    position = Position.objects.get(
        portfolio=portfolio,
        stock=stock
    )

    if quantity > position.quantity:
        return False, "Not enough shares."

    total = Decimal(quantity) * price

    # Add cash back
    portfolio.cash_balance += total
    portfolio.invested_amount -= Decimal(quantity) * position.average_price
    portfolio.save()

    # Save trade
    Trade.objects.create(
        user=user,
        stock=stock,
        trade_type="SELL",
        quantity=quantity,
        price=price,
        total_amount=total,
    )

    # Update position
    position.quantity -= quantity

    if position.quantity == 0:
        position.delete()
    else:
        position.current_price = price
        position.market_value = Decimal(position.quantity) * price
        position.unrealized_pnl = (
            price - position.average_price
        ) * Decimal(position.quantity)

        position.save()

    return True, "Stock Sold Successfully"