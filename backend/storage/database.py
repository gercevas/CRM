import sqlite3
import psycopg2
import json
import os


def load_config():
    path = os.path.join(os.path.dirname(__file__), "config.json")
    with open(path, "r") as config_file:
        return json.load(config_file)


def get_connection():
    config = load_config()
    db_type = config.get("db_type")

    if db_type == "sqlite":
        return sqlite3.connect(config.get("sqlite_path"))

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
