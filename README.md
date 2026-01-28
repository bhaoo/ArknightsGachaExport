# ArknightsGachaExport

> [!WARNING]
> 1. 本项目目前仅测试过国服账号，渠道服以及其他外服账号暂未测试。
> 2. 本项目在 Python 3.11.6 版本下开发，需自行测试其他版本下的可用性。

## 下载与安装

1. 通过 `git clone` 克隆本项目或前往 [Releases](https://github.com/bhaoo/ArknightsGachaExport/releases) 下载。
2. 运行 `pip install -r requirements.txt` 以安装依赖。
3. 完善配置文件 `config.yml` 的内容。
4. 前往 [游戏角色信息页面](https://user.hypergryph.com/myCharacters) 并设置默认角色。
5. 通过 `python3 main.py` 运行本项目 或使用 `nohup python3 main.py > log.txt 2>&1 &` 保持在后台运行。

## 数据格式

该数据以 JSON对象 的形式进行存储，示例如下：

```json
{
  "1714656890":{
    "p":"何以为我",
    "c":[
      ["深海色",3,0]
    ]
  }
}
```

数据的存储位置位于项目根目录下的 `data` 目录中，文件名为 `<账号UID>.json`

### 字段含义

- 时间戳：键名为字符串形式的时间戳，用于标识该数据记录的创建或发生时间。
- p：表示该时间戳对应的卡池名称。
- c：表示该时间戳下的所招聘的干员列表，每个子项为一个数组，包含：
  - 干员名：干员的名称。
  - 星级：干员的星级。
  - isNew：干员是否为首次获得（是则为 1）。

## 声明

本软件开源、免费，仅供学习交流使用。

Copyright © 2025-2026 Bhao, under MIT License.
