# 自愿节能试点到目标企业总体的效果迁移

本项目提供资源节约业务资料的读取、口径核对及确定性重放接口，使用本地合成记录，不连接真实企业或设备。现有实现范围见[来源契约](docs/contracts.md)。

`trial.py`、`population.py`、`selection.py`各自负责来源语义，`analytics.py`调用这些接口输出当前可用资料。当前没有统计拟合、反事实推断、最优方案搜索或预测功能。`common.py`提供有限数值、精确金额、修订读取和摘要绑定发布；报告缓存放在`.runtime/`。

Python 3.11，当前只使用标准库。命令在项目根目录执行：

```sh
python -m unittest discover -s tests -v
python -m compileall -q .
python -m analytics
```

容器运行方式：

```sh
docker build -t resource-analysis .
docker run --rm --network=none resource-analysis
docker run --rm --network=none resource-analysis python -m analytics
```
