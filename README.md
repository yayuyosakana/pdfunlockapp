# PDF Unlock App

macOS 用のシンプルな PDF ロック解除アプリ

## 特徴

- PDF の印刷・編集・コピー制限（権限パスワード）を解除
- **AES-256 / AES-128 / RC4 の暗号化に対応**（最新の暗号化PDFも解除可能）
- パスワード保護された PDF にも対応（空欄なら自動で試行）
- しおり・注釈・フォームなどの構造を保ったまま解除
- DOCX ファイルを PDF に変換
- 複数ファイルの一括処理に対応（**進捗バー表示・処理中も固まりません**）
- 元のファイルを直接置換（新しいファイルは作りません）
- 置換前に出力を検証するため、失敗しても元ファイルは失われません

## インストール

1. [Releases](../../releases)から`PDF Unlock.app.zip`をダウンロード
2. 解凍して`PDF Unlock.app`をアプリケーションフォルダへ
3. 初回起動時は右クリック →「開く」で実行

## 使い方

1. アプリを起動
2. 「ファイルを選択」ボタンでファイル（PDF または DOCX）を選択（複数選択可）
3. パスワードがあれば入力（なければ空欄）
4. 「ロック解除 / 変換」ボタンをクリック（または Enter キー）

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
→ パスワードを再確認してください（開くのにパスワードが必要なPDFは、正しいパスワードの入力が必要です）

**DOCX 変換に失敗する**  
→ DOCX→PDF 変換には Microsoft Word のインストールが必要です

## 技術スタック

- Python 3.12 + Tkinter
- [pypdf](https://github.com/py-pdf/pypdf)（PDF 処理）
- cryptography（AES 暗号化の復号）
- docx2pdf（DOCX 変換 / 要 Microsoft Word）
- py2app（macOS アプリ化）

## ライセンス

MIT License

---

**注意**: 合法的に所有している PDF ファイルのみに使用してください。
