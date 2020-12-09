# ver.0007b todo:
# 使用traceback模組 在程式執行出錯時將錯誤報告記錄到 main_runtime_error.log
# 追加設定檔變數 DEBUG_MODE 用來設定是否啟用degug模式，若為 False 則不進行debug動作；若為 True 則會將執行中的按鍵且左右搖桿三軸的狀況寫入到main_degug.txt，這個動作會進行頻繁寫入文字檔的動作，除非有特殊原因要進行除錯，否則請讓它保持在 False 的值。
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
VERSION="0007b"

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
        #讀取 main_config.ini參數
        with open("main_config.ini","r",encoding="utf-8") as f:
            tmp_content=f.read()
        f.close()
        exec(tmp_content)
        #print(KEY_CONFIG)
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
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"\t讀取main_config.ini失敗!請確認該檔是否存在或格式是否錯誤!")
        sys.exit()
    try:
        if DEBUG_MODE:
            print("DEBUG START")
            fp=open('main_runtime.log','w+')
            fp.writelines(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+'\tDEBUG記錄開始\n')
        #print("start")
        w=WindowMgr()
        #develope mode start
        #D3-Gamepad是否置頂 這是方便自己開發時用的 正式發佈時要把它設為False
        MONITOR_ONTOP=False
        if MONITOR_ONTOP:
            #D3-Gamepad的視窗標題
            MONITOR_TITLE="cmd.exe"
            w.find_window_wildcard(MONITOR_TITLE)
            w.set_cmd_title("MY-GAMEPAD-MAPER")
            w.set_foreground()
            w.set_window_on_top("MY-GAMEPAD-MAPER",300,200)
        num = JoyStick.joyGetNumDevs()
        ret, caps, startinfo = False, None, None
        for id in range(num):
            ret, caps = JoyStick.joyGetDevCaps(id)
            if ret:
                print("D3-GAMEPAD Ver."+VERSION+"\n偵測到控制器: " + caps.szPname + "\n目標視窗:"+ACTIVE_WIN_TITLE+"\t按鍵映射運作正常...\n--------------------\n按 [ ← Backspace ] 結束程式")
                ret, startinfo = JoyStick.joyGetPosEx(id)
                break
        else:
            print("未偵測到控制器。")
            sys.exit()
        #全域變數區.start
        KEY_MAP={"alt":Key.alt,"alt_l":Key.alt_l,"alt_r":Key.alt_r,"backspace":Key.backspace,"caps_lock":Key.caps_lock,"cmd":Key.cmd,"cmd_r":Key.cmd_r,"ctrl":Key.ctrl,"ctrl_l":Key.ctrl_l,"ctrl_r":Key.ctrl_r,"delete":Key.delete,"down":Key.down,"end":Key.end,"enter":Key.enter,"esc":Key.esc,"f1":Key.f1,"f10":Key.f10,"f11":Key.f11,"f12":Key.f12,"f13":Key.f13,"f14":Key.f14,"f15":Key.f15,"f16":Key.f16,"f17":Key.f17,"f18":Key.f18,"f19":Key.f19,"f2":Key.f2,"f20":Key.f20,"f3":Key.f3,"f4":Key.f4,"f5":Key.f5,"f6":Key.f6,"f7":Key.f7,"f8":Key.f8,"f9":Key.f9,"home":Key.home,"insert":Key.insert,"left":Key.left,"menu":Key.menu,"num_lock":Key.num_lock,"page_down":Key.page_down,"page_up":Key.page_up,"pause":Key.pause,"print_screen":Key.print_screen,"right":Key.right,"scroll_lock":Key.scroll_lock,"shift":Key.shift,"shift_r":Key.shift_r,"space":Key.space,"tab":Key.tab,"up":Key.up}
        keys_stat_last=[False,False,False,False,False,False,False,False,False,False]
        str_for_print_last=""
        run = ret
        LM_stat=[0,0]
        tmp_key_cfg_x=""
        cx,cy=Mouse.get_pos()
        xy_offset=XY_OFFSET_UNIT
        xy_offset_bonus=0
        current_onoff=[0,0,0,0,0,0,0,0,0,0]
        onoff_list=[]
        DEG_DICT=gent_degree_dict(360,XY_OFFSET_UNIT)
        #全域變數區.end
        while run:
            sleep(DELAY_SECOND)
            if msvcrt.kbhit() and msvcrt.getch() == chr(8).encode(): # detect F10
                run = False
            #判斷當前視窗完整標題文字是否包含 ACTIVE_WIN_TITLE 設定之文字，若是才繼續後續處理...
            if ACTIVE_WIN_TITLE in w.active_window_title():
                win_pos_size=w.get_window_pos_size() #[x,y,w,h]
                sleep(DELAY_SECOND)
                x_center=int(win_pos_size[0]+(win_pos_size[2]/2))
                y_center=int(win_pos_size[1]+(win_pos_size[3]/2)+(Y_CENTER_OFFSET))
                #print(win_pos_size)
                #print(x_center,y_center)
                ret, info = JoyStick.joyGetPosEx(id)
                if ret:
                    btns = [(1 << i) & info.dwButtons != 0 for i in range(caps.wNumButtons)]
                    axisXYZ = [info.dwXpos-startinfo.dwXpos, info.dwYpos-startinfo.dwYpos, info.dwZpos-startinfo.dwZpos]
                    axisRUV = [info.dwRpos-startinfo.dwRpos, info.dwUpos-startinfo.dwUpos, info.dwVpos-startinfo.dwVpos]
                    if DEBUG_MODE:
                        fp.writelines(str(btns)+"\t"+str(axisXYZ)+"\t"+str(axisRUV)+"\n")
                    #左右小搖桿同一時間只能有一個有作用(避免互相干擾)
                    right_stick_is_working=False
                    #if any([abs(v) > 10 for v in axisRUV]): #右小搖桿
                    if abs(axisRUV[0]) > 10 or abs(axisRUV[1]) > 10 : #右小搖桿
                        degree=int(math.atan2(axisRUV[1],axisRUV[0])/math.pi*180)
                        if degree<0: 
                            degree=180+(180+degree)
                        #print(degree)
                        tx,ty=deg_to_xy(degree)
                        if tx!=0 or ty!=0:
                            if xy_offset_bonus<20:
                                xy_offset_bonus+=0.1
                            cx,cy=Mouse.move_to(tx,ty)
                            right_stick_is_working=True
                    else:
                        xy_offset_bonus=0
                    #右小搖桿沒動作的話左邊搖桿才會work
                    if right_stick_is_working==False and any([abs(v) > 10 for v in axisXYZ]): #左小搖桿
                        degree=int(math.atan2(axisXYZ[0],axisXYZ[1])/math.pi*180)
                        if degree<0: 
                            degree=180+(180+degree)
                        tx,ty=deg_to_xy(degree)
                        if tx!=0 or ty!=0:
                            #如果按的是TRIG_L或TRIG_R
                            if axisXYZ[2]!=0:
                                if axisXYZ[2]>0:
                                    btns[8]=True
                                elif axisXYZ[2]<0:
                                    btns[9]=True
                            #如果 SET_LEFT_CONTROLLER_MOVE_AND_CLICK 為 True
                            elif SET_LEFT_CONTROLLER_MOVE_AND_CLICK:
                                tx=tx*8
                                ty=ty*8
                                Mouse.set_pos(x_center+tx,y_center+ty)
                                cx,cy=Mouse.get_pos()
                                if LEFT_CONTROLLER_CLICK_VAL not in ["LM","RM"]: #不是按滑鼠左右鍵
                                    kb_press_eval_key(LEFT_CONTROLLER_CLICK_VAL)
                                    sleep(0.01)
                                    kb_release_eval_key(LEFT_CONTROLLER_CLICK_VAL)
                                else: #是滑鼠左右鍵
                                    if LEFT_CONTROLLER_CLICK_VAL=="LM":
                                        Mouse.click('left',cx,cy)
                                        sleep(0.01)
                                        Mouse.click('left',cx,cy,0)
                                    elif LEFT_CONTROLLER_CLICK_VAL=="RM":
                                        Mouse.click('right',cx,cy)
                                        sleep(0.01)
                                        Mouse.click('right',cx,cy,0)
                            else:
                                tx=tx*2
                                ty=ty*2
                                cx,cy=Mouse.move_to(tx,ty)
    
                    process_btns(btns)
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