from lerobot.cameras.opencv import OpenCVCamera, OpenCVCameraConfig
from cogitron import config
from cogitron.query_device import get_device_id
from typing import Any

def get_camera_config():
    cameras = OpenCVCamera.find_cameras()
    cameras_filtered = list(filter(lambda x:get_device_id(x["id"])==config.LOGITECH_CAMERA_ID, cameras))
    
    try:
        camera:dict[str, Any] = cameras_filtered[0]
    except IndexError:
        raise RuntimeError(f"Logitech camera not found. Make sure it is plugged in. Found cameras: {cameras}")

    usb_camera_port = camera["id"]
    stream_profile = camera["default_stream_profile"]

    return OpenCVCameraConfig(index_or_path=usb_camera_port, width=stream_profile["width"], height=stream_profile["height"], fps=stream_profile["fps"])