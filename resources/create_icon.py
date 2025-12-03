#!/usr/bin/env python3
"""
モダンなアイコン作成スクリプト
グラデーションと3Dエフェクトを使った洗練されたデザイン
"""

try:
    from PIL import Image, ImageDraw, ImageFont
    import os
    
    # 1024x1024のアイコンを作成
    size = 1024
    img = Image.new('RGB', (size, size), color='white')
    draw = ImageDraw.Draw(img)
    
    # モダンなグラデーション背景（ディープブルー → ライトブルー）
    for y in range(size):
        r = int(30 + (42 - 30) * y / size)
        g = int(60 + (82 - 60) * y / size)
        b = int(114 + (152 - 114) * y / size)
        draw.line([(0, y), (size, y)], fill=(r, g, b))
    
    # PDF文書シェイプの描画（シャドウ付き）
    margin = 140
    doc_width = size - (margin * 2)
    doc_height = size - (margin * 2)
    
    # シャドウエフェクト（複数レイヤー）
    shadow_offset = 20
    for i in range(15, 0, -1):
        alpha = int(20 - i * 1.3)
        shadow_color = (0, 0, 0)
        draw.rounded_rectangle(
            [(margin + shadow_offset + i, margin + shadow_offset + i),
             (size - margin + shadow_offset + i, size - margin + shadow_offset + i)],
            radius=40,
            fill=shadow_color,
            outline=None
        )
    
    # メイン文書（白）
    draw.rounded_rectangle(
        [(margin, margin), (size - margin, size - margin)],
        radius=40,
        fill='#FFFFFF',
        outline='#E0E0E0',
        width=4
    )
    
    # モダンな折り目コーナー
    corner_size = 120
    points = [
        (size - margin, margin),
        (size - margin - corner_size, margin),
        (size - margin, margin + corner_size)
    ]
    draw.polygon(points, fill='#F5F5F5', outline='#E0E0E0')
    draw.line([(size - margin - corner_size, margin), (size - margin, margin + corner_size)], 
              fill='#E0E0E0', width=3)
    
    # 文書内のテキストライン
    line_color = '#CCCCCC'
    line_margin = margin + 60
    line_spacing = 50
    for i in range(5):
        y = margin + 120 + i * line_spacing
        if i == 4:
            draw.rounded_rectangle(
                [(line_margin, y), (size - margin - 200, y + 15)],
                radius=8,
                fill=line_color
            )
        else:
            draw.rounded_rectangle(
                [(line_margin, y), (size - margin - 80, y + 15)],
                radius=8,
                fill=line_color
            )
    
    # モダンなアンロックシンボル（グラデーション）
    center_x = size // 2
    center_y = size // 2 + 180
    
    # グリーングラデーション
    unlock_gradient_start = (46, 213, 115)   # エメラルドグリーン
    unlock_gradient_end = (39, 174, 96)      # ダークグリーン
    
    # 南京錠ボディのグラデーション
    lock_width = 160
    lock_height = 140
    lock_left = center_x - lock_width//2
    lock_top = center_y - lock_height//2
    
    # グラデーション効果を作成
    for y in range(lock_height):
        ratio = y / lock_height
        r = int(unlock_gradient_start[0] + (unlock_gradient_end[0] - unlock_gradient_start[0]) * ratio)
        g = int(unlock_gradient_start[1] + (unlock_gradient_end[1] - unlock_gradient_start[1]) * ratio)
        b = int(unlock_gradient_start[2] + (unlock_gradient_end[2] - unlock_gradient_start[2]) * ratio)
        draw.line(
            [(lock_left + 15, lock_top + y), (lock_left + lock_width - 15, lock_top + y)],
            fill=(r, g, b),
            width=1
        )
    
    # ロックボディのアウトライン
    draw.rounded_rectangle(
        [(lock_left, lock_top), (lock_left + lock_width, lock_top + lock_height)],
        radius=25,
        fill=None,
        outline='#229954',
        width=8
    )
    
    # キーホール（モダンなミニマルスタイル）
    keyhole_radius = 20
    draw.ellipse(
        [(center_x - keyhole_radius, center_y - 10),
         (center_x + keyhole_radius, center_y + 30)],
        fill='#1E8449'
    )
    draw.rectangle(
        [(center_x - 8, center_y + 10),
         (center_x + 8, center_y + 50)],
        fill='#1E8449'
    )
    
    # 開いたシャックル（アーチ）
    shackle_y = center_y - lock_height//2 - 60
    shackle_x_offset = 50
    
    # 太いアーチを描画
    for width_offset in range(8):
        draw.arc(
            [(lock_left - 20 + shackle_x_offset - width_offset*2, shackle_y - 70),
             (lock_left + 80 + shackle_x_offset + width_offset*2, shackle_y + 70)],
            start=180, end=270,
            fill=unlock_gradient_end,
            width=4
        )
    
    # ハイライト効果（3D感）
    draw.arc(
        [(lock_left - 15 + shackle_x_offset, shackle_y - 65),
         (lock_left + 75 + shackle_x_offset, shackle_y + 65)],
        start=200, end=250,
        fill='#52BE80',
        width=3
    )
    
    # PNG形式で保存
    img.save('app_icon.png', 'PNG')
    print("✨ モダンなアイコン画像を作成しました: app_icon.png")
    
    # macOS用icns形式に変換
    print("🎨 macOS用icns形式に変換中...")
    os.system('mkdir -p app_icon.iconset')
    
    # 各サイズのアイコンを生成
    sizes = [16, 32, 64, 128, 256, 512, 1024]
    for s in sizes:
        img_resized = img.resize((s, s), Image.Resampling.LANCZOS)
        img_resized.save(f'app_icon.iconset/icon_{s}x{s}.png')
        if s <= 512:
            img_resized_2x = img.resize((s*2, s*2), Image.Resampling.LANCZOS)
            img_resized_2x.save(f'app_icon.iconset/icon_{s}x{s}@2x.png')
    
    # icns形式に変換
    result = os.system('iconutil -c icns app_icon.iconset -o app_icon.icns')
    
    if result == 0:
        print("✅ macOS用アイコン(icns)を作成しました: app_icon.icns")
        os.system('rm -rf app_icon.iconset')
    else:
        print("⚠️  icns形式への変換に失敗しました（iconutilが必要です）")
        print("   app_icon.pngは使用できます")
    
except ImportError:
    print("⚠️  Pillowがインストールされていません")
    print("   次のコマンドでインストールできます:")
    print("   pip install Pillow")
    print("")
    print("   アイコンなしでもアプリは作成できます")
except Exception as e:
    print(f"❌ エラー: {e}")
    print("   アイコンなしでもアプリは作成できます")
