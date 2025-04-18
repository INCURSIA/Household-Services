from website import create_app, db
from website.models import create_admin

app = create_app()

with app.app_context():
    db.create_all()  
    create_admin(app) 

if __name__ == '__main__':
    app.run(debug = True)

