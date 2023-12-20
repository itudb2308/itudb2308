from flask import Blueprint, request, redirect, render_template, session, url_for
from blueprints.CustomerOrdersBlueprint import CustomerOrdersBlueprint
from blueprints.CustomerProductsBlueprint import CustomerProductsBlueprint
from blueprints.CustomerUsersBlueprint import CustomerUsersBlueprint
from validation.CustomerAuth import customerAuth, CUSTOMER_NOT_AUTHENTICATED


def CustomerBlueprint(name: str, importName: str, services: dict):
    bp = Blueprint(name, importName)

    bp.register_blueprint(CustomerOrdersBlueprint("orders", __name__, services["order"]), url_prefix="/orders")
    bp.register_blueprint(CustomerProductsBlueprint("products", __name__, services["product"]), url_prefix="/products")
    bp.register_blueprint(CustomerUsersBlueprint("users", __name__, services["user"]), url_prefix="")

    @bp.before_request
    def before_request():
        if request.endpoint != 'customer.loginPage' and request.endpoint != 'customer.users.signUpPage':
            try:
                customerAuth(session)
                session["uri"] = request.path
                services["user"].addEvent(session)
                session["sequence_number"] += 1
            except Exception as e:
                if e.args[0] == CUSTOMER_NOT_AUTHENTICATED:
                    return redirect(url_for('customer.loginPage'))
    '''        
        @bp.route('/home', methods=['GET'])
        def homePage():
            querySettings = request.args.to_dict()
            products = services["product"].productsPage(querySettings)
            if products is None:
                return render_template('404.html')
            return render_template('customerIndex.html', querySettings=querySettings, **products)
    '''

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
        return session

    return bp
