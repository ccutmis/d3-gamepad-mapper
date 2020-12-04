[![youtube demo ](https://blzmedia-a.akamaihd.net/d3/media/screenshots/guide/en-us/uee/xboxone-controls-thumb.jpg)](https://www.youtube.com/watch?v=sGJoHM30Mwc)

# D3-Gamepad-Mapper Introduction

### 更新日期: 2020-12-04 ver.0007a

-----

## 目錄

1. [關於 D3-Gamepad-Mapper | About](https://github.com/ccutmis/d3-gamepad-mapper#1-%E9%97%9C%E6%96%BC-d3-gamepad-mapper--about) 關於 D3-Gamepad-Mapper | About
2. 下載與安裝 | Download & Install
3. 如何使用 | How to Use
4. 注意事項 | Notice
5. 特別聲明 | Statement
6. 更新日誌 | Log
7. 參考資源 | References

-----

## 1. 關於 D3-Gamepad-Mapper | About

玩Diablo-Like遊戲的PC老玩家由於頻繁操控鍵盤滑鼠，如果沒有好好保護手腕很容易造成慢性傷害，例如腕隧道症候群，也許你會想:「如果可以使用搖桿來玩遊戲該有多好?」

類Diablo的PC ARPG遊戲主要大多以滑鼠作為指向工具，配合滑鼠左右鍵及鍵盤施放技能，這個部份如果要把它對應到搖桿是有一些難度，主要在於操作方面需要重新適應，由於暴雪自家並沒有針對PC版的搖桿提供支援，這邊aloha運用自己略懂的Python編程寫了一個簡單的用搖桿模擬鍵鼠功能的小程式，希望能帶給有需要善待手腕的D3玩家們一些更好的遊戲體驗。

-----

## 2. 下載與安裝移除 | Download & Install

D3-Gamepad-Mapper下載點:

[https://ccutmis.github.io/d3-gamepad/d3-gamepad-exe-0007a.zip](https://ccutmis.github.io/d3-gamepad/d3-gamepad-exe-0007a.zip)

下載並解壓縮會得到一個 dist 資料夾，裡面有兩個檔案:

* main.exe (主程式直接點兩下即可執行)
* main_config.ini (設定檔，建議使用Notepad++編輯)

本軟體無需安裝，將下載完成解壓縮的資料夾放到桌面(或好找的路徑)即完成部署。程式執行時不會修改電腦機碼，若要移除就是直接把主程式跟設定檔刪除即可。

### main_config.ini 設定檔內容

```
#這是一行註解

#設定要啟用搖桿對應的程式標題文字，防止在切換不同視窗程式時可能造成的誤操作
ACTIVE_WIN_TITLE="暗黑破壞神III"

#key_config字典用來定義按鍵值
KEY_CONFIG={
    "BTN_A":"1",
    "BTN_B":"2",
    "BTN_X":"3",
    "BTN_Y":"4",
    "BTN_L":"LM", #滑鼠左鍵
    "BTN_R":"RM", #滑鼠右鍵
    "BTN_START":"q", #喝水
    "BTN_BACK":"t", #回村
    "TRIG_L":"esc", #左邊Trigger
    "TRIG_R":"tab" #右邊Trigger
}

#設定左小搖桿在控制滑鼠移動後是否按一下滑鼠左鍵
#設為 True 則在左小搖桿控制滑鼠移動後會在滑鼠所在位置按一下左鍵，要取消則設為 False
SET_LEFT_CONTROLLER_MOVE_AND_CLICK = True

#左右小搖桿控制滑鼠位移的一單位(像素)(基本上勿動)
XY_OFFSET_UNIT=10

#延時設定(基本上勿動)
DELAY_SECOND=0.1

#勿動BTN_DICT
BTN_DICT={0:"BTN_A", 1:"BTN_B",2:"BTN_X", 3:"BTN_Y",4:"BTN_L",5:"BTN_R",6:"BTN_BACK",7:"BTN_START",8:"TRIG_L",9:"TRIG_R"}

```

![controller-mapping.png](https://ccutmis.github.io/d3-gamepad/controller-mapping.png)

修改 main_config.ini 注意事項:
1. 編輯此文件推薦使用Notepad++，如果用記事本編輯在存檔時需注意是否存為"utf-8"文件格式(不可為"Big5"或"utf-8 BOM"格式會出錯)。
2. 只能更改KEY_CONFIG字典裡的值，例如: "BTN_A":"1" 改成 "BTN_A":"i"，這樣執行程式時按下搖桿A鍵就會模擬按下i鍵，只可修改值不可破壞格式。


-----

## 3. 如何使用 | How to Use

1. 先開啟Diablo III，將畫面顯示設為"全螢幕視窗模式"或"視窗模式"。(這個很重要)
2. 確定你的xbox搖桿有接在PC端並正常運作中(可在控制台裡的裝置及印表機項目確認)
3. 執行 main.exe 並切換到 Diablo III，拿起搖桿測試看看。(可以將main.exe釘選在工作列，之後不論是要開啟或關閉程式都方便!)

-----

## 4. 注意事項 | Notice

### 系統需求:
1. Windows7以上作業系統
2. 目前只用usb介面的xbox相容搖桿測試(羅技)測試OK，沒有無線搖桿也沒經費購買故無法測試(如果有人要提供設備讓我測試的話可以私訊給我^^)。

-----

## 5. 特別聲明 | Statement

* 本程式無償提供任何人使用，歡迎轉載連結。
* 本程式執行時會依搖桿輸入模擬鍵盤滑鼠動作，若在執行中造成任何非預期之損失概不負責，特此聲明。
* 目前程式有些小bug，但基本運作應該是沒問題的，建議在執行main.exe的時候先不要開啟 Diablo III以外的任何程式，試試看有沒有問題，當然程式不可能完全沒bugs，未來有修正版會在這邊持續更新。

-----

## 6. 更新日誌 | Log

-----

### 更新日期: 2020-12-03 09:00:00 ver.0007a:
* 重寫左右小搖桿的運作規則，#左右小搖桿同一時間只能有一個有作用(避免互相干擾)，右小搖桿沒動作的話左邊搖桿才會work
* TRIG_L跟TRIG_R的按鍵修復

-----

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

## 7. 參考資源 | References

### D3官網對於家機搖桿的設置參考
https://diablo3.blizzard.com/en-us/game/guide/gameplay/fundamentals

### get controller event:
https://stackoverflow.com/questions/60309652/how-to-get-usb-controller-gamepad-to-work-with-python

### control mouse action:
https://stackoverflow.com/questions/4263608/ctypes-mouse-events

### simulor keydown:
https://stackoverflow.com/questions/11906925/python-simulate-keydown/11910555

### pynput使用簡單說明
https://www.itread01.com/content/1541887278.html
