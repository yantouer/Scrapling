# Scrapling Docker部署指南

本指南将帮助您在Docker环境中部署和使用Scrapling项目，实现环境隔离和方便的管理。

## 准备工作

1. 确保您的服务器已安装Docker和Docker Compose
2. 克隆项目代码到服务器

```bash
git clone https://github.com/D4Vinci/Scrapling.git
cd Scrapling
```

## 部署步骤

### 1. 构建Docker镜像

```bash
docker-compose build
```

这将构建一个包含Scrapling及其所有依赖的Docker镜像，包括浏览器支持。

### 2. 启动容器

```bash
docker-compose up -d
```

容器将在后台运行，并映射以下资源：
- 端口：8000（MCP服务器）
- 卷：
  - `./crawl_data`：持久化爬取数据
  - `./results`：持久化爬取结果

### 3. 执行爬虫

#### 方法1：使用默认配置爬取示例网站

```bash
docker exec -it scrapling python docker_crawler.py
```

#### 方法2：使用环境变量配置爬取参数

```bash
docker exec -it scrapling bash -c "START_URL=https://example.com MAX_DEPTH=5 python docker_crawler.py"
```

## 环境变量配置

您可以通过环境变量配置爬虫行为：

| 环境变量 | 默认值 | 描述 |
|---------|-------|------|
| START_URL | http://quotes.toscrape.com/ | 要爬取的起始URL |
| MAX_DEPTH | 3 | 最大爬取深度 |
| CONCURRENT_REQUESTS | 5 | 并发请求数 |
| DOWNLOAD_DELAY | 0.5 | 下载延迟（秒） |

## 管理容器

### 查看容器状态

```bash
docker-compose ps
```

### 查看容器日志

```bash
docker-compose logs -f scrapling
```

### 停止容器

```bash
docker-compose down
```

### 进入容器交互模式

```bash
docker exec -it scrapling bash
```

## 使用Scrapling命令行工具

您可以直接在Docker容器中使用Scrapling的命令行工具：

```bash
# 启动交互式shell
docker exec -it scrapling scrapling shell

# 提取网页内容
docker exec -it scrapling scrapling extract get 'https://example.com' content.md
```

## 自定义爬虫

您可以创建自己的爬虫脚本，然后在Docker容器中运行：

1. 创建自定义爬虫脚本 `my_crawler.py`
2. 将脚本复制到项目目录
3. 在容器中运行：

```bash
docker exec -it scrapling python my_crawler.py
```

## 持久化数据

- 爬取数据存储在 `./crawl_data` 目录
- 爬取结果存储在 `./results` 目录

这些目录会被持久化到宿主机，即使容器被删除，数据也不会丢失。

## 性能优化

1. **调整并发数**：根据服务器资源调整 `CONCURRENT_REQUESTS` 环境变量
2. **设置合理的延迟**：根据目标网站的承受能力调整 `DOWNLOAD_DELAY`
3. **限制爬取深度**：对于大型网站，适当减小 `MAX_DEPTH` 以避免内存占用过高

## 故障排除

### 容器启动失败

检查Docker日志：

```bash
docker-compose logs scrapling
```

### 爬取速度慢

- 检查网络连接
- 调整 `CONCURRENT_REQUESTS` 和 `DOWNLOAD_DELAY` 参数
- 对于大型网站，考虑增加服务器资源

### 内存占用过高

- 减小 `MAX_DEPTH`
- 减小 `CONCURRENT_REQUESTS`
- 增加服务器内存

## 示例：爬取整个网站

以下命令将爬取 example.com 网站，最大深度为5：

```bash
docker exec -it scrapling bash -c "START_URL=https://example.com MAX_DEPTH=5 CONCURRENT_REQUESTS=3 python docker_crawler.py"
```

爬取完成后，结果将保存到 `./results` 目录中。

## 版本信息

当前Scrapling版本：0.4.2

## 总结

通过Docker部署Scrapling，您可以：

1. 实现环境隔离，避免依赖冲突
2. 方便地管理和扩展爬虫功能
3. 持久化爬取数据和结果
4. 通过环境变量灵活配置爬取参数

这种部署方式特别适合在服务器上长期运行爬虫任务，或者在多个项目之间共享爬虫资源。
