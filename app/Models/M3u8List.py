"""M3u8List Model."""

from masoniteorm.models import Model
from masoniteorm.scopes import scope


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
            if data.status == self.STATUS_FINISHED or data.status == self.STATUS_CREATE:
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

        if data.status == self.STATUS_FINISHED or data.status == self.STATUS_CREATE:
            self.createGetInfoJob(data.id)

        return info

    @classmethod
    def createGetInfoJob(self, list_id, wait="0 s"):
        from app.jobs.GetM3u8InfoJob import GetM3u8InfoJob
        container().make('Queue').push(GetM3u8InfoJob(list_id), wait="3 seconds")

    @classmethod
    def getInfo(self, id):
        return self.find(id)

    @classmethod
    def changeStatus(self, id, status):
        self.find(id).update({
            'status': status,
        })

    # def ChangeStatus(self, list_id, status):
