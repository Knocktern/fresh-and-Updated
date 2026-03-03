from __init__ import create_app
from extensions import db, socketio
import os

# Create app instance (will auto-detect environment)
app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    # Use socketio.run for development, gunicorn will handle production
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    socketio.run(app, debug=debug, host='0.0.0.0', port=port)
