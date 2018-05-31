# ambari-elasticsearch-Head
ambari install elasticsearch-head plug-ins
扩展了ambari 安装 elasticsearch head 插件，目前已在正式环境部署，未发现什么bug，具体的内容后面在补充



2018年5月29日09:23:16
发现代码BUG1：head插件检测状态组件检测的事ES 的状态，并非自身状态。  目前仅head插件有此BUG  后续将被整改。

2018年5月31日10:30:14
修复检测状态bug，创建pid 以及检测pid 状态，已找到通用修复办法，寻找时间将进行修复。


另外预热一下，一套基于Ambari AMS 框架改造的Sink 收集器已经在生产环境上线，近期将会去敏发布在github开源。


