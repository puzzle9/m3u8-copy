"""M3u8List Model."""

from masoniteorm.models import Model


class M3u8List(Model):
    """M3u8List Model."""
    __guarded__ = []

    # 已创建
    STATUS_CREATE = 'created'
    # 等待执行
    STATUS_LOADING = 'loading'
    # 执行中
    STATUS_EXECUTING = 'executing'
    # 已完成
    STATUS_FINISHED = 'finished'

    @classmethod
    def start(self, url):
        data = self.where('url', url).first()

        if data:
            if data.status == self.STATUS_FINISHED:
                data.update({
                    "status": self.STATUS_CREATE,
                })
        else:
            from config.database import DB
            DB.begin_transaction()
            data = self.create({
                "url": url,
                "status": self.STATUS_CREATE,
            })
            DB.commit()

        info = self.where('url', url).first()

        list_id = info.id

        if info.status == self.STATUS_CREATE:
            info.update({
                "status": self.STATUS_LOADING,
            })
            self.createGetInfoJob(list_id, "5 seconds")

        info.path = self.getM3u8Path(list_id)

        return info

    @classmethod
    def createGetInfoJob(self, list_id, wait="3 seconds"):
        from app.jobs.GetM3u8InfoJob import GetM3u8InfoJob
        container().make('Queue').push(GetM3u8InfoJob(list_id), wait=wait)

    @classmethod
    def getInfo(cls, id):
        return cls.find(id)

    @classmethod
    def changeStatus(cls, id, status):
        cls.find(id).update({
            'status': status,
        })

    @classmethod
    def getM3u8Path(cls, live_id):
        return '/hls/{}/play.m3u8'.format(live_id)
