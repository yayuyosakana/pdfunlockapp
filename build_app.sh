#!/bin/bash

# PDF Unlock App - macOS Application Builder
# Mac M4 (Apple Silicon)用

APP="dist/PDF Unlock.app"

echo "🚀 PDF Unlock App - macOSアプリケーションをビルドします"
echo "================================================"

# ビルドに使う Python の確認（他のMacでも動くアプリにするため）
FRAMEWORK_PREFIX=$(python -c "import sysconfig; print(sysconfig.get_config_var('PYTHONFRAMEWORKPREFIX') or '')")
if [ "$FRAMEWORK_PREFIX" != "/Library/Frameworks" ]; then
    echo ""
    echo "⚠️  python.org 版以外の Python でビルドしようとしています: $FRAMEWORK_PREFIX"
    echo "   Homebrew 等の Python だと、ビルドしたMac以外で起動できないことがあります。"
    echo "   配布用には https://www.python.org/downloads/macos/ の Python 3.12"
    echo "   (universal2 インストーラ) で venv を作ってビルドするのがおすすめです。"
    echo ""
fi

# クリーンアップ
echo "📦 古いビルドをクリーンアップ中..."
rm -rf build dist

# アプリケーションをビルド
echo "🔨 macOSアプリケーションをビルド中..."
python setup.py py2app

if [ ! -d "$APP" ]; then
    echo ""
    echo "❌ ビルドに失敗しました"
    echo "エラーログを確認してください"
    exit 1
fi

echo ""
echo "🔏 アプリに署名中..."
codesign --force --deep --sign - "$APP"

# 起動テスト：アプリ内の Python で依存ライブラリが読み込めるか確認
echo ""
echo "🧪 起動テスト中..."
if ! "$APP/Contents/MacOS/PDF Unlock" --selftest; then
    echo ""
    echo "❌ 起動テストに失敗しました（このままだと 'Launch error' になります）"
    echo "   上のエラー内容を確認してください"
    exit 1
fi

# 動作するCPUとmacOSバージョンを表示（配布先のMacで動くかの目安）
ARCHS=$(lipo -archs "$APP/Contents/MacOS/PDF Unlock" 2>/dev/null)
MIN_OS=$(find "$APP" -type f \( -name "*.so" -o -name "*.dylib" -o -perm -u+x \) -print0 \
    | xargs -0 otool -l 2>/dev/null \
    | awk '/LC_BUILD_VERSION/{f=1} f && $1=="minos"{print $2; f=0} /LC_VERSION_MIN_MACOSX/{g=1} g && $1=="version"{print $2; g=0}' \
    | sort -V | tail -1)
while IFS= read -r -d '' f; do
    for a in $ARCHS; do
        if ! lipo -archs "$f" 2>/dev/null | grep -qw "$a"; then
            echo "⚠️  $(basename "$f") が $a に対応していません（$a のMacでは一部機能が動かない可能性）"
        fi
    done
done < <(find "$APP" -type f \( -name "*.so" -o -name "*.dylib" \) -print0)

echo ""
echo "✅ ビルド成功！"
echo "================================================"
echo "📱 アプリケーション: $APP"
echo "💻 対応CPU: ${ARCHS:-不明}  (arm64 = Apple Silicon, x86_64 = Intel)"
echo "🍎 必要な macOS: ${MIN_OS:-不明} 以降"
echo ""
echo "🎯 使い方:"
echo "  1. Finderで dist フォルダを開く"
echo "  2. 'PDF Unlock.app' をアプリケーションフォルダにドラッグ"
echo "  3. ダブルクリックして起動"
echo ""
echo "📦 他のMacに渡す場合は、次のコマンドで zip にしてください（署名が壊れません）:"
echo "  ditto -c -k --keepParent \"$APP\" \"dist/PDF Unlock.app.zip\""
echo ""
echo "📂 distフォルダを開きますか? (Finderで開く)"
open dist
