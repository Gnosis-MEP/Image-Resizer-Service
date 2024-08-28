#!/usr/bin/env python
import uuid
import json

import cv2

from event_service_utils.streams.redis import RedisStreamFactory

from image_resizer_service.file_cli import ReplaceKeyRedisImageCache
from image_resizer_service.conf import (
    REDIS_ADDRESS,
    REDIS_PORT,
    SERVICE_STREAM_KEY,
    EXAMPLE_IMAGE_ORIGIN,
    EXAMPLE_IMAGE_LRS,
)


def make_dict_key_bites(d):
    return {k.encode('utf-8'): v for k, v in d.items()}


def new_msg(event_data):
    event_data.update({'id': str(uuid.uuid4())})
    return {'event': json.dumps(event_data)}



def main():
    stream_factory = RedisStreamFactory(host=REDIS_ADDRESS, port=REDIS_PORT)
    redis_fs_cli_config = {
        'host': REDIS_ADDRESS,
        'port': REDIS_PORT,
        'db': 0,
    }
    file_storage_cli = ReplaceKeyRedisImageCache()
    file_storage_cli.file_storage_cli_config = redis_fs_cli_config
    file_storage_cli.expiration_time = 10
    file_storage_cli.initialize_file_storage_client()

    origin_img_bgr = cv2.imread(EXAMPLE_IMAGE_ORIGIN)
    origin_heigh, origin_width = origin_img_bgr.shape[:2]
    lrs_img_bgr = cv2.imread(EXAMPLE_IMAGE_LRS)
    lrs_img_rgb = cv2.cvtColor(lrs_img_bgr, cv2.COLOR_BGR2RGB)
    img_key = file_storage_cli.upload_inmemory_to_storage(lrs_img_rgb)

    data_stream = stream_factory.create(SERVICE_STREAM_KEY, stype='streamOnly')
    import ipdb; ipdb.set_trace()
    data_stream.write_events(
        new_msg(
            {
                'image_url': img_key,
                'width': origin_width,
                'height': origin_heigh,
                'color_channels': 'rgb',
                'vekg': {},
                'data_path': [],
                'data_flow': [['irs-data'], ['od-data']],
            }
        )
    )

    img_key = file_storage_cli.upload_inmemory_to_storage(lrs_img_rgb)


if __name__ == '__main__':
    main()
