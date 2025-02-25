from depth_anything.dpt import DepthAnything
from depth_anything.util.transform import Resize, NormalizeImage, PrepareForNet
import numpy as np
import cv2
import torch
from torchvision.transforms import Compose

encoder = 'vits' # can also be 'vitb' or 'vitl'
depth_anything = DepthAnything.from_pretrained('LiheYoung/depth_anything_{:}14'.format(encoder)).eval()

transform = Compose([
    Resize(
        width=518,
        height=518,
        resize_target=False,
        keep_aspect_ratio=True,
        ensure_multiple_of=14,
        resize_method='lower_bound',
        image_interpolation_method=cv2.INTER_CUBIC,
    ),
    NormalizeImage(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    PrepareForNet(),
])

image = cv2.cvtColor(cv2.imread('DSC01677.jpg'), cv2.COLOR_BGR2RGB) / 255.0
image = transform({'image': image})['image']
image = torch.from_numpy(image).unsqueeze(0)

# depth shape: 1xHxW
depth = depth_anything(image)
# Run the depth estimation model on the current frame
# The pipeline returns a dict with key "depth"
print(depth)




def save_tensor_as_image(tensor, filename):
    # Konverter til NumPy, frakoble fra beregningsgrafen og flytt til CPU
    tensor = tensor.detach().cpu().numpy()
    
    # Fjern unødvendige dimensjoner
    tensor = np.squeeze(tensor)
    
    # Normaliser til 0-255 og konverter til uint8
    tensor_norm = (tensor - np.min(tensor)) / (np.max(tensor) - np.min(tensor))
    tensor_uint8 = (tensor_norm * 255).astype(np.uint8)
    
    # Lagre bildet
    cv2.imwrite(filename, tensor_uint8)

# Bruk funksjonen til å lagre bildene
save_tensor_as_image(depth, "dybdeimage3.png")
save_tensor_as_image(depth, "depth_map.jpg")



"""
tensor  = depth.cpu().numpy() # make sure tensor is on cpu
cv2.imwrite(tensor, "Dybde.png")

depth_map = depth
# Ensure depth_map is a numpy array (if not already)
# save depth map
cv2.imwrite("depth_map.jpg", depth_map)

"""



