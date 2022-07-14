
from mysql.connector import errorcode
import mysql.connector
from numpy import float64, ndarray
import numpy
import pickle
from datetime import date


class dbase:
    def __init__(self, FaceRecognition):
        try:
            self.MyDB = mysql.connector.connect(
                host="localhost", user="root", password="00000000", database=f"{FaceRecognition}")
            self.Mycursor = self.MyDB.cursor()

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
                print("Creating Database")
                self.MyDB = mysql.connector.connect(
                    host="localhost", user="root", password="00000000")
                self.Mycursor = self.MyDB.cursor()
                self.Mycursor.execute(f"CREATE DATABASE {FaceRecognition}")

            else:
                print(err)

    # Selects the database to be used for sql queries
    def UseDB(self, dbname):
        self.Mycursor.execute(f"USE {dbname}")

    # Creates a table for Images. here i am using storing encodings of the images using a blob type table parameter
    def CreateTable(self):
        self.Mycursor.execute("""CREATE TABLE IF NOT EXISTS Images (
            Id INTEGER(45) NOT NULL AUTO_INCREMENT PRIMARY KEY, 
            Photo MEDIUMBLOB NOT NULL, 
            Name VARCHAR(100) NOT NULL ,
            Version VARCHAR(20),
            Date VARCHAR(20),
            Location VARCHAR(20) )""")
        print("TABLE CREATED")

    # This function inserts the encodings of an image to the table. Here encodings are first converted to bytes data type using ndarray.tobytes() function from numpy library.
    def InsertBlob(self, Photo, Name, Version="NULL", Date="NULL", Location="NULL"):
        sql = "INSERT INTO IMAGES (Photo,Name,Version,Date,Location) VALUES(%s,%s,%s,%s,%s)"
        self.Mycursor.execute(sql, (Photo, Name, Version, Date, Location, ))
        self.MyDB.commit()
        print("INSERT DONE")
    # This function helps retrieve the encoding value for a particular index id.

    def RetrieveBlob(self, ID):
        sql = "SELECT * FROM Images  where ID='{0}'"
        self.Mycursor.execute(sql.format(str(ID)))
        MyResult = self.Mycursor.fetchone()[1]
        blob = numpy.frombuffer(MyResult, float64)
        print("SELECT ENCODING DONE")
        return blob

    # This function helps retrieve the encoding of all the images stored in the database to be used later for face matching algorithm
    def GetListOfAllBlobs(self):
        sql = "SELECT * FROM Images "
        self.Mycursor.execute(sql)
        MyResult = self.Mycursor.fetchall()
        ans = []
        indexes = []
        for element in MyResult:
            encoding = element[1]
            idx = element[0]-1
            encoding = numpy.frombuffer(encoding, float64)
            ans.append(encoding)
            indexes.append(idx)
        print("LIST OF ALL BLOBS")
        return ans, indexes

    # This function helps retrieve the data value for a particular index id.
    def RetrieveData(self, ID):
        sql = "SELECT * FROM Images  where ID='{0}'"
        self.Mycursor.execute(sql.format(str(ID)))
        MyResult = self.Mycursor.fetchone()
        print("SELECT DONE")
        if(MyResult == None):
            return None
        return MyResult[0:1]+MyResult[2:]

    # function to insert all encodins of the dataset into the table
    def Inserting_Encodings_In_Table(self, filename):
        data = pickle.loads(open(f"{filename}", "rb").read())
        # print(data)
        encodings = data["encodings"]
        names = data["names"]
        versions = data["versions"]

        for i, j, k in zip(encodings, names, versions):
            binary_data = ndarray.tobytes(i)
            name = j
            # print(type(i), type(j))
            today = date.today()
            today = str(today)
            self.InsertBlob(binary_data, name, k, today)
        print("INSERT ALL DONE")

#Inserting Data to Database
# Mydb = dbase("FaceRecognition")
# Mydb.UseDB("FaceRecognition")
# Mydb.CreateTable()
# Mydb.Inserting_Encodings_In_Table('DataSet/face_enc')
# print(Mydb.GetListOfAllBlobs())
# print(Mydb.RetrieveData(3))
