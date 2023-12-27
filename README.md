# 3760
https://blog.left.pink/archives/3760 中用到的脚本

自行申请 settings.json 中提到的 Api Key

## 感谢

脚本在以下几位大师的指导下完成

<img src="https://github.com/Left024/3760/assets/20574903/8434a2c5-7682-418e-af59-3bf7d2a74249" width="200px" />

## Radarr

懒人用法：将 Radarr 文件夹放入 /root/ 目录，并给 run.sh 授予可执行权限，在 /root/Radarr/ 目录中创建 image 文件夹，Radarr 中如图设置即可

<img src="https://chevereto.left.pink/images/2023/12/27/20231227011927.png" width="300px" />

这里是运行 ```run.sh``` ，```run.sh``` 再运行 ```run.py```，如果你没有放在 root 目录下，请修改 ```run.sh``` 中的目录：

```
/usr/bin/python3 /root/Sonarr/run.py "${json}" & #将 python 脚本地址修改为你的
```

建议先手动运行下看能否运行，缺少什么依赖

## Sonarr

用法同上
