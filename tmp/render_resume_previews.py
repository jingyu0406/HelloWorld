from pathlib import Path
import fitz
from PIL import Image, ImageOps, ImageDraw

source = Path(r"C:\Users\mimi9\OneDrive\桌面\HelloWorld\簡歷")
preview_dir = Path(r"C:\Users\mimi9\OneDrive\桌面\HelloWorld\tmp\resume-previews")
preview_dir.mkdir(parents=True, exist_ok=True)
thumbs = []
for pdf_path in sorted(source.glob("*.pdf")):
    doc = fitz.open(pdf_path)
    page = doc[0]
    pix = page.get_pixmap(matrix=fitz.Matrix(1.2, 1.2), alpha=False)
    image_path = preview_dir / f"{pdf_path.stem}.png"
    pix.save(image_path)
    image = Image.open(image_path).convert("RGB")
    image.thumbnail((420, 600))
    card = Image.new("RGB", (460, 670), "white")
    card.paste(image, ((460 - image.width) // 2, 45))
    draw = ImageDraw.Draw(card)
    draw.text((18, 12), pdf_path.name, fill="#222222")
    thumbs.append(card)

sheet = Image.new("RGB", (920, 1340), "#dddddd")
for i, thumb in enumerate(thumbs):
    sheet.paste(thumb, ((i % 2) * 460, (i // 2) * 670))
sheet.save(preview_dir / "contact-sheet.png")
print(preview_dir / "contact-sheet.png")
