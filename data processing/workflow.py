#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
工作流脚本 - 依次执行多个爬虫处理步骤
1. 清理旧文件 (cleanup_utils.py)
2. 抓取链接 (link_scraper.py)
3. 过滤链接 (link_filter.py)
4. 抓取内容 (content_scraper.py)

使用方法:
- 完整运行所有步骤: python workflow.py
- 从特定步骤开始: python workflow.py [步骤编号]
  例如: python workflow.py 2  # 从第2步"抓取链接"开始运行
"""

import os
import sys
import time
import subprocess
import logging

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)-8s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("Workflow")

def run_script(script_name, description):
    """运行一个Python脚本并记录结果"""
    logger.info(f"开始执行: {description} ({script_name})")
    start_time = time.time()
    
    try:
        result = subprocess.run(
            [sys.executable, script_name],
            check=True,
            capture_output=True,
            text=True
        )
        
        # 将脚本的输出显示到终端
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
            
        duration = time.time() - start_time
        logger.info(f"成功完成: {description} ({script_name}) - 用时: {duration:.2f}秒")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"执行失败: {description} ({script_name}) - 错误代码: {e.returncode}")
        if e.stdout:
            logger.info(f"标准输出: {e.stdout}")
        if e.stderr:
            logger.error(f"错误输出: {e.stderr}")
        duration = time.time() - start_time
        logger.error(f"执行时间: {duration:.2f}秒")
        return False

def main():
    """主工作流函数"""
    # 定义要执行的脚本和描述
    scripts = [
        ("cleanup_utils.py", "清理旧文件"),
        ("link_scraper.py", "抓取链接"),
        ("link_filter.py", "过滤链接"),
        ("content_scraper.py", "抓取内容")
    ]
    
    # 处理命令行参数，确定从哪一步开始
    start_step = 1
    if len(sys.argv) > 1:
        try:
            start_step = int(sys.argv[1])
            if start_step < 1 or start_step > len(scripts):
                logger.error(f"无效的步骤编号: {start_step}，应该在1到{len(scripts)}之间")
                print(f"有效步骤范围: 1-{len(scripts)}")
                print("1. 清理旧文件 (cleanup_utils.py)")
                print("2. 抓取链接 (link_scraper.py)")
                print("3. 过滤链接 (link_filter.py)")
                print("4. 抓取内容 (content_scraper.py)")
                return False
        except ValueError:
            logger.error(f"无效的命令行参数: {sys.argv[1]}，应该是一个数字")
            return False
    
    scripts_to_run = scripts[start_step-1:]
    
    logger.info(f"开始执行爬虫工作流 (从步骤 {start_step} 开始)")
    start_time = time.time()
    
    # 依次执行每个脚本
    for script_name, description in scripts_to_run:
        if not os.path.exists(script_name):
            logger.error(f"脚本文件不存在: {script_name}")
            return False
            
        success = run_script(script_name, description)
        
        # 如果某个脚本失败，中断工作流
        if not success:
            logger.error(f"工作流中断: {description}失败")
            return False
        
        # 在脚本之间添加短暂暂停
        time.sleep(1)
    
    total_duration = time.time() - start_time
    logger.info(f"工作流程全部完成! 总用时: {total_duration:.2f}秒")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 