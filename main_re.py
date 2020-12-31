# ver.0008b todo:
# 使用traceback模組 在程式執行出錯時將錯誤報告記錄到 main_runtime_error.log
# 追加設定檔變數 DEBUG_MODE 用來設定是否啟用degug模式，若為 False 則不進行debug動作；若為 True 則會將執行中的按鍵且左右搖桿三軸的狀況寫入到main_degug.txt，這個動作會進行頻繁寫入文字檔的動作，除非有特殊原因要進行除錯，否則請讓它保持在 False 的值。
# 加上DPAD的功能等於多了四個按鍵
from datetime import datetime
import win32api
from time import sleep
import msvcrt
import myModule.joystick_api as JoyStick
from myModule.WindowMgr import *
import myModule.mouse_api as Mouse
from pynput.keyboard import Key, Controller
import math
import traceback,sys
VERSION="0008b"

def gent_degree_dict(divisions=360,radius=10):
    #divisions,radius=360,10
    out_dict={}
    # the difference between angles in radians -- don't bother with degrees
    angle = 2 * math.pi / divisions
    # a list of all angles using a list comprehension
    angles = [i*angle for i in range(divisions)]
    oi=0
    for a in angles:
        out_dict[oi]=[int(radius*math.sin(a)),(int(radius*math.cos(a)))]
        oi+=1
    #out_dict[divisions]=[0,10]
    return out_dict

def deg_to_xy(deg):
    global DEG_DICT
    xy_list=DEG_DICT[deg]
    return xy_list[0],xy_list[1]

def kb_press_eval_key(key_val):
    keyboard = Controller()
    if len(key_val)==1:
        keyboard.press(key_val)
    else:
        keyboard.press(eval("Key."+key_val))

def kb_release_eval_key(key_val):
    keyboard = Controller()
    if len(key_val)==1:
        keyboard.release(key_val)
    else:
        keyboard.release(eval("Key."+key_val))

def process_btns(btns):
    global cx,cy,x_center,y_center
    keyboard = Controller()
    global keys_stat_last,KEY_CONFIG,BTN_DICT,str_for_print_last
    global KEY_MAP,KEY_ONOFF_MODE,current_onoff,onoff_list
    x=0
    str_for_print=""
    for i in btns:
        curr_key=KEY_CONFIG[BTN_DICT[x]]
        if curr_key!="": #不是空白才繼續動作
            if i==True: #按下狀態，確認一下先前是否已按，若已按無需再做其它事
    
                if keys_stat_last[x]==True: #先前已按
                    if KEY_ONOFF_MODE[BTN_DICT[x]]==1 and BTN_DICT[x] in onoff_list:
                        onoff_list.remove(BTN_DICT[x])
                    pass
                else:
                    if KEY_ONOFF_MODE[BTN_DICT[x]]==1:
                        #檢查current_onoff[x]是否為0
                        if BTN_DICT[x] not in onoff_list:
                            onoff_list.append(BTN_DICT[x])
                            kb_press_eval_key(curr_key)
                            sleep(0.1)
                            kb_release_eval_key(curr_key)
                    if curr_key not in ["LM","RM"]: #不是按滑鼠左右鍵
                        kb_press_eval_key(curr_key)
                    else: #是滑鼠左右鍵
                        if curr_key=="LM":
                            Mouse.click('left',cx,cy)
                        elif curr_key=="RM":
                            Mouse.click('right',cx,cy)
                        else:
                            pass
                            #print(curr_key,"press")
                    keys_stat_last[x]=True
                            
            else:
                if KEY_ONOFF_MODE[BTN_DICT[x]]==1 and BTN_DICT[x] in onoff_list:
                    kb_press_eval_key(curr_key)
                    sleep(0.1)
                    kb_release_eval_key(curr_key)
                if keys_stat_last[x]==True: #先前已按目前沒按
                    if curr_key not in ["LM","RM"]: #不是滑鼠左右鍵
                        kb_release_eval_key(curr_key)
                    else:
                        if curr_key=="LM":
                            Mouse.click('left',cx,cy,0)
                        elif curr_key=="RM":
                            Mouse.click('right',cx,cy,0)
                        else:
                            pass
                    keys_stat_last[x]=False
        x+=1

if __name__ == '__main__':
    try:
        num = JoyStick.joyGetNumDevs()
        ret, caps, startinfo = False, None, None
        for id in range(num):
            ret, caps = JoyStick.joyGetDevCaps(id)
            if ret:
                print("偵測到控制器: " + caps.szPname + "\n----------------------------------------")
                ret, startinfo = JoyStick.joyGetPosEx(id)
                break
        else:
            print("未偵測到控制器。")
            sys.exit()
        print((caps.wCaps))
        run=True
        while run:
            sleep(2)
            if msvcrt.kbhit() and msvcrt.getch() == chr(8).encode(): # detect F10
                run = False

            ret, info = JoyStick.joyGetPosEx(id)
            if ret:
                btns = [(1 << i) & info.dwButtons != 0 for i in range(caps.wNumButtons)]
                pov=int(info.dwPOV) #Hat/D-pad
                #print(pov)
                axisXYZ = [info.dwXpos-startinfo.dwXpos, info.dwYpos-startinfo.dwYpos, info.dwZpos-startinfo.dwZpos]
                axisRUV = [info.dwRpos-startinfo.dwRpos, info.dwUpos-startinfo.dwUpos, info.dwVpos-startinfo.dwVpos]
                print(btns)

    except Exception as e:
        error_class = e.__class__.__name__ #取得錯誤類型
        detail = e.args[0] #取得詳細內容
        cl, exc, tb = sys.exc_info() #取得Call Stack
        lastCallStack = traceback.extract_tb(tb)[-1] #取得Call Stack的最後一筆資料
        fileName = lastCallStack[0] #取得發生的檔案名稱
        lineNum = lastCallStack[1] #取得發生的行號
        funcName = lastCallStack[2] #取得發生的函數名稱
        errMsg = "File \"{}\", line {}, in {}: [{}] {}".format(fileName, lineNum, funcName, error_class, detail)
        with open('main_runtime_error.log','a+',encoding='utf-8') as f:
            f.writelines(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+'\t'+errMsg+'\n')
        print(errMsg)
        sys.exit()
    if DEBUG_MODE:
        fp.writelines(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+'\tDEBUG記錄結束\n')
        print("DEBUG STOP")
        fp.close()
    print("按下 [ ← Backspace ] 程式結束")