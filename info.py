import psutil
import datetime
from convert import bytes2human

print(datetime.datetime.fromtimestamp(psutil.boot_time()))