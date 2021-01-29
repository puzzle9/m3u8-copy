"""A GetM3u8HlsJob Queue Job."""
from masonite.queues import Queueable

from app.Models.M3u8Hls import M3u8Hls

import func_timeout


class GetM3u8HlsJob(Queueable):
    """A GetM3u8HlsJob Job."""

    hls_id = None

    def __init__(self, hls_id):
        """A GetM3u8HlsJob Constructor."""
        self.hls_id = hls_id

    @func_timeout.func_set_timeout(3)
    def fetch(self, qiniu, url, key):
        bucket = qiniu.bucket()
        fetch, ret = bucket.fetch(url, qiniu.bucket_name, key)
        print(fetch)
        if ret.status_code == 200:
            return True
        else:
            return False

    def handle(self):
        """Logic to handle the job."""
        hls_id = self.hls_id
        print("收到 hls %d" % hls_id)

        hls_info = M3u8Hls.find(hls_id)

        if hls_info.status != M3u8Hls.STATUS_DEFAULT:
            print("hls {} 状态错误".format(hls_id))
            return

        hls_info.update({
            "status": M3u8Hls.STATUS_LOADING
        })

        key = 'hls/{}/{}.ts'.format(hls_info.m3u8_list_id, hls_id)

        qiniu = container().make('Qiniu')
        bucket = qiniu.bucket()
        try:
            fetch_status = self.fetch(qiniu, hls_info.url, key)
        except func_timeout.exceptions.FunctionTimedOut:
            print("{} 超时 {}".format(hls_id, key))
            fetch_status = False

        if fetch_status:
            hls_info.update({
                "key": key,
                "status": M3u8Hls.STATUS_SUCCESS
            })
            print("{} 成功 {}".format(hls_id, key))
        else:
            hls_info.update({
                "status": M3u8Hls.STATUS_ERROR
            })
            print("{} 失败".format(hls_id))
