## esp8266 deautch 解除认证攻击  
-------
通过修改micropython中esp8266的固件源码，调用ESP8266-SDK中wifi_send_pkt_freedom函数，
实现Deauth解除认证包的发送，从而达到WIFI干扰的效果。  
由[点我跳转](https://github.com/PakchoiFood/micropython-deauth)进行封装和改进。  
原理和功能参考: [esp8266_deauther](https://github.com/spacehuhn/esp8266_deauther)  
按照 esp8266_deauther_old/attack.h ，attack.cpp 折腾的，有空按照_new的来。
esp8266固件引出 wifi_send_pkt_freedom 函数，再编译。  
=====
## 文件
    * sinfffer  嗅探示例
    * arduino   arduino 实现的强制认证门户(CaptivePortal)
    * esp8266_deauther  是Arudino可以直接刷入的WIFI攻击开源程序(需要配置，比如说SDK2.0版本)  
    * main.py  是Deauth攻击的协作源码
    * main_ziyong.py 是自己用的Deauth攻击源码，通过通用串口调试代码。
    * main_cp.py 是扫描周围WIFI并挨个自动复制再实现强制认证门户的代码