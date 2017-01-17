# Some installation and compilation notes

## On Raspberry Pi 1 with Raspbian Lite

The aim is to compile OpenCV, install the necessary packages, Python 3, and a minimal window manager
and display server. With this we can use OpenCV's ```imshow``` display function.
 
```apt-get install build-essential cmake pkg-config```  
```apt-get install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev```  
```apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev```  
```apt-get install libgtk2.0-dev```  
```apt-get install libatlas-base-dev gfortran```  
```apt-get install python3-dev```  
```apt-get install python3-pip```  
```pip3 install numpy```  
```pip3 install picamera```  
```apt-get install libgtkglext1 libgtkglext1-dev``` (OpenGL support for OpenCV)  
```apt-get install libgl1-mesa-dri``` (OpenGL support for minimal Xorg + Openbox)  
  
Download OpenCV and opencv_contrib modules  
```
cd ~
wget -O opencv.zip https://github.com/Itseez/opencv/archive/3.0.0.zip
unzip opencv.zip
cd ..
wget -O opencv_contrib.zip https://github.com/Itseez/opencv_contrib/archive/3.0.0.zip
unzip opencv_contrib.zip
```
Compile OpenCV (takes ages on a RPI 1):  
```
sudo cmake -D CMAKE_BUILD_TYPE=RELEASE \
	-D CMAKE_INSTALL_PREFIX=/usr/local \
	-D INSTALL_C_EXAMPLES=OFF \
	-D INSTALL_PYTHON_EXAMPLES=OFF \
	-D BUILD_EXAMPLES=OFF \
	-D BUILD_DOCS=OFF
	-D OPENCV_EXTRA_MODULES_PATH=/root/opencv_contrib-3.0.0/modules
	-D WITH_OPENGL=0N ..

make -j1
make install
ldconfig
```  
Python bindings have to be renamed:  
```
cd /usr/local/lib/python3.4/dist-packages/
mv cv2.cpython-34m.so cv2.so
```
Verify OpenCV Python3 module:  
```
$ python3
>>> import cv2
>>> cv2.__version__
'3.0.0'
```
Install a lightweight Xorg display server, Openbox window manager and LightDM login manager:  
```
apt-get install --no-install-recommends xserver-xorg
apt-get install openbox
apt-get install lightdm
```
Reboot, done!  


## Pygame installation on Raspberry Pi 1

Pygame can be used to render to the frame buffer through Python.

```
apt-get install python3-dev python3-numpy libsdl-dev libsdl-image1.2-dev \
  libsdl-mixer1.2-dev libsdl-ttf2.0-dev libsmpeg-dev libportmidi-dev \
  libavformat-dev libswscale-dev libjpeg-dev libfreetype6-dev
apt-get install python-pygame 
```


## Compiling OpenCV on Mac OS Yosemite (10.10.5)

Homebrew package failed to install OpenCV, whatever option was passed in. Compile OpenCV manually.
Follow [Adrian Rosebrock's instructions](http://www.pyimagesearch.com/2015/06/29/install-opencv-3-0-and-python-3-4-on-osx/) 
but before the CMake configuration change in ```vtkRenderingOpenGL``` to ```vtkRenderingOpenGL2``` in ```cmake/OpenCVDetectVTK.cmake``` on line 6.  
  
CMake command (replace the Python3 folders according to your version):
```
cmake -D CMAKE_BUILD_TYPE=RELEASE \
	-D CMAKE_INSTALL_PREFIX=/usr/local \
	-D PYTHON3_PACKAGES_PATH=/usr/local/lib/python3.5/site-packages \
	-D PYTHON3_LIBRARY=/usr/local/Cellar/python3/3.5.2_3/Frameworks/Python.framework/Versions/3.5/lib/libpython3.5m.dylib \
	-D PYTHON3_INCLUDE_DIR=/usr/local/Cellar/python3/3.5.2_3/Frameworks/Python.framework/Versions/3.5/include/python3.5m \
	-D PYTHON3_EXECUTABLE=$(which python3) \
	-D INSTALL_C_EXAMPLES=OFF \
	-D INSTALL_PYTHON_EXAMPLES=ON \
	-D BUILD_EXAMPLES=OFF \
	-D BUILD_DOCS=OFF \
	-D WITH_FFMPEG=OFF \
	-D WITH_VTK=OFF \
	-D BUILD_opencv_python3=ON \
	-D OPENCV_EXTRA_MODULES_PATH=/Users/Arnaud/opencv_contrib/modules ..

make -j2
make install
```