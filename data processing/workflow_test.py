#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
工作流测试脚本 - 显示将要执行的步骤，但不实际执行
1. 清理旧文件 (cleanup_utils.py)
2. 抓取链接 (link_scraper.py)
3. 过滤链接 (link_filter.py)
4. 抓取内容 (content_scraper.py)

使用方法:
- 查看所有步骤: python workflow_test.py
- 从特定步骤开始: python workflow_test.py [步骤编号]
  例如: python workflow_test.py 2  # 从第2步"抓取链接"开始
"""

import os
import sys

def main():
    """主函数，显示工作流步骤"""
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
                print(f"无效的步骤编号: {start_step}，应该在1到{len(scripts)}之间")
                print(f"有效步骤范围: 1-{len(scripts)}")
                for idx, (script, desc) in enumerate(scripts, 1):
                    print(f"{idx}. {desc} ({script})")
                return False
        except ValueError:
            print(f"无效的命令行参数: {sys.argv[1]}，应该是一个数字")
            return False
    
    scripts_to_run = scripts[start_step-1:]
    
    print(f"工作流将从步骤 {start_step} 开始执行以下步骤:")
    
    # 显示将要执行的步骤
    for idx, (script_name, description) in enumerate(scripts_to_run, start_step):
        if os.path.exists(script_name):
            print(f"步骤 {idx}: {description} ({script_name}) - 文件存在")
        else:
            print(f"步骤 {idx}: {description} ({script_name}) - 文件不存在!")
    
    print("\n要执行完整工作流，请运行: python workflow.py")
    print("要从特定步骤开始，请运行: python workflow.py [步骤编号]")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 