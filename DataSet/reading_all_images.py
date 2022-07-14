from cgi import print_directory
from ensurepip import version
import os
import cv2
import face_recognition
from tqdm import tqdm
import pickle
import re

# Using regex to find version of the image


def getVersion(s):
    p = re.findall('[0-9]+', s)
    return p[0]


# Get the list of all files and directories
# in the root directory
path = f"{os.getcwd()}/LFW_Dataset/lfw_funneled"
dir_list = os.listdir(path)
images_list = []
knownNames = []
knownEncodings = []
versions = []


for i in tqdm(range(len(dir_list)), desc="Loading..."):
    folder = dir_list[i]
    path_image_folder = path+"/"+folder
    if '.' in path_image_folder:
        continue
    # Now we have a list of all the folders that contain the images
    # print(folder)

    # list of all the images
    images = os.listdir(path_image_folder)
    # print(images)
    for img_name in images:
        image_path = path_image_folder+"/"+img_name

        # GetVersion
        v = getVersion(img_name)
        test_img = cv2.imread(image_path)
        rgb = cv2.cvtColor(test_img, cv2.COLOR_BGR2RGB)
        images_list.append(rgb)
        # Use Face_recognition to locate faces using hog model
        boxes = face_recognition.face_locations(rgb, model='hog')

        # compute the facial embedding for the face
        encodings = face_recognition.face_encodings(rgb, boxes)

        # loop over the encodings
        for encoding in encodings:
            knownEncodings.append(encoding)
            knownNames.append(folder)
            versions.append(v)
        # cv2.imshow("OG", rgb)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

# print(knownEncodings)
# print(knownNames)

print("Files and directories in '", path, "' :")

# save emcodings along with their names in dictionary data
data = {"encodings": knownEncodings, "names": knownNames, "versions": versions}

# use pickle to save data into a file for later use
f = open("DataSet/face_enc", "wb")
f.write(pickle.dumps(data))
f.close()
