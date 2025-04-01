import datetime



path = './log/log.log'
def add_Log(text):
    file = open(path,mode="a",encoding="UTF-8")
    file.write(text+"\t"+datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')+"\n")
    file.close()
def read_Log():
    txtx = open(path, mode="r",encoding="UTF-8")
    r = txtx.read()
    txtx.close()
    return r
