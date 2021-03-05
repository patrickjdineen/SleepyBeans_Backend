from flask import request, jsonify
from functools import wraps
import jwt
import datetime
import json
from sleepybeans.models import User, Baby, Sleep
from sleepybeans import app

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': 'Token is missing'}),401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms = ['HS256'])
            current_user_token = User.query.filter_by(public_id = data['public_id']).first()
        except:
            return jsonify({'message':'Your token is invalid'}), 401
        return f(current_user_token,*args,**kwargs)
    return decorated