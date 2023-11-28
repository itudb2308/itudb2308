from flask import Blueprint, request, render_template
from repository.UserRepository import UserRepository
from dto.User import User

def UsersBlueprint(name: str, importName: str, connection):
    bp = Blueprint(name, importName)
    repository = UserRepository(connection)
    countryArray = [s[0] for s in repository.getDistinctCountry()]

    @bp.route('/', methods = ["GET", "POST"])
    def usersPage():
        settings = request.form.to_dict()
        users = repository.getAll(**settings)
        return render_template('users.html', users = users, countryArray = countryArray)

    @bp.route('/<id>', methods = ["GET"])
    def userDetailPage(id: str):
        return render_template('userDetail.html', user = User(repository.findById(int(id))))

    return bp