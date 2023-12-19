from dto.Transaction import Transaction
from .ProductForm import ProductForm


class AddProductForm(ProductForm):
    def __init__(self, service, transaction: Transaction, *args, **kwargs):
        super(AddProductForm, self).__init__(service, transaction, *args, **kwargs)
        self.submit.label.text = "Add Product"
