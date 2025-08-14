from query_device import get_devpath
import os

def get_device_id(device_filepath:str):
    """
    Get the unique vendor id and product id for an device.

    returns a string in the form of: "vendor_id:product_id"
    """
    
    if not os.path.exists(device_filepath):
        raise FileNotFoundError(f"{device_filepath} does not exist. 'device_filepath' is required to be a path pointing to an existing device file")

    path = os.path.abspath(device_filepath)
    path = get_devpath(path)
    path = "/sys" + path
    path = "/".join(path.split("/")[:-3])

    vendor_id_path = os.path.join(path, "idVendor")
    product_id_path = os.path.join(path, "idProduct")

    with open(vendor_id_path) as f:
        vendor_id = f.read().replace("\n", "")

    with open(product_id_path) as f:
        product_id = f.read().replace("\n", "")

    return f"{vendor_id}:{product_id}"