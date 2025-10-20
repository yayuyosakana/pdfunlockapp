# PDF Unlock App 🔓# PDF Unlock App 🔓# PDF Unlock App 🔓



macOS用のシンプルなPDFロック解除アプリケーション



<div align="center">macOS用のシンプルなPDFロック解除アプリケーションmacOS用のモダンなPDFロック解除アプリケーション

  <img src="app_icon.png" alt="PDF Unlock App Icon" width="200"/>

</div>



## ✨ 特徴<div align="center"><div align="center">



- 📄 **PDFパスワード解除**: 編集制限・閲覧制限を完全解除  <img src="app_icon.png" alt="PDF Unlock App Icon" width="200"/>  <img src="app_icon.png" alt="PDF Unlock App Icon" width="200"/>

- 🎯 **シンプル操作**: Browseボタンでファイルを選択するだけ

- ⌨️ **Enterキー対応**: パスワード入力後、Enterキーで即座に実行</div></div>

- 🔄 **元ファイル置換**: 新しいファイルを作らず、元のPDFを直接上書き

- 🔐 **AES暗号化対応**: 高度な暗号化PDFにも対応（pycryptodome使用）

- 🎨 **モダンなUI**: 洗練されたシンプルなデザイン

- 🚀 **Apple Silicon最適化**: Mac M1/M2/M3/M4でネイティブ動作## ✨ 機能## ✨ 機能



## 🔧 必要要件



- macOS 10.15以降- 📄 **PDFパスワード解除**: 編集制限・閲覧制限を完全解除- 📄 **PDFパスワード解除**: 編集制限・閲覧制限を完全解除

- Python 3.12以降（ソースからビルドする場合）

- 🎯 **簡単操作**: Browseボタンでファイルを選択するだけ- 🎯 **ドラッグ&ドロップ対応**: 直感的な操作で簡単にファイルを選択

## 💾 インストール方法

- ⌨️ **Enterキー対応**: パスワード入力後、Enterキーで即座に実行- ⌨️ **Enterキー対応**: パスワード入力後、Enterキーで即座に実行

### 方法1: リリースからダウンロード（推奨）

- 🔄 **元ファイル置換**: 新しいファイルを作らず、元のPDFを直接置き換え- 🔄 **元ファイル置換**: 新しいファイルを作らず、元のPDFを直接置き換え

1. [Releases](../../releases)ページから最新版の`PDF Unlock.app.zip`をダウンロード

2. ZIPファイルを解凍- 🔐 **AES暗号化対応**: 高度な暗号化PDFにも対応（pycryptodome使用）- 🔐 **AES暗号化対応**: 高度な暗号化PDFにも対応（pycryptodome使用）

3. `PDF Unlock.app`をアプリケーションフォルダにドラッグ

4. 初回起動時は右クリック→「開く」で実行- 🎨 **モダンなUI**: 洗練されたシンプルなデザイン- 🎨 **モダンなUI**: 洗練されたデザインと視覚的フィードバック



### 方法2: ソースからビルド- 🚀 **Apple Silicon最適化**: Mac M1/M2/M3/M4でネイティブ動作- 🚀 **Apple Silicon最適化**: Mac M1/M2/M3/M4でネイティブ動作



```bash

# リポジトリをクローン

git clone https://github.com/yayuyosakana/pdfunlockapp.git## 📸 スクリーンショット## 📸 スクリーンショット

cd pdfunlockapp



# 仮想環境を作成

python3 -m venv venvアプリを起動すると、シンプルなインターフェースでPDFファイルを選択できます。パスワードを入力してEnterキーを押すだけで即座にロック解除が完了します。アプリを起動すると、大きなドラッグ&ドロップエリアが表示されます。PDFファイルをドロップすると、エリアが緑色に変わり、パスワード入力フィールドに自動フォーカスします。

source venv/bin/activate



# 依存関係をインストール

pip install -r requirements.txt## 🔧 必要要件## 🔧 必要要件



# アプリをビルド（自動的に署名も実行されます）

./build_app.sh

- macOS 10.15以降- macOS 10.15以降

# ビルドされたアプリは dist/PDF Unlock.app に作成されます

```- Python 3.12以降（ビルドする場合）- Python 3.12以降（ビルドする場合）



## 📖 使い方



1. **アプリを起動**: `PDF Unlock.app`をダブルクリック## 💾 インストール方法## 💾 インストール方法

2. **PDFを選択**: 「📄 PDFファイルを選択」ボタンをクリック

3. **パスワード入力**: パスワード保護されている場合は入力（なければ空欄でOK）

4. **アンロック実行**: 

   - 「🔓 PDFのロックを解除」ボタンをクリック### 方法1: リリースからダウンロード（推奨）### 方法1: リリースからダウンロード（推奨）

   - またはEnterキーを押す

5. **完了**: 元のPDFファイルが制限なしの状態に上書きされます



## 🛠️ 技術スタック1. [Releases](../../releases)ページから最新版の`PDF Unlock.app.zip`をダウンロード1. [Releases](../../releases)ページから最新版の`PDF Unlock.app.zip`をダウンロード



- **言語**: Python 3.122. ZIPファイルを解凍2. ZIPファイルを解凍

- **GUI**: Tkinter（標準ライブラリ）

- **PDF処理**: PyPDF23. `PDF Unlock.app`をアプリケーションフォルダにドラッグ3. `PDF Unlock.app`をアプリケーションフォルダにドラッグ

- **暗号化**: pycryptodome（AES対応）

- **パッケージング**: py2app（macOS）4. 初回起動時は右クリック→「開く」で実行4. 初回起動時は右クリック→「開く」で実行

- **アイコン生成**: Pillow



## 📦 依存関係

### 方法2: ソースからビルド### 方法2: ソースからビルド

```

PyPDF2==3.0.1

pycryptodome==3.21.0

py2app==0.28.8```bash```bash

Pillow==11.3.0

```# リポジトリをクローン# リポジトリをクローン



## 🏗️ プロジェクト構成git clone https://github.com/yayuyosakana/pdfunlockapp.gitgit clone https://github.com/yourusername/pdfunlockapp.git



```cd pdfunlockappcd pdfunlockapp

pdfunlockapp/

├── pdf_unlock_app.py      # メインアプリケーション

├── setup.py               # py2appビルド設定

├── build_app.sh           # ビルド&署名スクリプト# 仮想環境を作成# 仮想環境を作成

├── create_icon.py         # アイコン生成スクリプト

├── app_icon.icns          # macOSアイコンpython3 -m venv venvpython3 -m venv venv

├── app_icon.png           # PNGアイコン

├── requirements.txt       # Python依存関係source venv/bin/activatesource venv/bin/activate

├── README.md              # このファイル

└── LICENSE                # MITライセンス

```

# 依存関係をインストール# 依存関係をインストール

## 🔐 セキュリティ

pip install -r requirements.txtpip install -r requirements.txt

- パスワードはメモリ上でのみ処理され、保存されません

- 元のPDFファイルは一時ファイル経由で安全に置換されます

- AES暗号化されたPDFにも対応（pycryptodome使用）

- アプリはadhoc署名でコード署名されています# アイコンを生成# アイコンを生成



## 🐛 トラブルシューティングpython create_icon.pypython create_icon.py



### 「開発元が未確認のため開けません」と表示される



macOSのセキュリティ機能により、初回起動時にこのメッセージが表示される場合があります:# アプリをビルド# アプリをビルド



1. アプリアイコンを右クリックpython setup.py py2apppython setup.py py2app

2. 「開く」を選択

3. 確認ダイアログで「開く」をクリック



### パスワードが正しいのにエラーになる# ビルドされたアプリは dist/PDF Unlock.app に作成されます# ビルドされたアプリは dist/PDF Unlock.app に作成されます



一部のPDFは複雑な暗号化を使用している場合があります:``````



1. パスワードを再確認してください

2. 別のPDF編集ソフトでパスワードを確認してください

または、ビルドスクリプトを使用:または、ビルドスクリプトを使用:

### アプリがクラッシュする



ビルド後に正しく署名されているか確認してください:

```bash```bash

```bash

codesign --verify --deep --strict --verbose=2 "dist/PDF Unlock.app"chmod +x build_app.shchmod +x build_app.sh

```

./build_app.sh./build_app.sh

## 🔨 開発者向け情報

``````

### ローカルでテスト実行



```bash

source venv/bin/activate## 📖 使い方## 📖 使い方

python pdf_unlock_app.py

```



### アプリのビルド1. **アプリを起動**: `PDF Unlock.app`をダブルクリック1. **アプリを起動**: `PDF Unlock.app`をダブルクリック



```bash2. **PDFを選択**: 2. **PDFを選択**: 

# クリーンビルド

rm -rf build dist   - 「📄 PDFファイルを選択」ボタンをクリック   - ドラッグ&ドロップエリアにPDFファイルをドロップ

python setup.py py2app

   - ファイル選択ダイアログでPDFを選択   - または「Browse」ボタンでファイルを選択

# adhoc署名を適用

codesign --force --deep --sign - "dist/PDF Unlock.app"3. **パスワード入力**: パスワード保護されている場合は入力（なければ空欄でOK）3. **パスワード入力**: パスワード保護されている場合は入力（なければ空欄でOK）

```

4. **アンロック実行**: 4. **アンロック実行**: 

または、ビルドスクリプトを使用:

   - 「🔓 PDFのロックを解除」ボタンをクリック   - 「Unlock PDF」ボタンをクリック

```bash

./build_app.sh   - またはEnterキーを押す   - またはEnterキーを押す

```

5. **完了**: 元のPDFファイルが制限なしの状態に置き換えられます5. **完了**: 元のPDFファイルが制限なしの状態に置き換えられます

### ビルド設定



`setup.py`の重要な設定:

- `strip: False` - バイナリストリップを無効化（コード署名保持のため）## 🛠️ 技術スタック## 🛠️ 技術スタック

- `argv_emulation: False` - コマンドライン引数エミュレーション無効

- `iconfile: 'app_icon.icns'` - アプリアイコン



## 📝 ライセンス- **言語**: Python 3.12- **言語**: Python 3.12



このプロジェクトはMITライセンスの下で公開されています。詳細は[LICENSE](LICENSE)ファイルを参照してください。- **GUI**: Tkinter（標準ライブラリ）- **GUI**: Tkinter（標準ライブラリ）



## 🤝 貢献- **PDF処理**: PyPDF2- **PDF処理**: PyPDF2



プルリクエストを歓迎します！大きな変更の場合は、まずissueを開いて変更内容を議論してください。- **暗号化**: pycryptodome（AES対応）- **暗号化**: pycryptodome（AES対応）



## 📧 お問い合わせ- **パッケージング**: py2app（macOS）- **パッケージング**: py2app（macOS）



問題や提案がある場合は、[Issues](../../issues)ページでお知らせください。- **アイコン生成**: Pillow- **アイコン生成**: Pillow



---



**注意**: このツールは合法的に所有しているPDFファイルのロック解除のみに使用してください。著作権法を遵守し、他人のファイルを無断で解除しないでください。## 📦 依存関係## 📦 依存関係



## 🎯 主な機能詳細



### PDFのロック解除とは？``````



このアプリは以下のような制限を解除できます:PyPDF2==3.0.1PyPDF2==3.0.1

- ✅ 印刷の制限

- ✅ 編集の制限pycryptodome==3.21.0pycryptodome==3.21.0

- ✅ コピー＆ペーストの制限

- ✅ 注釈追加の制限py2app==0.28.8py2app==0.28.8

- ✅ ページの抽出制限

- ✅ フォーム入力の制限Pillow==11.3.0Pillow==11.3.0



**注**: 閲覧パスワード（開くためのパスワード）が設定されている場合は、そのパスワードを入力する必要があります。``````



### 動作の仕組み



1. PDFファイルを読み込み## 🏗️ プロジェクト構成## 🏗️ プロジェクト構成

2. パスワードがあれば復号化

3. すべてのページとメタデータを制限なしでコピー

4. 新しいPDFとして一時保存

5. 元のファイルを削除して新しいファイルに置き換え``````



### 対応フォーマットpdfunlockapp/pdfunlockapp/



- PDF 1.0 〜 2.0├── pdf_unlock_app.py      # メインアプリケーション├── pdf_unlock_app.py    # メインアプリケーション

- AES暗号化PDF（pycryptodome使用）

- RC4暗号化PDF├── setup.py               # py2appビルド設定├── setup.py             # py2app設定

- パスワード保護PDF

├── build_app.sh           # ビルドスクリプト├── create_icon.py       # アイコン生成スクリプト

## 🚀 今後の予定

├── create_icon.py         # アイコン生成スクリプト├── requirements.txt     # Python依存関係

- [ ] バッチ処理（複数ファイルの一括処理）

- [ ] 処理履歴の表示├── app_icon.icns          # macOSアイコン├── build_app.sh         # ビルド自動化スクリプト

- [ ] ダークモード対応

- [ ] 多言語対応（英語、日本語）├── app_icon.png           # PNGアイコン├── app_icon.png         # アイコン画像（PNG）


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
