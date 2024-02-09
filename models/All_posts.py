from app import db

class All_posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_name = db.Column(db.String(50), nullable=False)
    post_content = db.Column(db.String(130), nullable=False)
    date = db.Column(db.String(30), nullable=False)
    slug = db.Column(db.String(25), nullable=False)
    img_file = db.Column(db.String(15), nullable=False)
    user_posted = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(30), nullable=False)