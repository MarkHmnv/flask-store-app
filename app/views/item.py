from flask.views import MethodView
from flask_smorest import Blueprint, abort
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


@blp.route('/items/<string:id>')
class ItemView(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, id):
        item = ItemModel.query.get_or_404(id)
        return item

    def delete(self, id):
        item = ItemModel.query.get_or_404(id)
        db.session.delete(item)
        db.session.commit()
        return '', 204

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, data, id):
        item = ItemModel.query.get_or_404(id)
        item.name = data['name']
        item.price = data['price']

        db.session.add(item)
        db.session.commit()

        return item
