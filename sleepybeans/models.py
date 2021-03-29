from sleepybeans import app, db

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    public_id = db.Column(db.String(100), unique=True)
    first_name = db.Column(db.String(150), nullable = True)
    last_name = db.Column(db.String(150), nullable = True)
    email_address = db.Column(db.String(200), nullable = False)
    password = db.Column(db.String, nullable = True)
    child = db.relationship('Baby', backref = 'parent', lazy=True, cascade = 'all, delete')

class Baby(db.Model):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    birth_date = db.Column(db.Date, nullable = False)
    parent_id = db.Column(db.String, db.ForeignKey('user.public_id'), nullable=False)
    sleep = db.relationship('Sleep', backref= "baby", lazy=True, cascade = 'all, delete')

class Sleep(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    sleep_type = db.Column(db.String(150), nullable = True)
    start_time =  db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable = True)
    sleep_duration = db.Column(db.DateTime, nullable = True)
    sleep_complete = db.Column(db.Boolean)
    child_id = db.Column(db.String, db.ForeignKey("baby.id"), nullable=False)