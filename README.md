### 最後更新日期: 2020-12-03 09:00:00 ver.0007a

-----

# 更新日誌:

-----

### 更新日期: 2020-12-03 09:00:00 ver.0007a:
* 重寫左右小搖桿的運作規則，#左右小搖桿同一時間只能有一個有作用(避免互相干擾)，右小搖桿沒動作的話左邊搖桿才會work
* TRIG_L跟TRIG_R的按鍵修復

### 更新日期: 2020-12-03 00:10:00 ver.0006a
1. 改善按鍵效果，目前按住abxy左右鍵可持續施放技能，不會再有卡卡的現象了
2. 打包時遇到一個情況是 pynput 模組太新導致報錯，最後參考這個方法解決了
Please fall back to 1.6.8 version of pynput. pip install pynput==1.6.8

-----

### 更新日期: 2020-12-02 20:05:00 ver.0005a
1. 為了判斷滑鼠按鍵狀態需用到win32api模組(已匯入使用)
2. 滑鼠左右鍵按住效果
3. Ltrigger跟Rtrigger按鍵讓它有作用
4. 在 main_config.ini 裡加入了左小搖桿控制滑鼠移動後是否立刻按一下左鍵的設定
5. 重寫左右小搖桿控制滑鼠移動的部份(可能還有bug)
目前就等下班測試沒問題再發佈到gitpage&巴哈

-----

### 更新日期: 2020-12-01 19:40:00 ver.0003a
修正了滑鼠右鍵無法復歸的問題，同時將左右小搖桿控制滑鼠移動的代碼作了一些優化。

-----

## Using gamepad in Windows system with Python

https://forum.gamer.com.tw/C.php?bsn=21400&snA=367056&tnum=2&last=1#down

# Requires:

1. Gamepad (xbox controller or ps4 controller with usb)
2. Python 3+ Env and install some modules
3. do some setting and run main.py


# 參考網路資源:

## get controller event:
https://stackoverflow.com/questions/60309652/how-to-get-usb-controller-gamepad-to-work-with-python

## control mouse action:
https://stackoverflow.com/questions/4263608/ctypes-mouse-events

## simulor keydown:
https://stackoverflow.com/questions/11906925/python-simulate-keydown/11910555


## no-use-in-win:

https://martytherobot.com/2019/02/12/control-marty-with-gamepad-python/

https://pypi.org/project/inputs/