from flask import jsonify, request, Blueprint
from api.models import Session, User, Portfolio


users = Blueprint("users", __name__, url_prefix="/users")


@users.route("/add", methods=["POST"])
def create_user():
    data = request.json
    name = data["name"]
    email = data["email"]
    price = data["password"]

    user = User(name=name, email=email, password=price, balance=0)
    portfolio = Portfolio(user=user, stock_id=2, shares=100)

    session = Session()
    session.add(user)
    session.add(portfolio)
    session.commit()

    return jsonify({"status": "success", "message": f"Stock {name} added successfully"})


@users.route("/<int:user_id>/portfolio", methods=["GET"])
def get_portfolio(user_id):
    session = Session()
    user = session.query(User).get(user_id)
    portfolio = user.portfolio

    data = []
    for holding in portfolio:
        data.append(
            {
                "id": holding.id,
                "stock_id": holding.stock_id,
                "name": holding.stock.name,
                "symbol": holding.stock.symbol,
                "shares": holding.shares,
                "price": holding.stock.price,
            }
        )

    return jsonify(data)
