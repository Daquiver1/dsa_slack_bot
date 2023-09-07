"""Setup database connection."""

from databases import Database
from fastapi import FastAPI


async def connect_to_db(app: FastAPI) -> None:
    """Connect to sqlite db."""
    try:
        print("Setting up database...")
        database = Database("sqlite:///app.db")
        await database.connect()
        app.state._db = database
        print("Database connected ")
    except Exception as e:
        print("Error setting up database: ", e)


# async def disconnect_to_db() -> None:
#     """Disconnect db."""
#     try:
#         print("Disconnecting database...")
#         database = Database("sqlite:///app.db")
#         await database.disconnect()
#         print("Database disconnected")
#     except Exception as e:
#         print("Error disconnecting database: ", e)
