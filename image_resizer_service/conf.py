import os

from decouple import config, Csv

SOURCE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SOURCE_DIR)

EXAMPLE_IMAGES_PATH = os.path.join(PROJECT_ROOT, 'data', 'example_images')
EXAMPLE_IMAGE_ORIGIN = os.path.join(EXAMPLE_IMAGES_PATH, 'origin', 'frame_1.png')
# EXAMPLE_IMAGE_ORIGIN_PIL = os.path.join(EXAMPLE_IMAGES_PATH, 'origin', 'pil_frame_1.png')
EXAMPLE_IMAGE_LRS = os.path.join(EXAMPLE_IMAGES_PATH, 'lrs', 'frame_1.png')
EXAMPLE_IMAGE_SRS = os.path.join(EXAMPLE_IMAGES_PATH, 'srs', 'frame_1.png')
EXAMPLE_IMAGE_SRS_CV2 = os.path.join(EXAMPLE_IMAGES_PATH, 'srs', 'cv2_frame_1.png')

REDIS_ADDRESS = config('REDIS_ADDRESS', default='localhost')
REDIS_PORT = config('REDIS_PORT', default='6379')

TRACER_REPORTING_HOST = config('TRACER_REPORTING_HOST', default='localhost')
TRACER_REPORTING_PORT = config('TRACER_REPORTING_PORT', default='6831')

SERVICE_STREAM_KEY = config('SERVICE_STREAM_KEY')

RESIZE_METHOD = config('RESIZE_METHOD', 'cloudseg')

default_carn_model_weights_path = os.path.join(PROJECT_ROOT, 'checkpoint', 'carn.pth')
CARN_MODEL_WEIGHTS_PATH = config('CARN_MODEL_WEIGHTS_PATH', default=default_carn_model_weights_path)
RESIZE_SCALE = config('RESIZE_SCALE', default=4)


# LISTEN_EVENT_TYPE_SOME_EVENT_TYPE = config('LISTEN_EVENT_TYPE_SOME_EVENT_TYPE')
# LISTEN_EVENT_TYPE_OTHER_EVENT_TYPE = config('LISTEN_EVENT_TYPE_OTHER_EVENT_TYPE')

SERVICE_CMD_KEY_LIST = [
]

PUB_EVENT_TYPE_SERVICE_WORKER_ANNOUNCED = config('PUB_EVENT_TYPE_SERVICE_WORKER_ANNOUNCED')

PUB_EVENT_LIST = [
    PUB_EVENT_TYPE_SERVICE_WORKER_ANNOUNCED,
]

# Only for Content Extraction services
# Using Cloudseg as a CE service, just to simplify its use on the framework.
# it should actually be added in the dataflow before the scheduling because
# it seems to belong more to the business domain of stream management rather than the content extraction domain
# but again, just to simplify running this evaluation...
# Example of how to define SERVICE_DETAILS from env vars:
SERVICE_DETAILS_SERVICE_TYPE = config('SERVICE_DETAILS_SERVICE_TYPE')
SERVICE_DETAILS_STREAM_KEY = config('SERVICE_DETAILS_STREAM_KEY')
SERVICE_DETAILS_QUEUE_LIMIT = config('SERVICE_DETAILS_QUEUE_LIMIT', cast=int)
SERVICE_DETAILS_THROUGHPUT = config('SERVICE_DETAILS_THROUGHPUT', cast=float)
SERVICE_DETAILS_ACCURACY = config('SERVICE_DETAILS_ACCURACY', cast=float)
SERVICE_DETAILS_ENERGY_CONSUMPTION = config('SERVICE_DETAILS_ENERGY_CONSUMPTION', cast=float)
SERVICE_DETAILS_CONTENT_TYPES = config('SERVICE_DETAILS_CONTENT_TYPES', cast=Csv())
SERVICE_DETAILS = {
    'service_type': SERVICE_DETAILS_SERVICE_TYPE,
    'stream_key': SERVICE_DETAILS_STREAM_KEY,
    'queue_limit': SERVICE_DETAILS_QUEUE_LIMIT,
    'throughput': SERVICE_DETAILS_THROUGHPUT,
    'accuracy': SERVICE_DETAILS_ACCURACY,
    'energy_consumption': SERVICE_DETAILS_ENERGY_CONSUMPTION,
    'content_types': SERVICE_DETAILS_CONTENT_TYPES
}

LOGGING_LEVEL = config('LOGGING_LEVEL', default='DEBUG')