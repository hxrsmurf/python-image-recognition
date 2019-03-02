# python-image-recognition

This uses [AWS Rekognition](https://docs.aws.amazon.com/rekognition/latest/dg/images-bytes.html). 

I did manage to find the Google Vision Python I copied from Google's documentation. [google_vision.py](https://github.com/hxrsmurf/python-image-recognition/blob/master/google_vision.py). I hope to implement this into the existing python script as a new function. And then maybe compare both results to double-check them. 

The `nullDirectories()` function is not really a function. It's a placeholder so I can quickly update the actual variables right below. Remember to do that when you run the Python script.

Python Requirements:

* pillow
* boto3

Bugs:

* Cannot Sort:
  * Multiple recognitions
  * GIF/GIFV
* Cannot parse names like:
  * John Doe "John" Doe

To Do:

* Correct error handling
* Multiple subreddits (done)
* Extract face from GIF/GIFV, then sort
* Implement a label selector
* Possibly separate function for folders, gifs, and other unsupported types
* Pair with Google Vision

Links:
* [Stackoverflow - Move Files](https://stackoverflow.com/questions/2909975/python-list-directory-subdirectory-and-files)
* [AWS Rekognition](https://docs.aws.amazon.com/rekognition/latest/dg/images-bytes.html)
* [Google Vision](https://cloud.google.com/vision/docs/internet-detection)
