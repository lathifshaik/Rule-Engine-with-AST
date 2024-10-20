from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config
from models import db
from rules import rule_blueprint

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize Extensions
db.init_app(app)
CORS(app)

# Register Blueprints
app.register_blueprint(rule_blueprint)

# Create the database tables within the application context
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

# Make sure app is exposed for import
if __name__ == '__main__':
    app.run(debug=True)
