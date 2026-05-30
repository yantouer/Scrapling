"""
Docker环境中的网站爬虫脚本

使用方法：
1. 构建Docker镜像: docker-compose build
2. 运行容器: docker-compose up -d
3. 执行爬虫: docker exec -it scrapling python docker_crawler.py

环境变量配置：
- START_URL: 要爬取的起始URL（默认: http://quotes.toscrape.com/）
- MAX_DEPTH: 最大爬取深度（默认: 3）
- CONCURRENT_REQUESTS: 并发请求数（默认: 5）
- DOWNLOAD_DELAY: 下载延迟（默认: 0.5）
"""

import os
from scrapling.spiders import Spider, Response
from urllib.parse import urlparse
import time

class DockerCrawler(Spider):
    """Docker环境中的网站爬虫"""
    name = "docker_crawler"
    # 从环境变量读取配置
    start_urls = [os.environ.get('START_URL', 'http://quotes.toscrape.com/')]
    # 并发请求数
    concurrent_requests = int(os.environ.get('CONCURRENT_REQUESTS', '5'))
    # 下载延迟
    download_delay = float(os.environ.get('DOWNLOAD_DELAY', '0.5'))
    # 爬取深度限制
    max_depth = int(os.environ.get('MAX_DEPTH', '3'))
    # 启用检查点（支持暂停/恢复）
    crawldir = "./crawl_data"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.visited_urls = set()
        self.start_netloc = urlparse(self.start_urls[0]).netloc
        self.start_time = time.time()
    
    def configure_sessions(self, manager):
        from scrapling.fetchers import FetcherSession
        
        # 添加普通HTTP会话
        manager.add("fast", FetcherSession(impersonate="chrome"))
    
    async def parse(self, response: Response):
        """解析页面内容"""
        # 检查是否已经访问过
        if response.url in self.visited_urls:
            return
        self.visited_urls.add(response.url)
        
        # 检查深度
        current_depth = response.meta.get('depth', 0)
        if current_depth > self.max_depth:
            return
        
        # 提取页面信息
        page_data = {
            "url": response.url,
            "title": response.css('title::text').get(),
            "depth": current_depth,
            "timestamp": time.time()
        }
        
        # 输出进度
        elapsed_time = time.time() - self.start_time
        print(f"[{current_depth}] [{elapsed_time:.2f}s] 爬取: {response.url}")
        
        # 存储结果
        yield page_data
        
        # 提取并跟进链接
        for link in response.css('a::attr(href)').getall():
            absolute_url = response.urljoin(link)
            # 只爬取同一域名下的链接
            if urlparse(absolute_url).netloc == self.start_netloc:
                # 递归爬取，增加深度
                yield response.follow(
                    absolute_url, 
                    callback=self.parse,
                    meta={'depth': current_depth + 1}
                )

if __name__ == "__main__":
    print("开始爬取网站...")
    print(f"目标网站: {DockerCrawler.start_urls[0]}")
    print(f"最大深度: {DockerCrawler.max_depth}")
    print(f"并发请求: {DockerCrawler.concurrent_requests}")
    print(f"下载延迟: {DockerCrawler.download_delay}秒")
    print("=" * 60)
    
    # 创建并启动爬虫
    spider = DockerCrawler()
    result = spider.start()
    
    # 保存结果
    elapsed_time = time.time() - spider.start_time
    print("=" * 60)
    print(f"爬取完成！")
    print(f"总耗时: {elapsed_time:.2f}秒")
    print(f"共爬取 {len(result.items)} 个页面")
    
    # 确保results目录存在
    os.makedirs('./results', exist_ok=True)
    
    # 保存结果到JSON文件
    output_file = f'./results/crawl_results_{int(time.time())}.json'
    result.items.to_json(output_file)
    print(f"结果已保存到 {output_file}")
    print("\n提示：可以通过环境变量配置爬虫参数")
