from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Search, Product, AutomatedProduct
from . import db
import json
import sys
from io import StringIO
from .webscraper import search as scrape_search

routes = Blueprint('routes', __name__)

@routes.route('/', methods=['POST', 'GET'])
@login_required
def home():
    if request.method == 'POST': 
        search = request.form.get('search')

        if len(search) < 1:
            flash('Search is too short!', category='error') 
        else:
            new_search = Search(data=search, user_id=current_user.id)  
            db.session.add(new_search) 
            db.session.commit()

            old_stdout = sys.stdout
            sys.stdout = StringIO()
            scrape_search(search)
            scraped_data = sys.stdout.getvalue()
            sys.stdout = old_stdout
            
            products = scrape_search(search)

            for product in products:
                new_product = Product(
                    name=product['name'],
                    url=product['url'],
                    price=product['price'],
                    image=product['image'],
                    rating=product['rating'],
                    ratings_number=product['ratings_number'],
                    description=product['description'],
                    availability=product['availability'],
                    prime=product['prime'],
                    discount=product['discount'],
                    seller=product['seller'],
                    search_id=new_search.id
                )
                db.session.add(new_product)
            db.session.commit()

            flash('Search and products added!', category='success')
            return redirect(url_for('routes.home'))

    return render_template("homepage.html", user=current_user)


@routes.route('/delete-search', methods=['POST'])
def delete_search():
    search  = json.loads(request.data)
    searchId = search['searchId']
    search = Search.query.get(searchId)
    if search:
        if search.user_id == current_user.id:
            Product.query.filter_by(search_id=searchId).delete()
            db.session.delete(search)
            db.session.commit()
            flash('Search deleted from scraped product list!', category='success')
        else:
            flash('Unauthorized action!', category='error')
    else:
        flash('Search not found!', category='error')
    
    return jsonify({})


@routes.route('/search/<int:search_id>', methods=['GET'])
@login_required
def view_search(search_id):
    search = Search.query.get_or_404(search_id)
    products = Product.query.filter_by(search_id=search_id).all()
    return render_template('viewproduct.html', user=current_user, search=search, products=products)


@routes.route('/favorites', methods=["POST", 'GET'])
@login_required
def automation():
    if request.method == 'POST':
        product_id = request.form.get('product_id')
        product = Product.query.get(product_id)
        if product:
            new_automated_product = AutomatedProduct(
                name=product.name,
                url=product.url,
                price=product.price,
                image=product.image,
                rating=product.rating,
                ratings_number = product.ratings_number,
                description = product.description,
                availability = product.availability,
                prime = product.prime,
                discount = product.discount,
                seller = product.seller,
                user_id=current_user.id
            )
            db.session.add(new_automated_product)
            db.session.commit()
            flash('Product added to favorites!', category='success')
        else:
            flash('Product not found!', category='error')
        return redirect(url_for('routes.view_search', search_id=product.search_id))

    automated_products = AutomatedProduct.query.filter_by(user_id=current_user.id).all()
    return render_template("automation.html", user=current_user, products=automated_products)

@routes.route('/delete-automated-product', methods=['POST'])
@login_required
def delete_automated_product():
    product_id = request.form.get('product_id')
    product = AutomatedProduct.query.get(product_id)
    if product:
        if product.user_id == current_user.id:
            db.session.delete(product)
            db.session.commit()
            flash('Product deleted from favorites!', category='success')
        else:
            flash('Unauthorized action!', category='error')
    else:
        flash('Product not found!', category='error')
    return redirect(url_for('routes.automation'))

