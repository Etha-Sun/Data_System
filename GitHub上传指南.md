# GitHub上传指南

## 一、本地Git仓库已准备就绪

项目已经初始化了Git仓库并创建了初始提交。

## 二、上传到GitHub步骤

### 方法1：使用GitHub CLI（推荐）

如果你安装了GitHub CLI：

```bash
# 在GitHub上创建仓库（会自动设置远程）
gh repo create DataSystem --public --source=. --remote=origin --push
```

### 方法2：使用Git命令（传统方法）

#### 步骤1：在GitHub上创建新仓库

1. 登录GitHub
2. 点击右上角的 "+" 号，选择 "New repository"
3. 填写仓库信息：
   - Repository name: `DataSystem` 或 `ustc-search-engine`
   - Description: `中科大校内文件搜索引擎 - 基于HBase的分布式文件搜索系统`
   - 选择 Public 或 Private
   - **不要**勾选 "Initialize this repository with a README"
4. 点击 "Create repository"

#### 步骤2：添加远程仓库并推送

```bash
# 添加远程仓库（将YOUR_USERNAME替换为你的GitHub用户名）
git remote add origin https://github.com/YOUR_USERNAME/DataSystem.git

# 或者使用SSH（如果你配置了SSH密钥）
# git remote add origin git@github.com:YOUR_USERNAME/DataSystem.git

# 推送代码到GitHub
git branch -M main
git push -u origin main
```

#### 步骤3：验证

访问 `https://github.com/YOUR_USERNAME/DataSystem` 查看你的代码。

## 三、后续更新代码

```bash
# 添加更改的文件
git add .

# 提交更改
git commit -m "描述你的更改"

# 推送到GitHub
git push
```

## 四、注意事项

1. **敏感信息**：确保没有提交敏感信息（API密钥、密码等）
2. **大文件**：data/目录已在.gitignore中，不会被提交
3. **依赖**：requirements.txt已包含，其他人可以通过pip安装
4. **文档**：README.md等文档已包含，方便他人理解项目

## 五、项目信息建议

在GitHub仓库页面，你可以添加以下信息：

### Topics（标签）
- `scrapy`
- `hbase`
- `search-engine`
- `flask`
- `chinese-nlp`
- `ustc`

### Description（描述）
```
中科大校内文件搜索引擎 - 基于HBase的分布式文件搜索系统

从科大网站爬取文件数据，存储在HBase中，实现校内文件搜索功能。
使用Scrapy爬虫、HBase存储、自建倒排索引和BM25算法。
```

## 六、许可证

如果需要，可以添加LICENSE文件。建议使用MIT License或Apache 2.0。

