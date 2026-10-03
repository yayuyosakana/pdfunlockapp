#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF Unlock Application
PDFファイルの編集制限・閲覧制限を解除するアプリケーション
"""

import os
import subprocess
import sys
import threading
import traceback
from pathlib import Path

LOG_PATH = Path.home() / "Library" / "Logs" / "PDF Unlock.log"


# ---------------------------------------------------------------------------
# 起動まわり（他のMacでの "Launch error" 対策）
# ---------------------------------------------------------------------------
def configure_bundled_tcl():
    """py2app でアプリに同梱した Tcl/Tk ライブラリを使うよう設定する。

    Homebrew の Python でビルドすると Tcl/Tk のスクリプト群（init.tcl など）が
    ビルドしたMacの /opt/homebrew を参照したままになり、他のMacでは
    Tk が起動できず "Launch error" になる。同梱分があればそちらを使う。
    """
    resources = os.environ.get("RESOURCEPATH")  # py2app のアプリ内でのみ設定される
    if not resources:
        return
    base = Path(resources) / "tcl-tk"
    for var, marker in (("TCL_LIBRARY", "init.tcl"), ("TK_LIBRARY", "tk.tcl")):
        for d in sorted(base.glob("*")):
            if (d / marker).is_file():
                os.environ[var] = str(d)
                break


def report_startup_error(text):
    """起動時の例外をログに書き、ダイアログで知らせる（Tk が使えなくても表示できるよう osascript）"""
    try:
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(text + "\n")
    except OSError:
        pass
    sys.stderr.write(text + "\n")
    last_line = text.strip().splitlines()[-1] if text.strip() else "不明なエラー"
    msg = f"PDF Unlock を起動できませんでした。\n\n{last_line}\n\n詳細: {LOG_PATH}"
    msg = msg.replace("\\", "\\\\").replace('"', '\\"')
    try:
        subprocess.run(
            ["/usr/bin/osascript", "-e",
             f'display alert "PDF Unlock" message "{msg}" as critical'],
            timeout=120,
        )
    except Exception:
        pass


def self_test():
    """ビルド後の動作確認（build_app.sh が --selftest 付きで実行する）"""
    import tkinter

    root = tkinter.Tk()
    root.withdraw()
    root.update()
    root.destroy()
    print(f"  Tk {tkinter.TkVersion}: OK")

    from pypdf._crypt_providers import crypt_provider

    if crypt_provider[0] != "cryptography":
        raise RuntimeError(
            f"cryptography が読み込めていません（{crypt_provider[0]}）。AES暗号化PDFを解除できません"
        )
    import cryptography.hazmat.primitives.ciphers  # noqa: F401  ネイティブ拡張の読み込み確認

    print(f"  pypdf + cryptography {crypt_provider[1]}: OK")

    import docx2pdf

    if not (Path(docx2pdf.__file__).parent / "convert.jxa").is_file():
        raise RuntimeError("docx2pdf の convert.jxa が同梱されていません")
    print("  docx2pdf: OK")


# ---------------------------------------------------------------------------
# コア処理（GUIから独立＝テスト可能）
# ---------------------------------------------------------------------------
SUPPORTED_EXTS = (".pdf", ".docx")


def unique_path(path):
    """同名ファイルがあれば「名前 (2).pdf」のように重複しない名前を返す。"""
    path = Path(path)
    if not path.exists():
        return path
    n = 2
    while True:
        candidate = path.with_name(f"{path.stem} ({n}){path.suffix}")
        if not candidate.exists():
            return candidate
        n += 1


def unlock_pdf(file_path, password="", keep_original=False):
    """PDF のパスワード/権限制限を解除する。

    keep_original=False なら元ファイルを非暗号化版で置き換え、True なら
    「名前_unlocked.pdf」として別に保存する。出力PDFを検証してから書き込む
    ため、途中で失敗しても元ファイルは失われない。

    戻り値: 出力したファイルのパス。もともと制限がない PDF は何もせず None。
    """
    from pypdf import PdfReader, PdfWriter

    reader = PdfReader(file_path)

    if not reader.is_encrypted:
        # 制限なし：書き直すと中身が変わるだけなので触らない
        return None

    # 空パスワード → 指定パスワード の順で試す
    # （所有者パスワードのみ設定され、閲覧は自由なPDFにも対応するため）
    decrypted = False
    for pw in dict.fromkeys(["", password or ""]):
        if reader.decrypt(pw):  # PasswordType.NOT_DECRYPTED (==0) は falsy
            decrypted = True
            break
    if not decrypted:
        raise ValueError(
            "パスワードが正しくありません" if password else "パスワードが必要です"
        )

    # ドキュメント全体を複製（しおり・注釈・フォーム等を保持）。書き出しは非暗号化。
    writer = PdfWriter(clone_from=reader)

    src = Path(file_path)
    if keep_original:
        dest = unique_path(src.with_name(f"{src.stem}_unlocked.pdf"))
    else:
        dest = src
    tmp = src.with_name(f"{src.stem}_temp_unlock.pdf")
    try:
        with open(tmp, "wb") as f:
            writer.write(f)

        # 検証：出力が暗号化されておらず、ページを持っているか
        check = PdfReader(str(tmp))
        if check.is_encrypted or len(check.pages) == 0:
            raise RuntimeError("出力PDFの検証に失敗しました")
    except Exception:
        if tmp.exists():
            tmp.unlink()
        raise

    # 検証OK → 原子的に書き込み（置換 or 別名保存）
    os.replace(tmp, dest)
    return str(dest)


def convert_docx(file_path, keep_original=False):
    """DOCX を PDF に変換する。keep_original=False なら変換後に元 DOCX を削除。

    同名の PDF が既にある場合は上書きせず「名前 (2).pdf」として保存する。
    戻り値: 出力した PDF のパス。
    """
    # docx2pdf は Word が必要なので、使う時だけ遅延 import する
    from docx2pdf import convert
    from pypdf import PdfReader

    output_path = str(unique_path(os.path.splitext(file_path)[0] + ".pdf"))
    try:
        convert(file_path, output_path)
    except SystemExit:
        # docx2pdf は Word 側のエラー時に sys.exit() するため、そのままだと
        # ワーカースレッドが黙って終了し「処理中...」のまま固まってしまう
        raise RuntimeError("Word での PDF 変換に失敗しました") from None

    # 検証：出力PDFが存在し、開けるか（Word未インストール等はここで検知）
    if not os.path.exists(output_path):
        raise RuntimeError(
            "PDFへの変換に失敗しました（Microsoft Word が必要です）"
        )
    PdfReader(output_path)  # 壊れていれば例外

    if not keep_original:
        # 検証OK → 元の DOCX を削除（従来どおり置換）
        os.remove(file_path)
    return output_path


def reveal_in_finder(paths):
    """ファイルを Finder で選択した状態で表示する。"""
    if paths:
        subprocess.run(["/usr/bin/open", "-R", *paths])


# ---------------------------------------------------------------------------
# GUI
# ---------------------------------------------------------------------------
import tkinter as tk  # noqa: E402
from tkinter import ttk, messagebox, filedialog  # noqa: E402


class PDFUnlockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Unlock App")
        self.root.geometry("600x520")
        self.root.resizable(False, False)

        self.file_paths = []
        self.output_paths = []
        self.processing = False
        self.keep_original = tk.BooleanVar(value=False)
        self.setup_ui()
        self.setup_key_bindings()
        self.setup_open_document()

    def setup_ui(self):
        """UIのセットアップ"""
        main_frame = ttk.Frame(self.root, padding="30")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # タイトル
        ttk.Label(
            main_frame, text="PDF Unlock Tool", font=("Arial", 24, "bold")
        ).grid(row=0, column=0, pady=(0, 20))

        # 説明ラベル
        ttk.Label(
            main_frame,
            text="PDFファイルの編集制限・閲覧制限を解除します",
            font=("Arial", 11),
            foreground="gray",
        ).grid(row=1, column=0, pady=(0, 20))

        # ファイル選択ボタン
        self.browse_button = ttk.Button(
            main_frame, text="📄 ファイルを選択", command=self.browse_file, width=30
        )
        self.browse_button.grid(row=2, column=0, pady=(0, 5))
        ttk.Label(
            main_frame,
            text="（Dock のアイコンにファイルをドロップしても選択できます）",
            font=("Arial", 9),
            foreground="gray",
        ).grid(row=3, column=0, pady=(0, 10))

        # ファイル名表示
        self.file_label = ttk.Label(
            main_frame, text="", foreground="blue", font=("Arial", 10), wraplength=500
        )
        self.file_label.grid(row=4, column=0, pady=(0, 15))

        # パスワード入力フレーム
        password_frame = ttk.Frame(main_frame)
        password_frame.grid(row=5, column=0, pady=(0, 15))
        ttk.Label(password_frame, text="パスワード:", font=("Arial", 11)).grid(
            row=0, column=0, padx=(0, 10)
        )
        self.password_entry = ttk.Entry(password_frame, width=30, show="*")
        self.password_entry.grid(row=0, column=1)
        ttk.Label(
            password_frame,
            text="(パスワードがない場合は空欄、Enterキーで実行)",
            font=("Arial", 9),
            foreground="gray",
        ).grid(row=1, column=0, columnspan=2, pady=(5, 0))

        # 元ファイルを残すオプション
        ttk.Checkbutton(
            main_frame,
            text="元のファイルを残す（PDF は「名前_unlocked.pdf」として保存）",
            variable=self.keep_original,
        ).grid(row=6, column=0, pady=(0, 15))

        # 解除ボタン
        self.unlock_button = ttk.Button(
            main_frame,
            text="🔓 ロック解除 / 変換",
            command=self.process_files,
            state=tk.DISABLED,
            width=30,
        )
        self.unlock_button.grid(row=7, column=0, pady=(0, 15))

        # プログレスバー（処理中のみ表示）
        self.progress = ttk.Progressbar(main_frame, mode="determinate", length=400)
        self.progress.grid(row=8, column=0, pady=(0, 10))
        self.progress.grid_remove()

        # ステータスラベル
        self.status_label = ttk.Label(
            main_frame, text="", foreground="green", font=("Arial", 10), wraplength=500
        )
        self.status_label.grid(row=9, column=0)

        # Finder で表示ボタン（処理完了後のみ表示）
        self.reveal_button = ttk.Button(
            main_frame,
            text="📂 Finder で表示",
            command=lambda: reveal_in_finder(self.output_paths),
            width=30,
        )
        self.reveal_button.grid(row=10, column=0, pady=(10, 0))
        self.reveal_button.grid_remove()

    def setup_key_bindings(self):
        """キーボードショートカットの設定"""
        self.password_entry.bind("<Return>", lambda e: self.process_files())
        self.root.bind(
            "<Return>",
            lambda e: self.process_files() if self.file_paths else None,
        )

    def setup_open_document(self):
        """Dock アイコンへのドロップ / 「このアプリで開く」で渡されたファイルを受け取る"""
        self.root.createcommand("::tk::mac::OpenDocument", self.open_documents)

    def open_documents(self, *paths):
        if self.processing:
            self.root.bell()
            return
        files = [p for p in paths if os.path.splitext(p)[1].lower() in SUPPORTED_EXTS]
        if not files:
            messagebox.showerror("エラー", "PDF または DOCX ファイルを選択してください。")
            return
        self.set_files(files)
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()

    def browse_file(self):
        """ファイル選択ダイアログを開く"""
        file_paths = filedialog.askopenfilenames(
            title="ファイルを選択",
            filetypes=[
                ("Supported Files", "*.pdf *.docx"),
                ("PDF Files", "*.pdf"),
                ("Word Files", "*.docx"),
                ("All Files", "*.*"),
            ],
        )
        if file_paths:
            self.set_files(file_paths)

    def set_files(self, file_paths):
        """ファイルを設定"""
        self.file_paths = list(file_paths)
        count = len(self.file_paths)
        if count == 1:
            display_text = f"選択済み: {os.path.basename(self.file_paths[0])}"
        else:
            display_text = f"選択済み: {count}個のファイル"
        self.file_label.config(text=display_text)
        self.unlock_button.config(state=tk.NORMAL)
        self.status_label.config(text="")
        self.reveal_button.grid_remove()
        self.password_entry.focus_set()

    # -- 処理（バックグラウンドスレッドで実行しUIをブロックしない） -------------
    def process_files(self):
        """選択されたファイルを処理（スレッド起動）"""
        if self.processing:
            return
        if not self.file_paths:
            messagebox.showerror("エラー", "ファイルが選択されていません。")
            return

        password = self.password_entry.get()
        files = list(self.file_paths)
        keep = self.keep_original.get()
        self._set_processing(True, len(files))
        threading.Thread(
            target=self._worker, args=(files, password, keep), daemon=True
        ).start()

    def _worker(self, files, password, keep_original):
        """ワーカースレッド：ファイルを順に処理し、UI更新はmainスレッドへ委譲"""
        from pypdf.errors import DependencyError, PdfReadError

        outputs = []
        skipped = []
        errors = []
        total = len(files)
        for i, file_path in enumerate(files, 1):
            name = os.path.basename(file_path)
            try:
                ext = os.path.splitext(file_path)[1].lower()
                if ext == ".pdf":
                    out = unlock_pdf(file_path, password, keep_original)
                elif ext == ".docx":
                    out = convert_docx(file_path, keep_original)
                else:
                    raise ValueError("未対応の形式です")
                if out is None:
                    skipped.append(name)
                else:
                    outputs.append(out)
            except DependencyError:
                errors.append(f"{name}: 暗号化解除に必要なライブラリが不足しています")
            except PdfReadError as e:
                errors.append(f"{name}: PDFを読み込めません（{e}）")
            except Exception as e:
                errors.append(f"{name}: {e}")
            self.root.after(0, self._on_progress, i, total, name)
        self.root.after(0, self._on_finished, outputs, skipped, errors)

    def _set_processing(self, on, total=0):
        self.processing = on
        if on:
            self.unlock_button.config(state=tk.DISABLED)
            self.browse_button.config(state=tk.DISABLED)
            self.reveal_button.grid_remove()
            self.progress.config(maximum=total, value=0)
            self.progress.grid()
            self.status_label.config(text=f"処理中... (0/{total})", foreground="black")
        else:
            self.browse_button.config(state=tk.NORMAL)
            self.progress.grid_remove()

    def _on_progress(self, done, total, name):
        self.progress.config(value=done)
        self.status_label.config(text=f"処理中... ({done}/{total}) {name}", foreground="black")

    def _on_finished(self, outputs, skipped, errors):
        self._set_processing(False)
        self.output_paths = outputs
        if outputs:
            self.reveal_button.grid()

        success = len(outputs)
        lines = [f"成功: {success}件"]
        if skipped:
            lines.append(f"制限なし（変更不要）: {len(skipped)}件")
        error_count = len(errors)
        if error_count == 0:
            self.status_label.config(
                text=f"✓ 全て完了！ {success + len(skipped)}個のファイルを確認しました",
                foreground="green",
            )
            messagebox.showinfo("完了", "処理が完了しました！\n\n" + "\n".join(lines))
            self.reset()
        else:
            self.status_label.config(
                text=f"⚠ 完了 (成功: {success}, 失敗: {error_count})",
                foreground="orange",
            )
            lines.append(f"失敗: {error_count}件")
            detail = "\n".join(errors[:5]) + ("\n..." if error_count > 5 else "")
            messagebox.showwarning(
                "一部エラー",
                "処理が完了しましたが、エラーが発生しました。\n\n"
                + "\n".join(lines)
                + f"\n\nエラー詳細:\n{detail}",
            )

    def reset(self):
        """アプリをリセット"""
        self.file_paths = []
        self.file_label.config(text="")
        self.password_entry.delete(0, tk.END)
        self.unlock_button.config(state=tk.DISABLED)


def main():
    """アプリケーションのメイン関数"""
    root = tk.Tk()
    PDFUnlockApp(root)
    root.mainloop()


def run():
    configure_bundled_tcl()
    if "--selftest" in sys.argv[1:]:
        try:
            self_test()
        except Exception:
            traceback.print_exc()
            sys.exit(1)
        print("selftest OK")
        return
    try:
        main()
    except Exception:
        report_startup_error(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    run()
