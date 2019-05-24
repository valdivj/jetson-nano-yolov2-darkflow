# jetson-nano-yolov2-darkflow
run yolov2 darkflow on jetson nano

Link to video:https://youtu.be/usdKZIZWSaE

These are the steps I used to get yolov2 darkflow to run on my jetson nano.
It runs about 4 fps.
Its straight up tiny yolo. Im working on a TensorRT version.

This whole procedure takes about 3 hours from start to finish.

1. You will need at least a 64 gb micro sd card.
I assume that you have already loaded the nano image onto youre jetson nano.
You will need an editor later on so you might want to load "nano":
sudo apt-get install nano

2.Open up the terminal and lets get started.

3.Head on over to jetsonhacks and run this tutorial:
https://www.jetsonhacks.com/2019/04/14/jetson-nano-use-more-memory/
This will give us more memory to take advantage of.
Dont forget to thank the good people of jetsonhacks.

4. Then head on over to PyImageSearch and run this tutorial:
https://www.pyimagesearch.com/2019/05/06/getting-started-with-the-nvidia-jetson-nano/
I went ahead and named my virtual env "cvnano".

5. Since we are at PyImageSearch lets move onto installing opencv4 on the nano.
I know this tutorial is for installing opencv4 on Ubunta in general but it worked on installing opencv4 on the nano.
:https://www.pyimagesearch.com/2018/08/15/how-to-install-opencv-4-on-ubuntu/
We can skip some of the steps that were completed in the last tutorial.
Like installing numpy and creating a virtual enviroment.
We will use the one we made in the previouse tutorial.
I also skipped the beginning were everything is updated.
I also ran this tutorial in the envoriment that I created in the last tutorial.

I got a bit confused when I got to step 5 in this tutorial.
You have to pay attention to the wording.

Here is my path:/usr/local/python/cv2/python-3.6
and here is my file: cv2.cpython-36-aarch64-linux-gnu.so

Here is my virtual env path:~/virtualenvs/cvnano/lib/python3.6/sitepackage/

Here is my final binding path:ln -s/usr/local/python/cv2/python3.6/cv2.so cv2.so

If you havent got in on Adrian's kickstarter campiagn you should.
He is the best 'explainer' I have come across.

6. OK now to install darkflow. Stay with me we are almost done.
go to this website for instructions to install Darkflow:
https://towardsdatascience.com/yolov2-object-detection-using-darkflow-83db6aa5cf5f


$ pip install Cython

$ git clone https://github.com/thtrieu/darkflow.git

$ cd darkflow

$ python3 setup.py build_ext --inplace

$ pip install .


Dont forget to download the weights and CFG file.
I will aslo have some in my repo you can use.

7. Now download the files from this repo.
There is a bin file and CFG file.
Put those in you darkflow folder

Also move labels.txt to the darkflow folder.
This is the list that matches the 'yolov2-tiny-voc.cfg' file that 
is provided in this repo.

To get tiny yolov2 to run go to the :'darkflow\darkflow\utils' folder
and open 'loader.py' and go to about line 122 and set self.offset to 16.

yolov2-voc:'self.offset = 20'

yolov2-tiny-voc:'self.offset = 16'

yolov2_od_webcam _csi.py : this runs yolov2 on a rasberry pi camera

yolov2_od_webcam.py : this runs yolov2 on a webcam:logitech webcam

# jetson-nano-yolov2-darkflow-webserver

I have added some programs that will let you stream the yolo model or just a webcam images to a web browser from the nano
If you have followed the instructions above you should be able to run this.

1.Make sure you are in the enviroment you created and install flask
:pip install flask. 

2.Take these items from this repo and put them in youre darkflow folder you created earlier.

:app.py

:base_camera.py

:camera_opencv.py #yolo webcam

:camera_opencv2.py #just webcam

:Templates folder

To start run this command in youre enviroment from inside the  darkflow folder you created earlier.

$ qunicorn --threads 5 --workers 1 --bind 0.0.0.0:5000 app:app

Then open up a web browser and put in the I.P. address of the nano followed by :5000

To change between yolo webcam and just webcam change camera_opencv.py to camera_opencv2.py
and rerun 

$ qunicorn --threads 5 --workers 1 --bind 0.0.0.0:5000 app:app









