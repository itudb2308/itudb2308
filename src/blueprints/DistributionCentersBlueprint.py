from flask import Blueprint, request, render_template, session, redirect, url_for
from service.DistributionCenterService import DistributionCenterService
from validation.auth import adminAuth, ADMIN_NOT_AUTHORIZED

def DistributionCentersBlueprint(name: str, importName: str, service):
    bp = Blueprint(name, importName)

    @bp.before_request
    def before_request():
        try:
            adminAuth(session)
        except Exception as e:
            if e.args[0] == ADMIN_NOT_AUTHORIZED:
                return redirect(url_for('admin.loginPage'))

    @bp.route('/', methods = ["POST","GET"])
    def distributionCentersPage():
        querySettings = request.args.to_dict()
        result = service.distributionCentersPage(querySettings)
        return render_template('distributionCenters.html', **result)

    @bp.route('/<int:id>', methods = ["GET"])
    def distributionCenterDetailPage(id):
        result = service.distributionCenterDetailPage(id)
        return render_template('distributionCenterDetail.html', **result)

    return bp
