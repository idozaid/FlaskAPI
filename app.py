from flask import Flask
import asyncio
from flask_routes import flask_routes

app = Flask(__name__)
app.register_blueprint(flask_routes)

async def main():
    app.run(port=5000)


if __name__ == '__main__':
    asyncio.run(main())