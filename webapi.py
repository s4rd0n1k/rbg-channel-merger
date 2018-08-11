import os, time, channel_merger
from flask import Flask, flash, request, redirect, url_for, render_template, send_file
from werkzeug.utils import secure_filename
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)
app.secret_key = '1235'
app.config['UPLOAD_FOLDER'] = 'images'
@app.route('/', methods=['GET', 'POST'])
def upload():
    timestamp = time.time()
    timestamp = str(timestamp).replace('.', '')
    if request.method == 'POST':
        print(str(len(request.files)))
        if 'redf' not in request.files or 'greenf' not in request.files or 'bluef' not in request.files:
            flash('Please upload all files before submitting!')
            print("error 1")
            return redirect(request.url)
        red = request.files["redf"]
        green = request.files["greenf"]
        blue = request.files["bluef"]
        if red.filename == '' or green.filename == '' or blue.filename == '':
            flash('Please upload all files before submitting!')
            print("error 2")
            return redirect(request.url)
        if red and green and blue:
            print("files found!")
            if True:#allowed_file(red) and allowed_file(green) and allowed_file(blue)
                red_name = secure_filename(red.filename)
                green_name = secure_filename(green.filename)
                blue_name = secure_filename(blue.filename)
                red.save(os.path.join(app.config['UPLOAD_FOLDER'], red_name))
                green.save(os.path.join(app.config['UPLOAD_FOLDER'], green_name))
                blue.save(os.path.join(app.config['UPLOAD_FOLDER'], blue_name))
                print(red_name)
                print(green_name)
                print(blue_name)
                print("success!")
                return redirect(url_for('merge', data=(red_name, green_name, blue_name, timestamp)))
            else:
                print("names not allowed")
        else:
            print("files not found")
    return render_template('index.html')

@app.route('/result', methods=['GET', 'POST'])
@app.route('/result<data>', methods=['GET', 'POST'])
def merge(data):
    data = data.replace('\'', '')
    data = data.replace('(', '')
    data = data.replace(')', '')
    data = data.replace(' ', '')
    data = data.split(',')
    print(data)
    file = 'static/results/' + data[3] + '.png'
    channel_merger.merge(channels = (data[0], data[1], data[2]), dest=data[3])
    if request.method == 'POST':
        return return_file(file)
    return render_template('result.html', image = file)

def return_file(file):
    print(file)
    try:
        return send_file(file)
    except Exception as e:
        print(e)
