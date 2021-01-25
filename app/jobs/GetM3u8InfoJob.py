"""A GetM3u8InfoJob Queue Job."""

from masonite.queues import Queueable

from app.Models.M3u8List import M3u8List
from app.Models.M3u8Hls import M3u8Hls

import m3u8

class GetM3u8InfoJob(Queueable):
    """A GetM3u8InfoJob Job."""

    list_id = None

    def __init__(self, list_id):
        """A GetM3u8InfoJob Constructor."""
        self.list_id = list_id

    def handle(self):
        """Logic to handle the job."""
        list_id = self.list_id
        print('收到 %d' % (list_id))

        info = M3u8List.getInfo(list_id)
        url = info.url

        print(info.status)

        if info.status == M3u8List.STATUS_FINISHED:
            print('%d %s 已完成' % (list_id, url))
            return

        if info.status == M3u8List.STATUS_EXECUTING:
            print('%d %s 正在执行' % (list_id, url))
            return

        M3u8List.changeStatus(list_id, M3u8List.STATUS_EXECUTING)

        play_lists = m3u8.load(url)

        for play_list in play_lists.segments:
            M3u8Hls.start(list_id, play_list.duration, play_list.absolute_uri, play_list.uri)

        M3u8List.changeStatus(list_id, M3u8List.STATUS_LOADING)

        M3u8List.createGetInfoJob(list_id)
