#File so that flask can run the webapp
from app import app

if __name__ == "__main__":
    app.run(debug=True, port=8123)