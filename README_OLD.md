# PDF Unlock App

PDF ファイルの編集制限・閲覧制限を解除するシンプルなデスクトップアプリケーションです。

## 機能

- **ドラッグ&ドロップ対応**: PDF ファイルをアプリにドラッグ&ドロップするだけで選択可能
- **パスワード対応**: パスワードで保護された PDF にも対応
- **制限解除**: 編集制限、閲覧制限などの PDF 保護を解除
- **簡単操作**: 直感的な GUI で誰でも簡単に使用可能
- **macOS ネイティブアプリ**: Mac M4 (Apple Silicon) 完全対応

## macOS アプリケーションとして使用（推奨）

### 🚀 クイックスタート

```bash
# 1. 依存パッケージをインストール
pip install -r requirements.txt

# 2. （オプション）アイコンを作成
pip install Pillow
python create_icon.py

# 3. macOS アプリをビルド
chmod +x build_app.sh
./build_app.sh
```

ビルドが完了すると、`dist/PDF Unlock.app` が作成されます。
これを「アプリケーション」フォルダにドラッグ&ドロップすれば、通常の Mac アプリとして使用できます！

### 初回起動時の注意

macOS のセキュリティ機能により、初回起動時に警告が出る場合があります：

1. 右クリック（または Control + クリック）でアプリを選択
2. 「開く」を選択
3. 確認ダイアログで「開く」をクリック

## Python スクリプトとして使用

### インストール

### 必要な環境

- Python 3.7 以上
- macOS, Windows, Linux に対応

### セットアップ

1. リポジトリをクローンまたはダウンロード

```bash
cd /Users/yu/projects/pdfunlockapp
```

2. 必要なパッケージをインストール

```bash
pip install -r requirements.txt
```

## 使い方

1. アプリケーションを起動

```bash
python pdf_unlock_app.py
```

2. PDF ファイルを選択

   - ドラッグ&ドロップで追加、または
   - 画面をクリックしてファイル選択ダイアログから選択

3. パスワードを入力（必要な場合のみ）

   - パスワードで保護されている PDF の場合は、パスワードを入力
   - 保護されていない場合は空欄のままで OK

4. 「PDF のロックを解除」ボタンをクリック

5. 解除された PDF は、元のファイルと同じフォルダに `_unlocked.pdf` という名前で保存されます

## 注意事項

- このツールは、正当な理由で PDF の制限を解除する目的でのみ使用してください
- 著作権やライセンスを侵害する使用は避けてください
- パスワードで保護された PDF を解除するには、正しいパスワードが必要です

## トラブルシューティング

### tkinterdnd2 のインストールでエラーが出る場合

macOS の場合:

```bash
brew install python-tk
pip install tkinterdnd2
```

Windows の場合:

```bash
pip install tkinterdnd2
```

### 「PDF が破損しています」というエラーが出る場合

- PDF ファイルが破損している可能性があります
- 別の PDF ファイルで試してみてください

### macOS アプリがビルドできない場合

```bash
# Xcodeコマンドラインツールをインストール
xcode-select --install

# 再度ビルド
./build_app.sh
```

## 技術仕様

- **対応 OS**: macOS (Apple Silicon M1/M2/M3/M4 完全対応)
- **フレームワーク**: Tkinter (Python 標準 GUI)
- **PDF 処理**: PyPDF2
- **パッケージング**: py2app

## ライセンス

MIT License
