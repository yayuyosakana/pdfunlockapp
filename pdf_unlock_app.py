#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF Unlock Application
PDFファイルの編集制限・閲覧制限を解除するアプリケーション
"""

import os
import sys
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PyPDF2 import PdfReader, PdfWriter


class PDFUnlockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Unlock App")
        self.root.geometry("700x550")
        self.root.resizable(False, False)
        
        self.pdf_path = None
        self.setup_ui()
        self.setup_macos_dnd()
        self.setup_key_bindings()
    
    def setup_ui(self):
        """UIのセットアップ"""
        # メインフレーム
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # タイトル
        title_label = ttk.Label(
            main_frame, 
            text="PDF Unlock Tool", 
            font=("Arial", 20, "bold")
        )
        title_label.grid(row=0, column=0, pady=(0, 20))
        
        # 説明ラベル
        desc_label = ttk.Label(
            main_frame,
            text="PDFファイルをここにドラッグ&ドロップ",
            font=("Arial", 11),
            foreground="gray"
        )
        desc_label.grid(row=1, column=0, pady=(0, 10))
        
        # ドラッグ&ドロップエリア
        self.drop_area = tk.Label(
            main_frame,
            text="�\n\nここにPDFファイルを\nドラッグ&ドロップ\n\nまたはクリックして選択",
            bg="#f0f0f0",
            fg="#666666",
            width=60,
            height=10,
            relief=tk.RIDGE,
            borderwidth=3,
            font=("Arial", 12),
            cursor="hand2"
        )
        self.drop_area.grid(row=2, column=0, pady=(0, 15))
        self.drop_area.bind('<Button-1>', self.browse_file)
        
        # Tkinterのネイティブドラッグ&ドロップ設定（macOS）
        try:
            self.drop_area.drop_target_register('DND_Files')
        except:
            pass
        
        # ファイル名表示
        self.file_label = ttk.Label(
            main_frame, 
            text="", 
            foreground="blue",
            font=("Arial", 10)
        )
        self.file_label.grid(row=3, column=0, pady=(0, 20))
        
        # パスワード入力フレーム
        password_frame = ttk.Frame(main_frame)
        password_frame.grid(row=4, column=0, pady=(0, 20))
        
        ttk.Label(
            password_frame, 
            text="パスワード:",
            font=("Arial", 11)
        ).grid(row=0, column=0, padx=(0, 10))
        
        self.password_entry = ttk.Entry(password_frame, width=30, show="*")
        self.password_entry.grid(row=0, column=1)
        
        ttk.Label(
            password_frame, 
            text="(パスワードがない場合は空欄、Enterキーで実行)", 
            font=("Arial", 9),
            foreground="gray"
        ).grid(row=1, column=0, columnspan=2, pady=(5, 0))
        
        # 解除ボタン
        self.unlock_button = ttk.Button(
            main_frame,
            text="🔓 PDFのロックを解除",
            command=self.unlock_pdf,
            state=tk.DISABLED,
            width=30
        )
        self.unlock_button.grid(row=5, column=0, pady=(0, 15))
        
        # ステータスラベル
        self.status_label = ttk.Label(
            main_frame, 
            text="", 
            foreground="green",
            font=("Arial", 10),
            wraplength=500
        )
        self.status_label.grid(row=6, column=0)
    
    def setup_macos_dnd(self):
        """macOS向けのドラッグ&ドロップサポート"""
        try:
            # macOSのファイルオープンイベントを処理
            self.root.createcommand('::tk::mac::OpenDocument', self.on_drop_macos)
        except:
            pass
    
    def setup_key_bindings(self):
        """キーボードショートカットの設定"""
        # Enterキーでアンロック実行
        self.password_entry.bind('<Return>', lambda e: self.unlock_pdf())
        self.root.bind('<Return>', lambda e: self.unlock_pdf() if self.pdf_path else None)
    
    def on_drop_macos(self, *args):
        """macOSのドラッグ&ドロップハンドラー"""
        if args:
            file_path = args[0]
            if file_path.lower().endswith('.pdf'):
                self.set_pdf_file(file_path)
            else:
                messagebox.showerror("エラー", "PDFファイルを選択してください。")
        
    def browse_file(self, event=None):
        """ファイル選択ダイアログを開く"""
        file_path = filedialog.askopenfilename(
            title="PDFファイルを選択",
            filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")]
        )
        if file_path:
            self.set_pdf_file(file_path)
    
    def set_pdf_file(self, file_path):
        """PDFファイルを設定"""
        self.pdf_path = file_path
        file_name = os.path.basename(file_path)
        self.file_label.config(text=f"選択: {file_name}")
        self.unlock_button.config(state=tk.NORMAL)
        self.status_label.config(text="")
        # ドラッグ&ドロップエリアの表示を更新
        self.drop_area.config(
            bg="#e0ffe0",
            text=f"✓ ファイル選択済み\n\n{file_name}\n\nパスワードを入力してEnterキー"
        )
        # パスワード入力欄にフォーカス
        self.password_entry.focus_set()
    
    def unlock_pdf(self):
        """PDFのロックを解除"""
        if not self.pdf_path:
            messagebox.showerror("エラー", "PDFファイルが選択されていません。")
            return
        
        password = self.password_entry.get()
        
        try:
            # PDFを読み込む
            reader = PdfReader(self.pdf_path)
            
            # パスワードで保護されている場合
            if reader.is_encrypted:
                if password:
                    # パスワードを試す
                    decrypt_result = reader.decrypt(password)
                    if decrypt_result == 0:
                        messagebox.showerror(
                            "エラー", 
                            "パスワードが正しくありません。"
                        )
                        return
                else:
                    # 空のパスワードを試す
                    decrypt_result = reader.decrypt('')
                    if decrypt_result == 0:
                        messagebox.showerror(
                            "エラー", 
                            "このPDFはパスワードで保護されています。\n"
                            "正しいパスワードを入力してください。"
                        )
                        return
            
            # 新しいPDFを作成
            writer = PdfWriter()
            
            # すべてのページをコピー（制限なしで）
            for page in reader.pages:
                writer.add_page(page)
            
            # メタデータをコピー
            if reader.metadata:
                writer.add_metadata(reader.metadata)
            
            # 一時ファイルに保存してから元ファイルと置き換え
            input_path = Path(self.pdf_path)
            temp_path = input_path.parent / f"{input_path.stem}_temp_unlock.pdf"
            
            # 一時ファイルに解除されたPDFを保存
            with open(temp_path, 'wb') as output_file:
                writer.write(output_file)
            
            # 元のファイルを削除
            try:
                os.remove(self.pdf_path)
            except Exception as e:
                # 削除失敗時は一時ファイルも削除
                os.remove(temp_path)
                raise Exception(f"元のファイルを削除できませんでした: {e}")
            
            # 一時ファイルを元のファイル名にリネーム
            os.rename(temp_path, self.pdf_path)
            
            self.status_label.config(
                text=f"✓ 成功！ {input_path.name} のロックを解除しました",
                foreground="green"
            )
            
            messagebox.showinfo(
                "完了",
                f"PDFのロックを解除しました！\n\n"
                f"ファイル: {input_path.name}\n"
                f"元のファイルを上書きしました。"
            )
            
            # リセット
            self.reset()
            
        except Exception as e:
            error_msg = str(e)
            if "PyCryptodome" in error_msg or "Crypto" in error_msg or "AES" in error_msg:
                messagebox.showerror(
                    "エラー",
                    "暗号化されたPDFを処理するには追加のライブラリが必要です。\n\n"
                    "このPDFはAES暗号化されています。\n"
                    "申し訳ございませんが、現在対応していません。"
                )
            else:
                messagebox.showerror(
                    "エラー",
                    f"PDFの処理中にエラーが発生しました:\n{error_msg}"
                )
            self.status_label.config(
                text="✗ エラーが発生しました",
                foreground="red"
            )
    
    def reset(self):
        """アプリをリセット"""
        self.pdf_path = None
        self.file_label.config(text="")
        self.password_entry.delete(0, tk.END)
        self.unlock_button.config(state=tk.DISABLED)
        self.drop_area.config(
            bg="#f0f0f0",
            text="📄\n\nここにPDFファイルを\nドラッグ&ドロップ\n\nまたはクリックして選択"
        )


def main():
    """アプリケーションのメイン関数"""
    root = tk.Tk()
    app = PDFUnlockApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
