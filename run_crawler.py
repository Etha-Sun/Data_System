#!/usr/bin/env python
"""
运行爬虫脚本
"""
import os
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 切换到crawler目录（Scrapy项目目录）
crawler_dir = project_root / 'crawler'
os.chdir(crawler_dir)

# 运行Scrapy爬虫
from scrapy.cmdline import execute

if __name__ == '__main__':
    # 设置Scrapy项目设置
    os.environ.setdefault('SCRAPY_SETTINGS_MODULE', 'crawler.settings')
    execute(['scrapy', 'crawl', 'ustc_spider'])


