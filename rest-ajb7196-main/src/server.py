from flask import Flask
from flask_restful import Resource, Api
from api.hello_world import HelloWorld
from api.management import *
from api.accountinfo import *
from api.rideinfo import *
from api.transaction import *

app = Flask(__name__)
api = Api(app)

api.add_resource(Init, '/manage/init') #Management API for initializing the DB

api.add_resource(Version, '/manage/version') #Management API for checking DB version

api.add_resource(HelloWorld, '/') 

api.add_resource(AccountRiderInfo, '/accountinfo/rider/<string:id>', methods=["PUT", "POST", "GET", "DELETE"])

api.add_resource(AccountDriverInfo, '/accountinfo/driver/<string:id>', methods=["PUT", "POST", "GET", "DELETE"])

api.add_resource(AccountInfo, '/accountinfo/accounts')

api.add_resource(RideInfo, '/rideinfo')

api.add_resource(TransactionInfo, '/transaction/reciept')


if __name__ == '__main__':
    rebuild_tables()
    app.run(debug=True)