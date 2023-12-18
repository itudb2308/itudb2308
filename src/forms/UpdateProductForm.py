from dto.Transaction import Transaction
from .ProductForm import ProductForm


class UpdateProductForm(ProductForm):
    def __init__(self, service, transaction: Transaction, *args, **kwargs):
        super(UpdateProductForm, self).__init__(service, transaction, *args, **kwargs)
        self.submit.label.text = "Update Product"
