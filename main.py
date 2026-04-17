import os
from server import app
from routes import auth, companies, companies_admin, users_admin, profile

if __name__ == "__main__":
    app.run(debug=os.environ.get('FLASK_DEBUG','false').lower() == 'true')