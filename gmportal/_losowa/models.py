from gmportal import db

class LosowaTab(db.Model):
    __tablename__='losowatab'


    id=db.Column(db.Integer, primary_key=True)
    rnd_num = db.Column(db.Integer)
    wynik = db.Column(db.Integer)
    nr_proby = db.Column(db.Integer)
    wynik_msg = db.Column(db.String(80))
    username = db.Column(db.String(80))

    def __init__(self, rnd_num,wynik,nr_proby,wynik_msg, username):
        self.rnd_num=rnd_num
        self.wynik=wynik
        self.nr_proby=nr_proby
        self.wynik_msg=wynik_msg
        self.username=username

    def __repr__(self):
        return (self.rnd_num,self.wynik,self.nr_proby)