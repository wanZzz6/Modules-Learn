windows环境，以管理员身份设置系统时间，一直循环执行



```python
# coding: utf-8

import ctypes
import time
import sys

import win32api
from threading import Thread


running_flag = True


def is_admin():
    try:
        # 获取当前用户的是否为管理员
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception as e:
        print(e)
        return False


def main(duration, interval=0.1):
    if not is_admin():
        # 请求管理员身份运行
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, __file__, None, 1)
        return

    assert duration > 0 and interval > 0
    Thread(target=maintainer, args=(duration,), daemon=True).start()
    while(running_flag):
        # tm_year, tm_mon, tm_wday, tm_mday, tm_hour, tm_min, tm_sec, int(msec)
        win32api.SetSystemTime(2022, 10, 0, 3, 14, 53, 0, 10)  # type: ignore
        time.sleep(interval)
        sys.stdout.write('#')
        sys.stdout.flush()


def maintainer(duration):
    global running_flag
    time.sleep(duration)
    running_flag = False


if __name__ == '__main__':
    main(120) # 120s

```

