# m3u8-copy

# install

```sh
pip install -r requirements.txt 
pip install git+https://github.com/puzzle9/m3u8-generator.git
```


# use

```sh
curl --location --request POST 'http://127.0.0.1:8000' \
--form 'm3u8_url="http://ivi.bupt.edu.cn/hls/cctv1hd.m3u8"'
```