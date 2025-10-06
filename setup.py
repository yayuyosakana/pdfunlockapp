"""
Setup script for creating macOS application
"""
from setuptools import setup

APP = ['pdf_unlock_app.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': False,
    'iconfile': 'app_icon.icns',  # オプション: アイコンファイルがある場合
    'plist': {
        'CFBundleName': 'PDF Unlock',
        'CFBundleDisplayName': 'PDF Unlock',
        'CFBundleGetInfoString': "PDF制限解除ツール",
        'CFBundleIdentifier': "com.pdfunlock.app",
        'CFBundleVersion': "1.0.0",
        'CFBundleShortVersionString': "1.0.0",
        'NSHumanReadableCopyright': "Copyright © 2025",
        'NSHighResolutionCapable': True,
    },
    'packages': ['tkinter', 'PyPDF2', 'Crypto'],
    'includes': ['tkinter', 'PyPDF2', 'Crypto.Cipher', 'Crypto.Util'],
}

setup(
    name='PDF Unlock',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
