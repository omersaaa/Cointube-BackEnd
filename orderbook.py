import time
from api.models import Session, User, Order, Stock, Portfolio

# from flask import jsonify


def update_prices():
    
    while True:
        session = Session()

        # Get all orders that are yet to be executed
        orders = session.query(Order).filter(Order.executed == False).all()

        for order in orders:
            # Get the matching orders
            if order.type == "buy":
                matches = (
                    session.query(Order)
                    .filter(
                        Order.stock_id == order.stock_id,
                        Order.type == "sell",
                        Order.price <= order.price,
                        Order.executed == False,
                    )
                    .all()
                )
            else:
                matches = (
                    session.query(Order)
                    .filter(
                        Order.stock_id == order.stock_id,
                        Order.type == "buy",
                        Order.price >= order.price,
                        Order.executed == False,
                    )
                    .all()
                )
            # return jsonify(matches)
            if matches:
                # Sort the matches based on price and time
                # matches = sorted(matches, key=lambda x: (x.price))

                matches = sorted(matches, key=lambda x: (x.price, x.created_at))
                # Execute the orders
                for match in matches:
                    if order.shares == match.shares:
                        order.executed = True
                        match.executed = True

                        # Update the portfolio of the users
                        user1 = session.query(User).get(order.user_id)
                        user2 = session.query(User).get(match.user_id)

                        # Update the portfolio of the buyer
                        holding1 = (
                            session.query(Portfolio)
                            .filter(
                                Portfolio.user_id == user1.id,
                                Portfolio.stock_id == order.stock_id,
                            )
                            .one_or_none()
                        )

                        if holding1:
                            holding1.shares += order.shares
                        else:
                            holding1 = Portfolio(
                                user_id=user1.id,
                                stock_id=order.stock_id,
                                shares=order.shares,
                            )
                            session.add(holding1)

                        # Update the portfolio of the seller
                        holding2 = (
                            session.query(Portfolio)
                            .filter(
                                Portfolio.user_id == user2.id,
                                Portfolio.stock_id == order.stock_id,
                            )
                            .one_or_none()
                        )

                        if holding2:
                            holding2.shares -= order.shares
                        else:
                            holding2 = Portfolio(
                                user_id=user2.id,
                                stock_id=order.stock_id,
                                shares=-order.shares,
                            )
                            session.add(holding2)

                        # Update the balance of the buyer and seller
                        user1.balance -= order.shares * order.price
                        user2.balance += order.shares * order.price

                        # Update the price of the stock
                        stock = session.query(Stock).get(order.stock_id)
                        stock.price = match.price

                        session.commit()

                        break
                    elif order.shares < match.shares:
                        match.shares -= order.shares
                        order.executed = True

                        # Update the portfolio of the buyer
                        user = session.query(User).get(order.user_id)
                        holding = (
                            session.query(Portfolio)
                            .filter(
                                Portfolio.user_id == user.id,
                                Portfolio.stock_id == order.stock_id,
                            )
                            .one_or_none()
                        )

                        if holding:
                            holding.shares += order.shares
                        else:
                            holding = Portfolio(
                                user_id=user.id,
                                stock_id=order.stock_id,
                                shares=order.shares,
                            )
                            session.add(holding)

                        # Update the balance of the buyer and seller
                        user.balance -= order.shares * order.price
                        seller = session.query(User).get(match.user_id)
                        seller.balance += order.shares * order.price

                        # Update the price of the stock
                        stock = session.query(Stock).get(order.stock_id)
                        stock.price = match.price

                        session.commit()

                        break
                    else:
                        order.shares -= match.shares
                        match.executed = True

                        # Update the portfolio of the buyer
                        user = session.query(User).get(match.user_id)
                        holding = (
                            session.query(Portfolio)
                            .filter(
                                Portfolio.user_id == user.id,
                                Portfolio.stock_id == order.stock_id,
                            )
                            .one_or_none()
                        )

                        if holding:
                            holding.shares -= match.shares
                        else:
                            holding = Portfolio(
                                user_id=user.id,
                                stock_id=order.stock_id,
                                shares=-match.shares,
                            )
                            session.add(holding)

                        # Update the balance of the buyer and seller
                        user.balance += match.shares * match.price
                        seller = session.query(User).get(match.user_id)
                        seller.balance -= match.shares * match.price

                        # Update the price of the stock
                        stock = session.query(Stock).get(order.stock_id)
                        stock.price = match.price

                        session.commit()

        time.sleep(1000)
        