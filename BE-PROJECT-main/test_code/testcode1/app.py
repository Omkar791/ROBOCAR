
from flask import Flask , render_template , redirect , request


app = Flask(__name__)

@app.route('/')
def Home():
    return render_template('index.html')




if __name__ == "__main__":
    app.run(debug=True,use_reloader=False, threaded=True)




