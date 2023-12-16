from flask import Blueprint, request, render_template, flash, session, redirect, url_for
from service.UserService import UserService
from validation.CustomerAuth import customerAuth, CUSTOMER_NOT_AUTHENTICATED


def CustomerUsersBlueprint(name: str, importName: str, service: UserService):
    bp = Blueprint(name, importName)

    @bp.before_request
    def before_request():
        try:
            customerAuth(session)
        except Exception as e:
            if e.args[0] == CUSTOMER_NOT_AUTHENTICATED:
                if request.url == 'http://localhost:5000/signup':
                    pass
                else:
                    return redirect(url_for('customer.loginPage'))

    @bp.route('/profile/<int:id>', methods=["GET", "POST"])
    def userPage(id: int):
        if request.method == "GET":
            result = service.userDetailPage(id)
            if result["user"] == None:
                return render_template("404.html")
            return render_template('customerUserDetail.html', **result)
        else:
            pass

    @bp.route('/signup', methods=["GET", "POST"])
    def signUpPage():
        form = request.form
        method = request.method
        result = service.signUpPage(method, form)
        if result["submitted_and_valid"] == True:
            showFlashMessages(result["flash"])
            return redirect(url_for('customer.users.userPage', id=result["id"]))
        else:
            showFlashMessages(result["flash"])
            return render_template('customerSignUp.html', form=result["form"])

    def showFlashMessages(flashMessages):
        if flashMessages != None:
            for flashMessage in flashMessages:
                flash(flashMessage[0], flashMessage[1])
    return bp
