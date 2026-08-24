from pathlib import Path
import pymupdf
from PIL import Image, ImageDraw

root = Path(r"C:\Users\mimi9\OneDrive\桌面\HelloWorld")
pdf_path = root / "簡歷" / "翁靖瑜_作品資料.pdf"
out_dir = root / "tmp" / "project-images"
out_dir.mkdir(parents=True, exist_ok=True)
doc = pymupdf.open(pdf_path)
targets = {1: "shooter", 4: "vr", 7: "idol", 9: "umbrella", 11: "boardgame"}
cards = []
for page_no, slug in targets.items():
    page = doc[page_no - 1]
    for index, image in enumerate(page.get_images(full=True)):
        payload = doc.extract_image(image[0])
        path = out_dir / f"{slug}-p{page_no}-img{index}.{payload['ext']}"
        path.write_bytes(payload["image"])
        img = Image.open(path).convert("RGB")
        img.thumbnail((260, 180))
        card = Image.new("RGB", (280, 225), "white")
        card.paste(img, ((280 - img.width) // 2, 28 + (180 - img.height) // 2))
        draw = ImageDraw.Draw(card)
        draw.text((8, 7), path.stem, fill="#111111")
        draw.text((8, 211), f"{Image.open(path).size}", fill="#555555")
        cards.append(card)

cols = 4
rows = (len(cards) + cols - 1) // cols
sheet = Image.new("RGB", (cols * 280, rows * 225), "#d0d0d0")
for i, card in enumerate(cards):
    sheet.paste(card, ((i % cols) * 280, (i // cols) * 225))
sheet_path = out_dir / "contact-sheet.jpg"
sheet.save(sheet_path, quality=92)
print(sheet_path)
