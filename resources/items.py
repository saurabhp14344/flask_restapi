from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.items import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='this field can not be left blank!')

    @jwt_required()
    def get(self, name):
        """Retrieve information"""
        # item = next(filter(lambda x: x['name'] == name, items), None)
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'item not found!'}, 400

    def post(self, name):
        """create some new items"""
        # if next(filter(lambda x: x['name'] == name, items), None) and not None:
        if ItemModel.find_by_name(name):
            """check if item exists"""
            return {'Message': 'already exists {} items.'.format(name)}, 404

        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'])
        try:
            item.save_to_db()
        except Exception as er:
            return {'error': str(er)}, 500  # internal error
        return item.json(), 201

    def delete(self, name):
        """delete items from database"""
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message': 'Item deleted.'}

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(name, data['price'])
        else:
            item.price = data['price']
        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        """retrieve all items from database"""
        return {'items': list(map(lambda x:x.json(), ItemModel.query.all()))}