from website import create_app, db
from flask_migrate import Migrate
import os


app = create_app()
migrate = Migrate(app, db, render_as_batch=True)

def save_profile_picture(file, name):
    return file.save(os.path.join(app.config['UPLOAD'], name))

if __name__ == '__main__':
    app.run(debug=True)
