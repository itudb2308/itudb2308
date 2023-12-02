from repository.DistributionCenterRepository import DistributionCenterRepository
from dto.DistributionCenter import DistributionCenter

class DistributionCenterService:
    def __init__(self, connection):
        self.repository = DistributionCenterRepository(connection)

    # PAGE METHODS
    def distributionCentersPage(self, querySettings: dict) -> dict:
        result = dict()
        result["distributionCenters"] = self.getAll(querySettings)
        return result

    def distributionCenterDetailPage(self, id: int) -> dict:
        result = dict()
        result["distributionCenter"] = self.findById(id)
        return result

    # SERVICE METHODS
    def findById(self, id: int) -> DistributionCenter:
        return DistributionCenter(self.repository.findById(id))

    def getAll(self, settings: dict) -> [DistributionCenter]:
        return [DistributionCenter(dc) for dc in self.repository.getAll(**settings)]
