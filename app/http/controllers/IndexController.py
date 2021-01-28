"""A IndexController Module."""
from datetime import datetime

from masonite.request import Request, Response
from masonite.validation import MessageBag
from masonite.controllers import Controller

from app.Models.M3u8List import M3u8List
from app.Models.M3u8Hls import M3u8Hls

from m3u8_generator import PlaylistGenerator

from masonite.helpers import config

from masonite.qiniu import Qiniu


class IndexController(Controller):
    """IndexController Controller Class."""

    def __init__(self):
        pass

    def show(self, response: Response):
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return response.json({
            'time': time
        })

    def create(self, request: Request):
        errors = request.validate({
            'm3u8_url': 'required'
        })

        errors = MessageBag(errors)

        if not errors.empty():
            return errors.all()

        m3u8_url = request.input('m3u8_url')

        info = M3u8List.start(m3u8_url)

        info_id = info.id

        play_url = "{}{}".format(config('application.URL'), route('play', {
            "list_id": info_id,
        }))

        return {
            'id': info_id,
            'status': info.status,
            'path': info.path,
            'play_url': play_url,
        }

    def play(self, request: Request, qiniu: Qiniu):
        list_id = request.param('list_id')

        infos = M3u8Hls.where('m3u8_list_id', list_id).where('status', M3u8Hls.STATUS_SUCCESS).select('key', 'duration').get()

        domain = qiniu.domain

        datas = []

        for info in infos:
            datas.append({
                "name": "{}{}".format(domain, info.key),
                "duration": info.duration
            })

        return PlaylistGenerator(datas).generate()
