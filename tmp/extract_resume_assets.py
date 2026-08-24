from pathlib import Path
import pymupdf

pdf_path = Path(r"C:\Users\mimi9\OneDrive\桌面\HelloWorld\簡歷\個人簡歷.pdf")
output_dir = Path(r"C:\Users\mimi9\OneDrive\桌面\HelloWorld\tmp\resume-assets")
output_dir.mkdir(parents=True, exist_ok=True)
doc = pymupdf.open(pdf_path)
for index, image in enumerate(doc[0].get_images(full=True)):
    payload = doc.extract_image(image[0])
    output_path = output_dir / f"img-{index}.{payload['ext']}"
    output_path.write_bytes(payload["image"])
    print(output_path)
