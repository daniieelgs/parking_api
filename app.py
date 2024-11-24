
from eventlet import monkey_patch

monkey_patch()


import os
import traceback
from flask import Flask, jsonify
from flask_cors import CORS
from flask_smorest import abort, Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from controller.Database.DatabaseController import db

from flask_cors import CORS

from globals import DEBUG, API_PREFIX, API_TITLE, API_VERSION, HOST, PORT, SWAGGER_URL, OPENAPI_SWAGGER_UI_URL, OPENAPI_URL_PREFIX, OPENAPI_VERSION, REDIS_URL, MYSQL_URI

from flask_socketio import SocketIO, emit, join_room, leave_room

from resources.socket.SocketMiddleware import SocketMiddleware

from resources.api.parking import blp as ParkingBlp
from resources.api.history import blp as HistoryBlp

import redis

def create_app():
    
    app = Flask(__name__)
    CORS(app)
        
    app.debug = DEBUG
    app.jinja_env.auto_reload = DEBUG
    
    app.config['API_TITLE'] = API_TITLE
    app.config['API_VERSION'] = API_VERSION
    app.config['OPENAPI_VERSION'] = OPENAPI_VERSION
    app.config['OPENAPI_URL_PREFIX'] = OPENAPI_URL_PREFIX if DEBUG else None
    app.config['OPENAPI_SWAGGER_UI_PATH'] = SWAGGER_URL if DEBUG else None
    app.config['OPENAPI_SWAGGER_UI_URL'] = OPENAPI_SWAGGER_UI_URL if DEBUG else None
    app.config['REDIS_URL'] = REDIS_URL
    
    app.config['SQLALCHEMY_DATABASE_URI'] = MYSQL_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    
    with app.app_context():
        db.create_all()
    
    Migrate(app, db)

    api = Api(app)
    
    api.spec.components.security_scheme(
        'jwt', {'type': 'http', 'scheme': 'bearer', 'bearerFormat': 'JWT', 'x-bearerInfoFunc': 'app.decode_token'}
    )
    
    jwt = JWTManager(app)
        
    socketio = SocketIO(app, cors_allowed_origins="*", message_queue=app.config['REDIS_URL'], logger=True, engineio_logger=True, async_mode='eventlet')
    
    redis_client = redis.StrictRedis.from_url(app.config['REDIS_URL'])
    
    def getApiPrefix(url): return f"{API_PREFIX}/{url}"
                
    ##NotImplementedError
    
    @app.errorhandler(NotImplementedError)
    def handle_not_implemented_error(error):
        response = {
            "error_message": str(error),
            "code": 501,
            "status": "Not Implemented"
        }
        return jsonify(response), 501
    
    ##Routes
    api.register_blueprint(ParkingBlp, url_prefix=getApiPrefix('parking'))
    api.register_blueprint(HistoryBlp, url_prefix=getApiPrefix('history'))
        
    with app.app_context():
        socketio.on_namespace(SocketMiddleware(redis_client, socketio, namespace='/socket'))
       
    return app, socketio


app, socketio = create_app()

if __name__ == '__main__':
    
    socketio.run(app, debug=True, host=HOST, port=PORT, allow_unsafe_werkzeug=True)