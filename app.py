from controllers import create_app
from models.account import create_default_admin
from waitress import serve


app = create_app()
create_default_admin(app)

if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=5000)
    #below is for development
    # app.run(host="0.0.0.0", port=5000,debug=True)

