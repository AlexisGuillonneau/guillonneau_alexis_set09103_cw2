import os
from my_app import app
app.secret_key = os.urandom(12)
app.run(host='set09103.napier.ac.uk', port='9134', debug=True)
