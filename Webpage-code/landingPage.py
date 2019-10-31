from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def firstPage():
    return render_template('index.html')


@app.route('/contributors')
def contriPage():
    return render_template('contributors.html')

if __name__ == '__main__':
    app.run()
    
