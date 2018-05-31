## esp8266 deautch 解除认证攻击  
----
通过修改micropython中esp8266的固件源码，调用ESP8266-SDK中wifi_send_pkt_freedom函数，
实现Deauth解除认证包的发送，从而达到WIFI干扰的效果。  
由[点我跳转](https://github.com/PakchoiFood/micropython-deauth)进行封装和改进。  
原理和功能参考: [esp8266_deauther](https://github.com/spacehuhn/esp8266_deauther)  
按照 esp8266_deauther_old/attack.h ，attack.cpp 折腾的，有空按照_new的来。
esp8266固件引出 wifi_send_pkt_freedom 函数，再编译。  