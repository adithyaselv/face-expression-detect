#!/usr/bin/python
#Title: Script to find emotion using facial expression
#Date:25/10/2015
#Author:Adithya Selvaprithiviraj
#PS: Not trained for nuetral expression


import argparse,sys

try:
    from FeatureGen import*
except ImportError:
    print "Make sure FeatureGen.pyc file is in the current directory"
    exit()

try:
    import dlib
    from skimage import io
    import numpy
    import cv2
    from sklearn.externals import joblib
except ImportError:
        print "Make sure you have OpenCV, dLib, scikit learn and skimage libraries properly installed"
        exit()

emotions={ 1:"Anger", 2:"Contempt", 3:"Disgust", 4:"Fear", 5:"Happy", 6:"Sadness", 7:"Surprise"}

def Predict_Emotion(filename):

    print "Opening image...."
    try:
        img=io.imread(filename)
        cvimg=cv2.imread(filename)
    except:
        print "Exception: File Not found."
        return

    win.clear_overlay()
    win.set_image(img)

    dets=detector(img,1)

    if len(dets)==0:
        print "Unable to find any face."
        return

    for k,d in enumerate(dets):

        shape=predictor(img,d)
        landmarks=[]
        for i in range(68):
            landmarks.append(shape.part(i).x)
            landmarks.append(shape.part(i).y)
        
    
        landmarks=numpy.array(landmarks)
    
        print "Generating features......"
        features=generateFeatures(landmarks)
        features= numpy.asarray(features)

        print "Performing PCA Transform......."
        pca_features=pca.transform(features)

        print "Predicting using trained model........"
        emo_predicts=classify.predict(pca_features)
        print "Predicted emotion using trained data is { " + emotions[int(emo_predicts[0])] + " }"
        print ""

        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(cvimg,emotions[int(emo_predicts[0])],(20,20), font, 1,(0,255,255),2)

        win.add_overlay(shape)

    cv2.namedWindow("Output")
    cv2.imshow("Output",cvimg)
    cv2.waitKey(0)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', type=str, nargs='+', help="Enter the filenames with extention of an Image")
    arg=parser.parse_args()
    
    if not len(sys.argv) > 1:
        parser.print_help()
        exit()

    landmark_path="shape_predictor_68_face_landmarks.dat"

    print "Initializing Dlib face Detector.."
    detector= dlib.get_frontal_face_detector()

    print "Loading landmark identification data..."
    try:
        predictor= dlib.shape_predictor(landmark_path)
    except:
        print "Unable to find trained facial shape predictor. \nYou can download a trained facial shape predictor from: \nhttp://sourceforge.net/projects/dclib/files/dlib/v18.10/shape_predictor_68_face_landmarks.dat.bz2"
        exit()

    win=dlib.image_window()

    print "Loading trained data....."

    try:
        classify=joblib.load("traindata.pkl")
        pca=joblib.load("pcadata.pkl")
    except:
        print "Unable to load trained data. \nMake sure that traindata.pkl and pcadata.pkl are in the current directory"
        exit()

    for filename in arg.i:
        Predict_Emotion(filename)


