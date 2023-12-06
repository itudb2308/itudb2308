from flask import Blueprint, request, render_template, session, redirect, url_for
from service.UserService import UserService
from validation.auth import adminAuth, ADMIN_NOT_AUTHORIZED

def UsersBlueprint(name: str, importName: str, service: UserService):
    bp = Blueprint(name, importName)

    @bp.before_request
    def before_request():
        try:
            adminAuth(session)
        except Exception as e:
            if e.args[0] == ADMIN_NOT_AUTHORIZED:
                return redirect(url_for('admin.loginPage'))

    @bp.route('/', methods = ["GET"])
    def usersPage():
        querySettings = request.args.to_dict()
        result = service.usersPage(querySettings)
        return render_template('users.html', querySettings=querySettings, **result)

    @bp.route('/<int:id>', methods = ["GET"])
    def userDetailPage(id: str):
        result = service.userDetailPage(int(id))
        return render_template('userDetail.html', **result)
    
    @bp.route('/events/<int:id>', methods = ["GET"])
    def eventDetailPage(id: str):
        result = service.eventDetailPage(int(id))
        return render_template('eventDetail.html', **result)

    return bp