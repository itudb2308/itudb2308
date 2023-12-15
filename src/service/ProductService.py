from dto.Product import Product
from repository.ProductRepository import ProductRepository
from repository.InventoryItemRepository import InventoryItemRepository

from forms.AddProductForm import AddProductForm
from forms.UpdateProductForm import UpdateProductForm
from service.Common import getPaginationObject, handleLimitAndOffset


class ProductService:
    def __init__(self, productRepository: ProductRepository,
                 inventoryItemRepository: InventoryItemRepository) -> None:
        self.productRepository = productRepository
        self.inventoryItemRepository = inventoryItemRepository
        self.distributionCenterService = None

    # PAGE METHODS
    def productsPage(self, querySettings: dict) -> dict:
        result = dict()
        products, count = self.getAllAndCount(querySettings)
        result["products"] = products
        result["pagination"] = getPaginationObject(count, querySettings)
        result["columnNames"] = self.getColumnNames()
        result["categories"] = self.getCategories()
        return result

    def productDetailPage(self, id: int) -> dict:
        result = dict()
        result["product"] = self.findById(id)
        result["totalStock"] = self.inventoryItemRepository.getTotalStock(id, result["product"].distribution_center_id )
        result["totalSold"] = self.inventoryItemRepository.getTotalSold(id, result["product"].distribution_center_id )
        return result

    # returns newly added products id
    def addProductPage(self, method, form) -> int:
        # flash holds tuples of (message, category)
        result = {"submitted_and_valid": False, "flash": [], "form": None}

        if method == "GET":
            result["submitted_and_valid"] = False
            result["form"] = AddProductForm(self)
        else:
            form = AddProductForm(self, form)

            if form.validate_on_submit():
                product = form.data
                # add product to database
                result["submitted_and_valid"] = True
                result["id"] = self.addProduct(product)
                # redirect to product detail page of the newly added product
                # add flash messages to this message ("Product added successfully", "success")
                result["flash"].append(("Product added successfully", "success"))

            else:
                result["submitted_and_valid"] = False
                result["flash"].append(("Form data is invalid", "danger"))
                for fieldName, errorMessages in form.errors.items():
                    for err in errorMessages:
                        result["flash"].append((f"{fieldName}: {err}", "danger"))
                result["form"] = form
        return result

    # returns the id of the added product
    def addProduct(self, product: dict) -> int:
        return self.productRepository.addProduct(product)

    def updateProductPage(self, method, form, id) -> int:
        result = {"submitted_and_valid": False, "flash": [], "form": None}

        if method == "GET":
            product = self.findById(id).toDict()

            result["form"] = UpdateProductForm(self, product)
        else:
            form = UpdateProductForm(self, form)

            if form.validate_on_submit():
                product = form.data
                # add id to product such that repository can use it to update the product
                product["id"] = id
                # update product on database
                id = self.productRepository.updateProduct(product)
                result["submitted_and_valid"] = True
                result["flash"].append(("Product updated successfully", "success"))

            else:
                result["flash"].append(("Form data is invalid", "danger"))
                for fieldName, errorMessages in form.errors.items():
                    for err in errorMessages:
                        result["flash"].append((f"{fieldName}: {err}", "danger"))
                result["form"] = form
        return result

    def deleteProductPage(self, id: int) -> dict:
        result = dict()
        result["id"] = self.deleteProduct(id)
        result["flash"] = [("Product deleted successfully", "success")]
        return result

    # SERVICE METHODS
    def findById(self, id: int) -> Product:
        return Product(self.productRepository.findById(id))

    def getAllAndCount(self, settings: dict) -> ([Product], int):
        settings = handleLimitAndOffset(settings)
        data = self.productRepository.getAllAndCount(**settings)
        products = [Product(p) for p in data]
        count = data[0][-1] if len(data) > 1 else 0
        return products, count

    def getColumnNames(self) -> [str]:
        return [cn[0] for cn in self.productRepository.getColumnNames()]

    def getCategories(self) -> [str]:
        return [c[0] for c in self.productRepository.getCategories()]

    # returns array of DistributionCenter data transfer objects
    def getDistributionCenters(self, settings: dict) -> [str]:
        return self.distributionCenterService.getAll(settings)

    def getBrandNames(self) -> [str]:
        return [b[0] for b in self.productRepository.getBrandNames()]

    def deleteProduct(self, id: int) -> int:
        return self.productRepository.deleteProductById(id)
