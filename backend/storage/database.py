import sqlite3
import psycopg2
import json
import os
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()


def load_config():
    # Obtener la ruta absoluta al directorio del proyecto
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    config_path = os.path.join(project_root, "crm.sqlite")
    
    # Si el archivo de configuración no existe, crear uno por defecto
    if not os.path.exists(config_path):
        sqlite_env_path = os.getenv("SQLITE_PATH", "crm.sqlite")
        sqlite_abs_path = os.path.join(project_root, sqlite_env_path)
        
        return {
            "db_type": "sqlite",
            "sqlite_path": sqlite_abs_path
        }
    
    # Si el archivo de configuración existe, cargarlo
    with open(os.path.join(project_root, "backend", "storage", "config.json"), "r") as config_file:
        config = json.load(config_file)
        # Asegurarse de que la ruta de SQLite sea absoluta y privada
        if "sqlite_path" in config:
            sqlite_env_path = os.getenv("SQLITE_PATH", config["sqlite_path"])
            config["sqlite_path"] = os.path.join(project_root, sqlite_env_path)
        
        return config


def get_connection():
    config = load_config()
    db_type = config.get("db_type")

    if db_type == "sqlite":
        # Asegurarse de que el directorio existe
        sqlite_path = config.get("sqlite_path")
        os.makedirs(os.path.dirname(sqlite_path), exist_ok=True)
        return sqlite3.connect(sqlite_path)

    elif db_type == "postgres":
        return psycopg2.connect(
            host=config.get("host"),
            database=config.get("database"),
            user=config.get("user"),
            password=config.get("password"),
            port=config.get("port")
        )

    else:
        raise ValueError(f"Unsupported database type: {db_type}")