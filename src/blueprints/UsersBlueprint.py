from sqlite3 import Connection
from flask import Blueprint, request, render_template
from repository.UserRepository import UserRepository

def UsersBlueprint(name: str, importName: str, connection: Connection):
    bp = Blueprint(name, importName)
    repository = UserRepository(connection)

    @bp.route('/', methods = ["GET"])
    def usersPage():
        return render_template('users.html')


    @bp.route('/searchUsers', methods = ["POST"])
    def getAll():
        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/json'):
            return repository.getAll(**request.get_json())
        else:
            return 'Content-Type not supported!'

    return bp