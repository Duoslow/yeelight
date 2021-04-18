from infi.systray import SysTrayIcon
from yeelight import discover_bulbs,Bulb
import easygui_qt as easy
import time
while True:
    try:
        bulb_data = discover_bulbs()
        if bulb_data:
            b_ip = bulb_data[-1]['ip']
            b_port = bulb_data[-1]['port']
            b_bulb = Bulb(b_ip)
            if b_bulb:
                print('Connected')
                break
        print('cannot find')
        time.sleep(5)
    except Exception as e :
        print('Error discovering bulbs',e)
   

def brgh25(systray):
    b_bulb.set_brightness(25)
def brgh50(systray):
    b_bulb.set_brightness(50)
def brgh75(systray):
    b_bulb.set_brightness(75)
def brgh100(systray):
    b_bulb.set_brightness(100)

def cs_brgh(systray):
    number = easy.get_int('Enter the brightness','Brightness',1,1,100,1)
    if number:
        b_bulb.set_brightness(int(number))
def rgbblb(systray):
    color = easy.get_color_rgb()
    if color:
        b_bulb.set_rgb(color[0],color[1],color[2])


optiona = (
    ('On', None,b_bulb.turn_on),
('Off', None,b_bulb.turn_off),
('Color',None,rgbblb),
('Brightness','brg.ico',(
    ('custom', None,cs_brgh),
    ('%25', None,brgh25),
    ('%50', None,brgh50),
    ('%75', None,brgh75),
    ('%100', None,brgh100)
    ))) 
systray = SysTrayIcon("icon.ico", "Yeelight Control", optiona)
systray.start()
