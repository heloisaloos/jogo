from config import *
from rotas import *

with app.app_context():
    db.create_all()
    CORS(app)
    app.run(debug=True, host="0.0.0.0")