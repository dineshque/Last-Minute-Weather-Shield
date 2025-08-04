from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Weather Shield Hackathon Project!"

if __name__ == '__main__':
    app.run(debug=True)
