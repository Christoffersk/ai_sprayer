# The AI sprayer

The AI sprayer is a system that uses a combination of traditional computer vision and modern ai based object detection to keep your cats (or other animals) away from certain areas. The system uses a combination of hardware(listed in the HARDWARE.md file) and software (from this repo) to detect animals and use an active deterrent system.

### Use it

The code is built using poetry and installed as a package. It is then run as a normal python module without argument.

```python
poetry build
pip install aisprayer.[].whl
python3 -m aisprayer
```

## How it works

The code consists of two parts that run in threads:

- The backend which runs the object detection and active deterrent
- The front end that allows you to change configurations and view the camera detections

### Detection backend

The detection system runs in two different modes. The normal detection takes an image every second(default) and uses PIL to measure how much the image has changed from the last one. If the change is small then the system sleeps until the next second.

If it is larger than a defined threshold, then the image is sent to a object detection endpoint (In this case [Deepstack](https://deepstack.cc/) is used) that looks for the objects defined in the configuration. If the object is found then the sprayer is activated, which in the default case starts a water pump for 1 second spraying water on the assailant.

## Frontend
