from app import db, create_app
from config import Config

import sqlalchemy as sqla
import sqlalchemy.orm as sqlo

app = create_app(Config)

@app.shell_context_processor
def make_shell_context():
    return {'sqla': sqla, 'sqlo': sqlo, 'db': db}

if __name__ == "__main__":
    app.run(debug=True)