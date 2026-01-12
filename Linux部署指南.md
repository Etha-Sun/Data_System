# Linux部署指南

## 📋 环境要求

- **操作系统**: Ubuntu 20.04+ / CentOS 7+ / Debian 10+
- **Python**: 3.8+
- **内存**: 至少2GB
- **磁盘**: 至少5GB可用空间

## 🚀 快速部署

### 1. 克隆项目

```bash
git clone https://github.com/YOUR_USERNAME/DataSystem.git
cd DataSystem
```

### 2. 创建Python环境

```bash
# 使用venv（推荐）
python3 -m venv venv
source venv/bin/activate

# 或者使用conda（如果安装了）
# conda create -n datasystem python=3.10
# conda activate datasystem
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 启动系统

```bash
# 构建索引（如果需要）
python build_index.py

# 启动Web服务
python run_web.py
```

访问: http://localhost:5000

## 🔧 详细配置

### HBase配置（可选）

如果需要使用HBase分布式存储：

#### Ubuntu/Debian:
```bash
# 安装Java
sudo apt update
sudo apt install openjdk-11-jdk

# 下载并安装Hadoop
wget https://downloads.apache.org/hadoop/common/hadoop-3.4.0/hadoop-3.4.0.tar.gz
tar -xzf hadoop-3.4.0.tar.gz
sudo mv hadoop-3.4.0 /usr/local/hadoop

# 下载并安装HBase
wget https://downloads.apache.org/hbase/2.6.0/hbase-2.6.0-bin.tar.gz
tar -xzf hbase-2.6.0-bin.tar.gz
sudo mv hbase-2.6.0 /usr/local/hbase
```

#### 配置环境变量:
```bash
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export HADOOP_HOME=/usr/local/hadoop
export HBASE_HOME=/usr/local/hbase
export PATH=$PATH:$JAVA_HOME/bin:$HADOOP_HOME/bin:$HBASE_HOME/bin
```

### 系统优化

#### 增加文件句柄限制:
```bash
echo "* soft nofile 65536" | sudo tee -a /etc/security/limits.conf
echo "* hard nofile 65536" | sudo tee -a /etc/security/limits.conf
```

#### 内存优化:
```bash
# 增加系统内存（如果内存不足）
sudo sysctl -w vm.max_map_count=262144
```

## 🧪 测试功能

### 运行测试:
```bash
python test_all.py
```

### 测试搜索功能:
```bash
python test_search.py
```

## 📊 性能监控

### 查看系统资源使用:
```bash
# CPU和内存使用
top

# 磁盘使用
df -h

# 网络连接
netstat -tlnp
```

### 应用程序日志:
```bash
# Web服务日志会输出到控制台
# 按Ctrl+C停止服务
```

## 🔄 数据管理

### 重新爬取数据:
```bash
python run_crawler.py
```

### 重新构建索引:
```bash
python build_index.py
```

### 备份数据:
```bash
tar -czf backup_$(date +%Y%m%d).tar.gz data/
```

## 🐛 故障排除

### 常见问题:

#### 1. 端口被占用
```bash
# 查看端口使用
sudo lsof -i :5000

# 杀死进程
sudo kill -9 PID
```

#### 2. 内存不足
```bash
# 查看内存使用
free -h

# 清理缓存
sudo sync; sudo echo 3 > /proc/sys/vm/drop_caches
```

#### 3. Python依赖问题
```bash
# 重新安装依赖
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

#### 4. 编码问题
```bash
# 设置系统编码
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
```

## 📈 扩展配置

### 生产环境部署:

#### 使用Nginx反向代理:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

#### 使用systemd服务:
```bash
# 创建服务文件
sudo nano /etc/systemd/system/datasystem.service
```

```ini
[Unit]
Description=USTC Data Search System
After=network.target

[Service]
User=your_user
WorkingDirectory=/path/to/DataSystem
ExecStart=/path/to/venv/bin/python run_web.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# 启动服务
sudo systemctl start datasystem
sudo systemctl enable datasystem
```

## 📞 技术支持

如果遇到问题，请检查:

1. **Python版本**: `python --version`
2. **依赖安装**: `pip list`
3. **磁盘空间**: `df -h`
4. **内存使用**: `free -h`
5. **日志输出**: 查看控制台输出

项目GitHub: https://github.com/YOUR_USERNAME/DataSystem
