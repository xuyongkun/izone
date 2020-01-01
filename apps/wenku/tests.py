from django.test import TestCase
from wenku.loginbaidu import LoginBaidu
# Create your tests here.





if __name__ == '__main__':
    import re
    # downloader = LoginBaidu()
    # downloader.login()

    p2 = re.compile(r'[(](.*)[)]', re.S)  # 贪婪匹配
    text = 'bd__cbs__epm4j1({ "errInfo":{ "no": "0" }, "data": { "hao123Param" : "ZGxiV05XTFZkRVRtZDRaM1ZWVkdobFltNU1NR2RPZmtwNGVWaFROMjF4WjA5VU9EbHBUVW80ZERsTFZVSmtTVkZCUVVGQkpDUUFBQUFBQUFBQUFBRUFBQUM4d2JvazBPelR3TUNrTWpJQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFIMmNHRjE5bkJoZE9E", "userName" : "", "phoneNumber" : "", "mail" : "", "u" : "https:\/\/www.baidu.com\/", "guideUpgradeMobile": "", "upgradeMobile": "", "upgradeMobileToken": "" }, "traceid": ""})'
    print(re.findall(p2, text)[0])
    resp_str = re.findall(p2, text)[0]
    resp_no = eval(resp_str)['errInfo']['no']

    print(resp_no)