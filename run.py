from flask import render_template
from app import create_app
from config import DevelopmentConfig , TestingConfig , ProductionConfig

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)