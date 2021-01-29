# m3u8-copy

# install

```sh
pip install -r requirements.txt
pip install git+https://github.com/puzzle9/m3u8-generator.git
```

# supervisord

## web

```ini
[program:m3u8-copy-web]
process_name = %(program_name)s
command = /m3u8-copy/bin/gunicorn --bind 0.0.0.0:7002 --chdir=/m3u8-copy wsgi:application
autostart = true
autorestart = true
redirect_stderr = true
stdout_logfile = /m3u8-copy/storage/logs/supervisord-web.log
```

## queue

```ini
[program:m3u8-copy-queue]
process_name = %(program_name)s
directory = /m3u8-copy
command = /m3u8-copy/bin/craft queue:work
autostart = true
autorestart = true
redirect_stderr = true
stdout_logfile = /m3u8-copy/storage/logs/supervisord-queue.log
```

# use

##req
```sh
curl --location --request POST 'http://127.0.0.1:8000' --form 'm3u8_url=http://ivi.bupt.edu.cn/hls/cctv1hd.m3u8'
```

## res
```json
{
    "id": 2,
    "status": "created",
    "path": "/hls/2/play.m3u8",
    "play_url": "http://localhost:7002/play/2"
}
```

# other

<https://github.com/MasoniteFramework/masonite/pull/403>

`/lib/python3.6/site-packages/masonite/helpers/time.py` change `pendulum.now("GMT")` to `pendulum.now()`

# todo

-[ ] 加密id
-[ ] 保存到本地
-[x] 第一版