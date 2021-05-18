from infi.systray import SysTrayIcon
from yeelight import discover_bulbs,Bulb
from win10toast import ToastNotifier
import easygui_qt as easy
import time , keyboard

from threading import Thread
bulb_data = b_ip = b_port = b_bulb = None
p = False

def bulb_finder():
    global bulb_data,b_ip,b_port,b_bulb
    while True:
        try:
            bulb_data = discover_bulbs()
            if bulb_data:
                b_ip = bulb_data[-1]['ip']
                b_port = bulb_data[-1]['port']
                b_bulb = Bulb(b_ip, effect="smooth", duration=1000)
                if b_bulb:
                    print('Connected')
                    print(b_bulb.get_properties())
                    break
            print('cannot find')
            time.sleep(5)
        except Exception as e :
            print('Error discovering bulbs',e)
Thread(target=bulb_finder ,args=[],daemon=True).start()

def bulb_brigtness(val_b):
    print(val_b)
    b_bulb.set_brightness(val_b)

def custom_brightness(systray):
    def smain():
        number = easy.get_int('Enter the brightness','Brightness',1,1,100,1)
        if number:
            b_bulb.set_brightness(int(number))
    Thread(target=smain ,args=[],daemon=True).start()

def bulb_color(systray):
    color = easy.get_color_rgb()
    if color:
        b_bulb.set_rgb(color[0],color[1],color[2])

def test3131(systray):
    systray.update(icon='brg.ico')

def notifier(mes):
    toaster = ToastNotifier()
    toaster.show_toast("Yeelight Control", mes, icon_path=None, duration=1, threaded=True)

def shortcut_toggle():
    global p
    p^=True
    if p:
        notifier("Hotkeys Active")
        keyboard.add_hotkey('ctrl+shift+"', lambda: b_bulb.toggle(),suppress=True)
        keyboard.add_hotkey('ctrl+shift+1', lambda: bulb_brigtness(1),suppress=True)
        keyboard.add_hotkey('ctrl+shift+2', lambda: bulb_brigtness(50),suppress=True)
        keyboard.add_hotkey('ctrl+shift+3', lambda: bulb_brigtness(100),suppress=True)
        keyboard.add_hotkey('ctrl+shift+4', lambda: custom_brightness(None),suppress=True)
    else:
        notifier("Hotkeys Passive")
        keyboard.remove_hotkey('ctrl+shift+"')
        keyboard.remove_hotkey('ctrl+shift+1')
        keyboard.remove_hotkey('ctrl+shift+2')
        keyboard.remove_hotkey('ctrl+shift+3')
        keyboard.remove_hotkey('ctrl+shift+4')


while True:
    try:
        option_main = (
            ('Toggle', None,b_bulb.toggle),
            ('Color',None,bulb_color),
            ('Brightness','icons\\brg.ico',(
                ('custom', None,custom_brightness),
                ('%25', None,lambda x:bulb_brigtness(25)),
                ('%50', None,lambda x:bulb_brigtness(50)),
                ('%75', None,lambda x:bulb_brigtness(75)),
                ('%100', None,lambda x:bulb_brigtness(100))
            )),
             ('Shortcuts', None,lambda x:shortcut_toggle())
            ) 
        systray = SysTrayIcon("icons\\main.ico", "Yeelight Control", option_main)
        systray.start()
        break
    except:
        time.sleep(5)