from flask import Blueprint, request, render_template, flash, session, redirect, url_for
from service.UserService import UserService
from validation.CustomerAuth import customerAuth, CUSTOMER_NOT_AUTHENTICATED


def CustomerUsersBlueprint(name: str, importName: str, service: UserService):
    bp = Blueprint(name, importName)

    @bp.route('/profile', methods=["GET"])
    def userPage():
        if request.method == "GET":
            id = session["user_id"]
            result = service.userDetailPage(id)
            if result["user"] == None:
                return render_template("404.html")
            return render_template('customerUserDetail.html', **result)

    @bp.route('/profile/update', methods=["GET", "POST"])
    def updateUserPage():
        method = request.method
        form = request.form
        id = session["user_id"]
        result = service.updateUserPage(method, form, id)

        if result["submitted_and_valid"] == True:
            showFlashMessages(result["flash"])
            return redirect(url_for('customer.users.userPage', id=id))
        else:
            showFlashMessages(result["flash"])
            return render_template('customerUpdate.html', form=result["form"], id=id)

    @bp.route('/signup', methods=["GET", "POST"])
    def signUpPage():
        form = request.form
        method = request.method
        result = service.signUpPage(method, form)
        if result["submitted_and_valid"] == True:
            showFlashMessages(result["flash"])
            email = request.form['email']
            user = service.customerLoginPage(email)
            sessionHandleUserLogin(user)
            return redirect(url_for('customer.homePage'))
        else:
            showFlashMessages(result["flash"])
            return render_template('customerSignUp.html', form=result["form"])

    def showFlashMessages(flashMessages):
        if flashMessages != None:
            for flashMessage in flashMessages:
                flash(flashMessage[0], flashMessage[1])

    def sessionHandleUserLogin(user):
        session["user_id"] = user.id
        session["name"] = user.first_name + " " + user.last_name
        session["user_logged_in"] = True
        session["session_id"] = service.sessionIdGenerator()
        session["sequence_number"] = 1
        session["cart"] = {}

        return session

    return bp
