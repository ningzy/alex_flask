from app import app, db
from app.models import User, Uploaded_files

@app.shell_context_processor
def make_shell_context():
    return {'db': db,
            'User': User,
            'files': Uploaded_files}