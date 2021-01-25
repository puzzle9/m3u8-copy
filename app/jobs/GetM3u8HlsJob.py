"""A GetM3u8HlsJob Queue Job."""

from masonite.queues import Queueable


class GetM3u8HlsJob(Queueable):
    """A GetM3u8HlsJob Job."""

    hls_id = None

    def __init__(self, hls_id):
        """A GetM3u8HlsJob Constructor."""
        self.hls_id = hls_id

    def handle(self):
        """Logic to handle the job."""
        hls_id = self.hls_id
        print("收到 hls %d" % hls_id)

