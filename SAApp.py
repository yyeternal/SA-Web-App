from app import db, create_app
from config import Config

import sqlalchemy as sqla
import sqlalchemy.orm as sqlo

from app.main.models import User, Instructor

app = create_app(Config)

@app.shell_context_processor
def make_shell_context():
    return {'sqla': sqla, 'sqlo': sqlo, 'db': db, 'user': User, 'instrctor': Instructor}

if __name__ == "__main__":
    app.run(debug=True)