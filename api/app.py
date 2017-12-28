"""
This his the main module of the api.
"""
from os import environ
from collections import OrderedDict
from datetime import datetime
from flask_httpauth import HTTPBasicAuth
from pymongo import MongoClient
from werkzeug.debug import DebuggedApplication
from flask_restful import Api, Resource, reqparse
from flask import Flask, jsonify
from flask import request

# Initialization
app = Flask(__name__)
app.config.from_object(environ.get('FLASK_CONFIG'))

# Debug log
if app.config['DEBUG']:
    app.wsgi_app = DebuggedApplication(app.wsgi_app, True)

# To keep ordered dict when using jsonify
app.config['JSON_SORT_KEYS'] = False
api = Api(app)
auth = HTTPBasicAuth()


# Adding the db info to the class ResourceDb
class ResourceDb(Resource):
    def __init__(self):
        self._user = 'root'
        self._pwd = environ.get('MONGODB_PASSWORD')
        self.client = MongoClient(connect=False, host='iAdvize-db-svc', port=27017)

class Posts(ResourceDb):
    def clean_date(self, date):
        format_date = '%Y-%m-%dT%H:%M:%SZ'
        return datetime.strptime(date, format_date)

    def __init__(self):
        super(Posts, self).__init__()
        # Connect to the db cdm
        self.db = self.client.iAdvize
        self.db.authenticate(str(self._user), str(self._pwd), source='admin')
        # Build arguments
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('from', type=str, required=False, location='args')
        self.reqparse.add_argument('to', type=str, required=False, location='args')
        self.reqparse.add_argument('author', type=str, required=False, location='args')

    def post(self):
        # from_ = request.args.get('from', type=str)
        # to = request.args.get('to', type = str)
        args = self.reqparse.parse_args()
        # Get the arguments
        from_ = args['from']
        to = args['to']
        author = args['author']
        print(to, from_)
        # print(author)
        # Build the query for the db
        query = {}
        if to:
            to = self.clean_date(to)
            query['date'] = {'$lte': to}
        # else:
        #     to = datetime.today()
        if from_:
            from_ = self.clean_date(from_)
            query['date'] = {'$gte': from_}
        # else:
        #     query['date'] = {'$lte': to}
        if author:
            query['autor'] = author

        # print(query)
        tmp = [item for item in self.db.vdm.find(query, {'_id': False})]
        res = OrderedDict()
        res['posts'] = tmp
        res['count'] = len(tmp)

        return jsonify(res)

    def get(self, id_):
        res = self.db.vdm.find_one({'id': id_}, {'_id': False})

        return jsonify(dict(posts=res))   


# Add the route
api.add_resource(Posts, '/api/posts', '/api/posts/<int:id_>')
# api.add_resource(PostsId, '/api/posts/<int:id_>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5500)


