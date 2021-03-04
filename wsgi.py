import sys
from application import create_app

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--debug":
        app = create_app(debug=True)
        app.run(debug=True)
    else:
        app = create_app()
        app.run()
