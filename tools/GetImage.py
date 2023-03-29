#-*- coding: UTF-8 -*-
import requests
import json
import os
from tkinter import *
from tkinter import messagebox

class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.path = StringVar()
        self.Createwidget()

    def Createwidget(self):
        self.tabe00 = Label(self, text="Get：")
        self.tabe00.pack()
        v0 = StringVar()
        self.entry00 = Entry(self, textvariable=v0)
        self.entry00.pack()
        self.tabe01 = Label(self, text="Get：")
        self.tabe01.pack()
        v2 = StringVar()
        self.entry01 = Entry(self, textvariable=v2)
        self.entry01.pack()
        Button(self, text="Start", command=self.login).pack()

    def login(self):
        n = 0
        pn = 1
        page = int(self.entry01.get()) + 1
        path = "./images"
        if not os.path.exists(path):
            os.makedirs(path)
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"
        }
        for m in range(1, page):
            url = "https://image.baidu.com/search/acjson?"
            param = {
                'tn': 'resultjson_com',
                'logid': "9593614055393928540",
                'ipn': 'rj',
                "ct": "201326592",
                "is": "",
                "fp": "result",
                "queryWord": self.entry00.get(),
                "cl": "",
                "lm": "",
                "ie": "utf-8",
                "oe": "utf-8",
                "adpicid": "",
                "st": "",
                "z": "",
                "ic": "",
                "hd": "",
                "latest": "",
                "copyright": "",
                "word": self.entry00.get(),
                "s": "",
                "se": "",
                "tab": "",
                "width": "",
                "height": "",
                "face": "",
                "istype": "",
                "qc": "",
                "nc": "1",
                "fr": "",
                "expermode": "",
                "force": "",
                "cg": "star",
                "pn": pn,
                "rn": "30",
                "gsm": "1e",
                "1615900803508": ""
            }
            image_url = list()
            response = requests.get(url=url, headers=header, params=param)
            response.encoding = "utf-8"
            response = response.text
            data_s = json.loads(response)
            a = data_s["data"]
            for i in range(len(a) - 1):
                data = a[i].get("thumbURL", "not exist")
                image_url.append(data)

            for image_src in image_url:
                image_data = requests.get(url=image_src, headers=header).content
                image_name = "{}".format(n + 1) + ".jpg"
                image_path = path + "/" + image_name
                with open(image_path, "wb") as f:
                    f.write(image_data)
                    print(image_name, "Success")
                    f.close()
                n += 1
            pn += 29


if __name__ == "__main__":
    root = Tk()
    root.geometry("400x200+300+200")
    app = Application(master=root)
    root.mainloop()