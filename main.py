import csv
from io import StringIO

import pandas as pd
from flask import Flask, flash, redirect, url_for
from flask import request
from flask_restful import Api
from flask_restful import Resource
from sqlalchemy.dialects.firebird import dialect
from werkzeug.utils import secure_filename

from models.base_class import db
from models.product import Product
from models.review import Review
from services import ALLOWED_EXTENSIONS

app = Flask(__name__)
api = Api(app)


def parseProduct(filePath):
    col_names = ['Title', 'Asin']
    csvData = pd.read_csv(filePath, names=col_names, header=None)
    for i, row in csvData.iterrows():
        db.create_all(i, row)


def parseReviews(filePath):
    col_names = ['Title', 'Asin', 'Review']
    csvData = pd.read_csv(filePath, names=col_names, header=None)
    for i, row in csvData.iterrows():
        db.create_all(i, row)


class ProductView(Resource):
    def get(self):
        products = Product.query.all()
        return {'Products': list(x.json() for x in products)}

    def post(self):
        data = request.get_json()

        new_product = Product(data['id'], data['title'], data['asin'])
        db.session.add(new_product)
        db.session.commit()
        return new_product.json(), 201


class ReviewView(Resource):

    def get(self, id):

        review = Review.filter_by(name=id).first()
        if review:
            return review.json()
        return {'message': 'Review not found'}, 404

    def put(self, id):
        data = request.get_json()

        review = Product.filter_by(name=id).first()

        if review:
            review.asin = data["asin"]
            review.title = data["title"]
        else:
            review = Product(id=id, **data)

        db.session.add(review)
        db.session.commit()

        return review.json()

    def delete(self, id):
        review = Review.filter_by(name=id).first()
        if review:
            db.session.delete(review)
            db.session.commit()
            return {'message': 'Deleted'}
        else:
            return {'message': 'product not found'}, 404


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/csv/review', methods=['GET', 'POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        return redirect(url_for('uploaded_file',
                                filename=filename))
    contents = file.read()
    decoded = contents.decode()
    buffer = StringIO(decoded)

    csv_reader = csv.DictReader(buffer, dialect=dialect)
    new_review = []
    new_product = []
    stats = {"new_product": 0, "new_review": 0}
    try:
        for row in csv_reader:
            review = {
                'Asin': row.get('Asin'),
                'Title': row.get('Title'),
                'Review': row.pop('Review'),
            }
            new_review.append(review)
        db.add_all(new_review)
        db.commit()
    except:
        for row in csv_reader:
            review = {
                'Asin': row.get('Asin'),
                'Title': row.get('Title'),
            }
            new_review.append(review)
        db.add_all(new_product)
        db.commit()
    stats["new_review"] = len(new_review)
    stats["new_product"] = len(new_product)
    return stats


api.add_resource(ProductView, '/review')
api.add_resource(ReviewView, '/product/')

app.debug = True
if __name__ == '__main__':
    app.run(host='localhost', port=5000)
