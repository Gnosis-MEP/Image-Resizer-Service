import torch

from image_resizer_service.cloudseg.load_model import setup_carn, run_model
import cv2

class Resizer():
    def __init__(self, scale, res_type):
        self.scale = scale
        self.res_type = res_type
        self.model = None
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        if self.res_type == 'cloudseg':
            self.res_func = self.cloudseg_res
        else:
            self.res_func = self.ocv_res

    def setup(self):
        if self.res_type == 'cloudseg':
            self.res_func = self.cloudseg_res
            self.model = setup_carn(self.device)

    def _resize(self, image, target_size, interpolation=cv2.INTER_AREA):
        # Resize the image to have a fixed shorter edge of target_size while maintaining the aspect ratio
        w, h = image.shape[:2]
        aspect_ratio = h / w

        if aspect_ratio < 1:
            width = target_size
            height = int(width / aspect_ratio)
        else:
            height = target_size
            width = int(height * aspect_ratio)

        resized_image = cv2.resize(image, (width, height), interpolation=interpolation)
        return resized_image

    def ocv_res(self, image_ndarray):
        res_size = min(image_ndarray.shape[:2]) * self.scale
        res_image_ndarray = self._resize(image_ndarray, res_size, interpolation=cv2.INTER_LINEAR)
        return res_image_ndarray

    def cloudseg_res(self, image_ndarray):
        with torch.no_grad():
            slr_image = run_model(self.model, self.device, image_ndarray)
        return slr_image

    def run(self, image_ndarray):
        return self.res_func(image_ndarray)