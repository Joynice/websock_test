from exts import create_db
db = create_db()
class Web_listen(db.Model):
    __tablename__ = 'web_listen'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.String(255), nullable=False)
