from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from ..models import StoreModel, ItemModel, TagModel
from ..db import db
from ..schemas import TagSchema

blp = Blueprint('tags', __name__, description='Tags API')


@blp.route('/stores/<int:id>/tags')
class TagInStoreView(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self, id):
        store = StoreModel.query.get_or_404(id)
        return store.tags.all()

    @jwt_required(fresh=True)
    @blp.arguments(TagSchema)
    @blp.response(200, TagSchema)
    def post(self, data, id):
        if TagModel.query.filter(TagModel.store_id == id, TagModel.name == data['name']).first():
            abort(400, message='A tag with that name already exists')
        tag = TagModel(**data, store_id=id)

        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))

        return tag


@blp.route('/tags/<int:id>')
class TagView(MethodView):
    @blp.response(200, TagSchema)
    def get(self, id):
        tag = TagModel.query.get_or_404(id)
        return tag

    @jwt_required(fresh=True)
    @blp.response(204)
    @blp.alt_response(404, description='Tag not found')
    @blp.alt_response(400, description='Returned if the tag is assigned to one or more items')
    def delete(self, id):
        tag = TagModel.query.get_or_404(id)
        if not tag.items:
            db.session.delete(tag)
            db.session.commit()
            return ''
        abort(400, message='Tag cannot be deleted because it is assigned to one or more items')


@blp.route('/items/<int:item_id>/tags/<int:tag_id>')
class LinkTagsToItemView(MethodView):
    @jwt_required(fresh=True)
    @blp.response(201, TagSchema)
    def post(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.append(tag)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))

        return tag

    @jwt_required(fresh=True)
    @blp.response(204)
    def delete(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.remove(tag)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        return ''
