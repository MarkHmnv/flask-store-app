from sqlite3 import IntegrityError

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from ..db import db
from ..models import StoreModel
from ..schemas import StoreSchema


blp = Blueprint('stores', __name__, description='Stores API')


@blp.route('/stores')
class StoreListView(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, data):
        store = StoreModel(**data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(404, message='A store with that name already exists')
        except SQLAlchemyError:
            abort(500, message="An error occurred while creating the store")

        return store


@blp.route('/stores/<string:id>')
class StoreView(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, id):
        store = StoreModel.query.get_or_404(id)
        return store

    def delete(self, id):
        store = StoreModel.query.get_or_404(id)
        db.session.delete(store)
        db.session.commit()
        return '', 204

