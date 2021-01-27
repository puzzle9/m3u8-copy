"""A IndexController Module."""
from datetime import datetime

from masonite.request import Request, Response
from masonite.validation import MessageBag
from masonite.controllers import Controller

from app.Models.M3u8List import M3u8List


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

        return {
            'id': info.id,
            'status': info.status,
            'path': info.path,
        }
