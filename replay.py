import requests
import argparse
import init
import os
from concurrent.futures import ThreadPoolExecutor

class Ddm3u8ToMp4:

    def __init__(self):
        self.flags()
        self.downloadUrl = "https://dtliving-sz.dingtalk.com/live_hp"
        self.session = requests.Session()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
            "Referer": "https://h5.dingtalk.com/",
            "Content-Type": "application/json",
        }
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.tsDir = "tsDir"
        self.GetVideo()

    def flags(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--input", type=str, default="video.m3u8",help="m3u8 filename", dest="m3u8f")
        parser.add_argument('--output', type=str, default="video.mp4", help="mp4 filename", dest="mp4f")
        args = parser.parse_args()
        self.m3u8f = str(args.m3u8f)
        self.mp4f = str(args.mp4f)

    def parseM3u8(self):
        tsList = []
        f = open(self.m3u8f,"r").read().split("\n")
        for ts in f:
            if "auth_key" in ts:
                tsList.append(ts)
        self.tsUrls = []
        for ts in tsList:
            self.tsUrls.append(ts.split("/")[1])
        self.suffix = tsList[0].split("/")[0]
        with open("new_video.m3u8", "w") as file:
            for ts in self.tsUrls:
                tsName = ts.split("?")[0]
                file.write(fr"file '{self.current_dir}/{self.tsDir}/{tsName}'")
                file.write("\n")
            file.close()

    def GetTsFile(self):
        tasks = []
        pool = ThreadPoolExecutor(max_workers=16)
        for ts in self.tsUrls:
            tsName = ts.split("?")[0]
            tasks.append(pool.submit(self.Download,ts,tsName))
        while True:
            if len(tasks) == 0:
                break
            for i in tasks:
                if i.done():
                    tasks.remove(i)
                    print("剩下任务数: {0}".format(len(tasks)))
        print("完成")
        return True
    
    def Download(self,url,name):
        binaryData = requests.get(f"{self.downloadUrl}/{self.suffix}/{url}",stream=True)
        open(f"{self.current_dir}/{self.tsDir}/{name}","wb").write(binaryData.content)

    def Ts2Mp4(self):
        cmd = fr"ffmpeg -f concat -safe 0 -i {self.current_dir}/new_video.m3u8 -c copy {self.current_dir}/video.mp4"
        os.system(cmd)
    
    def GetVideo(self):
        self.parseM3u8()
        if self.GetTsFile():
            self.Ts2Mp4()

if __name__ == "__main__":
    Ddm3u8ToMp4()