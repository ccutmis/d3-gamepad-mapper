""" 參考網址: https://stackoverflow.com/questions/60309652/how-to-get-usb-controller-gamepad-to-work-with-python """
# ver.0001b todo:
# 重寫左右小搖桿的控制判斷 並加入1234按鍵可以一鍵切換持續施法的功能(KEY_ONOFF_MODE用來定義按鍵是否啟用此功能)
from datetime import datetime
import win32api
from time import sleep
import msvcrt
import myModule.joystick_api as JoyStick
from myModule.WindowMgr import *
import myModule.mouse_api as Mouse
from pynput.keyboard import Key, Controller
import math

def process_btns(btns):
    keyboard = Controller()
    global keys_stat_last,KEY_CONFIG,BTN_DICT,str_for_print_last
    global KEY_MAP,KEY_ONOFF_MODE,current_onoff,onoff_list
    x=0
    str_for_print=""
    for i in btns:
        curr_key=KEY_CONFIG[BTN_DICT[x]]
        if i==True: #按下狀態，確認一下先前是否已按，若已按無需再做其它事
            if KEY_ONOFF_MODE[BTN_DICT[x]]==1:
                #檢查current_onoff[x]是否為0
                if BTN_DICT[x] not in onoff_list:
                    onoff_list.append(BTN_DICT[x])
                    keyboard.press(curr_key)
                    sleep(0.1)
                    keyboard.release(curr_key)
                else:
                    onoff_list.remove(BTN_DICT[x])
            if keys_stat_last[x]==True: #先前已按
                pass
            else:
                if curr_key not in ["LM","RM"]: #不是按滑鼠左右鍵
                    if len(curr_key)==1:
                        keyboard.press(curr_key)
                    else:
                        keyboard.press(eval("Key."+curr_key))
                    #print(curr_key)
                else: #是滑鼠左右鍵
                    if curr_key=="LM":
                        Mouse.click('left',cx,cy)
                    elif curr_key=="RM":
                        Mouse.click('right',cx,cy)
                    else:
                        print(curr_key,"press")
                        #Mouse.click(KEY_MAP[curr_key],cx,cy)
                keys_stat_last[x]=True
                        
        else:
            if KEY_ONOFF_MODE[BTN_DICT[x]]==1 and BTN_DICT[x] in onoff_list:
                keyboard.press(curr_key)
                sleep(0.1)
                keyboard.release(curr_key)
            if keys_stat_last[x]==True: #先前已按目前沒按
                if curr_key not in ["LM","RM"]: #不是滑鼠左右鍵
                    if len(curr_key)==1:
                        keyboard.release(curr_key)
                    else:
                        keyboard.release(eval("Key."+curr_key))
                    #keyboard.release(curr_key)
                else:
                    if curr_key=="LM":
                        Mouse.click('left',cx,cy,0)
                    elif curr_key=="RM":
                        Mouse.click('right',cx,cy,0)
                    else:
                        print(curr_key,"release")
                        #Mouse.click(KEY_MAP[curr_key],cx,cy,0)
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
    except:
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"\t讀取main_config.ini失敗!請確認該檔是否存在或格式是否錯誤!")
        exit()
    #print("start")
    w=WindowMgr()
    #develope mode start

    #D3-Gamepad是否置頂
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
            print("偵測到控制器: " + caps.szPname + "\n按鍵映射運作正常...\n按 [ ← Backspace ] 結束程式")
            ret, startinfo = JoyStick.joyGetPosEx(id)
            break
    else:
        print("未偵測到控制器。")
        exit()
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
    #全域變數區.end
    while run:
        sleep(DELAY_SECOND)
        if msvcrt.kbhit() and msvcrt.getch() == chr(8).encode(): # detect F10
            run = False
        #判斷當前視窗完整標題文字是否包含 ACTIVE_WIN_TITLE 設定之文字，若是才繼續後續處理...
        if ACTIVE_WIN_TITLE in w.active_window_title():
            win_pos_size=w.get_window_pos_size() #[x,y,w,h]
            x_center=int(win_pos_size[0]+(win_pos_size[2]/2))
            y_center=int(win_pos_size[1]+(win_pos_size[3]/2))
            #print(win_pos_size)
            #print(x_center,y_center)
            ret, info = JoyStick.joyGetPosEx(id)
            if ret:
                btns = [(1 << i) & info.dwButtons != 0 for i in range(caps.wNumButtons)]
                axisXYZ = [info.dwXpos-startinfo.dwXpos, info.dwYpos-startinfo.dwYpos, info.dwZpos-startinfo.dwZpos]
                axisRUV = [info.dwRpos-startinfo.dwRpos, info.dwUpos-startinfo.dwUpos, info.dwVpos-startinfo.dwVpos]
    
                #左右小搖桿同一時間只能有一個有作用(避免互相干擾)
                right_stick_is_working=False
                if any([abs(v) > 10 for v in axisRUV]): #右小搖桿
                    deg=int(math.atan2(axisRUV[0],axisRUV[1]))
                    direction="0" if deg==-1 else ("11" if deg==-2 else ("9" if deg==-3 else ("8" if deg==2 else ("6" if deg==1 else ("5" if axisRUV[0]>0 and axisRUV[1]>0 else ("3" if axisRUV[0]==-1 and axisRUV[1]>0 else ("1")))))))
                    tx= 0 if direction in ["0","6"] else ((xy_offset) if direction in ["5","3","1"] else (-xy_offset))
                    ty= 0 if direction in ["3","9"] else ((xy_offset) if direction in ["8","6","5"] else (-xy_offset))
                    if tx!=0 or ty!=0:
                        if xy_offset_bonus<25:
                            xy_offset_bonus+=1
                        tx=tx+xy_offset_bonus if tx>=0 else tx-xy_offset_bonus
                        ty=ty+xy_offset_bonus if ty>=0 else ty-xy_offset_bonus
                        cx,cy=Mouse.move_to(tx,ty)
                        right_stick_is_working=True
                else:
                    xy_offset_bonus=0
                #右小搖桿沒動作的話左邊搖桿才會work
                if right_stick_is_working==False and any([abs(v) > 10 for v in axisXYZ]): #左小搖桿
                    deg=int(math.atan2(axisXYZ[1],axisXYZ[0]))
                    #print(axisXYZ[1],axisXYZ[0],deg)
                    direction="0" if deg==-1 else ("11" if deg==-2 else ("9" if deg==-3 else ("8" if deg==2 else ("6" if deg==1 else ("5" if axisXYZ[1]>0 and axisXYZ[0]>0 else ("3" if axisXYZ[1]==-1 and axisXYZ[0]>0 else ("1")))))))
                    #print(direction)
                    tx= 0 if direction in ["0","6"] else ((xy_offset) if direction in ["5","3","1"] else (-xy_offset))
                    ty= 0 if direction in ["3","9"] else ((xy_offset) if direction in ["8","6","5"] else (-xy_offset))

                    if tx!=0 or ty!=0:
                        #如果 SET_LEFT_CONTROLLER_MOVE_AND_CLICK 為 True
                        if SET_LEFT_CONTROLLER_MOVE_AND_CLICK:
                            tx=tx*8
                            ty=ty*8 if ty>0 else ty*16
                            Mouse.set_pos(x_center,y_center)
                            sleep(0.01)
                            Mouse.set_pos(x_center+tx,y_center+ty)
                            cx,cy=Mouse.get_pos()
                            Mouse.click('left',cx,cy,1)
                            sleep(0.01)
                            Mouse.click('left',cx,cy,0)
                        else:
                            tx=tx*2
                            ty=ty*2
                            cx,cy=Mouse.move_to(tx,ty)
                    if axisXYZ[2]>0:
                        btns[8]=True
                    elif axisXYZ[2]<0:
                        btns[9]=True
                process_btns(btns)
    print("按下 [ ← Backspace ] 程式結束")