from flask import Flask, render_template

app = Flask(__name__)

@app.route('/test_bootstrap', methods=["GET","POST"])
def test_bootstrap():
    return render_template('test_bootstrap.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=82)