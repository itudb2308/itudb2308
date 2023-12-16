from flask import Blueprint, request, render_template, flash, session, redirect, url_for
from service.UserService import UserService
from validation.AdminAuth import adminAuth, ADMIN_NOT_AUTHENTICATED


def AdminUsersBlueprint(name: str, importName: str, service: UserService):
    bp = Blueprint(name, importName)

    @bp.before_request
    def before_request():
        try:
            adminAuth(session)
        except Exception as e:
            if e.args[0] == ADMIN_NOT_AUTHENTICATED:
                return redirect(url_for('admin.loginPage'))

    @bp.route('/', methods=["GET"])
    def usersPage():
        querySettings = request.args.to_dict()
        result = service.usersPage(querySettings)
        return render_template('users.html', querySettings=querySettings, **result)

    @bp.route('/delete_user/<int:id>', methods=["GET"])
    def deleteUserPage(id):
        result = service.deleteUserPage(id)
        showFlashMessages(result["flash"])
        return redirect(url_for('admin.users.usersPage'))

    @bp.route('/<int:id>', methods=["GET"])
    def userDetailPage(id: str):
        result = service.userDetailPage(int(id))
        return render_template('userDetail.html', **result)

    @bp.route('/events/<int:id>', methods=["GET"])
    def eventDetailPage(id: str):
        result = service.eventDetailPage(int(id))
        return render_template('eventDetail.html', **result)

    def showFlashMessages(flashMessages):
        if flashMessages != None:
            for flashMessage in flashMessages:
                flash(flashMessage[0], flashMessage[1])

    return bp
