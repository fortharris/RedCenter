def sizeformat(size):
    byteSize = len(list(str(size)))
    if byteSize < 4:
        return str(size) + "Bytes"
    elif 3 < byteSize < 7:
        return str(round(size / 1024, 2)) + "KB"
    elif 6 < byteSize < 10:
        return str(round(size / 1048576, 2)) + "MB"
    else:
        return str(round(size / 1073741824, 2)) + "GB"


def updateLogFile(logDict):
    file = open("Vault\\LOG", "w")
    for key, value in logDict.items():
        file.write('\n' + key + '||' + value)
    file.close()
