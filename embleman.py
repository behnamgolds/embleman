#!/usr/bin/python

# https://lazka.github.io/pgi-docs
# pip install PyGObject
# pacman -Syu python-gobject

from gi.repository import Gio

import re
import sys
import os
from typing import List, Pattern

# https://github.com/moses-palmer/pynput
# pip install pynput
from pynput.keyboard import Key, Controller

import argparse
from pathlib import Path

app_version = "0.1.0"
# type Namespace = argparse.Namespace

query_info_flags = Gio.FileQueryInfoFlags(0)


class PathResult:
    def __init__(self, ok=False, path=None):
        self.ok = ok
        self.path = path


class FsItem:
    def __init__(self, path: str, action: str, disable_refresh=False):
        self.__disable_refresh = disable_refresh
        self.__path = Gio.file_new_for_path(path)
        self.__action = action
        self.__path_info = self.__path.query_info('metadata::emblems', query_info_flags)
        self.__emblems = self.__path_info.get_attribute_stringv("metadata::emblems")
        self.__emb_num = -1
        self.__num_emblem_found = False

    def __refresh_window(self):
        if not self.__disable_refresh:
            Controller().tap(Key.f5)

    def __matches_pattern(self, pattern: Pattern, emblem: str) -> bool:
        # TODO: Check this later
        return pattern.match(emblem) is not None

    def __increase_num(self, n) -> int:
        if n == 19:
            return -1
        return n + 1

    def __decrease_num(self, n) -> int:
        if n == 1:
            return -1
        return n - 1

    def __is_increase_action(self) -> bool:
        return self.__action == "inc"

    def __set_one(self):
        one_emblem = "emblem-num-" + str(1) + "-symbolic"
        self.__emblems.append(one_emblem)
        self.__set_emblems()

    def __set_emblems(self):
        self.__path_info.set_attribute_stringv("metadata::emblems", self.__emblems)
        self.__path.set_attributes_from_info(self.__path_info, query_info_flags)
        self.__refresh_window()

    def __execute_num_action(self):
        for i in range(0, len(self.__emblems)):
            pattern = re.compile("^emblem-num-[0-9]+-symbolic$")
            if self.__matches_pattern(pattern, self.__emblems[i]):
                self.__num_emblem_found = True
                num = int(self.__emblems[i].split("-")[2])

                if self.__is_increase_action(self.__action):
                    num = self.__increase_num(num)
                else:
                    num = self.__decrease_num(num)

                if num == -1:
                    self.__emblems.pop(i)
                    self.__set_emblems()
                    return
                else:
                    new_num_emblem = "emblem-num-" + str(num) + "-symbolic"
                    self.__emblems[i] = new_num_emblem
                    self.__set_emblems()
                    return

        if not self.__num_emblem_found:
            if self.__is_increase_action():
                self.__set_one()
                return

    # toggles clock/check emblem on / off
    def __execute_toggle_action(self):
        if self.__action == "clock":
            emblem = "emblem-urgent"
        else:
            emblem = "vcs-normal"

        for i in range(0, len(self.__emblems)):
            if self.__emblems[i] == emblem:
                self.__emblems.pop(i)
                self.__set_emblems()
                return
        self.__emblems.append(emblem)
        self.__set_emblems()

    # clears all emblems
    def __execute_clear_action(self):
        self.__emblems = []
        self.__set_emblems()

    def execute_action(self):
        match self.__action:
            case "inc" | "dec":
                self.__execute_num_action()
            case "clock" | "check":
                self.__execute_toggle_action()
            case "clear":
                self.__execute_clear_action()


def init_cmd_parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="embleman",
        description="%(prog)s: a set of emblem actions",
        epilog="Hey noob ! o_O"
    )

    parser.add_argument(
        "-v", f"--version", action="version", version=f"%(prog)s {app_version}"
    )

    exclusive_action_group = parser.add_mutually_exclusive_group(required=True)

    exclusive_action_group.add_argument("--increase", action="store_const", const="inc",
                                        dest="action", help="Increase the number emblem")
    exclusive_action_group.add_argument("--decrease", action="store_const", const="dec",
                                        dest="action", help="Decrease the number emblem")
    exclusive_action_group.add_argument("--clock", action="store_const", const="clock",
                                        dest="action", help="Toggle clock sign emblem")
    exclusive_action_group.add_argument("--check", action="store_const", const="check",
                                        dest="action", help="Toggle check sign emblem")
    exclusive_action_group.add_argument("--clear", action="store_const",
                                        const="clear", dest="action", help="Clear all the emblems")

    parser.add_argument("paths", nargs="+",
                        help="Path or Paths, Only --clear action takes multiple paths")
    parser.add_argument("--disable-refresh", action="store_true", dest="disable_refresh",
                        default=False, help="Disables Sending F5 Key, useful when running from command line")

    return parser.parse_args()


def path_exists(path: str) -> PathResult:
    p = Path(path)
    if p.exists():
        return PathResult(True, str(p.absolute()))
    return PathResult()


def main():
    args = init_cmd_parser()
    if args.action == "clear":
        for path in args.paths:
            result = path_exists(path)
            if result.ok:
                item = FsItem(result.path, args.action, args.disable_refresh)
                item.execute_action()
    else:
        result = path_exists(args.paths[0])
        if result.ok:
            item = FsItem(result.path, args.action, args.disable_refresh)
            item.execute_action()


if __name__ == "__main__":
    main()
