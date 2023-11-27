from flask import Blueprint, request, render_template
from repository.UserRepository import UserRepository
from dto.User import User

def UsersBlueprint(name: str, importName: str, connection):
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
        return render_template('userDetail.html', user = User(repository.findById(int(id))))

    return bp