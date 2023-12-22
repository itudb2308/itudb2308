from flask import Blueprint, request, render_template, session, redirect, url_for, flash
from service.DistributionCenterService import DistributionCenterService
from service.TransactionService import TransactionService


def AdminDistributionCentersBlueprint(name: str, importName: str, transactionService: TransactionService, service: DistributionCenterService):
    bp = Blueprint(name, importName)

    @bp.route('/', methods=["POST", "GET"])
    def distributionCentersPage():
        querySettings = request.args.to_dict()
        result = service.distributionCentersPage(querySettings)
        return render_template('distributionCenters.html', **result)

    @bp.route('/<int:id>', methods=["GET"])
    def distributionCenterDetailPage(id):
        result = service.distributionCenterDetailPage(id)
        return render_template('distributionCenterDetail.html', **result)

    @bp.route('/add', methods=["POST", "GET"])
    def addDistributionCenterPage():
        method = request.method
        form = request.form

        result = service.addDistributionCenterPage(method, form)

        if result["submitted_and_valid"]:
            showFlashMessages(result["flash"])
            return redirect(url_for('admin.distributionCenters.distributionCenterDetailPage', id=result['id']))
        else:
            showFlashMessages(result["flash"])
            return render_template('addDistributionCenter.html', **result)

    @bp.route('/update/<int:id>', methods=["POST", "GET"])
    def updateDistributionCenterPage(id):
        method = request.method
        form = request.form

        result = service.updateDistributionCenterPage(id, method, form)

        if result["submitted_and_valid"]:
            showFlashMessages(result["flash"])
            return redirect(url_for('admin.distributionCenters.distributionCenterDetailPage', id=id))
        else:
            showFlashMessages(result["flash"])
            return render_template('updateDistributionCenter.html', **result)

    @bp.route('/delete/<int:id>', methods=["GET", "POST"])
    def deleteDistributionCenter(id):
        service.deleteDistributionCenterPage(id)
        flash(f"Distribution Center with id {id} deleted successfully", "success")
        return redirect(url_for('admin.distributionCenters.distributionCentersPage'))

    def showFlashMessages(flashMessages):
        if flashMessages != None:
            for flashMessage in flashMessages:
                flash(flashMessage[0], flashMessage[1])

    return bp
