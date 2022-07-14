Submitter name: RHYTHM JAIN

Roll No.: 2019CSB1111

=================================

# What does this program do

This program uses a database of photos to perform a "facial search." The application is a secure API service that may be accessed by submitting an HTTP post request to the endpoint of the API. The databse stores an efficient representation of the image. It performs efficient and fast retrieval of top-k matches of facial recognition.

# A description of how this program works (i.e. its logic)

### It contains the following files and folders:
* LWF_Dataset
* uploads
* Database.py
* face_recog.py
* main.py
* testing.py

For easy understanding and increase the utility of classes, I have made separate functions for different pupose and uses.

Dataset Folder
This folder contains a file that reads all the images in the LFW_Dataset folder and stores the encodins in a file called "face_enc".
This folder also contains "face_enc" file that contains face encodings of all 13813 images present in the LWF Dataset.

LFW_Dataset Folder
This folder contains the LWF dataset of around 13813 images. The images are organised such that first there is folder by name of a person and then the images of the person.

uploads folder
This folder is used as the storage folder for all the image files and zip files provided as input to the flask-api using html forms. All the files uploaded in functions such add_face(), add_faces_in_bulk() and search_faces(), the files are first saved in the uploads folder in the local directory.

Database Class
I have made a separete database class called database.py . Here i have defined proper functions with their respective workings.
Class dbase is the database class that contains following functions-

    * UseDB : Selects the database to be used for sql queries

    * CreateTable : Creates a table for Images. here i am using storing encodings of the images using a blob type table parameter

    * InsertBlob : This function inserts the encodings of an image to the table. Here encodings are first converted to bytes data type using ndarray.tobytes() function from numpy library.

    * RetrieveBlob : This function helps retrieve the encoding value for a particular index id.

    * GetListOfAllBlobs : This function helps retrieve the encoding of all the images stored in the database to be used later for face matching algorithm.

    * RetrieveData : This function helps retrieve the data value for a particular index id.

    * Inserting_Encodings_In_Table : This function inserts all the encodings the table from a given file.

main.py
This is our main flask-api file. This contains the functions such as:
    * add_face() : This endpoint contains a html form, where we have to provide input file as well as parameters such as name, location, version and date. This functions then extracts values and calls add_face() funtion defined in face_recg.py.

    * add_faces_in_bulk() : This endpoint contains a html form, where we have to provide input file . This functions then extracts values and calls add_faces_in_bulk() funtion defined in face_recg.py. Here zip file must be organised such that it contains folder of images by image name and then images inside those folder. For example, for eg, all images named Aaron_Eckhart must be in Aaron_Eckhart folder.

    * search_faces() : This endpoint contains a html form, where we have to provide input file as well as parameters such as value of K in top k matchings and value of confidence between 0-100 percent.This functions then extracts values and calls search_faces() funtion defined in face_recg.py.

    * get_face_info() : This endpoint contains a html form, where we have to provide input parameters such as image id for which information needed to be extracted. This functions then extracts values and calls get_face_info() funtion defined in face_recg.py.

    * success_add_face() : All other api-endpoints are redirected to the endpoints after succesfull query processing in order to display the result.

face_recog.py
This file contains most of the main functions used in main.py:

    * add_face() : It takes 5 values as input(filename,name,version,date,location).This functions then extracts values and  extracts encoding of the image and then convert it to bytes data and insert the respective values in the table.

    * add_faces_in_bulk() : It takes path of zip as input.This functions then extracts the zip file in uploads folder and then using os library iterate over all the folders, read the images, extracts encoding of the image and then convert it to bytes data and insert the respective values in the table.

    * search_faces() : It takes path of image as input along with K (topK matches) and Confidence . This functions then read the image, extracts encoding of the image and then using face_recognition library functions , compare them with all encodings in the database.
    Then among the matches, we picked up top k matches and returned them.

    * get_face_info() : It takes id of image as input. This functions then returns the corresponding values using RetreiveData function in database.py

Testing.py
This function contains testing of each of the functions used in main.py. We are using unittest library for the same purpose. We are using post request to test the output of the function if it is a success or not.

# How to compile and run this program

To Insert Data in the database , run the following in Dataset Folder:
python3 reading_all_images.py

To Run the server , run :
python3 main.py

To test, run:
python3 testing.py

To provide input to the main.py flask-api endpoints, open the cooresponding endpoint in your browser after running the server and then provide respective outputs.

# Assumptions

    1. Zip File format.The images are organised such that first there is folder by name of a person and then the    images of the person. Here zip file must be organised such that it contains folder of images by image name and then images inside those folder. For example, for eg, all images named Aaron_Eckhart must be in Aaron_Eckhart folder.

    2. All values in the html forms must be provided and cant be left blank.

    3. Make sure that server is running before running testing.py
