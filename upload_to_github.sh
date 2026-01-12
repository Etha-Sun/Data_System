#!/bin/bash
# GitHub上传脚本

echo "=========================================="
echo "GitHub上传助手"
echo "=========================================="
echo ""

# 检查是否已设置远程仓库
if git remote | grep -q "origin"; then
    echo "✓ 远程仓库已配置"
    git remote -v
    echo ""
    read -p "是否直接推送到GitHub? (y/n): " push_now
    if [ "$push_now" = "y" ]; then
        git push -u origin main
        exit 0
    fi
fi

echo "请选择操作："
echo "1. 设置远程仓库（HTTPS）"
echo "2. 设置远程仓库（SSH）"
echo "3. 直接推送（如果已设置远程）"
echo ""
read -p "请输入选项 (1-3): " choice

case $choice in
    1)
        read -p "请输入你的GitHub用户名: " username
        read -p "请输入仓库名称 (默认: DataSystem): " repo_name
        repo_name=${repo_name:-DataSystem}
        
        echo ""
        echo "设置远程仓库: https://github.com/$username/$repo_name.git"
        git remote add origin "https://github.com/$username/$repo_name.git" 2>/dev/null || \
        git remote set-url origin "https://github.com/$username/$repo_name.git"
        
        echo ""
        echo "推送代码到GitHub..."
        git branch -M main
        git push -u origin main
        
        if [ $? -eq 0 ]; then
            echo ""
            echo "✓ 上传成功！"
            echo "访问: https://github.com/$username/$repo_name"
        else
            echo ""
            echo "✗ 上传失败，请检查："
            echo "  1. 是否在GitHub上创建了仓库: $repo_name"
            echo "  2. 是否有推送权限"
            echo "  3. 网络连接是否正常"
        fi
        ;;
    2)
        read -p "请输入你的GitHub用户名: " username
        read -p "请输入仓库名称 (默认: DataSystem): " repo_name
        repo_name=${repo_name:-DataSystem}
        
        echo ""
        echo "设置远程仓库: git@github.com:$username/$repo_name.git"
        git remote add origin "git@github.com:$username/$repo_name.git" 2>/dev/null || \
        git remote set-url origin "git@github.com:$username/$repo_name.git"
        
        echo ""
        echo "推送代码到GitHub..."
        git branch -M main
        git push -u origin main
        
        if [ $? -eq 0 ]; then
            echo ""
            echo "✓ 上传成功！"
            echo "访问: https://github.com/$username/$repo_name"
        else
            echo ""
            echo "✗ 上传失败，请检查："
            echo "  1. 是否配置了SSH密钥"
            echo "  2. 是否在GitHub上创建了仓库: $repo_name"
            echo "  3. 是否有推送权限"
        fi
        ;;
    3)
        echo "推送代码到GitHub..."
        git branch -M main
        git push -u origin main
        
        if [ $? -eq 0 ]; then
            echo ""
            echo "✓ 上传成功！"
        else
            echo ""
            echo "✗ 上传失败，请先设置远程仓库"
        fi
        ;;
    *)
        echo "无效选项"
        exit 1
        ;;
esac

