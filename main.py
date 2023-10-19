import requests
import argparse
import json
import os
from concurrent.futures import ThreadPoolExecutor

class DingTalkReplay:

    def __init__(self):
        self.flags()
        self.rawUrl = "https://h5.dingtalk.com/group-live-share/index.htm"
        self.csrfUrl = "https://lv.dingtalk.com/csrf"
        self.infoUrl = "https://lv.dingtalk.com/getLivePublicInfoV2"
        self.downloadUrl = "https://dtliving-sh.dingtalk.com/live"
        self.session = requests.Session()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
            "Referer": "https://h5.dingtalk.com/",
            "Content-Type": "application/json",
        }
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.tsDir = "tsDir"
        self.GetViedo()

    def flags(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-e", type=str, required=True, help="encCid", dest="encCid")
        parser.add_argument('-l', type=str, required=True, help="liveUuid", dest="liveUuid")
        args = parser.parse_args()
        self.encCid = str(args.encCid)
        self.liveUuid = str(args.liveUuid)

    def GetCRSF(self):
        self.csrf_token = json.loads(self.session.get(url=self.csrfUrl).text)
        self.headers[self.csrf_token["headerName"]] = self.csrf_token["token"]

    def GetM3u8(self):
        data = {
            "encCid": self.encCid,
            "liveUuid": self.liveUuid,
        }
        res = self.session.post(url=self.infoUrl,data=json.dumps(data),headers=self.headers)
        playUrl = json.loads(res.text)["playUrl"]
        res = self.session.get(playUrl)
        tsList = res.text.split("\n")[4:-2]
        self.suffix = tsList[1].split("/")[0]
        self.tsUrls = []
        for i in range(0,len(tsList),2):
            self.tsUrls.append(tsList[i+1].split("/")[1])
        with open("video.m3u8", "w") as file:
            for ts in self.tsUrls:
                tsName = ts.split("?")[0]
                file.write(fr"file '{self.current_dir}/{self.tsDir}/{tsName}'")
                file.write("\n")
            file.close()
    
    def GetTsFile(self):
        # print(1)
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
        cmd = fr"ffmpeg -f concat -safe 0 -i {self.current_dir}/video.m3u8 -c copy {self.current_dir}/video.mp4"
        os.system(cmd)
    
    def GetViedo(self):
        self.GetCRSF()
        self.GetM3u8()
        self.Download(self.tsUrls[1],"1.ts")
        if self.GetTsFile():
            self.Ts2Mp4()

if __name__ == "__main__":
    DingTalkReplay()