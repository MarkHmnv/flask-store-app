from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError

from ..db import db
from ..models import ItemModel
from ..schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint('items', __name__, description='Items API')


@blp.route('/items')
class ItemListView(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()

    @jwt_required()
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, data):
        item = ItemModel(**data)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while creating the item")

        return item


@blp.route('/items/<int:id>')
class ItemView(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, id):
        item = ItemModel.query.get_or_404(id)
        return item

    @jwt_required()
    @blp.response(204)
    def delete(self, id):
        item = ItemModel.query.get_or_404(id)
        db.session.delete(item)
        db.session.commit()
        return ''

    @jwt_required()
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, data, id):
        item = ItemModel.query.get_or_404(id)
        item.name = data['name']
        item.price = data['price']

        db.session.add(item)
        db.session.commit()

        return item
