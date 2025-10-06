#!/bin/bash

# PDF Unlock App - macOS Application Builder
# Mac M4 (Apple Silicon)用

echo "🚀 PDF Unlock App - macOSアプリケーションをビルドします"
echo "================================================"

# クリーンアップ
echo "📦 古いビルドをクリーンアップ中..."
rm -rf build dist

# アプリケーションをビルド
echo "🔨 macOSアプリケーションをビルド中..."
python setup.py py2app

# ビルド結果を確認
if [ -d "dist/PDF Unlock.app" ]; then
    echo ""
    echo "✅ ビルド成功！"
    echo "================================================"
    echo "📱 アプリケーション: dist/PDF Unlock.app"
    echo ""
    echo "🎯 使い方:"
    echo "  1. Finderで dist フォルダを開く"
    echo "  2. 'PDF Unlock.app' をアプリケーションフォルダにドラッグ"
    echo "  3. ダブルクリックして起動"
    echo ""
    echo "📂 distフォルダを開きますか? (Finderで開く)"
    open dist
else
    echo ""
    echo "❌ ビルドに失敗しました"
    echo "エラーログを確認してください"
    exit 1
fi
