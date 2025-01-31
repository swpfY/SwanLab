#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""
@DATE: 2023-11-30 01:39:04
@File: swanlab\cli\main.py
@IDE: vscode
@Description:
    swanlab脚本命令的主入口
"""

import click
from .utils import is_valid_ip, is_valid_port, is_valid_root_dir, URL
from ..utils import FONT
from ..env import get_server_host, get_server_port, get_swanlog_dir
import time


@click.group()
def cli():
    pass


@cli.command()
# 控制服务发布的ip地址
@click.option(
    "--host",
    "-h",
    default=None,
    type=str,
    help="The host of swanlab web, default by 127.0.0.1",
    callback=is_valid_ip,
)
# 控制服务发布的端口，默认5092
@click.option(
    "--port",
    "-p",
    default=None,
    type=int,
    help="The port of swanlab web, default by 5092",
    callback=is_valid_port,
)
# 实验文件夹
@click.option(
    "--logdir",
    "-l",
    default=None,
    type=str,
    help="Specify the folder to store Swanlog, which is by default the folder where Swanlab Watch is run.",
    callback=is_valid_root_dir,
)
# 日志等级
@click.option(
    "--log-level",
    default="info",
    type=click.Choice(["debug", "info", "warning", "error", "critical"]),
    help="The level of log, default by info; You can choose one of [debug, info, warning, error, critical]",
)
def watch(log_level: str, **kwargs):
    """Run this command to turn on the swanlab service."""
    # 本质上此模块用于注入环境变量并启动服务
    start = time.time()
    # 导入必要的模块
    from ..log import swanlog as swl
    from ..server import app
    import uvicorn

    # debug一下当前日志文件夹的位置
    swl.debug("Try to explore the swanlab experiment logs in: " + FONT.bold(get_swanlog_dir()))

    # ---------------------------------- 日志等级处理 ----------------------------------
    swl.setLevel(log_level)
    # ---------------------------------- 服务地址处理 ----------------------------------
    # 当前服务地址
    host = get_server_host()
    # 当前服务端口
    port = get_server_port()
    # 所有可用ip
    ipv4 = URL.get_all_ip()
    # ---------------------------------- 日志打印 ----------------------------------
    # 耗时
    take_time = int((time.time() - start) * 1000).__str__() + "ms\n\n"
    # 可用URL
    if URL.is_zero_ip(host):
        tip = "\n".join([URL(i, port).__str__() for i in ipv4])
    else:
        tip = URL(host, port).__str__()
    tip = tip + "\n"
    swl.info(f"SwanLab Experiment Dashboard ready in " + FONT.bold(take_time) + tip)

    # ---------------------------------- 启动服务 ----------------------------------
    # 使用 uvicorn 启动 FastAPI 应用，关闭原生日志
    # 使用try expcept捕获退出，涉及端口占用等
    try:
        uvicorn.run(app, host=host, port=port, log_level="critical")
    except SystemExit as e:
        code = e.code
        if code == 1:
            critical = "Error while attempting to bind on address ({}, {}): address already in use".format(host, port)
            swl.critical(critical)
        else:
            swl.critical("Unhandled Exit Code: {}".format(code))


if __name__ == "__main__":
    cli()
