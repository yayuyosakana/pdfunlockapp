"""
Setup script for creating macOS application
"""
from setuptools import setup

APP = ['pdf_unlock_app.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': False,
    'iconfile': 'app_icon.icns',
    'strip': False,  # バイナリのストリップを無効化
    'plist': {
        'CFBundleName': 'PDF Unlock',
        'CFBundleDisplayName': 'PDF Unlock',
        'CFBundleGetInfoString': 'PDFファイルの編集制限・閲覧制限を解除',
        'CFBundleIdentifier': 'com.pdfunlockapp.PDFUnlock',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSHumanReadableCopyright': 'Copyright © 2024. All rights reserved.',
        'LSMinimumSystemVersion': '10.10.0',
    },
}

setup(
    name='PDF Unlock',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
