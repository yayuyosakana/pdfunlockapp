# PDF Unlock App

macOS 用のシンプルな PDF ロック解除アプリ

## 特徴

- PDF の印刷・編集・コピー制限を解除
- DOCX ファイルを PDF に変換して保存
- 複数ファイルの一括処理に対応
- Browse ボタンでファイルを選択するだけの簡単操作
- パスワード保護された PDF にも対応
- 元のファイルを直接置換（新しいファイルは作りません）

## インストール

1. [Releases](../../releases)から`PDF Unlock.app.zip`をダウンロード
2. 解凍して`PDF Unlock.app`をアプリケーションフォルダへ
3. 初回起動時は右クリック →「開く」で実行

## 使い方

1. アプリを起動
2. Browse ボタンでファイル（PDF または DOCX）を選択（複数選択可）
3. パスワードがあれば入力（なければ空欄）
4. ロック解除ボタンをクリック（または Enter キー）

完了すると元の PDF が制限なしの状態に置き換わります。

## ソースからビルド

```bash
git clone https://github.com/yayuyosakana/pdfunlockapp.git
cd pdfunlockapp
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
./build_app.sh
```

## トラブルシューティング

**「開発元が未確認」と表示される**  
→ 右クリック →「開く」で起動してください

**パスワードエラーが出る**  
→ パスワードを再確認してください

## 技術スタック

- Python 3.12 + Tkinter
- PyPDF2（PDF 処理）
- docx2pdf（DOCX 変換）
- pycryptodome（AES 暗号化対応）
- py2app（macOS アプリ化）

## ライセンス

MIT License

---

**注意**: 合法的に所有している PDF ファイルのみに使用してください。
