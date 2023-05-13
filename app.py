import threading
from flask import Flask, render_template


# from api.models import Session, Stock, User, Portfolio, Order
from api.stocks import stocks
from api.orders import orders
from api.users import users
from api.Portfolio import portfolios
from api.orderb import ppp

# from orderbook import update_prices

# from api.orders import app
# from api.users import app

app = Flask(__name__)
app.register_blueprint(stocks)
app.register_blueprint(orders)
app.register_blueprint(users)
app.register_blueprint(portfolios)
app.register_blueprint(ppp)


@app.route("/")
def hello_world():
    return render_template("index.html", title="Hello")


if __name__ == "__main__":
    # Start the background task to update prices
    # update_prices()
    # t = threading.Thread(target=update_prices)
    print('start')
    # t.start()
    app.run()
