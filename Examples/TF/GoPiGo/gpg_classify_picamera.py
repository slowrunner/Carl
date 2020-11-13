# python3
#
# File: gpg_classify_picamera.py
#
# Usage: ./gpg_classify_picamera.py \
#        --model  <models_path>/mobilenet_v1_1.0_224_quant.tflite \
#        --labels <models_path>/labels_mobilenet_quant_v1_224.txt \
#       [--preview y  \ ]   # optional flag to show preview on HDMI monitor
#       [--confidence 0.x \] # optional (default 0.6) set minimum confidence required
#       [--save y ]  # option to save annotated image to ./tagged/<label>-<date>-<time>.jpg
#
# Authors:
#   Alan McDonley
#   The TensorFlow Authors
#
# Copyright 2019 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Using TF Lite to classify objects with the Raspberry Pi camera."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import io
import time
import numpy as np
import picamera
from datetime import datetime
import os

from PIL import Image
from tflite_runtime.interpreter import Interpreter


def load_labels(path):
  with open(path, 'r') as f:
    return {i: line.strip() for i, line in enumerate(f.readlines())}


def set_input_tensor(interpreter, image):
  tensor_index = interpreter.get_input_details()[0]['index']
  input_tensor = interpreter.tensor(tensor_index)()[0]
  input_tensor[:, :] = image


def classify_image(interpreter, image, top_k=1):
  """Returns a sorted array of classification results."""
  set_input_tensor(interpreter, image)
  interpreter.invoke()
  output_details = interpreter.get_output_details()[0]
  output = np.squeeze(interpreter.get_tensor(output_details['index']))

  # If the model is quantized (uint8 data), then dequantize the results
  if output_details['dtype'] == np.uint8:
    scale, zero_point = output_details['quantization']
    output = scale * (output - zero_point)

  ordered = np.argpartition(-output, top_k)
  return [(i, output[i]) for i in ordered[:top_k]]


def main():
  parser = argparse.ArgumentParser(
      formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument(
      '--model', help='File path of .tflite file.', required=True)
  parser.add_argument(
      '--labels', help='File path of labels file.', required=True)
  parser.add_argument(
      '--preview', help='y to get a preview. Otherwise skip preview window for use in jupyter or command-line',default='n')
  parser.add_argument(
      '--confidence', help='Confidence level before printint output.', type=float, default='0.6')
  parser.add_argument(
      '--save', help='y to save tagged image when confidence level met.', default='n')
  args = parser.parse_args()

  labels = load_labels(args.labels)
  preview = args.preview == 'y'
  confidence = float(args.confidence)
  save_tagged_image = args.save == 'y'

  if save_tagged_image:
      if not os.path.exists('tagged'):
          os.makedirs('tagged')

  interpreter = Interpreter(args.model)
  interpreter.allocate_tensors()
  _, height, width, _ = interpreter.get_input_details()[0]['shape']

  print("Starting TensorFlow Lite Classification With PiCamera at 640x480")
  with picamera.PiCamera(resolution=(640, 480), framerate=30) as camera:
    if preview:
        camera.start_preview()
    try:
      stream = io.BytesIO()
      for _ in camera.capture_continuous(
          stream, format='jpeg', use_video_port=True):
        stream.seek(0)
        image = Image.open(stream).convert('RGB').resize((width, height),
                                                         Image.ANTIALIAS)
        start_time = time.time()
        results = classify_image(interpreter, image)
        elapsed_ms = (time.time() - start_time) * 1000
        label_id, prob = results[0]
        stream.seek(0)
        stream.truncate()

        camera.annotate_text = '%s %.2f\n%.1fms' % (labels[label_id], prob,
                                                      elapsed_ms)
        if (prob > confidence):
                print("%s %.2f %.1fms" % (labels[label_id],prob,elapsed_ms))
                if save_tagged_image:
                    fname = "%s-" % labels[label_id] + datetime.now().strftime("%Y%m%d-%H%M%S") + ".jpg"
                    camera.capture(fname)
                    time.sleep(2)

    except KeyboardInterrupt:
        print("\nExiting")

    finally:
      if preview:
          camera.stop_preview()
      print("Finally")

if __name__ == '__main__':
  main()
