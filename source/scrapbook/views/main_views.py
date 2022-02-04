from flask import flash
from flask_restx import Resource, Namespace

Main = Namespace('Main')

@Main.route('test')
class testGet(Resource):
    def get(self):
        return {
            'status': 200,
            'message': 'success',
            'data': {
                'test': 'good'
            }
        }
        

@Main.route('id/<int:id>')
class showId(Resource):
    def get(self,id):
        return {'test':'getTest', 'id':id}
    def post(self,id):
        return {'test':'postTest', 'id':id}