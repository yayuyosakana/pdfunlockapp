# PDF Unlock App

macOS 用のシンプルな PDF ロック解除アプリ

## 特徴

- PDF の印刷・編集・コピー制限（権限パスワード）を解除
- **AES-256 / AES-128 / RC4 の暗号化に対応**（最新の暗号化PDFも解除可能）
- パスワード保護された PDF にも対応（空欄なら自動で試行）
- しおり・注釈・フォームなどの構造を保ったまま解除
- DOCX ファイルを PDF に変換
- 複数ファイルの一括処理に対応（**進捗バー表示・処理中も固まりません**）
- 元のファイルを直接置換（「元のファイルを残す」にチェックすると `名前_unlocked.pdf` として別に保存）
- もともと制限のない PDF は変更せずにスキップ
- Dock のアイコンへのドロップや「このアプリで開く」でもファイルを渡せます
- 処理後は「Finder で表示」ボタンで出力ファイルをすぐ確認できます
- 置換前に出力を検証するため、失敗しても元ファイルは失われません

## インストール

1. [Releases](../../releases)から`PDF Unlock.app.zip`をダウンロード
2. 解凍して`PDF Unlock.app`をアプリケーションフォルダへ
3. 初回起動時は右クリック →「開く」で実行（macOS 15 以降は下の「トラブルシューティング」参照）

## 使い方

1. アプリを起動
2. 「ファイルを選択」ボタンでファイル（PDF または DOCX）を選択（複数選択可）
   - Dock のアイコンにドロップ、または右クリック →「このアプリで開く」でもOK
3. パスワードがあれば入力（なければ空欄）
4. 元のファイルを残したい場合は「元のファイルを残す」にチェック
5. 「ロック解除 / 変換」ボタンをクリック（または Enter キー）

完了すると元の PDF が制限なしの状態に置き換わります（チェック時は `名前_unlocked.pdf` を作成）。
DOCX は同じ場所に PDF を作成し、同名の PDF がある場合は `名前 (2).pdf` として保存します。

## ソースからビルド

他のMacでも動くアプリにするため、[python.org](https://www.python.org/downloads/macos/) の Python 3.12（macOS 64-bit universal2 installer）でビルドしてください。
Homebrew の Python でビルドすると、ビルドしたMac以外で「Launch error」になることがあります。

```bash
git clone https://github.com/yayuyosakana/pdfunlockapp.git
cd pdfunlockapp
/usr/local/bin/python3.12 -m venv venv   # python.org 版の Python
source venv/bin/activate
pip install -r requirements.txt
./build_app.sh
```

`build_app.sh` はビルド後に起動テストを行い、対応CPU（Apple Silicon / Intel）と必要な macOS バージョンを表示します。
他のMacに渡すときは `ditto -c -k --keepParent "dist/PDF Unlock.app" "dist/PDF Unlock.app.zip"` で zip にしてください。

## トラブルシューティング

**「開発元が未確認」と表示される**  
→ 右クリック →「開く」で起動してください。macOS 15 以降では「システム設定」→「プライバシーとセキュリティ」→「このまま開く」を押してください

**「Launch error」と表示される**  
→ 起動できなかった理由が `~/Library/Logs/PDF Unlock.log` に記録されます。python.org 版の Python で作り直すと直ることが多いです

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
