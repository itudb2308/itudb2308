from flask import Blueprint, request, render_template
from service.DistributionCenterService import DistributionCenterService

def DistributionCentersBlueprint(name: str, importName: str, service):
    bp = Blueprint(name, importName)

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
