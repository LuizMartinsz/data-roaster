from flask import Flask
from app.routes import bp
import os

app = Flask(__name__, template_folder='app/templates')

app.register_blueprint(bp)

if __name__ == '__main__':
    if not os.path.exists('reports'):
        os.makedirs('reports')
        
    app.run(debug=True, port=5000, host='0.0.0.0')