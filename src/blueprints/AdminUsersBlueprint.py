from flask import Blueprint, request, render_template, flash, session, redirect, url_for
from service.UserService import UserService


def AdminUsersBlueprint(name: str, importName: str, service: UserService):
    bp = Blueprint(name, importName)

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
    def eventDetailPage(id: int):
        result = service.eventDetailPage(int(id))
        return render_template('eventDetail.html', **result)

    @bp.route('/delete_event/<int:id>', methods=["GET"])
    def deleteEventPage(id: int):
        service.deleteEventPage(id)
        return redirect(url_for('admin.users.usersPage', id=id))

    def showFlashMessages(flashMessages):
        if flashMessages != None:
            for flashMessage in flashMessages:
                flash(flashMessage[0], flashMessage[1])

    return bp
