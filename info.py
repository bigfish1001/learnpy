import psutil
import datetime
import sys
from convert import bytes2human

print(datetime.datetime.fromtimestamp(psutil.boot_time()))
print(sys.version_info)
print(sys.version)