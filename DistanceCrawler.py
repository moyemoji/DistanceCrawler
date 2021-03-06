from selenium import webdriver
import json
import os,sys

"""
路径通行距离爬虫类
"""
class DistanceCrawler:
    """
    __init__: 构造函数
    :param tempate_path: 模板地址
    :param result_temp: 结果缓存，用于对比前后两次结果是否发生变化
    :param browser: 一个浏览器对象，用于模拟用户操作
    """
    def __init__(self):
        print("------init the crawler------")
        base_path = os.path.split(os.path.realpath(__file__))[0]
        base_path = base_path.replace('\\', '/')
        self.template_path =  'file:///'+ base_path + '/index.html'
        self.result_temp = ''
        opt = webdriver.ChromeOptions()
        opt.set_headless()
        self.browser = webdriver.Chrome(options=opt)
        self.browser.get(self.template_path)
        print("------init the crawler, done------")

    """
    displayTemplatePath: 打印模板路径
    """
    def displayTemplatePath(self):
        print(self.template_path)

    """
    getDistance: 获取通行距离
    :param query_json_str: json字符串格式的输入参数，包含有起终点id及其经纬度六个参数
    输入参数的一个示例：'{"startid":1, "endid":2, "lonstart":113.41, "latstart":29.58, "lonend":113.40, "latend":29.57}'
    :return val_result: json格式的返回值，包含起终点id以及他们之间的通行距离及持续时间，距离单位为m，时间单位为s
    输出参数示例：{'startid':1, 'endid':2, 'distance':7127, 'duration':731}
    """
    def getDistance(self, query_json_str):
        elem_data = self.browser.find_element_by_id("dataInput")
        elem_btn = self.browser.find_element_by_id("btnGetDistance")
        elem_result = self.browser.find_element_by_id('resultInput')
        elem_data.clear()
        elem_data.send_keys(query_json_str)
        elem_btn.click()
        val_result = elem_result.get_attribute("value")
        # 判断结果输入框不为空且同上次结果相比已经发生了变化
        while val_result == '' or val_result is None or val_result == self.result_temp:
            val_result = elem_result.get_attribute("value")
        self.result_temp = val_result
        return json.dumps(val_result)

    """
    stopBrowser: 关闭浏览器释放资源
    """
    def stopBrowser(self):
        self.browser.close()
        print("------crawler stopped------")

