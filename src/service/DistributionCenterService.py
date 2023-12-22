from dto.Transaction import Transaction
from repository.DistributionCenterRepository import DistributionCenterRepository
from dto.DistributionCenter import DistributionCenter

from forms.DistributionCenterForm import DistributionCenterForm, UpdateDistributionCenterForm


class DistributionCenterService:
    def __init__(self, repositories: dict):
        self._distributionCenterRepository: DistributionCenterRepository = repositories["distributionCenter"]

    # PAGE METHODS
    def distributionCentersPage(self, querySettings: dict, **kwargs) -> dict:
        transaction = kwargs["transaction"]
        result = dict()
        result["distributionCenters"] = self.getAll(transaction, querySettings)
        return result

    def distributionCenterDetailPage(self, id: int, **kwargs) -> dict:
        transaction = kwargs["transaction"]
        result = dict()
        result["distributionCenter"] = self.findById(transaction, id)
        return result

    def addDistributionCenterPage(self, method: str, form: dict, **kwargs) -> dict:
        transaction = kwargs["transaction"]
        result = {"submitted_and_valid": False, "flash": [], "form": None}

        if method == "GET":
            result["submitted_and_valid"] = False
            result["form"] = DistributionCenterForm()
        else:
            form = DistributionCenterForm(form)

            if form.validate_on_submit():
                distributionCenter = form.data
                # add product to database
                result["submitted_and_valid"] = True
                result["id"] = self._distributionCenterRepository.addDistributionCenter(transaction, distributionCenter)
                result["flash"].append(("Distribution Center added successfully", "success"))

            else:
                result["submitted_and_valid"] = False
                result["flash"].append(("Form data is invalid", "danger"))
                for fieldName, errorMessages in form.errors.items():
                    for err in errorMessages:
                        result["flash"].append((f"{fieldName}: {err}", "danger"))
                result["form"] = form

        return result

    def updateDistributionCenterPage(self, id: int, method: str, form, **kwargs) -> dict:
        transaction = kwargs["transaction"]
        result = {"submitted_and_valid": False, "flash": [], "form": None, "id": id}
        if method == "GET":
            distributionCenter = self.findById(transaction, id)
            formData = {"id": distributionCenter.id, "name": distributionCenter.name, "latitude": distributionCenter.latitude, "longitude": distributionCenter.longitude}

            form = UpdateDistributionCenterForm(formData)
            result["form"] = form
            result["submitted_and_valid"] = False

        else:
            form = UpdateDistributionCenterForm(form)

            if form.validate_on_submit():
                distributionCenter = form.data
                distributionCenter["id"] = id
                # add product to database
                result["submitted_and_valid"] = True
                result["id"] = self._distributionCenterRepository.updateDistributionCenter(transaction, distributionCenter)
                result["flash"].append(("Distribution Center updated successfully", "success"))
            else:
                result["submitted_and_valid"] = False
                result["flash"].append(("Form data is invalid", "danger"))
                for fieldName, errorMessages in form.errors.items():
                    for err in errorMessages:
                        result["flash"].append((f"{fieldName}: {err}", "danger"))
                result["form"] = form

        return result

    # may be success or failure message depending on the result of the delete operation can be returned
    def deleteDistributionCenterPage(self, id: int, **kwargs):
        transaction = kwargs["transaction"]
        return self._distributionCenterRepository.deleteDistributionCenter(transaction, id)

    # SERVICE METHODS

    def findById(self, transaction: Transaction, id: int) -> DistributionCenter:
        return DistributionCenter(self._distributionCenterRepository.findById(transaction, id))

    def getAll(self, transaction: Transaction, settings: dict) -> [DistributionCenter]:
        return [DistributionCenter(dc) for dc in self._distributionCenterRepository.getAll(transaction, **settings)]
