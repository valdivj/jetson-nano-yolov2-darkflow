# jetson-nano-stuff
Items in this repository

1.Instructions on how to setup and run yoloV2 darkflow on jetson nano 

2.Instructions on how to setup and run yoloV2 darkflow as webserver on Jetson nano

3.Instructions on how to setup and run Kinect2 on Jetson nano

4.Instructions on how to run YoloV2 Model using the Kinect2

5.Instructions on how to record and playback video on Jetson nano

6. Instructions to how to send Data from the Jetson Nano to a Allen Bradley CLX5000


# 1.jetson-nano-yolov2-darkflow

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

When you get to the part where you download opencv make sure you get the latest version.
There is a bug in  Ver 4.0 that was repaired
Use this:

$ wget -O opencv.zip https://github.com/opencv/opencv/archive/4.1.0.zip

$ wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/4.1.0.zip




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

8.$ python yolov2_od_webcam _csi.py : this runs yolov2 on a rasberry pi camera

9.$ python yolov2_od_webcam.py : this runs yolov2 on a webcam:logitech webcam

#2.jetson-nano-yolov2-darkflow-webserver

link to video:https://youtu.be/DG5Sc1Iy-Gs

I have added some programs that will let you stream the yolo model or just a webcam images to a web browser from the nano.
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


#3.Jetson_nano_YOLO_Kinect2_Depth

Take 'nano_kinect.py' from this repo and put it in youre darkflow folder you created earlier.
You will need at least 5v at 4 amps to run this program.
You have to install libfreenect2 & pylibfreenect2 to run:nano_Kinect.py

Following are the steps I took to get the Kinect2 to run on  jetson nano.
These steps will let you run the Kinect2 in C++ and Python.

you need to have youre nano setup with instructions from this repo:
https://github.com/valdivj/jetson-nano-yolov2-darkflow

You need to make sure that you have installed Opencv 4.1.
There is a bug in opencv 4.0 that makes the Kinect2 angry.

To get started head on over to: https://github.com/OpenKinect/libfreenect2
This is the Libfreenect2 repo.
We will need to install this first before we can install Pylibfreenect2.
Scroll down to the LINUX install section and start there:

You need to replace "/joev/" with youre path name.

These are the commands I used:

1.$git clone https://github.com/OpenKinect/libfreenect2.git

2.$cd libfreenect2

3.$sudo apt-get install build-essential cmake pkg-config

4.$sudo apt-get install libusb-1.0-0-dev

5.$sudo apt-get install libturbojpeg0-dev

6.$sudo apt-get install libglfw3-dev

7.$sudo apt-get install libopenni2-dev

8.$mkdir build

9.$cd build

10.$cmake .. -DCMAKE_INSTALL_PREFIX=$HOME/freenect2

11.$make

12.$make install

13.$sudo cp ../platform/linux/udev/90-kinect2.rules /etc/udev/rules.d/

14.$cd /home/joev/libfreenect2/build

To test that everything works run:sudo ./bin/Protonect.
You should get a video and depth streams.
This install was preaty straight forward.

# Now to install Plibfreenect2 so we can run Kinect2 in python

head over to :https://github.com/r9y9/pylibfreenect2

You need to replace "/joev/" with youre path name.

1. $sudo ~/.bashrc

2. Scroll down to the bottom and install this:

export LIBFREENECT2_INSTALL_PREFIX=/home/joev/libfreenect2/

export LD_LIBRARY_PATH=/home/joev/freenect2/lib:$LD_LIBRARY_PATH

3. ctrl x then enter yes then enter.

4. $source ~/.bashrc

5. Copy "config.h" & "export.h" from /home/joev/libfreenect2/build/libfreenect2/
and install them in:
/home/joev/libfreenect2/include/libfeenect2/

6. to test run:
${LIBFREENECT2_INSTALL_PREFIX}include/libfreenect2/config.h
if everything is in right place it will return:
bash: /home/joev/libfreenect2/include/libfreenect2/config.h:permission denied

7. copy "lib" folder from :/home/joev/libfreenect2/build/
and put in:
/home/joev/libfreenect2/ 

8. Go ahead and start youre .virtual enviroment.

9.$pip install pylibfreenect2

10.$pip install git+https://github.com/r9r9/pylibfreenect2

11.$git clone https://github.com/r9r9/pylibfreenect2.git

12.$cd /home/joev/pyliqbfreenect2/examples

13.to test install run :$python selective_stream.py


# 4. To run nano_kinect.py

1.Take 'nano_Kinect.py' from this repo and put it in youre darkflow folder you created earlier.

2.$ cd darkflow

3.$ python nano_kinect.py


# 5. To run record and playback function on jetson nano

1.Go ahead and move 'webcam_YOLO_Player.py' & 'webcam_record.py' from this repo to the darkflow folder you created eairler.

2.Change the paths to your videos folder in both programs.

3.Make sure youre webcam is pluged in and get in youre virtual enviroment.

4.$ cd darkflow

5.$ python webcam_record.py :to record video.

6.$ python webcam_YOLO_Player.py : to playback recorded video in YOLO model

# 6. To send data from Nano to Allen Bradley CLX5000 PLC
Now this one is really only for people that will be using there Nano in a Industrial or manufactoring emviroment.
Communiication to a PLC is a must for those enviroments.

1. Move these files from this repo to the darkflow folder you created earlier.

:cli.py

:eip.py

:lgxDevice.py

:yolov2_PLC.py

2. $ pip install pylogic

3. You will need Allen Bradley RSlogix 5000 software to complete the folowing task. Using RSLOGIX software create 2 Tags in processor.

:Nano_YOLO_Label :as a string Tag

:Nano_YOLO_Confidence :as a string Tag

4. Change the I.P. address in the 'yolov2_PLC.py' program to the address of youre CLX 5000 processor.

5. There is no comms checking in this program so if you run this and it hangs up make sure you can ping the CLX5000 processor.















