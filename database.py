from flask_sqlalchemy import SQLAlchemy
import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()

def get_db_connection_string():
    """Get database connection string for Docker SQL Server"""
    server = os.getenv('DB_SERVER', 'localhost')
    database = os.getenv('DB_NAME', 'COMP2001_Test')
    username = os.getenv('DB_USERNAME', 'SA')
    password = os.getenv('DB_PASSWORD', 'C0mp2001!')
    
    return f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}"

def init_db(app):
    """Initialize database with the Flask app"""
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mssql+pyodbc:///?odbc_connect={get_db_connection_string()}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    
    with app.app_context():
        db.create_all()