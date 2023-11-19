import sqlite3
from flask import Flask, render_template
from blueprints.OrdersBlueprint import OrdersBlueprint
from blueprints.UsersBlueprint import UsersBlueprint

connection = sqlite3.connect("./src/db/db.sqlite", check_same_thread=False)

app = Flask(__name__)
app.register_blueprint(OrdersBlueprint("orders", __name__, connection), url_prefix="/orders")
app.register_blueprint(UsersBlueprint("users",__name__,connection), url_prefix="/users")

@app.route('/', methods = ['GET'])
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
