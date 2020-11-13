# Tensor Flow Lite On GoPiGo3 Robot Carl

Requirements:
- Raspbian For Robots PiOS version 
- PiCamera


== Install TensorFlowLite

https://www.tensorflow.org/lite/guide/python

(For Pi OS 10 which has Python 3.7) 
```
pip3 install https://github.com/google-coral/pycoral/releases/download/release-frogfish/tflite_runtime-2.5.0-cp37-cp37m-linux_armv7l.whl
```

== image classification example for Raspberry Pi

https://github.com/tensorflow/examples/tree/master/lite/examples/image_classification/raspberry_pi

Clone TF examples

```
mkdir ~/Carl/Examples/TF
mkdir ~/Carl/Examples/TF/models
git clone https://github.com/tensorflow/examples --depth 1
cd examples/lite/examples/image_classification/raspberry_pi
bash download.sh /home/pi/Carl/Examples/TF/models


python3 classify_picamera.py  \
 --model /home/pi/Carl/Examples/TF/models/mobilenet_v1_1.0_224_quant.tflite  \
 --labels /home/pi/Carl/Examples/TF/models//labels_mobilenet_quant_v1_224.txt
```

BUT that version assumes you have an HDMI display attached ..


Created gpg_classify_picamera.py 
 - modified to print result to the command-line if confidence greater than setting, 
 - option --confidence to set minimum confidence level (default 0.6)
 - option --preview to show annotated image on HDMI display (default is not to)
 - option --save  to save annotated image (to ./tagged/<label>-<date>-<time>.jpg)

```
Usage: ./gpg_classify_picamera.py \
        --model  <models_path>/mobilenet_v1_1.0_224_quant.tflite \
        --labels <models_path>/labels_mobilenet_quant_v1_224.txt \
       [--preview y  \ ]   # optional flag to show preview on HDMI monitor
       [--confidence 0.x \] # optional (default 0.6) set minimum confidence required
       [--save y ]  # option to save annotated image to ./tagged/<label>-<date>-<time>.jpg
```

created shortcut run_it.sh

Moved the example to ~/Carl/Examples/TF/GoPiGo/  

```
pi@Carl:~/Carl/Examples/TF/GoPiGo/ $ ./run_it.sh 
analog clock 0.71 310.1ms
analog clock 0.60 309.5ms
analog clock 0.62 309.8ms
sliding door 0.60 337.7ms
sliding door 0.61 312.8ms
sliding door 0.66 311.9ms
sliding door 0.69 312.2ms
sliding door 0.62 312.3ms
sliding door 0.74 309.8ms
sliding door 0.67 309.7ms
sliding door 0.70 309.8ms
sliding door 0.66 309.7ms
turnstile 0.69 309.9ms
turnstile 0.79 309.8ms
^C
Exiting
Finally

```
