import psutil
import datetime
from convert import bytes2human

print('系统开机时间是：{}'.format(datetime.datetime.fromtimestamp(psutil.boot_time())))
print('系统内存大小：{}'.format(bytes2human(psutil.virtual_memory().total)))
print('交换分区大小：{}'.format(bytes2human(psutil.swap_memory().total)))
print('物理处理器数量：{}'.format(psutil.cpu_count(logical=False)))
print('逻辑处理器数量：{}'.format(psutil.cpu_count()))