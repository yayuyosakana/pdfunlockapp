#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF Unlock Application
PDFファイルの編集制限・閲覧制限を解除するアプリケーション
"""

import os
import threading
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from pypdf import PdfReader, PdfWriter
from pypdf.errors import DependencyError, PdfReadError


# ---------------------------------------------------------------------------
# コア処理（GUIから独立＝テスト可能）
# ---------------------------------------------------------------------------
def unlock_pdf(file_path, password=""):
    """PDF のパスワード/権限制限を解除し、元ファイルを非暗号化版で置き換える。

    置換の直前に出力PDFが正常に開けるか検証するため、途中で失敗しても
    元ファイルは失われない（成功時は従来どおり元ファイルを直接置換）。
    """
    reader = PdfReader(file_path)

    if reader.is_encrypted:
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

    # 検証OK → 元ファイルを原子的に置換
    os.replace(tmp, file_path)


def convert_docx(file_path):
    """DOCX を PDF に変換。出力PDFを検証してから元 DOCX を削除する。"""
    # docx2pdf は Word が必要なので、使う時だけ遅延 import する
    from docx2pdf import convert

    output_path = os.path.splitext(file_path)[0] + ".pdf"
    convert(file_path, output_path)

    # 検証：出力PDFが存在し、開けるか（Word未インストール等はここで検知）
    if not os.path.exists(output_path):
        raise RuntimeError(
            "PDFへの変換に失敗しました（Microsoft Word が必要です）"
        )
    PdfReader(output_path)  # 壊れていれば例外

    # 検証OK → 元の DOCX を削除（従来どおり置換）
    os.remove(file_path)


# ---------------------------------------------------------------------------
# GUI
# ---------------------------------------------------------------------------
class PDFUnlockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Unlock App")
        self.root.geometry("600x440")
        self.root.resizable(False, False)

        self.file_paths = []
        self.processing = False
        self.setup_ui()
        self.setup_key_bindings()

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
        self.browse_button.grid(row=2, column=0, pady=(0, 15))

        # ファイル名表示
        self.file_label = ttk.Label(
            main_frame, text="", foreground="blue", font=("Arial", 10), wraplength=500
        )
        self.file_label.grid(row=3, column=0, pady=(0, 20))

        # パスワード入力フレーム
        password_frame = ttk.Frame(main_frame)
        password_frame.grid(row=4, column=0, pady=(0, 20))
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

        # 解除ボタン
        self.unlock_button = ttk.Button(
            main_frame,
            text="🔓 ロック解除 / 変換",
            command=self.process_files,
            state=tk.DISABLED,
            width=30,
        )
        self.unlock_button.grid(row=5, column=0, pady=(0, 15))

        # プログレスバー（処理中のみ表示）
        self.progress = ttk.Progressbar(main_frame, mode="determinate", length=400)
        self.progress.grid(row=6, column=0, pady=(0, 10))
        self.progress.grid_remove()

        # ステータスラベル
        self.status_label = ttk.Label(
            main_frame, text="", foreground="green", font=("Arial", 10), wraplength=500
        )
        self.status_label.grid(row=7, column=0)

    def setup_key_bindings(self):
        """キーボードショートカットの設定"""
        self.password_entry.bind("<Return>", lambda e: self.process_files())
        self.root.bind(
            "<Return>",
            lambda e: self.process_files() if self.file_paths else None,
        )

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
        self._set_processing(True, len(files))
        threading.Thread(
            target=self._worker, args=(files, password), daemon=True
        ).start()

    def _worker(self, files, password):
        """ワーカースレッド：ファイルを順に処理し、UI更新はmainスレッドへ委譲"""
        success = 0
        errors = []
        total = len(files)
        for i, file_path in enumerate(files, 1):
            name = os.path.basename(file_path)
            try:
                ext = os.path.splitext(file_path)[1].lower()
                if ext == ".pdf":
                    unlock_pdf(file_path, password)
                elif ext == ".docx":
                    convert_docx(file_path)
                else:
                    raise ValueError("未対応の形式です")
                success += 1
            except DependencyError:
                errors.append(f"{name}: 暗号化解除に必要なライブラリが不足しています")
            except PdfReadError as e:
                errors.append(f"{name}: PDFを読み込めません（{e}）")
            except Exception as e:
                errors.append(f"{name}: {e}")
            self.root.after(0, self._on_progress, i, total, name)
        self.root.after(0, self._on_finished, success, errors)

    def _set_processing(self, on, total=0):
        self.processing = on
        if on:
            self.unlock_button.config(state=tk.DISABLED)
            self.browse_button.config(state=tk.DISABLED)
            self.progress.config(maximum=total, value=0)
            self.progress.grid()
            self.status_label.config(text=f"処理中... (0/{total})", foreground="black")
        else:
            self.browse_button.config(state=tk.NORMAL)
            self.progress.grid_remove()

    def _on_progress(self, done, total, name):
        self.progress.config(value=done)
        self.status_label.config(text=f"処理中... ({done}/{total}) {name}", foreground="black")

    def _on_finished(self, success, errors):
        self._set_processing(False)
        error_count = len(errors)
        if error_count == 0:
            self.status_label.config(
                text=f"✓ 全て完了！ {success}個のファイルを処理しました",
                foreground="green",
            )
            messagebox.showinfo("完了", f"処理が完了しました！\n\n成功: {success}件")
            self.reset()
        else:
            self.status_label.config(
                text=f"⚠ 完了 (成功: {success}, 失敗: {error_count})",
                foreground="orange",
            )
            detail = "\n".join(errors[:5]) + ("\n..." if error_count > 5 else "")
            messagebox.showwarning(
                "一部エラー",
                f"処理が完了しましたが、エラーが発生しました。\n\n"
                f"成功: {success}件\n"
                f"失敗: {error_count}件\n\n"
                f"エラー詳細:\n{detail}",
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


if __name__ == "__main__":
    main()
