from controllers import create_app
from models.account import create_default_admin
from waitress import serve
import os
from dotenv import load_dotenv

load_dotenv()

app = create_app()
app.secret_key = os.getenv('SECRET_KEY')  # use secret key from environment variable
create_default_admin(app)

if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=5000)
    #below is for development
    # app.run(host="0.0.0.0", port=5000,debug=True)