from flask import Blueprint, request, redirect, render_template, session, url_for
from blueprints.CustomerOrdersBlueprint import CustomerOrdersBlueprint
from blueprints.CustomerProductsBlueprint import CustomerProductsBlueprint
from blueprints.CustomerUsersBlueprint import CustomerUsersBlueprint
from service.TransactionService import TransactionService


def CustomerBlueprint(name: str, importName: str, services: dict):
    bp = Blueprint(name, importName)
    transactionService: TransactionService = services["transaction"]

    customerOrdersBP = CustomerOrdersBlueprint("orders", __name__, transactionService, services["order"])
    customerProductsBP = CustomerProductsBlueprint("products", __name__, transactionService, services["product"])
    customerUsersBP = CustomerUsersBlueprint("users", __name__, transactionService, services["user"])

    bp.register_blueprint(customerOrdersBP, url_prefix="/orders")
    bp.register_blueprint(customerProductsBP, url_prefix="/products")
    bp.register_blueprint(customerUsersBP, url_prefix="")

    @bp.before_request
    def before_request():
        if request.endpoint != 'customer.loginPage' and request.endpoint != 'customer.users.signUpPage':
            isLogged: str = session.get("user_logged_in")
            if isLogged == None or isLogged == False:
                return redirect(url_for('customer.loginPage'))
            session["uri"] = request.path
            services["user"].addEvent(session)
            session["sequence_number"] += 1

    @bp.route('/', methods=['GET'])
    def indexPage():
        return redirect(url_for('customer.homePage'))

    @bp.route('/home', methods=['GET'])
    def homePage():
        categories = services["product"].getCategoriesPage()
        return render_template('homePage.html', categories=categories)

    @bp.route('/login', methods=["GET", "POST"])
    def loginPage():
        if request.method == "GET":
            if session.get("user_logged_in") == True:
                return redirect(url_for('customer.homePage'))
            else:
                session["user_logged_in"] = False
                return render_template('customerLogin.html')
        elif request.method == "POST":
            try:
                email = request.form['email']
                password = request.form["password"]
                if email != password:
                    raise Exception("Email or Password is wrong")

                user = services["user"].customerLoginPage(email)
                sessionHandleUserLogin(user)
                return redirect(url_for('customer.homePage'))
            except Exception as e:
                # TODO: show flash messages such as user logged in, password is wrong etc
                return redirect(url_for('customer.loginPage'))

    @bp.route('/logout', methods=["GET"])
    def logoutPage():
        if request.method == "GET":
            session.clear()
            return redirect(url_for('customer.homePage'))

    def sessionHandleUserLogin(user):
        session["user_id"] = user.id
        session["name"] = user.first_name + " " + user.last_name
        session["user_logged_in"] = True
        session["session_id"] = services["user"].sessionIdGenerator()
        session["sequence_number"] = 1
        session["cart"] = {}

        return session

    return bp
