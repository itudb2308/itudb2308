from .ProductForm import ProductForm

class UpdateProductForm(ProductForm):
    def __init__(self, service, *args, **kwargs):
        super(UpdateProductForm, self).__init__(service, *args, **kwargs)
        self.submit.label.text = "Update Product"
