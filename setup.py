"""
Setup script for creating macOS application
"""
import os
import tkinter

from setuptools import setup


def tcl_tk_library_dirs():
    """ビルド中の Python が使っている Tcl/Tk のスクリプトライブラリ（init.tcl 等）の場所。

    アプリに同梱しておかないと、ビルドしたMac以外では Tk が初期化できず
    "Launch error" になる（特に Homebrew の Python でビルドした場合）。
    Tcl 9 のようにライブラリが dylib に埋め込まれている場合は空になる。
    """
    tcl = tkinter.Tcl()
    tcl_lib = tcl.eval("info library")
    version = tcl.eval("info tclversion")
    dirs = []
    for d in (tcl_lib, os.path.join(os.path.dirname(tcl_lib), f"tk{version}")):
        if os.path.isdir(d):
            dirs.append(d)
    return dirs


APP = ['pdf_unlock_app.py']
DATA_FILES = [('tcl-tk', tcl_tk_library_dirs())]
OPTIONS = {
    'argv_emulation': False,
    'iconfile': 'resources/app_icon.icns',
    'strip': False,  # バイナリのストリップを無効化
    # ネイティブ拡張(cryptography/cffi)やデータファイル(docx2pdf の convert.jxa)を
    # 含むパッケージは zip に入れず、そのままの形でアプリに同梱する
    'packages': ['pypdf', 'cryptography', 'cffi', 'docx2pdf', 'tqdm'],
    'includes': ['_cffi_backend'],
    'plist': {
        'CFBundleName': 'PDF Unlock',
        'CFBundleDisplayName': 'PDF Unlock',
        'CFBundleGetInfoString': 'PDFファイルの編集制限・閲覧制限を解除',
        'CFBundleIdentifier': 'com.pdfunlockapp.PDFUnlock',
        'CFBundleVersion': '1.1.1',
        'CFBundleShortVersionString': '1.1.1',
        'NSHumanReadableCopyright': 'Copyright © 2026. All rights reserved.',
        'LSMinimumSystemVersion': '10.13.0',
    },
}

setup(
    name='PDF Unlock',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
