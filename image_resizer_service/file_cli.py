from event_service_utils.img_serialization.redis import RedisImageCache

class ReplaceKeyRedisImageCache(RedisImageCache):

    def replace_inmemory_storage(self, img_key,  img_numpy_array):
        nd_array_bytes = img_numpy_array.tobytes(order='C')
        ret = self.client.set(img_key, nd_array_bytes)
        if not ret:
            raise Exception('Couldnt replace image in redis')
        return img_key
