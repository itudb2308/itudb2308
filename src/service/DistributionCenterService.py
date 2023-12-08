from repository.DistributionCenterRepository import DistributionCenterRepository
from dto.DistributionCenter import DistributionCenter

from forms.DistributionCenterForm import DistributionCenterForm , UpdateDistributionCenterForm

class DistributionCenterService:
    def __init__(self, distributionCenterRepository: DistributionCenterRepository):
        self.distributionCenterRepository = distributionCenterRepository

    # PAGE METHODS
    def distributionCentersPage(self, querySettings: dict) -> dict:
        result = dict()
        result["distributionCenters"] = self.getAll(querySettings)
        return result

    def distributionCenterDetailPage(self, id: int) -> dict:
        result = dict()
        result["distributionCenter"] = self.findById(id)
        return result
    def addDistributionCenterPage(self, method: str, form: dict) -> dict:
        result = { "submitted_and_valid" : False, "flash" : [] , "form" : None}

        if method == "GET":
            result["submitted_and_valid"] = False
            result["form"] = DistributionCenterForm()
        else :
            form = DistributionCenterForm(form)

            if form.validate_on_submit():
                distributionCenter = form.data
                # add product to database
                result["submitted_and_valid"] = True
                result["id"] = self.distributionCenterRepository.addDistributionCenter(distributionCenter)
                result["flash"].append(("Distribution Center added successfully", "success"))

            else :
                result["submitted_and_valid"] = False
                result["flash"].append(("Form data is invalid", "danger"))
                for fieldName, errorMessages in form.errors.items():
                    for err in errorMessages:
                        result["flash"].append((f"{fieldName}: {err}", "danger"))
                result["form"] = form

        return result
    
    def updateDistributionCenter(self, id: int, method: str, form) -> dict:
        result = { "submitted_and_valid" : False, "flash" : [] , "form" : None, "id" : id}
        print(f" method : {method} , form : {form}")
        if method == "GET":
            distributionCenter = self.findById(id)
            formData = {"id" : distributionCenter.id, "name" : distributionCenter.name, "latitude" : distributionCenter.latitude, "longitude" : distributionCenter.longitude}
            
            form = UpdateDistributionCenterForm(formData)
            result["form"] = form
            result["submitted_and_valid"] = False
            
        else :
            form = UpdateDistributionCenterForm(form)

            if form.validate_on_submit():
                print("Form is valid")
                distributionCenter = form.data
                distributionCenter["id"] = id
                print(f"form data: {distributionCenter}")
                # add product to database
                result["submitted_and_valid"] = True
                result["id"] = self.distributionCenterRepository.updateDistributionCenter(distributionCenter)
                result["flash"].append(("Distribution Center updated successfully", "success"))
            else :
                result["submitted_and_valid"] = False
                result["flash"].append(("Form data is invalid", "danger"))
                for fieldName, errorMessages in form.errors.items():
                    for err in errorMessages:
                        result["flash"].append((f"{fieldName}: {err}", "danger"))
                result["form"] = form

        return result

    # may be success or failure message depending on the result of the delete operation can be returned
    def deleteDistributionCenter(self, id: int) : 
        return self.distributionCenterRepository.deleteDistributionCenter(id)


    # SERVICE METHODS
    def findById(self, id: int) -> DistributionCenter:
        return DistributionCenter(self.distributionCenterRepository.findById(id))

    def getAll(self, settings: dict) -> [DistributionCenter]:
        return [DistributionCenter(dc) for dc in self.distributionCenterRepository.getAll(**settings)]
