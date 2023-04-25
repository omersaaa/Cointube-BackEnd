# Defines the routes (URL endpoints) for the application, and the functions that handle the HTTP requests.
from flask import jsonify, request, Blueprint
from api.models import Session, Stock


stocks = Blueprint("stocks", __name__, url_prefix="/stocks")


@stocks.route("/add", methods=["POST"])
def add_stock():
    data = request.json
    name = data["name"]
    symbol = data["symbol"]
    price = data["price"]

    stock = Stock(name=name, symbol=symbol, price=price)

    session = Session()
    session.add(stock)
    session.commit()

    return jsonify(
        {"status": "success", "message": f"Stock {symbol} added successfully"}
    )


@stocks.route("/get", methods=["GET"])
def get_stocks():
    session = Session()
    stocks_copy = session.query(Stock).all()

    data = []
    for stock in stocks_copy:
        data.append(
            {
                "id": stock.id,
                "name": stock.name,
                "symbol": stock.symbol,
                "price": stock.price,
            }
        )

    return jsonify(data)
    # return jsonify({"status": "success"})


@stocks.route("/<int:stockid>/price", methods=["PUT"])
def update_price(stockid):
    data = request.json
    new_price = data["price"]

    session = Session()
    stock = session.query(Stock).filter(Stock.id == stockid).one()
    stock.price = new_price
    session.commit()

    return jsonify(
        {
            "status": "success",
            "message": f"Price of stock {stock.symbol} updated to {new_price}",
        }
    )
