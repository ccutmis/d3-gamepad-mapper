from myModule.WindowMgr import *
from time import sleep
w=WindowMgr()
w.find_window_wildcard("暗黑破壞神III")
w.set_foreground()
w.set_window_state()
pns=w.get_window_pos_size()
print(pns)
while True:
    print(w.active_window_title())
    sleep(5)