import requests
import json
import re
import execjs

class BaiduTranslateSpider(object):
    def __init__(self):
        self.get_url='https://fanyi.baidu.com/?aldtype=16047'
        self.post_url = 'https://fanyi.baidu.com/v2transapi'
        self.headers = {
           # 必须注释掉,检查长度
            # "content-length": "121",
            "cookie": "BAIDUID=33F73A12F1C59AA0A6A58671D045D815:FG=1; PSTM=1568272125; BIDUPSID=3D3508B0D3A4999CEEA92269E5813851; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; BDRCVFR[mkUqnUt8juD]=aeXf-1x8UdYcs; delPer=0; H_PS_PSSID=1461_21093_29522_29519_29568_29220; locale=zh; to_lang_often=%5B%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%5D; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; from_lang_often=%5B%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%2C%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%5D; PSINO=1; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1568789935,1568794846; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1568794864; __yjsv5_shitong=1.0_7_9ddad96b49e57b93d7decb75275d47e0310c_300_1568794863156_43.254.90.134_4162b891; yjs_js_security_passport=d756d16051617d22fa323aee5e91f68bc8b76c5e_1568794866_js",
            "referer": "https://fanyi.baidu.com/?aldtype=16047",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36",
        }

    # 获取token+gtk
    def get_token_gtk(self):

        html = requests.get(
            url=self.get_url,
            headers=self.headers
        ).text
        gtk_re = "window.gtk = '(.*?)'"
        token_re = "token: '(.*?)'"
        # 获取gtk
        pattern = re.compile(gtk_re)
        gtk = pattern.findall(html)[0]
        # 获取token
        pattern = re.compile(token_re)
        token = pattern.findall(html)[0]

        return token,gtk


    # 获取sign
    def get_sign(self,word,gtk):
        with open('translate.js','r') as f:
            js_data = f.read()

        exec_obj = execjs.compile(js_data)
        sign = exec_obj.eval('e("{}","{}")'.format(word,gtk))

        return sign

    # 入口函数
    def run(self):
        word = input('请输入要翻译的单词:')
        token,gtk = self.get_token_gtk()

        sign = self.get_sign(word,gtk)

        data = {
            "from": "auto",
            "to": "auto",
            "query": word,
            "transtype": "realtime",
            "simple_means_flag": "3",
            "sign": sign,
            "token": token,
        }
        html = requests.post(
            url=self.post_url,
            data=data,
            headers=self.headers
        ).json()
        result = html['trans_result']['data'][0]['dst']
        print(result)

if __name__ == '__main__':
    spider = BaiduTranslateSpider()
    spider.run()





















