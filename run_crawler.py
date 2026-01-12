#!/usr/bin/env python
"""
运行爬虫脚本
"""
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def run_spider():
    """
    直接运行爬虫，不使用scrapy命令
    """
    from scrapy.crawler import CrawlerProcess
    from scrapy.utils.project import get_project_settings
    from crawler.spiders.ustc_spider import UstcSpider

    # 获取爬虫设置
    settings = get_project_settings()
    settings.set('SCRAPY_SETTINGS_MODULE', 'crawler.settings')

    # 创建爬虫进程
    process = CrawlerProcess(settings)

    # 添加爬虫
    process.crawl(UstcSpider)

    # 启动爬虫
    print("=" * 50)
    print("开始运行爬虫...")
    print("=" * 50)

    process.start()

if __name__ == '__main__':
    run_spider()


