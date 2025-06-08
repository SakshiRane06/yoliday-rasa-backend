import os
import sys
from rasa.__main__ import main
from rasa.core.run import serve_application
from sanic_cors import CORS

def patched_serve_application():
    app = serve_application()
    CORS(app, resources={r"/*": {"origins": "*"}})
    port = int(os.environ.get("PORT", 5005))
    app.run(host="0.0.0.0", port=port)

sys.modules["rasa.core.run"].serve_application = patched_serve_application

if __name__ == '__main__':
    main()