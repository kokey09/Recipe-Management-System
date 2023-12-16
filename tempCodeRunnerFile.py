from controllers import create_app
from models.account import create_default_admin

app = create_app()
create_default_admin(app)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000,debug=True)