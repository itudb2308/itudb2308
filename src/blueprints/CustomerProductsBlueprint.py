from flask import Blueprint, request, render_template, session, redirect, url_for
from service.ProductService import ProductService
from validation.CustomerAuth import customerAuth, CUSTOMER_NOT_AUTHENTICATED


def CustomerProductsBlueprint(name: str, importName: str, service: ProductService):
    bp = Blueprint(name, importName)

    # only GET method for now
    @bp.route('/<int:id>', methods=["GET"])
    def productDetailPage(id):
        product = service.getUserProductDetailPage(id)
        if product is None:
            return render_template('404.html')
        return render_template('customerProductDetail.html', product=product)

    @bp.route('/', methods=["GET"])
    def productPage():
        querySettings = request.args.to_dict()
        products = service.productsPage(querySettings)
        if products is None:
            return render_template('404.html')
        return render_template('customerIndex.html', querySettings=querySettings, **products)

    @bp.route('/category/<string:category>/department/<string:department>', methods=["GET", "POST"])
    def customerCategoryDepartmentPage(category, department):
        
        if request.method == "POST" and request.form.get("brand") is not None:
            brand = request.form.get("brand")
            return redirect(url_for('customer.products.customerCategoryDepartmentBrandPage', category=category, department=department, brand=brand))
        
        # result will contain the products with given category and department
        # and the list of all brand names
        result = service.productCategoryDepartmentPage(category, department)

        # list the products ---> DONE   
        # put search bar the search among all the brands 
        return render_template('category-department.html', **result)

    @bp.route('/category/<string:category>/department/<string:department>/brand/<string:brand>', methods=["GET"])
    def customerCategoryDepartmentBrandPage(category, department, brand):
        result = service.productsPage(querySettings={"category": category, "department": department, "brand": brand})
        return render_template('category-department-brand.html', **result)

    return bp
