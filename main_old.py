""" 參考網址: https://stackoverflow.com/questions/60309652/how-to-get-usb-controller-gamepad-to-work-with-python """
# ver.0005a todo:
# [--]4.重寫左右小搖桿控制滑鼠移動的部份
import codecs
from datetime import datetime
import win32api
import time
import msvcrt
import myModule.joystick_api as JoyStick
import myModule.keyboard_api as KeyBoard
import myModule.mouse_api as Mouse

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
            print("偵測到控制器: " + caps.szPname + "\n按鍵映射運作正常...\n按[ESC]結束程式")
            ret, startinfo = JoyStick.joyGetPosEx(id)
            break
    else:
        print("未偵測到控制器。")
        exit()
    run = ret
    LM_stat=[0,0]
    tmp_key_cfg_x=""
    cx,cy=Mouse.get_pos()
    xy_offset=15
    while run:
        time.sleep(DELAY_SECOND)
        if msvcrt.kbhit() and msvcrt.getch() == chr(27).encode(): # detect F10
            run = False
        ret, info = JoyStick.joyGetPosEx(id)
        if ret:
            tmp_kb_str=""
            btns = [(1 << i) & info.dwButtons != 0 for i in range(caps.wNumButtons)]
            axisXYZ = [info.dwXpos-startinfo.dwXpos, info.dwYpos-startinfo.dwYpos, info.dwZpos-startinfo.dwZpos]
            axisRUV = [info.dwRpos-startinfo.dwRpos, info.dwUpos-startinfo.dwUpos, info.dwVpos-startinfo.dwVpos]
            #print(axisXYZ[2],axisRUV[2])
            if info.dwButtons:
                clm_stat=win32api.GetAsyncKeyState(0x01)&0x8000
                crm_stat=win32api.GetAsyncKeyState(0x02)&0x8000
                x=0
                #tmp_kb_str=""
                for i in btns:
                    if i==True:
                        tmp_key_cfg_x=KEY_CONFIG[BTN_DICT[x]]
                        if tmp_key_cfg_x not in ["LM","RM"]:
                            tmp_kb_str+=tmp_key_cfg_x
                        else:
                            if tmp_key_cfg_x=="LM":
                                if (clm_stat <= 0): #當前滑鼠左鍵未按下
                                    print("滑鼠左按下")
                                    Mouse.click('left',cx,cy) #滑鼠左鍵按下
                            else:
                                if (crm_stat <= 0): #當前滑鼠右鍵未按下
                                    print("滑鼠右按下")
                                    Mouse.click('right',cx,cy) #滑鼠右鍵按下
                    else:
                        if tmp_key_cfg_x in ["LM","RM"]:
                            if tmp_key_cfg_x=="LM":
                                if (clm_stat <= 0): #當前滑鼠左鍵未按下
                                    Mouse.click('left',cx,cy,0) #滑鼠左鍵放開
                            else:
                                if (crm_stat <= 0): #當前滑鼠右鍵未按下
                                    Mouse.click('right',cx,cy,0) #滑鼠右鍵放開
                    x+=1
                #輸出連續文字
                #for event in #KeyBoard.keyboard_stream(tmp_kb_str):
                #    KeyBoard.SendInput(event)
            cx,cy=Mouse.get_pos()
            if any([abs(v) > 10 for v in axisXYZ]): #左小搖桿
                #cx = cx if axisXYZ[0]==128 else ((cx + xy_offset) if axisXYZ[0]>128 else (cx - xy_offset))
                #cy = cy if axisXYZ[1]==-129 else ((cy - xy_offset) if axisXYZ[1]<-129 else (cy + xy_offset))
                #Mouse.set_pos(cx,cy)
                tx= 0 if axisXYZ[0]==128 else ((XY_OFFSET_UNIT) if axisXYZ[0]>128 else (-XY_OFFSET_UNIT))
                ty = 0 if axisXYZ[1]==-129 else ((-XY_OFFSET_UNIT) if axisXYZ[1]<-129 else (XY_OFFSET_UNIT))
                cx,cy=Mouse.move_to(tx,ty)
                #如果 SET_LEFT_CONTROLLER_MOVE_AND_CLICK 為 True 則按一下滑鼠
                if (tx!=0 or ty!=0) and SET_LEFT_CONTROLLER_MOVE_AND_CLICK:
                    Mouse.click('left',cx,cy,1)
                    time.sleep(0.05)
                    Mouse.click('left',cx,cy,0)
                if axisXYZ[2]>0:
                    #print("L press")
                    tmp_kb_str+=KEY_CONFIG['TRIG_L']
                elif axisXYZ[2]<0:
                    #print("R press")
                    tmp_kb_str+=KEY_CONFIG['TRIG_R']
            if any([abs(v) > 10 for v in axisRUV]): #右小搖桿
                #cx = cx if axisRUV[1]==128 else ((cx + xy_offset) if axisRUV[1]>128 else (cx - xy_offset))
                #cy = cy if axisRUV[0]==-129 else ((cy - xy_offset) if axisRUV[0]<-129 else (cy + xy_offset))
                #Mouse.set_pos(cx,cy)
                tx= 0 if axisRUV[1]==128 else ((xy_offset*2) if axisRUV[1]>128 else (-xy_offset*2))
                ty = 0 if axisRUV[0]==-129 else ((-xy_offset*2) if axisRUV[0]<-129 else (xy_offset*2))
                cx,cy=Mouse.move_to(tx,ty)
            #輸出連續文字
            for event in KeyBoard.keyboard_stream(tmp_kb_str):
                KeyBoard.SendInput(event)
    print("按下[ESC] 程式結束")
