""" 參考網址: https://stackoverflow.com/questions/60309652/how-to-get-usb-controller-gamepad-to-work-with-python """
# ver.0007a todo:
# 重寫左右小搖桿的運作規則
# TRIG_L跟TRIG_R的按鍵修復
import codecs
from datetime import datetime
import win32api
from time import sleep
import msvcrt
import myModule.joystick_api as JoyStick
#import myModule.keyboard_api as KeyBoard
import myModule.mouse_api as Mouse
from pynput.keyboard import Key, Controller
keyboard = Controller()
def process_btns(btns):
    global keys_stat_last,KEY_CONFIG,BTN_DICT,str_for_print_last
    x=0
    str_for_print=""
    for i in btns:
        curr_key=KEY_CONFIG[BTN_DICT[x]]
        if i==True: #按下狀態，確認一下先前是否已按，若已按無需再做其它事
            if keys_stat_last[x]==True: #先前已按
                pass
            else:
                if curr_key not in ["LM","RM"]: #不是按滑鼠左右鍵
                    keyboard.press(curr_key)
                else: #是滑鼠左右鍵
                    if curr_key=="LM":
                        Mouse.click('left',cx,cy)
                    else:
                        Mouse.click('right',cx,cy)
                keys_stat_last[x]=True
                        
        else:
            if keys_stat_last[x]==True: #先前已按目前沒按
                if curr_key not in ["LM","RM"]: #不是滑鼠左右鍵
                    keyboard.release(curr_key)
                else:
                    if curr_key=="LM":
                        Mouse.click('left',cx,cy,0)
                    else:
                        Mouse.click('right',cx,cy,0)
                keys_stat_last[x]=False
        x+=1
    #if str_for_print_last!="":print("\b"*len(str_for_print_last),end="")
    #print(keys_stat_last)
    #print(btns)

if __name__ == '__main__':
    try:
        #讀取 main_config.ini參數
        with open("main_config.ini","r",encoding="utf-8") as f:
            tmp_content=f.read()
        f.close()
        exec(tmp_content)
        #print(KEY_CONFIG)
    except:
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"\t讀取main_config.ini失敗!請確認該檔是否存在或格式是否錯誤!")
        exit()
    #print("start")
    num = JoyStick.joyGetNumDevs()
    ret, caps, startinfo = False, None, None
    for id in range(num):
        ret, caps = JoyStick.joyGetDevCaps(id)
        if ret:
            print("偵測到控制器: " + caps.szPname + "\n按鍵映射運作正常...\n按 [ ← Backspace ] 結束程式")
            ret, startinfo = JoyStick.joyGetPosEx(id)
            break
    else:
        print("未偵測到控制器。")
        exit()
    keys_stat_last=[False,False,False,False,False,False,False,False,False,False]
    str_for_print_last=""
    run = ret
    LM_stat=[0,0]
    tmp_key_cfg_x=""
    cx,cy=Mouse.get_pos()
    xy_offset=15
    while run:
        sleep(DELAY_SECOND)
        if msvcrt.kbhit() and msvcrt.getch() == chr(8).encode(): # detect F10
            run = False
        ret, info = JoyStick.joyGetPosEx(id)
        if ret:
            btns = [(1 << i) & info.dwButtons != 0 for i in range(caps.wNumButtons)]
            axisXYZ = [info.dwXpos-startinfo.dwXpos, info.dwYpos-startinfo.dwYpos, info.dwZpos-startinfo.dwZpos]
            axisRUV = [info.dwRpos-startinfo.dwRpos, info.dwUpos-startinfo.dwUpos, info.dwVpos-startinfo.dwVpos]

            #左右小搖桿同一時間只能有一個有作用(避免互相干擾)
            right_stick_is_working=False
            if any([abs(v) > 10 for v in axisRUV]): #右小搖桿
                tx= 0 if axisRUV[1]==128 else ((xy_offset*2) if axisRUV[1]>128 else (-xy_offset*2))
                ty = 0 if axisRUV[0]==-129 else ((-xy_offset*2) if axisRUV[0]<-129 else (xy_offset*2))
                if tx!=0 or ty!=0:
                    cx,cy=Mouse.move_to(tx,ty)
                    right_stick_is_working=True
            #右小搖桿沒動作的話左邊搖桿才會work
            if right_stick_is_working==False and any([abs(v) > 10 for v in axisXYZ]): #左小搖桿
                    tx= 0 if axisXYZ[0]==128 else ((XY_OFFSET_UNIT*2) if axisXYZ[0]>128 else (-XY_OFFSET_UNIT*2))
                    ty = 0 if axisXYZ[1]==-129 else ((-XY_OFFSET_UNIT*2) if axisXYZ[1]<-129 else (XY_OFFSET_UNIT*2))
                    if tx!=0 or ty!=0:
                        cx,cy=Mouse.move_to(tx,ty)
                    #如果 SET_LEFT_CONTROLLER_MOVE_AND_CLICK 為 True 則按一下滑鼠
                    if (tx!=0 or ty!=0) and SET_LEFT_CONTROLLER_MOVE_AND_CLICK:
                        Mouse.click('left',cx,cy,1)
                        sleep(0.01)
                        Mouse.click('left',cx,cy,0)
                    if axisXYZ[2]>0:
                        btns[8]=True
                    elif axisXYZ[2]<0:
                        btns[9]=True

            process_btns(btns)
    print("按下 [ ← Backspace ] 程式結束")
