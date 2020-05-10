import argparse
import os
import re
import textwrap
from multiprocessing.dummy import Pool

import commonmark
import huepy
import requests
from tenacity import retry, stop_after_attempt

from _version import __version__
from command import COMMAND

TAG_HEADING = "heading"
TAG_ITEM = "item"
TAG_CODE_BLOCK = "code_block"
TAG_LIST = "list"
TAG_PARAGRAPH = "paragraph"
TAG_HTML_BLOCK = "html_block"
TAG_STRONG = "strong"
TAG_TEXT = "text"
TAG_BLOCK_QUOTE = "block_quote"

EXT = ".md"
MAX_WIDTH = 40
MAX_CONCURRENCY = 8

COMMAND_DIR = os.path.join(os.path.expanduser("~"), ".command")
FILE_URL = "https://unpkg.com/linux-command/command/{}.md"


class Tag:
    def __init__(self, t, literal, level):
        self.t = t
        self.literal = literal
        self.level = level

    def __repr__(self):
        return "[<t: {}> <literal: {}> <level: {}>]".format(
            self.t, self.literal, self.level
        )


def docs_need_space(docs):
    left = re.compile(r"([a-zA-Z0-9)])([\u4e00-\u9fa5])")
    right = re.compile(r"([\u4e00-\u9fa5])([a-zA-Z0-9\[])")
    return re.sub(right, r"\1 \2", re.sub(left, r"\1 \2", docs))


def wrap_text(text):
    return textwrap.fill(text=text, width=MAX_WIDTH) + "\n"


def highlight(text: str, keyword: str):
    return re.sub(
        keyword,
        "\33[0m" + "\33[93m" + keyword + "\33[0m" + "\33[37m",
        text,
        flags=re.IGNORECASE,
    )


def get_content(command):
    file_path = os.path.join(COMMAND_DIR, command + EXT)
    if not os.path.exists(file_path):
        download_file(command)
    if not os.path.exists(file_path):
        return ""
    with open(file_path, "r", encoding="utf8") as f:
        return f.read()


def how_to_use(command):
    content = get_content(command)
    if not content:
        print("Sorry: could not find the `{}` command".format(command))
        return

    parse = commonmark.Parser()
    ast = parse.parse(content)

    tags = []
    for obj, entering in ast.walker():
        if not entering or obj.t == TAG_HTML_BLOCK:
            continue
        tags.append(Tag(obj.t, obj.literal, obj.level))

    tag_length, out = len(tags), ""
    for i, tag in enumerate(tags):
        if i < tag_length - 1:
            if tag.t == TAG_HEADING:
                tag.literal = huepy.bold("#" * tag.level + " ")
            if tag.t == TAG_TEXT:
                if tags[i + 1].t in (TAG_PARAGRAPH, TAG_HEADING, TAG_CODE_BLOCK):
                    tag.literal = tag.literal + "\n" * 2
                if tags[i + 1].t == TAG_ITEM:
                    tag.literal = tag.literal + "\n" + "- "
                if tags[i + 1].t == TAG_LIST:
                    tag.literal = tag.literal + "\n" * 2 + "- "
                if tags[i + 1].t == TAG_BLOCK_QUOTE:
                    tag.literal = tag.literal + "\n" * 2 + "> "
            if tag.t == TAG_CODE_BLOCK:
                tag.literal = tag.literal + "\n"

        if tag.literal:
            out += tag.literal
    doc = [wrap_text(d) for d in docs_need_space(out).strip().split("\n")]
    print(highlight("".join(doc), command))


@retry(stop=stop_after_attempt(3))
def download_file(command):
    if not os.path.exists(COMMAND_DIR):
        os.makedirs(COMMAND_DIR)

    url = FILE_URL.format(command)
    response = requests.get(url)
    if response.status_code >= 400:
        return

    file_path = os.path.join(COMMAND_DIR, command + EXT)
    with open(file_path, "w+", encoding="utf8") as f:
        f.write(response.text)


cnt = 0


def download_file_progress(command):
    download_file(command)
    global cnt
    cnt += 1
    print("\rInitializing commands: {}/{} ".format(cnt, len(COMMAND)), end="")


def init_command():
    # speed up
    p = Pool(MAX_CONCURRENCY)
    p.map(download_file_progress, COMMAND)
    p.close()
    p.join()
    print()


def get_parser():
    parser = argparse.ArgumentParser(
        description="Impressive Linux commands cheat sheet."
    )
    parser.add_argument(
        "command", metavar="COMMAND", type=str, nargs="*", help="the puzzling command"
    )
    parser.add_argument(
        "-i", "--init", action="store_true", help="initialize all commands"
    )
    parser.add_argument(
        "-v",
        "--version",
        action="store_true",
        help="displays the current version of `how`",
    )
    return parser


def command_line_runner():
    parser = get_parser()
    args = vars(parser.parse_args())

    command = "".join(args["command"]).lower()

    if args["version"]:
        print(huepy.info("how " + __version__))
        return

    if args["init"]:
        init_command()
        return

    if not args["command"]:
        parser.print_help()
        return

    how_to_use(command)


if __name__ == "__main__":
    command_line_runner()
