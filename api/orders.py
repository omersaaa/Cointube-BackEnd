# Defines the routes (URL endpoints) for the application, and the functions that handle the HTTP requests.
from flask import jsonify, request, Blueprint
from api.models import Session, Order


orders = Blueprint("orders", __name__, url_prefix="/orders")


@orders.route("/add", methods=["POST"])
def add_order():
    data = request.json
    user_id = data["user_id"]
    stock_id = data["stock_id"]
    order_type = data["type"]
    shares = data["shares"]
    price = data["price"]

    order = Order(
        user_id=user_id, stock_id=stock_id, type=order_type, shares=shares, price=price
    )

    session = Session()
    session.add(order)
    session.commit()

    return jsonify(
        {"status": "success", "message": f"Order {order.id} added successfully"}
    )


@orders.route("/get", methods=["GET"])
def get_orders():
    session = Session()
    ordersx = session.query(Order).all()

    data = []
    for order in ordersx:
        data.append(
            {
                "id": order.id,
                "user_id": order.user_id,
                "stock_id": order.stock_id,
                "type": order.type,
                "price": order.price,
                "shares": order.shares,
            }
        )

    return jsonify(data)
