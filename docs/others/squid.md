安装 squid 代理服务器
```
sudo apt-get update
sudo apt-get install squid
```
编辑配置文件
```
/etc/squid/squid.conf
```
```
http_port 3128 -> http_port 32001
http_access deny all -> http_access allow all
```
重启
```
systemctl restart squid
```
加入开机自启
```
systemctl enable squid
```

# 测试端口是否成功: 
https://tcp.ping.pe/152.32.173.95:32001