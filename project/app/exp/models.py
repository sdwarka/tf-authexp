from app import db

class Expense(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    exp_date = db.Column(db.Date())
    exp_catg = db.Column(db.String(100))
    exp_desc = db.Column(db.String(255))
    exp_amt  = db.Column(db.Float())
    exp_type = db.Column(db.String(100))
    exp_mode = db.Column(db.String(100))
    exp_rem  = db.Column(db.String(512))

