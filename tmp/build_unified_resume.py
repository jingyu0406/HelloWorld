from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.lib.utils import ImageReader

ROOT = Path(r"C:\Users\mimi9\OneDrive\桌面\HelloWorld")
OUT_DIR = ROOT / "簡歷"
OUT_PDF = OUT_DIR / "翁靖瑜_統一風格履歷.pdf"
OUT_HTML = OUT_DIR / "翁靖瑜_統一風格履歷_可編輯.html"
PHOTO = ROOT / "tmp" / "resume-assets" / "img-0.jpeg"
ASSET_DIR = OUT_DIR / "履歷素材"

FONT = r"C:\Windows\Fonts\NotoSansTC-VF.ttf"
pdfmetrics.registerFont(TTFont("NotoTC", FONT))

PAGE_W, PAGE_H = A4
BLACK = colors.HexColor("#111111")
ORANGE = colors.HexColor("#F5A300")
PALE = colors.HexColor("#F3F3F1")
MID = colors.HexColor("#676767")
WHITE = colors.white

styles = {
    "body": ParagraphStyle("body", fontName="NotoTC", fontSize=8.4, leading=13, textColor=BLACK),
    "small": ParagraphStyle("small", fontName="NotoTC", fontSize=7.6, leading=11.5, textColor=BLACK),
    "muted": ParagraphStyle("muted", fontName="NotoTC", fontSize=7.4, leading=11, textColor=MID),
    "project": ParagraphStyle("project", fontName="NotoTC", fontSize=8, leading=12, textColor=BLACK),
}


def para(c, text, x, y_top, width, style="body"):
    p = Paragraph(text, styles[style])
    _, h = p.wrap(width, PAGE_H)
    p.drawOn(c, x, y_top - h)
    return y_top - h


def section(c, title, x, y, width):
    c.setFillColor(ORANGE)
    c.roundRect(x, y - 7 * mm, width, 7 * mm, 1.5 * mm, fill=1, stroke=0)
    c.setFillColor(BLACK)
    c.setFont("NotoTC", 10)
    c.drawString(x + 3 * mm, y - 5 * mm, title)
    return y - 10 * mm


def tag(c, text, x, y, width):
    c.setFillColor(PALE)
    c.roundRect(x, y - 6 * mm, width, 6 * mm, 3 * mm, fill=1, stroke=0)
    c.setFillColor(BLACK)
    c.setFont("NotoTC", 7.2)
    c.drawCentredString(x + width / 2, y - 4.25 * mm, text)


def header(c, page_label):
    c.setFillColor(BLACK)
    c.rect(0, PAGE_H - 55 * mm, PAGE_W, 55 * mm, fill=1, stroke=0)
    c.setFillColor(ORANGE)
    c.rect(0, PAGE_H - 4 * mm, PAGE_W, 4 * mm, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("NotoTC", 26)
    c.drawString(18 * mm, PAGE_H - 22 * mm, "翁靖瑜")
    c.setFont("NotoTC", 10)
    c.drawString(18 * mm, PAGE_H - 31 * mm, "WENG JING YU")
    c.setFillColor(ORANGE)
    c.setFont("NotoTC", 9)
    c.drawString(18 * mm, PAGE_H - 41 * mm, "互動設計 × 遊戲開發 × 視覺整合")
    c.setFillColor(colors.HexColor("#BEBEBE"))
    c.setFont("NotoTC", 7)
    c.drawRightString(PAGE_W - 14 * mm, PAGE_H - 47 * mm, page_label)


def footer(c, page_number):
    c.setStrokeColor(colors.HexColor("#D9D9D9"))
    c.line(15 * mm, 12 * mm, PAGE_W - 15 * mm, 12 * mm)
    c.setFillColor(MID)
    c.setFont("NotoTC", 6.8)
    c.drawString(15 * mm, 7.5 * mm, "作品與經歷整理自原始簡歷及作品資料")
    c.drawRightString(PAGE_W - 15 * mm, 7.5 * mm, str(page_number))


def page_one(c):
    header(c, "PROFILE / EXPERIENCE")
    # Portrait card
    c.setFillColor(WHITE)
    c.roundRect(PAGE_W - 52 * mm, PAGE_H - 51 * mm, 34 * mm, 43 * mm, 4 * mm, fill=1, stroke=0)
    c.drawImage(str(PHOTO), PAGE_W - 50.5 * mm, PAGE_H - 49.5 * mm, 31 * mm, 40 * mm,
                preserveAspectRatio=True, anchor="c", mask="auto")

    left_x, gap = 15 * mm, 7 * mm
    left_w = 70 * mm
    right_x = left_x + left_w + gap
    right_w = PAGE_W - right_x - 15 * mm
    top = PAGE_H - 63 * mm

    y = section(c, "核心定位", left_x, top, left_w)
    y = para(c,
        "具備程式開發與視覺設計雙領域能力，能從企劃、UI/UX、互動邏輯、視覺製作一路推進至部署與測試。擅長把抽象設計語彙轉譯為可執行的技術規格，並在團隊中協調設計端與開發端。",
        left_x + 2 * mm, y, left_w - 4 * mm)
    y -= 5 * mm

    y = section(c, "學歷", left_x, y, left_w)
    y = para(c, "<b>國立臺北教育大學｜數位科技設計學系</b><br/>111－114｜平均成績 89.95｜班排 7 / 40（17.5%）",
             left_x + 2 * mm, y, left_w - 4 * mm)
    y -= 5 * mm

    y = section(c, "專業工具", left_x, y, left_w)
    tag_w = 31.5 * mm
    tags = ["Unity / C#", "C++ / OpenGL", "HTML / CSS / JS", "React Native", "Python / Git", "Figma / UI UX",
            "Ps / Ai", "CSP / Krita", "3ds Max / Rhino", "Pr / Ae / L2D"]
    for i, item in enumerate(tags):
        tx = left_x + (i % 2) * (tag_w + 3 * mm)
        ty = y - (i // 2) * 8 * mm
        tag(c, item, tx, ty, tag_w)
    y -= 43 * mm

    y = section(c, "語言與亮點", left_x, y, left_w)
    para(c, "• JLPT N1 日本語能力試驗最高級（2023/12）<br/>• 跨領域自主學習與原語境資料閱讀能力<br/>• 團隊領導、進度統籌與跨職能溝通",
         left_x + 2 * mm, y, left_w - 4 * mm, "small")

    y2 = section(c, "經歷", right_x, top, right_w)
    experiences = [
        ("程式設計課程助教", "國北數位系｜114/09－115/06", "協助大一必修課程學習與程式問題釐清。"),
        ("數位美術創作班老師", "國北教大夏令營｜114/07－114/08", "設計國小、國中數位繪圖課程，以工具入門與角色設計回應不同能力層級。"),
        ("女子排球隊副隊長", "國北數位系｜112/09－114/06", "協助團隊溝通、訓練與組織協作。"),
        ("數位營美宣組組長", "國北數位營｜113/03－113/08", "負責視覺宣傳規劃與美宣工作協調。"),
        ("系學會幹部", "國北數位系第 18 屆｜112/09－113/06", "參與系務活動規劃與執行。"),
        ("新生宿營關卡設計組長", "國北數位系｜112/05－112/10", "統籌關卡體驗、分工與現場執行。"),
    ]
    for title, meta, body in experiences:
        c.setFillColor(BLACK)
        c.setFont("NotoTC", 9.2)
        c.drawString(right_x + 2 * mm, y2 - 2 * mm, title)
        c.setFillColor(ORANGE)
        c.setFont("NotoTC", 7.2)
        c.drawRightString(right_x + right_w - 2 * mm, y2 - 2 * mm, meta)
        y2 = para(c, body, right_x + 2 * mm, y2 - 5 * mm, right_w - 4 * mm, "small") - 4 * mm
        c.setStrokeColor(colors.HexColor("#E3E3E3"))
        c.line(right_x + 2 * mm, y2 + 1.5 * mm, right_x + right_w - 2 * mm, y2 + 1.5 * mm)

    y2 -= 2 * mm
    y2 = section(c, "專業成果", right_x, y2, right_w)
    para(c,
        "<b>「愛在台灣、守護萬物」藝術設計徵件第三名</b>｜2023<br/>以《林中碩鼠》將山林保育議題轉化為可拆裝、可遊玩的立體桌遊。<br/><br/>"
        "<b>JLPT N1 日本語能力試驗最高級</b>｜2023/12<br/>能直接閱讀日本數位內容、互動設計與遊戲領域資料。<br/><br/>"
        "<b>完整跨媒介實作經驗</b><br/>涵蓋桌遊、App、2D 遊戲、VR 與 2.5D 敘事養成遊戲，並多次擔任組長、主程式或主美術。",
        right_x + 2 * mm, y2, right_w - 4 * mm, "small")
    footer(c, 1)


def draw_contain(c, path, x, y, width, height):
    image = ImageReader(str(path))
    iw, ih = image.getSize()
    scale = min(width / iw, height / ih)
    dw, dh = iw * scale, ih * scale
    c.setFillColor(PALE)
    c.roundRect(x, y, width, height, 2 * mm, fill=1, stroke=0)
    c.drawImage(image, x + (width - dw) / 2, y + (height - dh) / 2, dw, dh, mask="auto")


def project_block(c, x, y, width, number, title, meta, role, summary, outcomes, image_path):
    c.setFillColor(BLACK)
    c.roundRect(x, y - 11 * mm, width, 11 * mm, 2 * mm, fill=1, stroke=0)
    c.setFillColor(ORANGE)
    c.setFont("NotoTC", 15)
    c.drawString(x + 3 * mm, y - 7.5 * mm, number)
    c.setFillColor(WHITE)
    c.setFont("NotoTC", 10)
    c.drawString(x + 15 * mm, y - 6.6 * mm, title)
    c.setFont("NotoTC", 6.8)
    c.drawRightString(x + width - 3 * mm, y - 6.5 * mm, meta)
    y -= 14 * mm
    image_w, image_h = 39 * mm, 24 * mm
    draw_contain(c, image_path, x + 2 * mm, y - image_h, image_w, image_h)
    text_x = x + image_w + 6 * mm
    text_w = width - image_w - 8 * mm
    text_y = para(c, f"<font color='#F5A300'><b>{role}</b></font><br/>{summary}", text_x, y, text_w, "project")
    text_y = para(c, outcomes, text_x, text_y - 1.5 * mm, text_w, "small")
    return min(y - image_h, text_y) - 4 * mm


def page_two(c):
    header(c, "SELECTED PROJECTS")
    x = 15 * mm
    width = PAGE_W - 30 * mm
    y = PAGE_H - 63 * mm
    y = project_block(c, x, y, width, "01", "Idol Pact｜2.5D 偶像養成模擬遊戲", "113-2－114-2",
        "組長／企劃／主美術／統籌｜C#・Unity・Ink・Git・CSP・Ai・L2D・Pr",
        "結合 2D 與 3D、多故事線、角色培育與公演機制的畢業專題；玩家以經紀人身分組建偶像團體並透過決策影響結局。",
        "• 統整企劃、美術與程式需求，建立素材、變數命名規範及美術骨架對照表。<br/>• 維護事件觸發、物件屬性與角色數值管理表，協助多人協作與內容一致性。",
        ASSET_DIR / "project-idol.jpg")
    y = project_block(c, x, y, width, "02", "2D 彈幕射擊遊戲", "113-2",
        "獨立製作｜C++・OpenGL",
        "以基礎圖形、矩陣變換與互動邏輯完成多型態飛船、Boss 戰、護盾與追蹤彈幕。",
        "• 封裝 CShape 繼承架構，讓形狀組件可共用移動與旋轉功能。<br/>• 以雙向鏈結串列管理高波動子彈生命週期；加入粒子、拖尾、追蹤彈與場景變化。",
        ASSET_DIR / "project-shooter.jpg")
    y = project_block(c, x, y, width, "03", "竹籤不是用來烤肉的｜VR 互動模擬遊戲", "113-2",
        "主程式／設備測試｜C#・Unity・OpenXR・XR Interaction Toolkit・Git",
        "以糖葫蘆店經營為題，設計三關體感操作與精準訂單判定，使用 Meta Quest 3S 測試。",
        "• 完成 VR 抓握、碰撞、物件掛載、訂單序列比對及關卡流程。<br/>• 多輪調整場景尺度、工作臺高度與移動參數，在遊戲性和 3D 暈眩控制間取得平衡。",
        ASSET_DIR / "project-vr.jpg")
    y = project_block(c, x, y, width, "04", "傘電｜校園愛心傘借用 App", "112-2",
        "組長／企劃／主程式｜React Native・JavaScript・Git",
        "從校園忘記帶傘與濕傘收納痛點出發，規劃帳號驗證、即時定位、跨點借還、狀態提醒與留言板。",
        "• 負責核心借還流程、定位、狀態顯示與 Dark Mode 等互動回饋。<br/>• 共同規劃 Functional Map、Flow Chart 與 UI Flow，將真實需求轉化為數位服務流程。",
        ASSET_DIR / "project-umbrella.jpg")
    y = project_block(c, x, y, width, "05", "林中碩鼠｜山林保育教育桌遊", "112-1",
        "組長／企劃／立體架構設計",
        "把山老鼠防治、森林科普與經濟取捨融入卡牌規則，以立體棋盤呈現山川高度與棲地。",
        "• 統籌團隊、設計可拆裝收納結構，獨立完成卡牌內容、卡面、插圖與科普文本。<br/>• 獲「愛在台灣、守護萬物」藝術設計徵件第三名。",
        ASSET_DIR / "project-boardgame.jpg")
    footer(c, 2)


def build():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUT_PDF), pagesize=A4)
    c.setTitle("翁靖瑜｜統一風格履歷")
    c.setAuthor("翁靖瑜")
    page_one(c)
    c.showPage()
    page_two(c)
    c.save()
    html = """<!doctype html>
<html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>翁靖瑜｜統一風格履歷</title><style>
@page{size:A4;margin:0}*{box-sizing:border-box}body{margin:0;background:#ddd;font-family:'Noto Sans TC','Microsoft JhengHei',sans-serif;color:#111}.page{width:210mm;min-height:297mm;margin:8mm auto;background:#fff;padding:0 15mm 16mm;page-break-after:always}.head{height:55mm;background:#111;margin:0 -15mm 8mm;padding:12mm 18mm;color:#fff;border-top:4mm solid #f5a300}.head h1{font-size:30px;font-weight:500;margin:0}.head p{margin:5px 0;color:#f5a300;letter-spacing:.08em}.grid{display:grid;grid-template-columns:38% 1fr;gap:8mm}.section h2{font-size:14px;background:#f5a300;padding:5px 10px;border-radius:6px;margin:0 0 8px}.section{margin-bottom:15px}.section p,.section li{font-size:11px;line-height:1.65;margin:4px 0}.tags{display:grid;grid-template-columns:1fr 1fr;gap:5px}.tag{font-size:10px;text-align:center;background:#f1f1ef;border-radius:20px;padding:5px}.item{border-bottom:1px solid #ddd;padding:0 3px 8px;margin-bottom:8px}.item b{font-size:12px}.meta{float:right;color:#c88700;font-size:9px}.project{margin:0 0 13px}.project h2{background:#111;color:#fff;border-radius:7px;padding:9px 12px;font-size:14px;font-weight:500}.project h2 span{color:#f5a300;margin-right:18px}.project .content{display:grid;grid-template-columns:40mm 1fr;gap:7mm;padding:3px 8px}.project img{width:40mm;height:27mm;object-fit:contain;background:#f1f1ef;border-radius:6px}.project .role{color:#c88700;font-size:10px}.project p{font-size:10.5px;line-height:1.55;margin:3px 0}.muted{color:#777}@media print{body{background:#fff}.page{margin:0}}
</style></head><body>
<section class="page"><header class="head"><h1>翁靖瑜</h1><div>WENG JING YU</div><p>互動設計 × 遊戲開發 × 視覺整合</p></header><div class="grid">
<main><div class="section"><h2>核心定位</h2><p>具備程式開發與視覺設計雙領域能力，能從企劃、UI/UX、互動邏輯、視覺製作一路推進至部署與測試。擅長把抽象設計語彙轉譯為可執行的技術規格。</p></div><div class="section"><h2>學歷</h2><p><b>國立臺北教育大學｜數位科技設計學系</b><br>111－114｜平均成績 89.95｜班排 7 / 40（17.5%）</p></div><div class="section"><h2>專業工具</h2><div class="tags"><span class="tag">Unity / C#</span><span class="tag">C++ / OpenGL</span><span class="tag">HTML / CSS / JS</span><span class="tag">React Native</span><span class="tag">Python / Git</span><span class="tag">Figma / UI UX</span><span class="tag">Ps / Ai</span><span class="tag">CSP / Krita</span><span class="tag">3ds Max / Rhino</span><span class="tag">Pr / Ae / L2D</span></div></div><div class="section"><h2>語言與亮點</h2><ul><li>JLPT N1（2023/12）</li><li>跨領域自主學習</li><li>團隊領導與跨職能溝通</li></ul></div></main>
<aside><div class="section"><h2>經歷</h2><div class="item"><b>程式設計課程助教</b><span class="meta">114/09－115/06</span><p>協助大一必修課程學習與程式問題釐清。</p></div><div class="item"><b>數位美術創作班老師</b><span class="meta">114/07－114/08</span><p>設計國小、國中數位繪圖課程，以工具入門與角色設計回應不同能力層級。</p></div><div class="item"><b>女子排球隊副隊長</b><span class="meta">112/09－114/06</span><p>協助團隊溝通、訓練與組織協作。</p></div><div class="item"><b>數位營美宣組組長</b><span class="meta">113/03－113/08</span><p>負責視覺宣傳規劃與美宣工作協調。</p></div><div class="item"><b>系學會幹部</b><span class="meta">112/09－113/06</span></div><div class="item"><b>新生宿營關卡設計組長</b><span class="meta">112/05－112/10</span></div></div><div class="section"><h2>專業成果</h2><p><b>藝術設計徵件第三名</b>｜2023<br>《林中碩鼠》山林保育立體桌遊。</p><p><b>JLPT N1</b>｜2023/12<br>可直接閱讀日本數位內容與遊戲領域資料。</p><p><b>跨媒介實作</b><br>涵蓋桌遊、App、2D 遊戲、VR 與 2.5D 敘事遊戲。</p></div></aside></div></section>
<section class="page"><header class="head"><h1>翁靖瑜</h1><div>SELECTED PROJECTS</div><p>互動設計 × 遊戲開發 × 視覺整合</p></header>
<div class="project"><h2><span>01</span>Idol Pact｜2.5D 偶像養成模擬遊戲</h2><div class="content"><img src="履歷素材/project-idol.jpg"><div><p class="role">組長／企劃／主美術／統籌｜C#・Unity・Ink・Git・CSP・Ai・L2D・Pr</p><p>結合 2D 與 3D、多故事線、角色培育與公演機制。統整企劃、美術與程式需求，建立素材與變數命名規範，維護事件、物件屬性及角色數值管理表。</p></div></div></div>
<div class="project"><h2><span>02</span>2D 彈幕射擊遊戲</h2><div class="content"><img src="履歷素材/project-shooter.jpg"><div><p class="role">獨立製作｜C++・OpenGL</p><p>封裝 CShape 繼承架構，以雙向鏈結串列管理子彈生命週期，完成多型態飛船、Boss、追蹤彈幕、粒子、拖尾與場景變化。</p></div></div></div>
<div class="project"><h2><span>03</span>竹籤不是用來烤肉的｜VR 互動模擬遊戲</h2><div class="content"><img src="履歷素材/project-vr.jpg"><div><p class="role">主程式／設備測試｜C#・Unity・OpenXR・XR Interaction Toolkit・Git</p><p>完成 VR 抓握、碰撞、物件掛載、訂單比對及關卡流程；使用 Meta Quest 3S 多輪調整場景尺度與移動參數，降低 3D 暈眩風險。</p></div></div></div>
<div class="project"><h2><span>04</span>傘電｜校園愛心傘借用 App</h2><div class="content"><img src="履歷素材/project-umbrella.jpg"><div><p class="role">組長／企劃／主程式｜React Native・JavaScript・Git</p><p>規劃帳號驗證、即時定位、跨點借還、狀態提醒與留言板；負責核心流程與互動回饋，並共同規劃 Functional Map、Flow Chart 與 UI Flow。</p></div></div></div>
<div class="project"><h2><span>05</span>林中碩鼠｜山林保育教育桌遊</h2><div class="content"><img src="履歷素材/project-boardgame.jpg"><div><p class="role">組長／企劃／立體架構設計</p><p>設計可拆裝立體棋盤，獨立完成卡牌內容、配圖與科普文本；獲「愛在台灣、守護萬物」藝術設計徵件第三名。</p></div></div></div></section></body></html>"""
    OUT_HTML.write_text(html, encoding="utf-8")
    print(OUT_PDF)
    print(OUT_HTML)


if __name__ == "__main__":
    build()
