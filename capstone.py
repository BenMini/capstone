from app import app, db, cli
from app.models import Business, Customer


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Business': Business, 'Customer': Customer}
