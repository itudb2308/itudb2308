from dto.Product import Product
from repository.ProductRepository import ProductRepository
from repository.InventoryItemRepository import InventoryItemRepository

class ProductService:
    def __init__(self, productRepository: ProductRepository,
                 inventoryItemRepository: InventoryItemRepository) -> None:
        self.productRepository = productRepository
        self.inventoryItemRepository = inventoryItemRepository
        self.distributionCenterService = None

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

    # returns newly added products id
    def addProductPage(self, product: dict) -> int:
        return  self.productRepository.addProduct(product)

    def updateProductPage(self, product: dict) -> int:
        return  self.productRepository.updateProduct(product)


    # SERVICE METHODS
    def findById(self, id: int) -> Product:
        return Product(self.productRepository.findById(id))

    def getAll(self, settings: dict) -> [Product]:
        return [Product(p) for p in self.productRepository.getAll(**settings)]

    def getColumnNames(self) -> [str]:
        return [cn[0] for cn in self.productRepository.getColumnNames()]

    def getCategories(self) -> [str]:
        return [c[0] for c in self.productRepository.getCategories()]

    # returns array of DistributionCenter data transfer objects
    def getDistributionCenters(self, settings : dict ) -> [str]:
        return self.distributionCenterService.getAll(settings) 

    def getBrandNames(self) -> [str]:
        return [b[0] for b in self.productRepository.getBrandNames()]    