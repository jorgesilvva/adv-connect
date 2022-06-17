import os
from app import app
from app.controller import controller
from flask_cors import CORS

cors = CORS(app, resouce={r'/*':{'origins': '*'}})

def main():
    port= int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

if __name__ == "__main__":
    main()
    app.run
