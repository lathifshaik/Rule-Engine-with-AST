from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Rule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    rule_string = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f"<Rule {self.name}>"
