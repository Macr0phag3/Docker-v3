```
Main
├──基本操作
│    ├──检查连接
│    ├──分配容器（高层；负责分配拉起容器）
│    ├──回收容器（高层；负责分配回收容器）
│    ├──查看镜像（高层；列出镜像）
│    ├──查看容器（高层；列出容器）
│    ├──详细信息（高层；查看系统的所有信息）
│    ├──返回
│    └──退出
│
├──更多操作（底层；更多的细节操作）
│    ├──网络相关
│    │  ├──显示可用 ip
│    │  └──显示已用 ip
│    │
│    ├──运行
│    │
│    ├──停止
│    │  ├──单个容器
│    │  ├──多个容器
│    │  ├──所有容器
│    │  ├──返回
│    │  └──退出
│    │
│    ├──删除
│    │  ├──单个容器
│    │  ├──多个容器
│    │  ├──所有容器
│    │  ├──返回
│    │  └──退出
│    │
│    ├──返回
│    └──退出
│
├──使用说明
│
└──退出
```

```
[+]虚拟机: 192.168.12.1
  [-]负载:
    [-]cpu:
    [-]mem:
  [-]网络:
    [-]外网:
    [-]内网:
  [-]拥有镜像()
    [-]
  [-]拥有容器()
    [-]short id
      [-]id:
      [-]状态:
      [-]时间:
      [-]ip:
      [-]镜像名:
```

```
1. short id:
  [-]id
  [-]状态:
  [-]时间:
  [-]容器 ip:
  [-]虚拟机 ip:
  [-]镜像名:
```


```
docker images|grep none|awk '{print $3}'|xargs docker rmi
```
