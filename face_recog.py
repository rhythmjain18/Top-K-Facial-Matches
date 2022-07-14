from numpy import ndarray
import numpy
from Database import dbase
import face_recognition
import re
import cv2
import os
from datetime import date
from zipfile import ZipFile

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'zip'}


def getVersion(s):
    p = re.findall('[0-9]+', s)
    return p[0]


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# It takes 5 values as input(filename,name,version,date,location).
# This functions then extracts values and  extracts encoding of the image and then
# convert it to bytes data and insert the respective values in the table.


def add_face(filename, name, version="NULL", date="NULL", location="NULL"):
    img = cv2.imread(filename)
    print(filename)
    # convert the input frame from BGR to RGB
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # the facial embeddings for face in input
    boxes = face_recognition.face_locations(rgb, model='hog')

    # Encodings
    encodings = face_recognition.face_encodings(rgb, boxes)

    # Connecting to Database
    Mydb = dbase("FaceRecognition")
    Mydb.UseDB("FaceRecognition")

    # for each encoding insert in table
    for encoding in encodings:
        binaryData = ndarray.tobytes(encoding)
        Mydb.InsertBlob(binaryData, name, version, date, location)

# It takes path of zip as input.This functions then extracts the zip file in uploads folder and
# then using os library iterate over all the folders, read the images, extracts encoding of the
# image and then convert it to bytes data and insert the respective values in the table.


def add_faces_in_bulk(path):

    knownNames = []
    knownEncodings = []
    versions = []

    # Extracting Zip File
    print(path)
    with ZipFile(path) as zf:
        zf.extractall(f"{os.getcwd()}/uploads")
    print("Extract Done")

    # Folder Path
    path = f"{path[0:len(path)-4]}"
    print(path)
    listdir = os.listdir(path)
    print(listdir)

    for image_folder in listdir:
        if '.' in image_folder:
            continue

        path_image_folder = f"{path}/{image_folder}"
        print(path_image_folder)

        # list of all the images
        images = os.listdir(path_image_folder)
        for img_name in images:
            image_path = f"{path_image_folder}/{img_name}"
            v = getVersion(img_name)
            test_img = cv2.imread(image_path)
            rgb = cv2.cvtColor(test_img, cv2.COLOR_BGR2RGB)

            # Use Face_recognition to locate faces using hog model
            boxes = face_recognition.face_locations(rgb, model='hog')

            # compute the facial embedding for the face
            encodings = face_recognition.face_encodings(rgb, boxes)

            # loop over the encodings
            for encoding in encodings:
                knownEncodings.append(encoding)
                knownNames.append(image_folder)
                versions.append(v)
    result = {}
    idx = 1
    for i, j, k in zip(knownEncodings, knownNames, versions):
        # print(i, j, k)
        binary_data = ndarray.tobytes(i)
        name = j
        # print(type(i), type(j))
        today = date.today()
        today = str(today)
        MyDB = dbase("FaceRecognition")
        MyDB.InsertBlob(binary_data, name, k, today)
        result[f"img{idx}"] = {"name": name, "version": k, "date": today}
        idx += 1
    return result

# It takes id of image as input. This functions then returns the corresponding values using
# RetreiveData function in database.py


def get_face_info(id):
    Mydb = dbase("FaceRecognition")
    Mydb.UseDB("FaceRecognition")
    ans = Mydb.RetrieveData(id)
    result = {}
    if(ans == None):
        return result
    result = {"ID": ans[0], "Name": ans[1],
              "Version": ans[2], "Date": ans[3], "Location": ans[4]}
    return result

# It takes path of image as input along with K (topK matches) and Confidence .
# This functions then read the image, extracts encoding of the image and then using face_recognition library
# functions , compare them with all encodings in the database.
# Then among the matches, we picked up top k matches and returned them.


def search_faces(filename, k, confidence):
    # data = pickle.loads(open('DataSet/face_enc', "rb").read())
    # image for facial recognition
    img = cv2.imread(filename)

    # convert the input frame from BGR to RGB
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # the facial embeddings for face in input
    boxes = face_recognition.face_locations(rgb, model='hog')

    # Encodings
    encodings = face_recognition.face_encodings(rgb, boxes)

    # Creating Dictionary of encodings from database
    Mydb = dbase("FaceRecognition")
    Mydb.UseDB("FaceRecognition")
    known_encodings_data, indexes = Mydb.GetListOfAllBlobs()

    # create a dictionary containing count of all the names then extract top k names
    # Dictionary for ID Numbers in databse for top k matches
    ids = {}
    for i in range(1, len(known_encodings_data)+1):
        ids[i] = 0

    # looping over the facial embeddings incase
    # we have multiple embeddings for multiple faces
    np_known_encodings = numpy.array(known_encodings_data)
    for encoding in encodings:
        np_target_encoding = numpy.array(encoding)

        # Compare encodings with encodings in data["encodings"]
        # Matches contain array with boolean values and True for the embeddings it matches closely
        # and False for rest
        face_distances = face_recognition.face_distance(
            np_known_encodings, np_target_encoding)

        result = []
        for i in range(len(face_distances)):
            if(face_distances[i] <= confidence):
                result.append([face_distances[i], indexes[i]])

    # Top K Matches
    result.sort()
    result = result[0:k]

    # Top K Hits
    ans = {}
    idx = 1
    for i in range(len(result)):
        data = Mydb.RetrieveData(result[i][1])
        ans[f"img{idx}"] = {"ID": data[0], "Name": data[1],
                            "Version": data[2], "Date": data[3], "Location": data[4]}
        idx += 1
    return ans
