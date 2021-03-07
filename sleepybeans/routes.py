from sleepybeans import app, db
from flask import Flask, jsonify, request, make_response
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import json
from datetime import datetime
from sleepybeans.models import User, Baby, Sleep
from functools import wraps
from sleepybeans.helpers import token_required

#signup/create new user
@app.route('/signup', methods=['POST'])
def sign_up():
    #defines data as the item that comes in to the request, and formas as json
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = User(
        public_id=str(uuid.uuid4()),
        email_address=data['email_address'],
        password=hashed_password,
        first_name = data['first_name'],
        last_name = data['last_name'] 
        )
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify( {'message':'new user created'} )


#Login Route
@app.route('/login')
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify',401,{'WWW-Authenticate': 'Basic realm="Login Required!"'})
    user = User.query.filter_by(email_address=auth.username).first()
    if not user:
        return make_response('Could not verify',401,{'WWW-Authenticate': 'Basic realm="Login Required!"'})
    if check_password_hash(user.password, auth.password):
        #this JWT includes an expiration time on the token - revisit this step for second portion of the JWT
        token = jwt.encode(
            {'public_id':user.public_id,
            'issue_time': json.dumps(datetime.utcnow(), indent=4, sort_keys=4, default=str)}, 
            app.config['SECRET_KEY'],
            algorithm = 'HS256')
        return jsonify({'token': token })

    return make_response('Could not verify',401,{'WWW-Authenticate': 'Basic realm="Login Required!"'})


#Baby Routes
#create new baby
@app.route('/baby', methods = ["POST"])
@token_required
def create_baby(current_user_token):
    data = request.get_json()
    new_baby = Baby(
        id = str(uuid.uuid4()),
        name = data['name'],
        birth_date = data['birth_date'],
        parent_id = current_user_token.public_id
    )
    db.session.add(new_baby)
    db.session.commit()
    
    return jsonify( {'message':'new baby created'} )

#return all babies belonging to single user
@app.route('/baby', methods= ['GET'])
@token_required
def get_all_babies(current_user_token):
    babies = Baby.query.filter_by(parent_id=current_user_token.public_id).all()
    if not babies:
        return jsonify({'message': 'You currently do not have any babies'})
    output = []
    for baby in babies:
        baby_data = {}
        baby_data['id']=baby.id
        baby_data['name'] = baby.name
        baby_data['birth_date'] = baby.birth_date
        baby_data['parent'] = baby.parent_id
        output.append(baby_data)
    return jsonify({'babies': output})

#return single baby belonging to a user
@app.route('/baby/<baby_id>', methods=['GET'])
@token_required
def get_single_baby(current_user_token, baby_id):
    baby = Baby.query.filter_by(id=baby_id,parent_id=current_user_token.public_id).first()
    if not baby:
        return jsonify({'message': 'No baby by that ID found'})
    baby_data = {}
    baby_data['id']=baby.id
    baby_data['name'] = baby.name
    baby_data['birth_date'] = baby.birth_date
    baby_data['parent'] = baby.parent_id
    return jsonify({'baby' : baby_data})

#delete a baby
@app.route('/baby/<baby_id>', methods = ['DELETE'])
@token_required
def del_baby(current_user_token,baby_id):
    baby = Baby.query.filter_by(id=baby_id,parent_id=current_user_token.public_id).first()
    if not baby:
        return jsonify({'message': 'No baby by that ID found'})
    db.session.delete(baby)
    db.session.commit()
    return jsonify ({'message':'This baby has been deleted'})

#update a babys attributes
#note - different requests can change the types of updats by adding or leaving things off
@app.route('/baby/<baby_id>', methods=['PUT'])
@token_required
def update_baby(current_user_token,baby_id):
    update_baby = Baby.query.filter_by(id=baby_id,parent_id=current_user_token.public_id).first()
    if not update_baby:
        return jsonify ({'message': 'no baby by this id'})
    data = request.get_json()
    update_baby.name = data['name']
    update_baby.birth_date=data['birth_date']
    db.session.commit()
    return jsonify({'message' : 'baby has been updated'})


#Sleep Routes

#start new sleep
@app.route('/baby/<baby_id>/sleep', methods=['POST'])
@token_required
def new_sleep(current_user_token,baby_id):
    data = request.get_json()
    new_sleep = Sleep(
        sleep_type = data['sleep_type'],
        start_time = datetime.utcnow(),
        child_id = baby_id,
        sleep_complete=False
    )
    db.session.add(new_sleep)
    db.session.commit()
    return jsonify({'message':'sleep session started'})

#Get active sleeps for a baby
@app.route('/baby/<baby_id>/sleep', methods = ['GET'])
@token_required
def show_current_sleep(current_user_token, baby_id):
    sleeps = Sleep.query.filter_by(child_id=baby_id,sleep_complete=False).all()
    if not sleeps:
        return jsonify({'message':'No babies are currently sleeping'})
    output = []
    for sleep in sleeps:
        sleep_data = {}
        sleep_data['id']=sleep.id
        sleep_data['sleep_type']=sleep.sleep_type
        sleep_data['start_time']=sleep.start_time
        output.append(sleep_data)
    return jsonify({'Sleep Sessions':output})

#end a sleep
@app.route('/baby/<baby_id>/sleep/<sleep_id>',methods = ['PUT'])
@token_required
def end_sleep(current_user_token,baby_id,sleep_id):
    end_sleep = Sleep.query.filter_by(child_id=baby_id,id=sleep_id).first()
    if not end_sleep:
        return jsonify({'message':'There is no baby currently sleeping in this id'})
    end_sleep.end_time = datetime.utcnow()
    end_sleep.sleep_complete = True
    end_sleep.sleep_duration = end_sleep.end_time - end_sleep.start_time
    print(end_sleep.end_time - end_sleep.start_time)
    db.session.commit()
    return jsonify({'message':f'sleep session ended with total time {end_sleep.sleep_duration}'})