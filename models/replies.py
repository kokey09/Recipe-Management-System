from controllers import db

class Replies(db.Model):
    __tablename__ = 'replies'
    reply_id = db.Column(db.Integer, primary_key=True)
    review_id = db.Column(db.Integer, db.ForeignKey('reviews.review_id'), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    reply_text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.TIMESTAMP, server_default=db.text('CURRENT_TIMESTAMP'), nullable=False)

    review = db.relationship('Review', backref='replies')
    account = db.relationship('Account', backref='replies')
