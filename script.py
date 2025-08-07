from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")  # you need templates/index.html for this to work

if __name__ == "__main__":
    app.run()
