import requests, struct
from pprint import pprint


class Mp4info:
    def __init__(self, file):
        self.file = file
        self.seek = 0
        self.duration = 0
        self.s = requests.session()
        self.timeout = 200
        self.s.headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': '_uab_collina=158099356218517362584412; acw_tc=707c9f9d15809935624926727e3de40a58560ba6a44dd4d3cab4b8d21211cc; login_token=4bc891c38b87c3048edb8b59493b42f725176e3408875bc1e96a5fc0109b47da; teachweb=d4f4172703f4ec24a7f6c1a4c16efa458b4d0b74; SERVERID=da350d2ba570698afee980c284304ee2|1581183791|1581183764',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'
        }

    # 设置请求头
    def _set_headers(self, seek):
        self.s.headers['Range'] = 'bytes={}-{}'.format(seek, seek + 7)

    def _send_request(self):
        try:
            data = self.s.get(url=self.file, stream=True,
                              timeout=self.timeout).raw.read()
        except requests.Timeout:
            raise self.file + '连接超时:超过200秒(默认)服务器没有响应任何数据！'
        return data

    def _find_moov_request(self):
        self._set_headers(self.seek)
        data = self._send_request()
        size = int(struct.unpack('>I', data[:4])[0])
        flag = data[-4:].decode('ascii')
        return size, flag

    def _find_duration_request(self):
        # 4+4是moov的大小和标识,跳过20个字符，直接读到time_scale，duration
        self._set_headers(seek=self.seek + 4 + 4 + 20)
        data = self._send_request()
        time_scale = int(struct.unpack('>I', data[:4])[0])
        duration = int(struct.unpack('>I', data[-4:])[0])
        return time_scale, duration

    def get_duration(self):
        while True:
            size, flag = self._find_moov_request()
            if flag == 'moov':
                time_scale, duration = self._find_duration_request()
                self.duration = duration / time_scale
                return self.duration
            else:
                self.seek += size
