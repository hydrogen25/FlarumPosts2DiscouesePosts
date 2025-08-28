中文版本 | [English Version](README_CN.md) 


[![Python](https://img.shields.io/badge/Python-3776AB?logo=python\&logoColor=fff)](#)

# FlarumPosts2DiscouesePosts

一个将 Flarum 帖子转发到 Discourse 的简单工具

## 使用说明

建议使用 UV 构建运行环境

请参考 [UV 安装指南](https://github.com/astral-sh/uv)，安装完成后执行如下命令：

```shell
# 请根据实际情况替换以下参数

# 英文版
uv run main.py --start_id=1 --end_id=400 --api_key="your_api_key" --api_username="UserName" --flarum_url="https://old.flarum.com/" --discourse_url="https://new.discourse.com/"

# 中文版
uv run main_zh_hans.py --start_id=1 --end_id=400 --api_key="your_api_key" --api_username="UserName" --flarum_url="https://old.flarum.com/" --discourse_url="https://new.discourse.com/"
```

## 参数说明

* **start\_id**：Flarum 中要开始迁移的帖子 ID，可从 Flarum 帖子 URL 中 `https://your.flarum.website/d/` 后看到。默认值为 1

* **end\_id**：Flarum 中要结束迁移的帖子 ID，可从 Flarum 帖子 URL 中 `https://your.flarum.website/d/` 后看到。默认值为 100

* **api\_key**：在 Discourse 管理后台 “高级 > API Key” 中获取

* **api\_username**：用于创建 API Key 的用户名

* **flarum\_url**：要迁移帖子所在的 Flarum 站点的 URL

* **discourse\_url**：要将帖子转发到的 Discourse 站点 URL
