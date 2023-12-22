import typing
from dto.Product import Product, UserProduct
from dto.Transaction import Transaction
from repository.ProductRepository import ProductRepository
from repository.InventoryItemRepository import InventoryItemRepository
from forms.AddProductForm import AddProductForm
from forms.UpdateProductForm import UpdateProductForm

if typing.TYPE_CHECKING:
    from service.DistributionCenterService import DistributionCenterService


class ProductService:
    def __init__(self, repositories: dict) -> None:
        self._productRepository: ProductRepository = repositories["product"]
        self._inventoryItemRepository: InventoryItemRepository = repositories["inventoryItem"]
        self._distributionCenterService: DistributionCenterService = None

    def setDistributionCenterService(self, distributionCenterService):
        self._distributionCenterService = distributionCenterService

    # PAGE METHODS
    def productsPage(self, querySettings: dict, **kwargs) -> dict:
        transaction = kwargs["transaction"]
        result = dict()
        products, count = self.getAllAndCount(transaction, querySettings)
        result["products"] = products
        result["pagination"] = getPaginationObject(count, querySettings)
        result["columnNames"] = self.getColumnNames(transaction)
        result["categories"] = self.getCategories(transaction)
        return result

    def productDetailPage(self, id: int, **kwargs) -> dict:
        transaction = kwargs["transaction"]
        result = dict()
        result["product"] = self.findById(transaction, id)
        stockAndSold = self._inventoryItemRepository.getTotalStockAndSold(transaction, id, result["product"].distribution_center_id)
        result["totalStock"] = stockAndSold[0][0]
        result["totalSold"] = stockAndSold[0][1]
        return result

    # given query settings includign filters and category and department
    # returns the result dict that contains the products, brands, pagination, columnNames, categories
    def productCategoryDepartmentPage(self, querySettings: dict, **kwargs) -> dict:
        transaction = kwargs["transaction"]
        result = dict()
        result["brands"] = self.getBrandNamesByCategoryAndDepartment(querySettings["category"], querySettings["department"], transaction)
        result["products"], count = self.getAllAndCount(transaction, querySettings)
        result["pagination"] = getPaginationObject(count, querySettings)
        result["columnNames"] = self.getColumnNames(transaction)
        result["categories"] = self.getCategories(transaction)

        return result

    # returns newly added products id

    def addProductPage(self, method, form, **kwargs) -> int:
        transaction = kwargs["transaction"]

        # flash holds tuples of (message, category)
        result = {"submitted_and_valid": False, "flash": [], "form": None}

        if method == "GET":
            result["submitted_and_valid"] = False
            result["form"] = AddProductForm(self, transaction)
        else:
            form = AddProductForm(self, transaction, form)

            if form.validate_on_submit():
                product = form.data
                # add product to database
                result["submitted_and_valid"] = True
                result["id"] = self.addProduct(transaction, product)
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

    def updateProductPage(self, method, form, id, **kwargs) -> int:
        transaction = kwargs["transaction"]
        result = {"submitted_and_valid": False, "flash": [], "form": None}

        if method == "GET":
            product = self.findById(transaction, id).toDict()

            result["form"] = UpdateProductForm(self, transaction, product)
        else:
            form = UpdateProductForm(self, transaction, form)

            if form.validate_on_submit():
                product = form.data
                # add id to product such that repository can use it to update the product
                product["id"] = id
                # update product on database
                id = self._productRepository.updateProduct(transaction, product)
                result["submitted_and_valid"] = True
                result["flash"].append((f"Product with id = {id} updated successfully", "success"))

            else:
                result["flash"].append(("Form data is invalid", "danger"))
                for fieldName, errorMessages in form.errors.items():
                    for err in errorMessages:
                        result["flash"].append((f"{fieldName}: {err}", "danger"))
                result["form"] = form
        return result

    def deleteProductPage(self, id: int, **kwargs) -> dict:
        transaction = kwargs["transaction"]
        result = dict()
        result["id"] = self.deleteProduct(transaction, id)
        result["flash"] = [("Product deleted successfully", "success")]
        return result

    def getUserProductDetailPage(self, id: int, **kwargs) -> UserProduct | None:
        # return the product information with given id
        transaction = kwargs["transaction"]
        return self.getUserProductById(transaction, id)

    # Function to add stock to a product that is specified with id.

    def addStockToInventoryPage(self, id: int, quantity: int, **kwargs):
        transaction = kwargs["transaction"]
        self.addStockToInventory(transaction, id, quantity)

    # SERVICE METHODS

    def findById(self, transaction: Transaction, id: int) -> Product:
        return Product(self._productRepository.findById(transaction, id))

    def findByIds(self, transaction: Transaction, ids: [int]) -> [Product]:
        return [Product(p) for p in self._productRepository.findByIds(transaction, ids)]

    def getAllAndCount(self, transaction: Transaction, settings: dict) -> ([Product], int):
        settings = handleLimitAndOffset(settings)
        data = self._productRepository.getAllAndCount(transaction, **settings)
        products = [Product(p) for p in data]
        count = data[0][-1] if len(data) > 1 else 0
        return products, count

    def getColumnNames(self, transaction: Transaction) -> [str]:
        return [cn[0] for cn in self._productRepository.getColumnNames(transaction)]

    def getCategoriesPage(self, **kwargs):
        transaction = kwargs["transaction"]
        return self.getCategories(transaction)

    def getCategories(self, transaction: Transaction) -> [str]:
        return [c[0] for c in self._productRepository.getCategories(transaction)]

    # returns array of DistributionCenter data transfer objects
    def getDistributionCenters(self, transaction: Transaction, settings: dict) -> [str]:
        return self._distributionCenterService.getAll(transaction, settings)

    def getBrandNames(self, transaction: Transaction) -> [str]:
        return [b[0] for b in self._productRepository.getBrandNames(transaction)]

    def getBrandNamesByCategoryAndDepartment(self, category: str, department: str, transaction: Transaction) -> [str]:
        return [b[0] for b in self._productRepository.getBrandNamesByCategoryDepartment(transaction, category, department)]

    def deleteProduct(self, transaction: Transaction, id: int) -> int:
        return self._productRepository.deleteProductById(transaction, id)

    # returns the id of the added product
    def addProduct(self, transaction: Transaction, product: dict) -> int:
        return self._productRepository.addProduct(transaction, product)

    # Function to add stock to a product that is specified with id.
    def addStockToInventory(self, transaction: Transaction, id, quantity):
        # get the stocks information

        product = self._productRepository.findById(transaction, id)

        for i in range(quantity):
            self._inventoryItemRepository.addInventoryItem(transaction, product)

        return

    # Given dictionary of product ids and quantities, makes the sold_at field of the inventory item current time
    # and returns the ids of the effected inventory items
    def sellProducts(self, transaction: Transaction, products: dict) -> dict:
        # sell products and update the database
        result = dict()
        for productId, quantity in products.items():
            productId = int(productId)
            idsAndPrices = self._inventoryItemRepository.sellInventoryItem(transaction, productId, quantity)
            result[productId] = {
                "ids": list(map(lambda x: x[0], idsAndPrices)),
                "price": idsAndPrices[0][1]
            }
        return result

    # Given a list of inventory item ids , makes the sold_at field of the inventory item null
    def cancelSale(self, transaction: Transaction, inventory_item_ids: list) -> None:
        for id in inventory_item_ids:
            self._inventoryItemRepository.cancelSale(transaction, id)

    def getUserProductById(self, transaction: Transaction, productId: int) -> UserProduct | None:
        userProduct = self._inventoryItemRepository.getProductDetailByProductId(transaction, productId)
        # TODO: throw exception instead of returning none
        if userProduct is None:
            return None
        return UserProduct(userProduct)
