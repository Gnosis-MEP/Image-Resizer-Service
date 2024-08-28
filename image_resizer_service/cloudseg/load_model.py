from collections import OrderedDict

from PIL import Image
import cv2
import numpy as np
import torch
import torchvision.transforms as transforms

from image_resizer_service.cloudseg.model import carn
from image_resizer_service.conf import CARN_MODEL_WEIGHTS_PATH, RESIZE_SCALE


def setup_carn(device):
    model = carn.Net(multi_scale=True, group=1)
    state_dict = torch.load(CARN_MODEL_WEIGHTS_PATH, weights_only=False)

    new_state_dict = OrderedDict()
    for name, v in state_dict.items():
        new_state_dict[name] = v

    model.load_state_dict(new_state_dict)
    torch.set_grad_enabled(False)

    model = model.to(device)
    model.eval()
    return model

def resize(image, target_size, interpolation=cv2.INTER_AREA):
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


transform = transforms.Compose([
            transforms.ToPILImage(),
            transforms.ToTensor()
        ])

def get_input_tensor(ndarr):
    return transform(ndarr)


def run_model(net, device, image):
    lrs = torch.cat([
        get_input_tensor(image).unsqueeze(0)
    ]).to(device)

    srs_tensor = net(lrs, RESIZE_SCALE).detach().squeeze(0)
    srs_image = srs_tensor.cpu().mul(255).clamp(0, 255).byte().permute(1, 2, 0).numpy()
    return srs_image


def run_sample():
    import time
    from image_resizer_service.conf import (
        EXAMPLE_IMAGE_ORIGIN,
        EXAMPLE_IMAGE_LRS,
        EXAMPLE_IMAGE_SRS,
        EXAMPLE_IMAGE_SRS_CV2,
    )
    img_origin = cv2.imread(EXAMPLE_IMAGE_ORIGIN)

    lrs_img_bgr = resize(img_origin, 270)
    cv2.imwrite(EXAMPLE_IMAGE_LRS, lrs_img_bgr)
    lrs_img_rgb = cv2.cvtColor(lrs_img_bgr, cv2.COLOR_BGR2RGB)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = setup_carn(device)
    with torch.no_grad():
        t0 = time.perf_counter()
        slr_image = run_model(model, device, lrs_img_rgb)
        t1 = time.perf_counter()
        slr_image_bgr = cv2.cvtColor(slr_image, cv2.COLOR_RGB2BGR)
        cv2.imwrite(EXAMPLE_IMAGE_SRS, slr_image_bgr)

        print(t1 - t0)
    slr_simple_bgr = resize(lrs_img_bgr, 1080, interpolation=cv2.INTER_LINEAR)
    cv2.imwrite(EXAMPLE_IMAGE_SRS_CV2, slr_simple_bgr)




if __name__ == '__main__':
    run_sample()