import psutil
import datetime
import sys
from convert import bytes2human

print(datetime.datetime.fromtimestamp(psutil.boot_time()))
print(sys.version_info)
print(sys.version)
# system info 系统信息
# Creating a new branch is quick & simple.