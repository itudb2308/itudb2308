from flask import Blueprint, request, render_template, session, redirect, url_for
from service.UserService import UserService

def UsersBlueprint(name: str, importName: str, service):
    bp = Blueprint(name, importName)

    @bp.route('/', methods = ["GET"])
    def usersPage():
        querySettings = request.args.to_dict()
        result = service.usersPage(querySettings)
        return render_template('users.html', querySettings=querySettings, **result)

    @bp.route('/<int:id>', methods = ["GET"])
    def userDetailPage(id: str):
        result = service.userDetailPage(int(id))
        return render_template('userDetail.html', **result)
    
    @bp.route('/login', methods=["GET","POST"])
    def loginPage():
        if request.method == "GET":
            return render_template('login.html')
        elif request.method == "POST":
            email = request.form["email"]
            password = request.form["password"]
            if email == 'admin@admin.net' and password == 'admin':
                session["user"] = 'admin'
                return redirect(url_for('homePage'))
            else:
                return redirect(url_for('admin.users.loginPage'))


    return bp