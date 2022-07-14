from re import L
from flask import send_from_directory
from unittest import result
from urllib import response
from flask import Flask, jsonify, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import json
import ast
from Database import dbase
import face_recog

UPLOAD_FOLDER = f'{os.getcwd()}/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png',
                      'jpg', 'jpeg', 'gif', 'zip', 'targz'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["ALLOWED_EXTENTIONS"] = ALLOWED_EXTENSIONS


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# This endpoint contains a html form, where we have to provide input file as well as parameters
# such as name, location, version and date. This functions then extracts values and
# calls add_face() funtion defined in face_recg.py.


@app.route('/add_face/', methods=['GET', 'POST'])
def add_face():
    if request.method == 'POST':
        # check if the post request has the file part
        if request.files:

            # INFORMATION
            information = request.form
            name = information.get("name")
            version = information.get("version")
            date = information.get("date")
            location = information.get("location")
            print(name, version, date, location)

            info = {"name": name, "version": version,
                    "date": date, "location": location}
            result = {"status": "Success", "Body": info}
            file = request.files["file"]

            if file.filename == '':
                print('No selected file')
                result["status"] = "No selected file"
                return redirect(url_for('success_add_face', data=result))

            if not allowed_file(file.filename):
                print("File Extention Not Allowed")
                result["status"] = "File Extention Not Allowed"
                return redirect(url_for('success_add_face', data=result))

            # SAVING FILE TO UPLOADS FOLDER
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print("File Saved in Uploads Directory")

            # INSERT IMAGE
            file_name = UPLOAD_FOLDER+"/"+filename
            print(file_name)
            face_recog.add_face(
                file_name, info["name"], info["version"], info["date"], info["location"])
            return redirect(url_for('success_add_face', data=result))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>ADD FACE</h1>
    <form method=post enctype=multipart/form-data>
        <h2>Upload new File</h2>
            <input type=file name="file" placeholder="Upload File">
        <h2>Give Name</h2>
            <input type=text name="name" placeholder="Enter Name">
        <h2>Give Version</h2>
            <input type=text name="version" placeholder="Enter Version">
        <h2>Give Date</h2>
            <input type=text name="date" placeholder="YYYY-MM-DD">
        <h2>Give Location</h2>
            <input type=text name="location" placeholder="Enter Location">
        <br>
        <br>
        <br>
        <input type=submit value=Submit>
    </form>
    '''


@app.route('/<data>')
def success_add_face(data):
    dict = ast.literal_eval(data)
    return dict

# Home Page


@app.route('/')
def home():
    return '<h1>WELCOME TO FACIAL RECOGNITION PROGRAM<h1>'

# This endpoint contains a html form, where we have to provide input file as well as
# parameters such as value of K in top k matchings and value of confidence between 0-100 percent.
# This functions then extracts values and calls search_faces() funtion defined in face_recg.py.


@app.route("/search_faces/", methods=['GET', 'POST'])
def search_faces():
    if request.method == 'POST':
        # check if the post request has the file part
        if request.files:

            # INFORMATION
            information = request.form
            topk = int(information.get("k"))
            confidence = int(information.get("confidence"))
            confidence = (100-confidence)/100

            info = {"status": "Success"}

            file = request.files["file"]

            if file.filename == '':
                print('No selected file')
                result["status"] = "No selected file"
                return redirect(url_for('success_add_face', data=info))

            if not allowed_file(file.filename):
                print("File Extention Not Allowed")
                result["status"] = "File Extention Not Allowed"
                return redirect(url_for('success_add_face', data=info))

            # SAVING FILE TO UPLOADS FOLDER
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print("File Saved in Uploads Directory")

            # INSERT IMAGE
            path_file_name = UPLOAD_FOLDER+"/"+filename
            print(path_file_name)
            info = face_recog.search_faces(path_file_name, topk, confidence)
            result = {"Status": "Success", "Body": info}
            return redirect(url_for('success_add_face', data=result))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>SEARCH FACES</h1>
    <form method=post enctype=multipart/form-data>
        <h2>Upload new File</h2>
            <input type=file name="file" placeholder="Upload File">
        <h2>Enter K</h2>
            <input type=number min="0" name="k"  placeholder="Enter The Value of K" required>
        <h2>Enter Confidence Level</h2>
            <input type=number min="0" max="100" name="confidence" placeholder="0-100" required>
        <br>
        <br>
        <br>
        <input type=submit value=Submit>
    </form>
    '''

# This endpoint contains a html form, where we have to provide input file .
# This functions then extracts values and calls add_faces_in_bulk() funtion defined in face_recg.py.


@app.route("/add_faces_in_bulk/", methods=['GET', 'POST'])
def add_faces_in_bulk():
    if request.method == 'POST':
        # check if the post request has the file part
        if request.files:

            # INFORMATION
            info = {"status": "Success"}

            file = request.files["file"]

            if file.filename == '':
                print('No selected file')
                info["status"] = "No selected file"
                return redirect(url_for('success_add_face', data=info))

            if not allowed_file(file.filename):
                print("File Extention Not Allowed")
                info["status"] = "File Extention Not Allowed"
                return redirect(url_for('success_add_face', data=info))

            # SAVING FILE TO UPLOADS FOLDER
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print("File Saved in Uploads Directory")

            # INSERT IMAGE
            zip_file_name = UPLOAD_FOLDER+"/"+filename
            info = face_recog.add_faces_in_bulk(zip_file_name)
            result = {"Status": "Success", "Body": info}
            return redirect(url_for('success_add_face', data=result))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>ADD FACES IN BULK</h1>
    <form method=post enctype=multipart/form-data>
        <h2>Upload new File</h2>
            <input type=file name="file" placeholder="Upload File">
        <br>
        <br>
        <br>
        <input type=submit value=Submit>
    </form>
    '''

# This endpoint contains a html form, where we have to provide input parameters such as image id for which
# information needed to be extracted.
# This functions then extracts values and calls get_face_info() funtion defined in face_recg.py.


@app.route("/get_face_info/", methods=['GET', 'POST'])
def get_face_info():
    if request.method == 'POST':
        # check if the post request has the file part

        # INFORMATION
        information = request.form
        id = int(information.get("id"))

        info = face_recog.get_face_info(id)
        result = {"Status": "Success", "Body": info}
        if(len(info) == 0):
            result["Status"] = "No Such Image"
        return redirect(url_for('success_add_face', data=result))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>GET FACE INFO</h1>
    <form method=post enctype=multipart/form-data>
        <h2>Enter Face ID</h2>
            <input type=number min="1" name="id" placeholder="Enter Id" required>
        <br>
        <br>
        <br>
        <input type=submit value=Submit>
    </form>
    '''


if __name__ == "__main__":
    app.run(debug=True)
