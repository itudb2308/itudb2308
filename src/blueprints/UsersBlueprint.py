from sqlite3 import Connection
from flask import Blueprint, request, render_template
from repository.UserRepository import UserRepository

def UsersBlueprint(name: str, importName: str, connection: Connection):
    bp = Blueprint(name, importName)
    repository = UserRepository(connection)

    @bp.route('/', methods = ["GET", "POST"])
    def usersPage():
        if request.method == "POST":
            settings = request.form.to_dict()
            users = repository.getAll(**settings)
            return render_template('users.html', users = users)
        else:
            return render_template('users.html')

    @bp.route('/<id>', methods = ["GET"])
    def userDetailPage(id: str):
        user = repository.findById(int(id))
        user_info = []
        for infos in user:
            user_info.append(infos)
        return user_info

    return bp