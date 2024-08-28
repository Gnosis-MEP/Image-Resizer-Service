import functools
from PIL import Image

from event_service_utils.logging.decorators import timer_logger
from event_service_utils.services.event_driven import BaseEventDrivenCMDService
from event_service_utils.tracing.jaeger import init_tracer

from image_resizer_service.conf import RESIZE_SCALE
from image_resizer_service.cloudseg import load_model as load_cloud_seg
from image_resizer_service.resize_model import Resizer


class ImageResizerService(BaseEventDrivenCMDService):
    def __init__(self,
                 service_stream_key, service_cmd_key_list,
                 pub_event_list, service_details,
                 file_storage_cli,
                 resize_method,
                 stream_factory,
                 logging_level,
                 tracer_configs):
        tracer = init_tracer(self.__class__.__name__, **tracer_configs)
        super(ImageResizerService, self).__init__(
            name=self.__class__.__name__,
            service_stream_key=service_stream_key,
            service_cmd_key_list=service_cmd_key_list,
            pub_event_list=pub_event_list,
            service_details=service_details,
            stream_factory=stream_factory,
            logging_level=logging_level,
            tracer=tracer,
        )
        self.resize_method = resize_method
        self.fs_client = file_storage_cli
        self.cmd_validation_fields = ['id']
        self.data_validation_fields = ['id']
        self.setup_resize()

    def setup_resize(self):
        self.resize = Resizer(scale=RESIZE_SCALE, res_type=self.resize_method)
        self.resize.setup()

    def process_data_event(self, event_data, json_msg):
        if not super(ImageResizerService, self).process_data_event(event_data, json_msg):
            return False
        srs_image_ndarray = self.resize_image(event_data)
        event_data = self.replace_event_image(event_data, srs_image_ndarray)
        self.send_to_next_destinations(event_data)

    def get_event_data_image_ndarray(self, event_data):
        img_key = event_data['image_url']
        width = event_data['width'] // RESIZE_SCALE
        height = event_data['height'] // RESIZE_SCALE
        color_channels = event_data['color_channels']
        n_channels = len(color_channels)
        nd_shape = (int(height), int(width), n_channels)
        image_nd_array = self.fs_client.get_image_ndarray_by_key_and_shape(img_key, nd_shape)

        return image_nd_array

    def resize_image(self, event_data):
        image_ndarray = self.get_event_data_image_ndarray(event_data)
        srs_image_ndarray = self.resize.run(image_ndarray)
        return srs_image_ndarray

    def replace_event_image(self, event_data, srs_image_ndarray):
        img_key = event_data['image_url']
        self.fs_client.replace_inmemory_storage(img_key,  srs_image_ndarray)
        return event_data

    def send_to_next_destinations(self, event_data):
        data_path = event_data.get('data_path', [])
        data_path.append(self.service_stream.key)
        next_data_flow_i = len(data_path)
        data_flow = event_data.get('data_flow', [])
        if next_data_flow_i >= len(data_flow):
            self.logger.info(f'Ignoring event without a next destination available: {event_data}')
            return

        next_destinations = data_flow[next_data_flow_i]
        for destination in next_destinations:
            self.send_event_to_destination(destination, event_data)

    def send_event_to_destination(self, destination, event_data):
        self.logger.debug(f'Sending event to destination: {event_data} -> {destination}')
        destination_stream = self.get_destination_streams(destination)
        self.write_event_with_trace(event_data, destination_stream)

    @functools.lru_cache(maxsize=5)
    def get_destination_streams(self, destination):
        return self.stream_factory.create(destination, stype='streamOnly')


    def process_event_type(self, event_type, event_data, json_msg):
        if not super(ImageResizerService, self).process_event_type(event_type, event_data, json_msg):
            return False

    def log_state(self):
        super(ImageResizerService, self).log_state()
        self.logger.info(f'Service name: {self.name}')
        self.logger.info(f'Using Resize Method: {self.resize_method}, scale: {RESIZE_SCALE}')

    def run(self):
        super(ImageResizerService, self).run()
        self.log_state()
        self.run_forever(self.process_data)
