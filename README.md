[中文版本](README_CN.md) | English version

[![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff)](#)


# FlarumPosts2DiscouesePosts
A simple program which forwarding the Flarum posts to The Discourse posts

## Usage

It is recommended to use the UV to build the operating environment

Please follow [this guide](https://github.com/astral-sh/uv) to install UV, then run the following command



```shell
#Please change these arguments to yourself arguments

#English Version
uv run main.py --start_id=1 --end_id=400 --api_key="your_api_key" --api_username="UserName" --flarum_url="https://old.flarum.com/" --discourse_url="https://new.discourse.com/"

#Simplified Chinese Version
uv run main_zh_hans.py --start_id=1 --end_id=400 --api_key="your_api_key" --api_username="UserName" --flarum_url="https://old.flarum.com/" --discourse_url="https://new.discourse.com/"
```

## Arguements

- **start_id**:  The post you want FlarumPosts2DiscouesePosts to start transferring, you can find it after the Flarum post URL `https://your.flarum.website/d/` . The default value is 1

- **end_id**: The post you want FlarumPosts2DiscouesePosts to end up transferring.,you can find it after the flarum post URL `https://your.flarum.website/d/` . The default value is 100

- **api_key**: Get it in `Advanced > API Key` from your discourse website console

- **api_username**: The username you used when creating the api_key

- **flarum_url**: The URL of the post you want to transfer

- **discourse_url**: The URL you want to transfer the post to