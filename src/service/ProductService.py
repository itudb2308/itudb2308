from dto.Product import Product
from repository.ProductRepository import ProductRepository

class ProductService:
    def __init__(self, connection) -> None:
        self.repository = ProductRepository(connection)

    # PAGE METHODS
    def productsPage(self, querySettings: dict) -> dict:
        result = dict()
        result["products"] = self.getAll(querySettings)
        result["columnNames"] = self.getColumnNames()
        result["categories"] = self.getCategories()
        return result

    def productDetailPage(self, id: int) -> dict:
        result = dict()
        result["product"] = self.findById(id)
        return result

    # SERVICE METHODS
    def findById(self, id: int) -> Product:
        return Product(self.repository.findById(id))

    def getAll(self, settings: dict) -> [Product]:
        return [Product(p) for p in self.repository.getAll(**settings)]

    def getColumnNames(self) -> [str]:
        return [cn[0] for cn in self.repository.getColumnNames()]

    def getCategories(self) -> [str]:
        return [c[0] for c in self.repository.getCategories()]
