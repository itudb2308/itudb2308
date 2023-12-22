from flask import Blueprint, request, render_template, session, redirect, url_for
from service.ProductService import ProductService
from service.TransactionService import TransactionService


def CustomerProductsBlueprint(name: str, importName: str, transactionService: TransactionService, service: ProductService):
    bp = Blueprint(name, importName)

    # only GET method for now

    @bp.route('/<int:id>', methods=["GET"])
    def productDetailPage(id):
        # when there is no product with given id database returns None.
        # DTO constructor raises TypeError when None is passed as argument.
        # So we catch the TypeError and return 404 Not Found page.
        try:
            product = service.getUserProductDetailPage(id)
        except TypeError:
            return render_template('404.html')

        return render_template('customerProductDetail.html', product=product)

    @bp.route('/', methods=["GET"])
    def productPage():
        querySettings = request.args.to_dict()
        products = service.productsPage(querySettings)
        if products is None:
            return render_template('404.html')
        return render_template('customerIndex.html', querySettings=querySettings, **products)

    @bp.route('/department/<string:department>/category/<string:category>', methods=["GET", "POST"])
    def customerCategoryDepartmentPage(category, department):

        if request.method == "POST" and request.form.get("brand") is not None:
            brand = request.form.get("brand")
            return redirect(url_for('customer.products.customerCategoryDepartmentBrandPage', category=category, department=department, brand=brand))

        querySettings = request.args.to_dict()
        querySettings["category"] = category
        querySettings["department"] = department

        result = service.productCategoryDepartmentPage(querySettings)

        return render_template('category-department.html', querySettings=querySettings, **result)

    @bp.route('department/<string:department>/category/<string:category>/brand/<string:brand>', methods=["GET"])
    def customerCategoryDepartmentBrandPage(category, department, brand):
        querySettings = request.args.to_dict()

        querySettings["category"] = category
        querySettings["department"] = department
        querySettings["brand"] = brand

        result = service.productsPage(querySettings=querySettings)
        return render_template('category-department-brand.html', querySettings=querySettings, **result)

    return bp
