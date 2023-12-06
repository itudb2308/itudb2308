from .ProductForm import ProductForm

class AddProductForm(ProductForm):
    def __init__(self, service, *args, **kwargs):
        super(AddProductForm, self).__init__(service, *args, **kwargs)
        self.submit.label.text = "Add Product"
