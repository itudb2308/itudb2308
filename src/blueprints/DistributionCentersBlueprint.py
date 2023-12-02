from flask import Blueprint, request, render_template
from repository.DistributionCentersRepository import DistributionCentersRepository
from dto.DistributionCenter import DistributionCenter

def DistributionCentersBlueprint(name: str, importName: str, connection):
    bp = Blueprint(name, importName)
    repository = DistributionCentersRepository(connection)
    
    @bp.route('/', methods = ["POST","GET"])
    def distributionCentersPage():
        settings = request.args.to_dict()
        fetchedProducts = repository.getAll(**settings)
        distributionCenters = [DistributionCenter(p) for p in fetchedProducts]

        return render_template('distributionCenters.html', distributionCenters = distributionCenters )
    
    @bp.route('/<int:id>', methods = ["GET"])
    def distributionCenterDetailPage(id):
        return render_template('distributionCenterDetail.html',distributionCenter = DistributionCenter(repository.findById(int(id))) )

    return bp

    
