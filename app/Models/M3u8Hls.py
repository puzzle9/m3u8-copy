"""M3u8Hls Model."""

from masoniteorm.models import Model


class M3u8Hls(Model):
    """M3u8Hls Model."""
    __guarded__ = []

    # 默认
    STATUS_DEFAULT = 'default'
    # 等待执行
    STATUS_LOADING = 'loading'
    # 成功
    STATUS_SUCCESS = 'success'
    # 失败
    STATUS_ERROR = 'error'

    @classmethod
    def start(self, list_id, duration, url, path):
        from config.database import DB

        # todo: 批量插入可能存在问题
        DB.begin_transaction()

        info = self.where('m3u8_list_id', list_id).where('path', path).first()
        if not info:
            print('没有 %s' % path)
            info = self.create({
                'm3u8_list_id': list_id,
                'duration': duration,
                'url': url,
                'path': path,
                'status': self.STATUS_DEFAULT,
            })

            DB.commit()

            from app.jobs.GetM3u8HlsJob import GetM3u8HlsJob
            container().make('Queue').push(GetM3u8HlsJob(info.id))
