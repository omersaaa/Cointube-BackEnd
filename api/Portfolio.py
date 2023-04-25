from flask import jsonify, request, Blueprint
from api.models import Session, Portfolio, User


portfolios = Blueprint("portfolios", __name__, url_prefix="/portfolios")


@portfolios.route("/add", methods=["POST"])
def create_portfolio():
    session = Session()

    data = request.json
    user_id = data["user_id"]
    stock_id = data["stock_id"]
    shares = data["shares"]
    user = session.query(User).filter_by(id=user_id).first()
    portfolio = Portfolio(user_id=user_id, stock_id=stock_id, shares=shares, user=user)

    session.add(portfolio)
    session.commit()

    return jsonify(
        {"status": "success", "message": f"Stock {user.name} added successfully"}
    )
