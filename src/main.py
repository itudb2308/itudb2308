import psycopg2
from flask import Flask, render_template
from blueprints.AdminBlueprint import AdminBlueprint

connection = psycopg2.connect(
    host = "localhost",
    database = "postgres",
    user = "postgres",
    password = "postgres"
)

app = Flask(__name__)
app.register_blueprint(AdminBlueprint("admin", __name__, connection), url_prefix="/admin")

@app.route('/', methods = ['GET'])
def homePage():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
