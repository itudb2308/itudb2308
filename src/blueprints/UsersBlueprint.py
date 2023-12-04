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

    return bp