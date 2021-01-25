"""A IndexController Module."""
from datetime import datetime

from masonite.request import Request, Response
from masonite.validation import Validator, MessageBag
from masonite.view import View
from masonite.controllers import Controller

from app.Models.M3u8List import M3u8List
from app.Models.M3u8Hls import M3u8Hls

from masonite import Queue

import m3u8


class IndexController(Controller):
    """IndexController Controller Class."""

    def __init__(self, request: Request):
        """IndexController Initializer

        Arguments:
            request {masonite.request.Request} -- The Masonite Request class.
        """
        self.request = request

    def show(self, response: Response, queue: Queue):
        # return M3u8List.start('http://ivi.bupt.edu.cn/hls/cctv1hd.m3u8')
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return response.json({
            'time': time
        })

    def create(self, request: Request, validate: Validator):
        errors = request.validate({
            'm3u8_url': 'required'
        })

        errors = MessageBag(errors)

        if not errors.empty():
            return errors.all()

        m3u8_url = request.input('m3u8_url')

        return m3u8_url
