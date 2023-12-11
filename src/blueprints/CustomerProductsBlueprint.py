from flask import Blueprint, request, render_template, session, redirect, url_for
from service.ProductService import ProductService
from validation.CustomerAuth import customerAuth, CUSTOMER_NOT_AUTHENTICATED


def CustomerProductsBlueprint(name: str, importName: str, service: ProductService):
    bp = Blueprint(name, importName)

    @bp.before_request
    def before_request():
        try:
            customerAuth(session)
        except Exception as e:
            if e.args[0] == CUSTOMER_NOT_AUTHENTICATED:
                return redirect(url_for('customer.loginPage'))

    return bp
