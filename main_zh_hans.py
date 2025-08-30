from typing import List
from pyflarum import FlarumError, FlarumUser, Discussion
from pydiscourse import DiscourseClient
import asyncio
from retry import retry
import html2text
from tqdm import tqdm
import click

SEM = asyncio.Semaphore(5)


class Post:
    author: str
    content: str

    def __init__(self, author: str, content: str) -> None:
        self.author = author
        self.content = content


class Passage:
    title: str
    author: str
    content: str
    posts: List[Post]

    def __init__(self, title: str, author: str, content: str) -> None:
        self.author = author
        self.title = title
        self.content = content
        self.posts = []

    def push_posts(self, post: Post) -> None:
        self.posts.append(post)


async def post_passages(
    passages: List[Passage], client: DiscourseClient, category_id: int
):
    tasks = []
    print("-----正在发布帖子-----")
    for passage in tqdm(passages):
        task = asyncio.create_task(_post_passage(passage, client, category_id))
        tasks.append(task)
        await asyncio.gather(*tasks)
    print("-----已完成发布帖子-----")


@retry(tries=5, delay=1)
async def _post_passage(passage: Passage, client: DiscourseClient, category_id: int):
    topic = client.create_post(
        title=passage.title,
        content=f"原发帖人：{passage.author}\n\n\n\n\n{passage.content}",
        category_id=category_id,
    )
    if topic is None:
        return
    topic_id = topic["topic_id"]

    for reply in passage.posts:
        client.create_post(
            topic_id=topic_id,
            content=f"原发帖人：{reply.author} \n\n\n {reply.content}",
        )


async def get_passages(
    user: FlarumUser, start_id: int = 1, end_id=400
) -> List[Passage]:
    end_id += 1
    tasks = []
    passages: List[Passage] = []
    print("-----正在获取帖子-----")
    for id in tqdm(range(start_id, end_id)):
        try:
            discussion: Discussion = user.get_discussion_by_id(id)
        except FlarumError:
            print(f"帖子 {id} 不存在，已跳过")
            continue
        task = asyncio.create_task(_get_passage(user, discussion))
        tasks.append(task)
    passages = await asyncio.gather(*tasks)
    print("-----已完成获取帖子-----")

    return passages


@retry(tries=5, delay=1)
async def _get_passage(user: FlarumUser, discussion: Discussion) -> Passage:
    author_data = discussion.get_author()
    if not author_data:
        author = "未知用户"
    else:
        author = author_data["data"]["attributes"].get("displayName", "未知用户")

    title = discussion.title or "None"
    posts = discussion.get_posts()

    if not posts:
        return Passage(author=author, title=title, content="(内容为空)")

    html_content = posts[0]["data"]["attributes"].get("contentHtml", "")
    content = html2text.html2text(html_content)

    passage = Passage(author=author, title=title, content=content)
    for post in posts[1:]:
        if post["data"]["type"] != "posts":
            continue
        if not post["data"]["attributes"].get("contentHtml"):
            continue

        # 处理缺少 user 的情况
        relationships = post["data"].get("relationships", {})
        user_rel = relationships.get("user")
        if not user_rel or not user_rel.get("data"):
            user_name = "未知用户"
        else:
            user_id = user_rel["data"]["id"]
            user_data = user.get_user_by_id(user_id)
            user_name = (
                user_data["data"]["attributes"].get("displayName", "未知用户")
                if user_data
                else "未知用户"
            )

        html_content = post["data"]["attributes"]["contentHtml"]
        content = html2text.html2text(html_content)
        post_object = Post(user_name, content)
        passage.push_posts(post_object)

    return passage


async def start(
    user: FlarumUser,
    client: DiscourseClient,
    start_id: int,
    end_id: int,
    category_id: int,
):
    passages = await get_passages(user, start_id, end_id)
    await post_passages(passages, client, category_id)


@click.command()
@click.option("--start_id", default=1, help="转发FlarumID的开始数字", type=int)
@click.option("--end_id", default=100, help="转发FlarumID的结束数字", type=int)
@click.option(
    "--category_id",
    default=1,
    help="你想迁移到Discourse的类别",
    type=int,
)
@click.option("--flarum_url", required=True, type=str)
@click.option("--discourse_url", required=True, type=str)
@click.option("--api_key", required=True, type=str)
@click.option("--api_username", required=True, type=str)
def main(
    flarum_url: str,
    discourse_url: str,
    api_key: str,
    api_username: str,
    start_id: int,
    end_id: int,
    category_id: int,
):
    USER = FlarumUser(forum_url=flarum_url)
    CLIENT = DiscourseClient(
        discourse_url,
        api_key=api_key,
        api_username=api_username,
    )
    asyncio.run(start(USER, CLIENT, start_id, end_id, category_id))


if __name__ == "__main__":
    main()
