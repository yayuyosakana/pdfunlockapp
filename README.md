# PDF Unlock App 🔓# PDF Unlock App 🔓



macOS用のシンプルなPDFロック解除アプリケーションmacOS用のモダンなPDFロック解除アプリケーション



<div align="center"><div align="center">

  <img src="app_icon.png" alt="PDF Unlock App Icon" width="200"/>  <img src="app_icon.png" alt="PDF Unlock App Icon" width="200"/>

</div></div>



## ✨ 機能## ✨ 機能



- 📄 **PDFパスワード解除**: 編集制限・閲覧制限を完全解除- 📄 **PDFパスワード解除**: 編集制限・閲覧制限を完全解除

- 🎯 **簡単操作**: Browseボタンでファイルを選択するだけ- 🎯 **ドラッグ&ドロップ対応**: 直感的な操作で簡単にファイルを選択

- ⌨️ **Enterキー対応**: パスワード入力後、Enterキーで即座に実行- ⌨️ **Enterキー対応**: パスワード入力後、Enterキーで即座に実行

- 🔄 **元ファイル置換**: 新しいファイルを作らず、元のPDFを直接置き換え- 🔄 **元ファイル置換**: 新しいファイルを作らず、元のPDFを直接置き換え

- 🔐 **AES暗号化対応**: 高度な暗号化PDFにも対応（pycryptodome使用）- 🔐 **AES暗号化対応**: 高度な暗号化PDFにも対応（pycryptodome使用）

- 🎨 **モダンなUI**: 洗練されたシンプルなデザイン- 🎨 **モダンなUI**: 洗練されたデザインと視覚的フィードバック

- 🚀 **Apple Silicon最適化**: Mac M1/M2/M3/M4でネイティブ動作- 🚀 **Apple Silicon最適化**: Mac M1/M2/M3/M4でネイティブ動作



## 📸 スクリーンショット## 📸 スクリーンショット



アプリを起動すると、シンプルなインターフェースでPDFファイルを選択できます。パスワードを入力してEnterキーを押すだけで即座にロック解除が完了します。アプリを起動すると、大きなドラッグ&ドロップエリアが表示されます。PDFファイルをドロップすると、エリアが緑色に変わり、パスワード入力フィールドに自動フォーカスします。



## 🔧 必要要件## 🔧 必要要件



- macOS 10.15以降- macOS 10.15以降

- Python 3.12以降（ビルドする場合）- Python 3.12以降（ビルドする場合）



## 💾 インストール方法## 💾 インストール方法



### 方法1: リリースからダウンロード（推奨）### 方法1: リリースからダウンロード（推奨）



1. [Releases](../../releases)ページから最新版の`PDF Unlock.app.zip`をダウンロード1. [Releases](../../releases)ページから最新版の`PDF Unlock.app.zip`をダウンロード

2. ZIPファイルを解凍2. ZIPファイルを解凍

3. `PDF Unlock.app`をアプリケーションフォルダにドラッグ3. `PDF Unlock.app`をアプリケーションフォルダにドラッグ

4. 初回起動時は右クリック→「開く」で実行4. 初回起動時は右クリック→「開く」で実行



### 方法2: ソースからビルド### 方法2: ソースからビルド



```bash```bash

# リポジトリをクローン# リポジトリをクローン

git clone https://github.com/yayuyosakana/pdfunlockapp.gitgit clone https://github.com/yourusername/pdfunlockapp.git

cd pdfunlockappcd pdfunlockapp



# 仮想環境を作成# 仮想環境を作成

python3 -m venv venvpython3 -m venv venv

source venv/bin/activatesource venv/bin/activate



# 依存関係をインストール# 依存関係をインストール

pip install -r requirements.txtpip install -r requirements.txt



# アイコンを生成# アイコンを生成

python create_icon.pypython create_icon.py



# アプリをビルド# アプリをビルド

python setup.py py2apppython setup.py py2app



# ビルドされたアプリは dist/PDF Unlock.app に作成されます# ビルドされたアプリは dist/PDF Unlock.app に作成されます

``````



または、ビルドスクリプトを使用:または、ビルドスクリプトを使用:



```bash```bash

chmod +x build_app.shchmod +x build_app.sh

./build_app.sh./build_app.sh

``````



## 📖 使い方## 📖 使い方



1. **アプリを起動**: `PDF Unlock.app`をダブルクリック1. **アプリを起動**: `PDF Unlock.app`をダブルクリック

2. **PDFを選択**: 2. **PDFを選択**: 

   - 「📄 PDFファイルを選択」ボタンをクリック   - ドラッグ&ドロップエリアにPDFファイルをドロップ

   - ファイル選択ダイアログでPDFを選択   - または「Browse」ボタンでファイルを選択

3. **パスワード入力**: パスワード保護されている場合は入力（なければ空欄でOK）3. **パスワード入力**: パスワード保護されている場合は入力（なければ空欄でOK）

4. **アンロック実行**: 4. **アンロック実行**: 

   - 「🔓 PDFのロックを解除」ボタンをクリック   - 「Unlock PDF」ボタンをクリック

   - またはEnterキーを押す   - またはEnterキーを押す

5. **完了**: 元のPDFファイルが制限なしの状態に置き換えられます5. **完了**: 元のPDFファイルが制限なしの状態に置き換えられます



## 🛠️ 技術スタック## 🛠️ 技術スタック



- **言語**: Python 3.12- **言語**: Python 3.12

- **GUI**: Tkinter（標準ライブラリ）- **GUI**: Tkinter（標準ライブラリ）

- **PDF処理**: PyPDF2- **PDF処理**: PyPDF2

- **暗号化**: pycryptodome（AES対応）- **暗号化**: pycryptodome（AES対応）

- **パッケージング**: py2app（macOS）- **パッケージング**: py2app（macOS）

- **アイコン生成**: Pillow- **アイコン生成**: Pillow



## 📦 依存関係## 📦 依存関係



``````

PyPDF2==3.0.1PyPDF2==3.0.1

pycryptodome==3.21.0pycryptodome==3.21.0

py2app==0.28.8py2app==0.28.8

Pillow==11.3.0Pillow==11.3.0

``````



## 🏗️ プロジェクト構成## 🏗️ プロジェクト構成



``````

pdfunlockapp/pdfunlockapp/

├── pdf_unlock_app.py      # メインアプリケーション├── pdf_unlock_app.py    # メインアプリケーション

├── setup.py               # py2appビルド設定├── setup.py             # py2app設定

├── build_app.sh           # ビルドスクリプト├── create_icon.py       # アイコン生成スクリプト

├── create_icon.py         # アイコン生成スクリプト├── requirements.txt     # Python依存関係

├── app_icon.icns          # macOSアイコン├── build_app.sh         # ビルド自動化スクリプト

├── app_icon.png           # PNGアイコン├── app_icon.png         # アイコン画像（PNG）

├── requirements.txt       # Python依存関係├── app_icon.icns        # アイコン画像（macOS形式）

├── README.md              # このファイル└── README.md            # このファイル

└── LICENSE                # ライセンス```

```

## ⚠️ 注意事項

## 🔐 セキュリティ

- このアプリは**既知のパスワード**を使ってPDFのロックを解除するためのものです

- パスワードはメモリ上でのみ処理され、保存されません- パスワードクラッキングや不正アクセスには使用できません

- 元のPDFファイルは一時ファイル経由で安全に置換されます- 著作権やライセンスで保護されたPDFの不正な配布は違法です

- AES暗号化されたPDFにも対応（pycryptodome使用）- **自分が権利を持つPDFファイル**にのみ使用してください



## 🐛 トラブルシューティング## 🤝 コントリビューション



### 「開発元が未確認のため開けません」と表示されるプルリクエストは大歓迎です！大きな変更の場合は、まずissueを開いて変更内容を議論してください。



macOSのセキュリティ機能により、初回起動時にこのメッセージが表示される場合があります:1. このリポジトリをフォーク

2. 機能ブランチを作成 (`git checkout -b feature/AmazingFeature`)

1. アプリアイコンを右クリック3. 変更をコミット (`git commit -m 'Add some AmazingFeature'`)

2. 「開く」を選択4. ブランチにプッシュ (`git push origin feature/AmazingFeature`)

3. 確認ダイアログで「開く」をクリック5. プルリクエストを作成



### パスワードが正しいのにエラーになる## 📝 ライセンス



一部のPDFは複雑な暗号化を使用している場合があります。その場合は:MIT License - 詳細は[LICENSE](LICENSE)ファイルをご覧ください



1. パスワードを再確認## 🐛 バグ報告・機能要望

2. 別のPDF編集ソフトでパスワードを確認

バグを見つけた場合や新機能のアイデアがある場合は、[Issues](../../issues)ページで報告してください。

## 📝 ライセンス

## 🙏 謝辞

このプロジェクトはMITライセンスの下で公開されています。詳細は[LICENSE](LICENSE)ファイルを参照してください。

- [PyPDF2](https://github.com/py-pdf/pypdf) - PDF処理ライブラリ

## 🤝 貢献- [pycryptodome](https://github.com/Legrandin/pycryptodome) - 暗号化サポート

- [py2app](https://github.com/ronaldoussoren/py2app) - macOSアプリケーションのパッケージング

プルリクエストを歓迎します！大きな変更の場合は、まずissueを開いて変更内容を議論してください。

---

## 📧 お問い合わせ

Made with ❤️ for macOS

問題や提案がある場合は、[Issues](../../issues)ページでお知らせください。

---

**注意**: このツールは合法的に所有しているPDFファイルのロック解除のみに使用してください。著作権法を遵守し、他人のファイルを無断で解除しないでください。
