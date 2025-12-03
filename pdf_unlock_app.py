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
from docx2pdf import convert


class PDFUnlockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Unlock App")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        
        self.file_paths = []
        self.setup_ui()
        self.setup_key_bindings()
    
    def setup_ui(self):
        """UIのセットアップ"""
        # メインフレーム
        main_frame = ttk.Frame(self.root, padding="30")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # タイトル
        title_label = ttk.Label(
            main_frame, 
            text="PDF Unlock Tool", 
            font=("Arial", 24, "bold")
        )
        title_label.grid(row=0, column=0, pady=(0, 30))
        
        # 説明ラベル
        desc_label = ttk.Label(
            main_frame,
            text="PDFファイルの編集制限・閲覧制限を解除します",
            font=("Arial", 11),
            foreground="gray"
        )
        desc_label.grid(row=1, column=0, pady=(0, 20))
        
        # ファイル選択ボタン
        browse_button = ttk.Button(
            main_frame,
            text="📄 ファイルを選択",
            command=self.browse_file,
            width=30
        )
        browse_button.grid(row=2, column=0, pady=(0, 15))
        
        # ファイル名表示
        self.file_label = ttk.Label(
            main_frame, 
            text="", 
            foreground="blue",
            font=("Arial", 10),
            wraplength=500
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
            text="🔓 ロック解除 / 変換",
            command=self.process_files,
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
    
    def setup_key_bindings(self):
        """キーボードショートカットの設定"""
        # Enterキーで実行
        self.password_entry.bind('<Return>', lambda e: self.process_files())
        self.root.bind('<Return>', lambda e: self.process_files() if self.file_paths else None)
    
    def browse_file(self):
        """ファイル選択ダイアログを開く"""
        file_paths = filedialog.askopenfilenames(
            title="ファイルを選択",
            filetypes=[
                ("Supported Files", "*.pdf *.docx"),
                ("PDF Files", "*.pdf"), 
                ("Word Files", "*.docx"),
                ("All Files", "*.*")
            ]
        )
        if file_paths:
            self.set_files(file_paths)
    
    def set_files(self, file_paths):
        """ファイルを設定"""
        self.file_paths = file_paths
        count = len(file_paths)
        if count == 1:
            file_name = os.path.basename(file_paths[0])
            display_text = f"選択済み: {file_name}"
        else:
            display_text = f"選択済み: {count}個のファイル"
            
        self.file_label.config(text=display_text)
        self.unlock_button.config(state=tk.NORMAL)
        self.status_label.config(text="")
        # パスワード入力欄にフォーカス
        self.password_entry.focus_set()
    
    def process_files(self):
        """選択されたファイルを処理"""
        if not self.file_paths:
            messagebox.showerror("エラー", "ファイルが選択されていません。")
            return
        
        password = self.password_entry.get()
        success_count = 0
        error_count = 0
        errors = []
        
        for file_path in self.file_paths:
            try:
                ext = os.path.splitext(file_path)[1].lower()
                
                if ext == '.docx':
                    self.convert_docx(file_path)
                    success_count += 1
                elif ext == '.pdf':
                    self.unlock_pdf(file_path, password)
                    success_count += 1
                else:
                    errors.append(f"{os.path.basename(file_path)}: 未対応の形式です")
                    error_count += 1
                    
            except Exception as e:
                error_count += 1
                error_msg = str(e)
                if "PyCryptodome" in error_msg or "Crypto" in error_msg or "AES" in error_msg:
                    errors.append(f"{os.path.basename(file_path)}: AES暗号化は未対応です")
                else:
                    errors.append(f"{os.path.basename(file_path)}: {error_msg}")

        # 結果表示
        if error_count == 0:
            self.status_label.config(
                text=f"✓ 全て完了！ {success_count}個のファイルを処理しました",
                foreground="green"
            )
            messagebox.showinfo(
                "完了",
                f"処理が完了しました！\n\n"
                f"成功: {success_count}件"
            )
            self.reset()
        else:
            self.status_label.config(
                text=f"⚠ 完了 (成功: {success_count}, 失敗: {error_count})",
                foreground="orange"
            )
            error_details = "\n".join(errors[:5])
            if len(errors) > 5:
                error_details += "\n..."
            
            messagebox.showwarning(
                "一部エラー",
                f"処理が完了しましたが、エラーが発生しました。\n\n"
                f"成功: {success_count}件\n"
                f"失敗: {error_count}件\n\n"
                f"エラー詳細:\n{error_details}"
            )

    def convert_docx(self, file_path):
        """DOCXをPDFに変換して置き換え"""
        # docx2pdfはWordが必要
        try:
            # 出力先（同じ場所、拡張子pdf）
            output_path = os.path.splitext(file_path)[0] + ".pdf"
            
            # 変換実行
            convert(file_path, output_path)
            
            # 元のファイルを削除
            os.remove(file_path)
            
        except Exception as e:
            raise Exception(f"DOCX変換エラー: {e}")

    def unlock_pdf(self, file_path, password):
        """PDFのロックを解除"""
        # PDFを読み込む
        reader = PdfReader(file_path)
        
        # パスワードで保護されている場合
        if reader.is_encrypted:
            if password:
                # パスワードを試す
                decrypt_result = reader.decrypt(password)
                if decrypt_result == 0:
                    raise Exception("パスワードが正しくありません")
            else:
                # 空のパスワードを試す
                decrypt_result = reader.decrypt('')
                if decrypt_result == 0:
                    raise Exception("パスワードが必要です")
        
        # 新しいPDFを作成
        writer = PdfWriter()
        
        # すべてのページをコピー（制限なしで）
        for page in reader.pages:
            writer.add_page(page)
        
        # メタデータをコピー
        if reader.metadata:
            writer.add_metadata(reader.metadata)
        
        # 一時ファイルに保存してから元ファイルと置き換え
        input_path = Path(file_path)
        temp_path = input_path.parent / f"{input_path.stem}_temp_unlock.pdf"
        
        # 一時ファイルに解除されたPDFを保存
        with open(temp_path, 'wb') as output_file:
            writer.write(output_file)
        
        # 元のファイルを削除
        try:
            os.remove(file_path)
        except Exception as e:
            # 削除失敗時は一時ファイルも削除
            os.remove(temp_path)
            raise Exception(f"元のファイルを削除できませんでした: {e}")
        
        # 一時ファイルを元のファイル名にリネーム
        os.rename(temp_path, file_path)
    
    def reset(self):
        """アプリをリセット"""
        self.file_paths = []
        self.file_label.config(text="")
        self.password_entry.delete(0, tk.END)
        self.unlock_button.config(state=tk.DISABLED)


def main():
    """アプリケーションのメイン関数"""
    root = tk.Tk()
    app = PDFUnlockApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
