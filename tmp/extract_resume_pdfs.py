from pathlib import Path
from pypdf import PdfReader

source_dir = Path(r"C:\Users\mimi9\OneDrive\桌面\HelloWorld\簡歷")
output = Path(r"C:\Users\mimi9\OneDrive\桌面\HelloWorld\tmp\resume-extracted.txt")
output.parent.mkdir(parents=True, exist_ok=True)

chunks = []
for pdf in sorted(source_dir.glob("*.pdf")):
    reader = PdfReader(str(pdf))
    chunks.append(f"\n{'=' * 72}\nFILE: {pdf.name}\nPAGES: {len(reader.pages)}\n")
    for index, page in enumerate(reader.pages, 1):
        text = page.extract_text() or ""
        chunks.append(f"\n--- PAGE {index} ---\n{text.strip()}\n")

output.write_text("".join(chunks), encoding="utf-8")
print(output)
