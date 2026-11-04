# -*- coding: utf-8 -*-
"""Сборка широкоформатных PPTX: плакатный стиль СССР и современные лекции."""

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu, Inches, Pt

W = 13.333
H = 7.5

ALIGN = {"left": PP_ALIGN.LEFT, "center": PP_ALIGN.CENTER, "right": PP_ALIGN.RIGHT}
ANCHOR = {"top": "t", "middle": "ctr", "bottom": "b"}


def rgb(value):
    return RGBColor.from_string(value.replace("#", "").upper())


def mix(a, b, t):
    def parts(h):
        h = h.replace("#", "")
        return [int(h[i : i + 2], 16) for i in (0, 2, 4)]

    pa, pb = parts(a), parts(b)
    out = [max(0, min(255, round(pa[i] + (pb[i] - pa[i]) * t))) for i in range(3)]
    return "{:02X}{:02X}{:02X}".format(*out)


def theme(
    tid,
    bg,
    ink,
    muted,
    accent,
    accent2,
    dark,
    paper,
    display,
    font,
    light,
    cover,
    kicker,
    line,
    on_accent="FFFFFF",
    statement="dark",
):
    return {
        "id": tid,
        "bg": bg,
        "ink": ink,
        "muted": muted,
        "accent": accent,
        "accent2": accent2,
        "dark": dark,
        "paper": paper,
        "display": display,
        "font": font,
        "light": light,
        "cover": cover,
        "kicker": kicker,
        "line": line,
        "on_accent": on_accent,
        "statement": statement,
        "ussr": cover in {"poster", "memorial", "construct", "journal", "avant"},
    }


def base_ussr(**kwargs):
    defaults = dict(
        bg="F6EDD8",
        ink="1A120C",
        muted="5C5146",
        accent="C8102E",
        accent2="C8962E",
        dark="14110E",
        paper="FBF6EC",
        display="Arial Black",
        font="Arial",
        light="F7F1E4",
        kicker="C8962E",
        line="E4D3B0",
        on_accent="F7F1E4",
        statement="accent",
    )
    defaults.update(kwargs)
    return theme(**defaults)


THEMES = {
    "poster": base_ussr(tid="poster", cover="poster"),
    "memorial": base_ussr(
        tid="memorial",
        cover="memorial",
        bg="F3F0EA",
        ink="1B1916",
        muted="5F5A54",
        accent="8C1D1D",
        accent2="A68556",
        dark="141210",
        paper="F7F4EE",
        display="Times New Roman",
        kicker="A68556",
        line="DDD6CC",
        light="F3EDE3",
        statement="dark",
    ),
    "construct": base_ussr(
        tid="construct",
        cover="construct",
        bg="F3E2C0",
        accent="D0121E",
        accent2="E0B23A",
        dark="101010",
        paper="FBF3E2",
        kicker="E0B23A",
        line="E3D0A4",
        statement="dark",
    ),
    "journal": base_ussr(
        tid="journal",
        cover="journal",
        bg="F7F3EA",
        ink="1C1612",
        muted="5E564C",
        accent="A4161A",
        accent2="8C7348",
        paper="FBF8F2",
        display="Times New Roman",
        kicker="A4161A",
        line="E5DCCB",
        statement="accent",
    ),
    "avant": base_ussr(
        tid="avant",
        cover="avant",
        bg="F4E7D4",
        accent="D10F26",
        accent2="E2B657",
        dark="0E0E0E",
        paper="FBF4EA",
        kicker="E2B657",
        line="E6D4B4",
        statement="accent",
    ),
    "ai": theme(
        "ai", "F5F4FB", "1B1A26", "5E5A6E", "6E5CE7", "A79BFF", "141326", "FFFFFF",
        "Segoe UI", "Segoe UI", "F4F2FF", "band", "6E5CE7", "E4E2EE",
    ),
    "climate": theme(
        "climate", "F3F6F1", "14241C", "5A6A60", "2F7D57", "8FBF7A", "10241C", "FFFFFF",
        "Segoe UI", "Segoe UI", "F4FBF6", "split", "2F7D57", "DCE5DC", "F4FBF6",
    ),
    "internet": theme(
        "internet", "F3F7F8", "12202B", "5A6B76", "1B93B0", "8FD4E4", "0E1C2E", "FFFFFF",
        "Segoe UI", "Segoe UI", "F3FBFD", "band", "1B93B0", "D5E2E6",
    ),
    "energy": theme(
        "energy", "F8F4EC", "23180F", "6E5E4C", "E0922F", "F2C48A", "1C140C", "FFFFFF",
        "Segoe UI", "Segoe UI", "FFF8EE", "split", "E0922F", "E8DFD0", "1C140C",
    ),
    "cities": theme(
        "cities", "F7F4F0", "241E1A", "6B6158", "C4522A", "E0A090", "2C2622", "FFFFFF",
        "Segoe UI", "Segoe UI", "FFF6F3", "band", "C4522A", "E6DFD6",
    ),
    "decisions": theme(
        "decisions", "F7F4F8", "241C28", "6A5E70", "8E5E9E", "D2B4DC", "291E33", "FFFFFF",
        "Segoe UI", "Segoe UI", "FDF8FF", "split", "8E5E9E", "E6DEE8", "FFF8FF",
    ),
    "photo": theme(
        "photo", "F4F2EE", "1A1A1A", "6A6762", "C6A15B", "E7E2D6", "121212", "FFFFFF",
        "Georgia", "Segoe UI", "F7F4EC", "band", "C6A15B", "E3E0DA",
    ),
    "ocean": theme(
        "ocean", "F2F7F8", "0E2430", "5A7178", "1C7F96", "9ED7E2", "062033", "FFFFFF",
        "Segoe UI", "Segoe UI", "F4FBFC", "split", "1C7F96", "D3E3E6", "F4FBFC",
    ),
    "coffee": theme(
        "coffee", "F8F3EC", "2A1A14", "6E584C", "A65A3A", "E2B596", "2A160F", "FFFFFF",
        "Georgia", "Segoe UI", "FFF8F3", "band", "A65A3A", "EADFD4",
    ),
    "quantum": theme(
        "quantum", "F5F4F8", "16141F", "5E5A6C", "6D5CFF", "2AAEAE", "100E1A", "FFFFFF",
        "Segoe UI", "Segoe UI", "F7F8FF", "split", "2AAEAE", "E2E0EA", "FFFFFF",
    ),
    "music": theme(
        "music", "F8F4F4", "261418", "6E5A5E", "A33B4A", "E2B3BA", "2A1218", "FFFFFF",
        "Georgia", "Segoe UI", "FFF6F7", "band", "A33B4A", "E8DCDF",
    ),
    "sleep": theme(
        "sleep", "F4F6FB", "1A2033", "5C6478", "7E96D6", "C9D4F0", "151B2E", "FFFFFF",
        "Georgia", "Segoe UI", "F7F8FC", "split", "7E96D6", "DDE3F0", "151B2E",
    ),
}


def style_run(run, font, size, color, bold=False, italic=False, spacing=None):
    run.font.name = font
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = rgb(color)
    rpr = run._r.get_or_add_rPr()
    rpr.set("lang", "ru-RU")
    if spacing is not None:
        rpr.set("spc", str(int(spacing)))
    for tag in ("a:latin", "a:ea", "a:cs"):
        el = rpr.find(qn(tag))
        if el is None:
            el = rpr.makeelement(qn(tag), {"typeface": font})
            rpr.append(el)
        else:
            el.set("typeface", font)


def add_text(
    slide,
    x,
    y,
    w,
    h,
    content,
    font,
    size,
    color,
    bold=False,
    italic=False,
    align="left",
    anchor="top",
    spacing=None,
    line_spacing=1.0,
):
    if w <= 0 or h <= 0:
        return None
    if x < -0.2 or y < -0.2 or x + w > W + 0.15 or y + h > H + 0.08:
        preview = content if isinstance(content, str) else "..."
        print(f"  ! text box near edge: {x:.2f},{y:.2f} {w:.2f}x{h:.2f} {str(preview)[:48]}")
    shape = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = shape.text_frame
    tf.word_wrap = True
    tf.auto_size = None
    tf.margin_left = Emu(0)
    tf.margin_right = Emu(0)
    tf.margin_top = Emu(0)
    tf.margin_bottom = Emu(0)
    tf._txBody.bodyPr.set("anchor", ANCHOR[anchor])

    if isinstance(content, str):
        blocks = [{"text": part} for part in content.split("\n")]
    else:
        blocks = []
        for block in content:
            blocks.append({"text": block} if isinstance(block, str) else block)

    for i, block in enumerate(blocks):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = ALIGN[block.get("align", align)]
        p.line_spacing = block.get("line_spacing", line_spacing)
        before = block.get("before", 0)
        if before:
            p.space_before = Pt(before)
        runs = block.get("runs")
        if runs is None:
            runs = [
                {
                    "text": block.get("text", ""),
                    "bold": block.get("bold", bold),
                    "italic": block.get("italic", italic),
                    "color": block.get("color", color),
                    "size": block.get("size", size),
                    "font": block.get("font", font),
                    "spc": block.get("spc", spacing),
                }
            ]
        for spec in runs:
            run = p.add_run()
            run.text = spec.get("text", "")
            style_run(
                run,
                spec.get("font", font),
                spec.get("size", size),
                spec.get("color", color),
                spec.get("bold", bold),
                spec.get("italic", italic),
                spec.get("spc", spacing),
            )
    return shape


def rect(slide, x, y, w, h, fill, line=None, line_w=1.0):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    shape.fill.solid()
    shape.fill.fore_color.rgb = rgb(fill)
    if line is None:
        shape.line.fill.background()
    else:
        shape.line.color.rgb = rgb(line)
        shape.line.width = Pt(line_w)
    return shape


def oval(slide, x, y, w, h, fill):
    shape = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x), Inches(y), Inches(w), Inches(h))
    shape.fill.solid()
    shape.fill.fore_color.rgb = rgb(fill)
    shape.line.fill.background()
    return shape


def star(slide, x, y, w, h, fill):
    shape = slide.shapes.add_shape(MSO_SHAPE.STAR_5_POINT, Inches(x), Inches(y), Inches(w), Inches(h))
    shape.fill.solid()
    shape.fill.fore_color.rgb = rgb(fill)
    shape.line.fill.background()
    return shape


def bg(slide, color):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = rgb(color)


def frame(slide, x, y, w, h, color, thickness):
    rect(slide, x, y, w, thickness, color)
    rect(slide, x, y + h - thickness, w, thickness, color)
    rect(slide, x, y, thickness, h, color)
    rect(slide, x + w - thickness, y, thickness, h, color)


def display_bold(theme_dict):
    return "Black" not in theme_dict["display"]


def ink_on(fill):
    """Светлый текст на тёмной плашке и тёмный — на светлой."""
    h = fill.replace("#", "")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    luminance = (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255
    return "1A140C" if luminance > 0.55 else "FFFFFF"


def title_size(text, theme_dict, base):
    longest = max(len(part) for part in text.split("\n"))
    size = base
    wide = "Black" in theme_dict["display"]
    if wide and longest > 18:
        size -= 4
    elif wide and longest > 12:
        size -= 2
    if not wide and longest > 28:
        size -= 4
    elif not wide and longest > 20:
        size -= 2
    return size


def footer(slide, theme_dict, deck, page, total, dark=False):
    if dark:
        line = mix(theme_dict["dark"], "FFFFFF", 0.28)
        color = mix(theme_dict["light"], theme_dict["dark"], 0.25)
    else:
        line = theme_dict["line"]
        color = theme_dict["muted"]
    rect(slide, 0.5, 7.12, 12.33, 0.012, line)
    add_text(slide, 0.5, 7.18, 8.6, 0.26, deck["series"], theme_dict["font"], 12, color, anchor="middle")
    add_text(
        slide,
        9.4,
        7.18,
        3.43,
        0.26,
        f"{page:02d}   /   {total:02d}",
        theme_dict["font"],
        12,
        color,
        align="right",
        anchor="middle",
        bold=True,
    )


def paint(slide, color):
    bg(slide, color)


def cover_title_size(title, theme_dict):
    lines = title.split("\n")
    longest = max(len(line) for line in lines)
    wide = "Black" in theme_dict["display"]
    size = 54 if wide else 48
    if len(lines) >= 3:
        size -= 8
    if wide and longest > 12:
        size -= 6
    if not wide and longest > 22:
        size -= 6
    return max(size, 36)


def draw_cover(slide, theme_dict, deck, spec, total):
    kind = theme_dict["cover"]
    title = spec["title"]
    size = cover_title_size(title, theme_dict)
    bold = display_bold(theme_dict)
    if kind == "poster":
        paint(slide, theme_dict["accent"])
        rect(slide, 0, 0, 0.22, H, theme_dict["accent2"])
        rect(slide, 0, 6.48, W, 1.02, theme_dict["dark"])
        rect(slide, 0, 6.48, W, 0.045, theme_dict["accent2"])
        oval(slide, 10.15, 0.48, 2.45, 2.45, theme_dict["dark"])
        star(slide, 10.5, 0.84, 1.75, 1.75, theme_dict["accent2"])
        add_text(
            slide, 0.62, 1.15, 9.0, 0.36, spec["kicker"].upper(), theme_dict["font"], 15,
            theme_dict["accent2"], True, spacing=240,
        )
        add_text(
            slide, 0.58, 1.65, 9.1, 2.7, title, theme_dict["display"], size,
            theme_dict["light"], bold, line_spacing=0.92,
        )
        add_text(
            slide, 0.62, 4.55, 8.6, 1.45, spec["subtitle"], theme_dict["font"], 20,
            theme_dict["light"], line_spacing=1.15,
        )
        add_text(slide, 0.62, 6.68, 7.4, 0.42, deck["series"], theme_dict["font"], 14, theme_dict["light"], anchor="middle")
        add_text(
            slide, 8.3, 6.68, 4.5, 0.42, spec.get("meta", ""), theme_dict["font"], 14,
            theme_dict["accent2"], True, align="right", anchor="middle",
        )
    elif kind == "memorial":
        paint(slide, theme_dict["dark"])
        rect(slide, 0.7, 1.42, 1.7, 0.028, theme_dict["accent2"])
        add_text(
            slide, 0.7, 1.62, 10, 0.34, spec["kicker"].upper(), theme_dict["font"], 14,
            theme_dict["accent2"], True, spacing=220,
        )
        add_text(
            slide, 0.68, 2.15, 11.6, 2.15, title, theme_dict["display"], size,
            theme_dict["light"], bold, line_spacing=0.95,
        )
        add_text(
            slide, 0.72, 4.55, 9.4, 1.35, spec["subtitle"], theme_dict["font"], 20,
            mix(theme_dict["light"], theme_dict["dark"], 0.28), line_spacing=1.15,
        )
        rect(slide, 0.72, 6.35, 2.4, 0.02, theme_dict["accent"])
        add_text(slide, 0.7, 6.55, 7.5, 0.4, deck["series"], theme_dict["font"], 14, mix(theme_dict["light"], theme_dict["dark"], 0.35))
        add_text(
            slide, 8.4, 6.5, 4.2, 0.42, spec.get("meta", ""), theme_dict["display"], 20,
            theme_dict["light"], True, align="right",
        )
        star(slide, 12.15, 0.42, 0.48, 0.48, theme_dict["accent2"])
    elif kind == "construct":
        paint(slide, theme_dict["bg"])
        rect(slide, 0, 0, 0.42, H, theme_dict["dark"])
        oval(slide, 9.85, -1.15, 4.5, 4.5, theme_dict["accent"])
        rect(slide, 0.42, 6.05, W, 1.45, theme_dict["dark"])
        rect(slide, 0.85, 4.62, 1.45, 0.12, theme_dict["accent"])
        add_text(
            slide, 0.85, 0.48, 8.2, 0.34, spec["kicker"].upper(), theme_dict["font"], 14,
            theme_dict["accent"], True, spacing=200,
        )
        add_text(
            slide, 0.82, 1.05, 8.8, 3.2, title, theme_dict["display"], size,
            theme_dict["ink"], bold, line_spacing=0.92,
        )
        add_text(slide, 0.85, 6.28, 8.2, 0.85, spec["subtitle"], theme_dict["font"], 18, theme_dict["light"], line_spacing=1.05)
        add_text(
            slide, 9.3, 6.45, 3.5, 0.55, spec.get("meta", ""), theme_dict["font"], 16,
            theme_dict["accent2"], True, align="right", anchor="middle",
        )
    elif kind == "journal":
        paint(slide, theme_dict["bg"])
        frame(slide, 0.32, 0.28, W - 0.64, H - 0.56, theme_dict["accent"], 0.025)
        frame(slide, 0.46, 0.42, W - 0.92, H - 0.84, theme_dict["accent2"], 0.012)
        star(slide, 11.55, 0.68, 0.52, 0.52, theme_dict["accent"])
        add_text(
            slide, 0.85, 1.15, 10, 0.32, spec["kicker"].upper(), theme_dict["font"], 14,
            theme_dict["accent"], True, spacing=200,
        )
        add_text(
            slide, 0.82, 1.7, 11.2, 2.5, title, theme_dict["display"], min(size, 46),
            theme_dict["ink"], True, line_spacing=0.96,
        )
        rect(slide, 0.88, 4.4, 1.5, 0.018, theme_dict["accent"])
        add_text(slide, 0.85, 4.65, 10.2, 1.2, spec["subtitle"], theme_dict["font"], 20, theme_dict["muted"], line_spacing=1.12)
        add_text(slide, 0.85, 6.35, 7.2, 0.35, deck["series"], theme_dict["font"], 14, theme_dict["ink"])
        add_text(
            slide, 8.3, 6.35, 3.9, 0.35, spec.get("meta", ""), theme_dict["font"], 14,
            theme_dict["accent"], True, align="right",
        )
    elif kind == "avant":
        paint(slide, theme_dict["dark"])
        rect(slide, 8.15, 0, W - 8.15, H, theme_dict["accent"])
        rect(slide, 8.02, 0, 0.09, H, theme_dict["accent2"])
        add_text(
            slide, 0.55, 0.85, 7.0, 0.34, spec["kicker"].upper(), theme_dict["font"], 14,
            theme_dict["accent2"], True, spacing=220,
        )
        add_text(
            slide, 0.5, 1.4, 7.15, 3.3, title, theme_dict["display"], size,
            theme_dict["light"], bold, line_spacing=0.9,
        )
        add_text(slide, 0.55, 5.15, 6.9, 1.35, spec["subtitle"], theme_dict["font"], 18, mix(theme_dict["light"], "000000", 0.15), line_spacing=1.1)
        add_text(slide, 0.55, 6.7, 6.8, 0.35, spec.get("meta", ""), theme_dict["font"], 14, theme_dict["accent2"], True)
        stack = spec.get("stack") or ["ФОРМА", "БУКВА", "КАДР"]
        for i, word in enumerate(stack[:4]):
            add_text(
                slide, 8.5, 1.15 + i * 1.15, 4.4, 0.85, word, theme_dict["display"], 26,
                theme_dict["light"], False, anchor="middle",
            )
    elif kind == "band":
        paint(slide, theme_dict["dark"])
        rect(slide, 0, 0, 0.14, H, theme_dict["accent"])
        add_text(
            slide, 0.7, 1.25, 8.5, 0.36, spec["kicker"].upper(), theme_dict["font"], 14,
            theme_dict["kicker"], True, spacing=180,
        )
        add_text(
            slide, 0.68, 1.8, 9.3, 2.55, title, theme_dict["display"], size,
            "FFFFFF", bold, line_spacing=0.96,
        )
        add_text(
            slide, 0.72, 4.6, 8.6, 1.35, spec["subtitle"], theme_dict["font"], 20,
            mix("FFFFFF", theme_dict["dark"], 0.28), line_spacing=1.12,
        )
        rect(slide, 0.72, 6.25, 1.4, 0.018, theme_dict["accent"])
        add_text(slide, 0.7, 6.5, 7.6, 0.4, deck["series"], theme_dict["font"], 14, mix("FFFFFF", theme_dict["dark"], 0.35))
        add_text(
            slide, 8.6, 6.5, 4.1, 0.4, spec.get("meta", f"{total} слайдов"), theme_dict["font"], 14,
            theme_dict["accent2"], True, align="right",
        )
        add_text(
            slide, 10.35, 1.55, 2.5, 1.3, deck["mark"], theme_dict["display"], 40,
            mix(theme_dict["dark"], "FFFFFF", 0.16), bold, align="right",
        )
    elif kind == "split":
        paint(slide, theme_dict["dark"])
        rect(slide, 8.35, 0, W - 8.35, H, theme_dict["accent"])
        add_text(
            slide, 0.6, 1.35, 7.2, 0.34, spec["kicker"].upper(), theme_dict["font"], 14,
            theme_dict["kicker"], True, spacing=180,
        )
        add_text(
            slide, 0.55, 1.9, 7.4, 2.6, title, theme_dict["display"], min(size, 46),
            "FFFFFF", bold, line_spacing=0.96,
        )
        add_text(
            slide, 0.6, 4.75, 7.2, 1.4, spec["subtitle"], theme_dict["font"], 18,
            mix("FFFFFF", theme_dict["dark"], 0.25), line_spacing=1.12,
        )
        add_text(slide, 0.6, 6.55, 7.2, 0.4, deck["series"], theme_dict["font"], 14, mix("FFFFFF", theme_dict["dark"], 0.4))
        add_text(
            slide, 8.55, 2.15, 4.5, 1.5, deck["mark"], theme_dict["display"], 60,
            theme_dict["on_accent"], bold, align="center",
        )
        add_text(
            slide, 8.55, 3.75, 4.5, 0.4, spec.get("meta", ""), theme_dict["font"], 14,
            theme_dict["on_accent"], True, align="center", spacing=120,
        )
    else:
        raise ValueError(kind)


def inner_title_size(title, theme_dict):
    longest = max(len(part) for part in title.split("\n"))
    wide = "Black" in theme_dict["display"]
    size = 28 if wide else 32
    if longest > 42:
        size -= 6
    elif longest > 34:
        size -= 3
    if "\n" in title:
        size -= 2
    return size


def chrome(slide, theme_dict, deck, spec, page, total):
    paint(slide, theme_dict["bg"])
    title = spec.get("title", "")
    size = inner_title_size(title, theme_dict)
    lines = title.count("\n") + 1 if title else 1
    bold = display_bold(theme_dict)
    note = spec.get("note")
    footer(slide, theme_dict, deck, page, total, dark=False)
    note_top = 6.62
    bottom = note_top - 0.06 if note else 6.98

    if theme_dict["cover"] == "construct":
        band_h = 1.72 if lines > 1 else 1.42
        rect(slide, 0, 0, W, band_h, theme_dict["dark"])
        rect(slide, 0, 0, 0.16, H, theme_dict["accent"])
        add_text(
            slide, 0.48, 0.14, 9.5, 0.28, spec.get("kicker", "").upper(), theme_dict["font"], 12,
            theme_dict["accent2"], True, spacing=160,
        )
        add_text(
            slide, 0.46, 0.46, 11.6, band_h - 0.58, title, theme_dict["display"], size,
            theme_dict["light"], bold, line_spacing=0.95,
        )
        sq = 0.34
        rect(slide, 12.5, 0.28, sq, sq, theme_dict["accent"])
        top = band_h + 0.28
    else:
        rect(slide, 0, 0, W, 0.08, theme_dict["accent"])
        if theme_dict["ussr"] and theme_dict["cover"] != "memorial":
            rect(slide, 0, 0, 0.1, H, theme_dict["accent"])
        add_text(
            slide, 0.48, 0.22, 9.6, 0.28, spec.get("kicker", "").upper(), theme_dict["font"], 12,
            theme_dict["kicker"], True, spacing=160,
        )
        title_y = 0.52
        title_h = 1.22 if lines > 1 else 0.84
        add_text(
            slide, 0.46, title_y, 12.35, title_h, title, theme_dict["display"], size,
            theme_dict["ink"], bold, line_spacing=0.96,
        )
        rule_y = title_y + title_h + 0.02
        if theme_dict["ussr"]:
            rect(slide, 0.48, rule_y, 1.25, 0.045, theme_dict["accent"])
            if theme_dict["cover"] == "journal":
                rect(slide, 0.48, rule_y + 0.07, 1.25, 0.012, theme_dict["accent2"])
                top = rule_y + 0.24
            else:
                top = rule_y + 0.18
        else:
            top = rule_y + 0.12

    if note:
        add_text(slide, 0.48, note_top, 12.35, 0.4, note, theme_dict["font"], 12, theme_dict["muted"])
    return {"top": top, "bottom": bottom}


def bullet_blocks(items, theme_dict, size):
    blocks = []
    for item in items:
        if isinstance(item, str):
            runs = [
                {"text": "—  ", "bold": True, "color": theme_dict["accent"], "size": size, "font": theme_dict["font"]},
                {"text": item, "bold": False, "color": theme_dict["ink"], "size": size, "font": theme_dict["font"]},
            ]
        else:
            runs = [
                {"text": "—  ", "bold": True, "color": theme_dict["accent"], "size": size, "font": theme_dict["font"]},
                {"text": item["b"], "bold": True, "color": theme_dict["ink"], "size": size, "font": theme_dict["font"]},
                {"text": "  " + item["t"], "bold": False, "color": theme_dict["ink"], "size": size, "font": theme_dict["font"]},
            ]
        blocks.append({"runs": runs, "before": 0, "line_spacing": 1.05})
    return blocks


def draw_bullets(slide, theme_dict, spec, box):
    y = box["top"]
    lead = spec.get("lead")
    if lead:
        lead_h = 1.05 if len(lead) > 110 else 0.72
        add_text(slide, 0.48, y, 12.35, lead_h, lead, theme_dict["font"], 18, theme_dict["muted"], line_spacing=1.08)
        y += lead_h + 0.08
    items = spec["items"]
    size = 20 if len(items) <= 3 else 18 if len(items) <= 4 else 16 if len(items) <= 5 else 15
    before = 14 if len(items) <= 4 else 10
    blocks = bullet_blocks(items, theme_dict, size)
    for i, block in enumerate(blocks):
        block["before"] = 0 if i == 0 else before
    add_text(slide, 0.48, y, 12.35, box["bottom"] - y, blocks, theme_dict["font"], size, theme_dict["ink"])


def draw_stats(slide, theme_dict, spec, box):
    items = spec["items"]
    n = len(items)
    gap = 0.18
    width = (12.36 - gap * (n - 1)) / n
    height = min(3.55, box["bottom"] - box["top"] - (0.7 if spec.get("foot") else 0))
    y = box["top"]
    for i, item in enumerate(items):
        x = 0.48 + i * (width + gap)
        rect(slide, x, y, width, height, theme_dict["paper"])
        rect(slide, x, y, width, 0.08, theme_dict["accent"])
        add_text(
            slide, x + 0.22, y + 0.35, width - 0.4, 1.15, item["n"], theme_dict["display"],
            40 if n <= 3 else 32, theme_dict["accent"], display_bold(theme_dict),
        )
        add_text(slide, x + 0.22, y + 1.5, width - 0.4, 0.4, item.get("u", ""), theme_dict["font"], 14, theme_dict["kicker"], True)
        add_text(
            slide, x + 0.22, y + 2.05, width - 0.44, height - 2.25, item["t"], theme_dict["font"],
            15 if n <= 3 else 14, theme_dict["ink"], line_spacing=1.05,
        )
    if spec.get("foot"):
        add_text(slide, 0.5, y + height + 0.2, 12.3, 0.7, spec["foot"], theme_dict["font"], 15, theme_dict["muted"])


def draw_split(slide, theme_dict, spec, box):
    y = box["top"]
    height = box["bottom"] - y
    panel_w = 5.85
    fill = theme_dict["dark"] if theme_dict["cover"] in {"construct", "avant", "memorial"} else theme_dict["accent"]
    if not theme_dict["ussr"]:
        fill = theme_dict["dark"]
    rect(slide, 0.48, y, panel_w, height, fill)
    rect(slide, 0.48, y, 0.08, height, theme_dict["accent2"] if theme_dict["ussr"] else theme_dict["accent"])
    add_text(
        slide, 0.78, y + 0.28, panel_w - 0.55, 0.3, spec.get("panel_kicker", "").upper(),
        theme_dict["font"], 12, theme_dict["accent2"] if theme_dict["ussr"] else theme_dict["accent2"], True, spacing=120,
    )
    add_text(
        slide, 0.76, y + 0.68, panel_w - 0.55, 1.3, spec["panel_title"], theme_dict["display"],
        24, theme_dict["light"], display_bold(theme_dict), line_spacing=0.98,
    )
    blocks = []
    for i, line in enumerate(spec["panel"]):
        blocks.append(
            {
                "text": line,
                "before": 0 if i == 0 else 12,
                "size": 15,
                "color": theme_dict["light"],
                "font": theme_dict["font"],
                "line_spacing": 1.05,
            }
        )
    add_text(slide, 0.78, y + 2.15, panel_w - 0.6, height - 2.4, blocks, theme_dict["font"], 15, theme_dict["light"])
    rx = 6.6
    rw = 6.2
    add_text(slide, rx, y + 0.06, rw, 0.7, spec.get("side_title", ""), theme_dict["display"], 22, theme_dict["ink"], display_bold(theme_dict))
    items = spec["items"]
    size = 16 if len(items) <= 4 else 15
    blocks = bullet_blocks(items, theme_dict, size)
    for i, block in enumerate(blocks):
        block["before"] = 0 if i == 0 else 10
    add_text(slide, rx, y + 0.9, rw, height - 1.0, blocks, theme_dict["font"], size, theme_dict["ink"])


def draw_timeline(slide, theme_dict, spec, box):
    items = spec["items"]
    n = len(items)
    top = box["top"]
    height = (box["bottom"] - top) / n
    line_x = 2.05
    rect(slide, line_x, top + height * 0.35, 0.025, height * (n - 1), theme_dict["accent"])
    for i, item in enumerate(items):
        y = top + i * height
        oval(slide, line_x - 0.07, y + height * 0.28, 0.17, 0.17, theme_dict["accent"])
        add_text(
            slide, 0.4, y + 0.08, 1.5, height - 0.1, item["y"], theme_dict["display"],
            16 if n > 5 else 18, theme_dict["accent"], display_bold(theme_dict), anchor="top",
        )
        blocks = [
            {
                "runs": [
                    {"text": item["t"], "bold": True, "size": 16 if n > 5 else 18, "color": theme_dict["ink"], "font": theme_dict["font"]},
                ],
                "line_spacing": 1.0,
            },
            {
                "text": item["d"],
                "before": 2,
                "size": 14 if n > 5 else 15,
                "color": theme_dict["muted"],
                "font": theme_dict["font"],
                "line_spacing": 1.02,
            },
        ]
        add_text(slide, 2.4, y + 0.06, 10.4, height - 0.08, blocks, theme_dict["font"], 15, theme_dict["ink"])


def draw_cards(slide, theme_dict, spec, box):
    items = spec["items"]
    n = len(items)
    cols = 2 if n == 4 else n
    rows = 2 if n == 4 else 1
    gap = 0.16
    avail_w = 12.36
    cw = (avail_w - gap * (cols - 1)) / cols
    max_h = box["bottom"] - box["top"]
    ch = (max_h - gap * (rows - 1)) / rows
    if rows == 1:
        ch = min(ch, 4.05)
    constructs = theme_dict["id"] == "construct" and n == 3
    fills_cycle = [theme_dict["accent"], theme_dict["dark"], theme_dict["paper"]]
    text_cycle = [theme_dict["light"], theme_dict["light"], theme_dict["ink"]]
    for i, item in enumerate(items):
        r, c = divmod(i, cols)
        x = 0.48 + c * (cw + gap)
        y = box["top"] + r * (ch + gap)
        if constructs:
            fill = fills_cycle[i]
            color = text_cycle[i]
            muted = mix(color, "000000", 0.25) if color != theme_dict["ink"] else theme_dict["muted"]
            rect(slide, x, y, cw, ch, fill)
        else:
            fill = theme_dict["paper"]
            color = theme_dict["ink"]
            muted = theme_dict["muted"]
            rect(slide, x, y, cw, ch, fill, line=theme_dict["line"], line_w=1)
            rect(slide, x, y, cw, 0.07, theme_dict["accent"])
        pad = 0.22
        number_color = theme_dict["accent2"] if constructs and color != theme_dict["ink"] else theme_dict["accent"]
        add_text(slide, x + pad, y + 0.16, cw - pad * 2, 0.28, item["n"], theme_dict["font"], 13, number_color, True, spacing=80)
        add_text(
            slide, x + pad, y + 0.46, cw - pad * 2, 0.72, item["t"], theme_dict["display"],
            18 if cols == 2 else 16, color, display_bold(theme_dict), line_spacing=0.98,
        )
        desc_color = muted if constructs else theme_dict["muted"]
        add_text(
            slide, x + pad, y + 1.22, cw - pad * 2, max(0.4, ch - 1.38), item["d"], theme_dict["font"],
            14 if cols == 3 or rows == 2 else 15, desc_color, line_spacing=1.05,
        )


def draw_steps(slide, theme_dict, spec, box):
    items = spec["items"]
    n = len(items)
    height = (box["bottom"] - box["top"]) / n
    for i, item in enumerate(items):
        y = box["top"] + i * height
        oval(slide, 0.5, y + 0.08, 0.52, 0.52, theme_dict["accent"])
        add_text(
            slide, 0.5, y + 0.08, 0.52, 0.52, item["n"], theme_dict["font"], 13,
            ink_on(theme_dict["accent"]), True, align="center", anchor="middle",
        )
        add_text(slide, 1.25, y + 0.06, 11.4, 0.4, item["t"], theme_dict["display"], 18, theme_dict["ink"], display_bold(theme_dict))
        add_text(slide, 1.25, y + 0.48, 11.4, height - 0.56, item["d"], theme_dict["font"], 15, theme_dict["muted"], line_spacing=1.05)


def draw_compare(slide, theme_dict, spec, box):
    y = box["top"]
    height = box["bottom"] - y
    gap = 0.2
    width = (12.36 - gap) / 2
    headers = [spec["left_h"], spec["right_h"]]
    columns = [spec["left"], spec["right"]]
    head_colors = [theme_dict["dark"], theme_dict["accent"]]
    for i in range(2):
        x = 0.48 + i * (width + gap)
        rect(slide, x, y, width, height, theme_dict["paper"], line=theme_dict["line"], line_w=1)
        rect(slide, x, y, width, 0.62, head_colors[i])
        add_text(slide, x + 0.24, y + 0.12, width - 0.4, 0.4, headers[i], theme_dict["display"], 18, theme_dict["light"], display_bold(theme_dict), anchor="middle")
        blocks = bullet_blocks(columns[i], theme_dict, 15)
        for j, block in enumerate(blocks):
            block["before"] = 0 if j == 0 else 10
        add_text(slide, x + 0.24, y + 0.85, width - 0.48, height - 1.05, blocks, theme_dict["font"], 15, theme_dict["ink"])


def draw_quote(slide, theme_dict, spec, box):
    add_text(slide, 0.4, box["top"] - 0.15, 1.6, 0.9, "«", theme_dict["display"], 66, theme_dict["accent"], display_bold(theme_dict))
    text = spec["text"]
    size = 30 if len(text) < 90 else 26 if len(text) < 160 else 22
    add_text(
        slide, 0.55, box["top"] + 0.85, 12.1, 3.3, text, theme_dict["display"], size,
        theme_dict["ink"], display_bold(theme_dict), line_spacing=1.05,
    )
    add_text(slide, 0.55, box["top"] + 4.25, 12.1, 0.45, spec["by"], theme_dict["font"], 16, theme_dict["accent"], True)


def draw_statement(slide, theme_dict, deck, spec, page, total):
    tone = spec.get("tone", "paper")
    if tone == "accent":
        if theme_dict["statement"] == "accent":
            background = theme_dict["accent"]
        else:
            background = theme_dict["dark"]
        color = theme_dict["light"]
        kicker = theme_dict["accent2"] if theme_dict["ussr"] else theme_dict["kicker"]
        note_color = mix(theme_dict["light"], background, 0.2)
        footer_dark = True
        paint(slide, background)
    else:
        background = theme_dict["bg"]
        color = theme_dict["ink"]
        kicker = theme_dict["kicker"]
        note_color = theme_dict["muted"]
        footer_dark = False
        paint(slide, background)
        rect(slide, 0, 0, W, 0.08, theme_dict["accent"])
    footer(slide, theme_dict, deck, page, total, dark=footer_dark)
    add_text(
        slide, 0.7, 1.15, 11.8, 0.36, spec.get("kicker", "").upper(), theme_dict["font"], 14,
        kicker, True, spacing=180,
    )
    text = spec["text"]
    longest = max(len(part) for part in text.split("\n"))
    if longest <= 14 and text.count("\n") == 0:
        size = 64
    elif longest <= 28:
        size = 40
    else:
        size = 30
    if "Black" in theme_dict["display"] and size > 48 and longest > 10:
        size = 48
    add_text(
        slide, 0.7, 1.8, 11.9, 4.0, text, theme_dict["display"], size, color,
        display_bold(theme_dict), anchor="middle", line_spacing=0.98,
    )
    if spec.get("note"):
        add_text(slide, 0.7, 6.15, 11.8, 0.7, spec["note"], theme_dict["font"], 16, note_color)


def draw_close(slide, theme_dict, deck, spec, page, total):
    light_close = theme_dict["cover"] == "journal"
    if light_close:
        paint(slide, theme_dict["bg"])
        frame(slide, 0.32, 0.28, W - 0.64, H - 0.56, theme_dict["accent"], 0.02)
        title_color = theme_dict["ink"]
        body = theme_dict["ink"]
        kicker = theme_dict["accent"]
        num_bg = theme_dict["accent"]
        num_fg = "FFFFFF"
    elif theme_dict["cover"] in {"poster", "avant"} or theme_dict["statement"] == "accent" and theme_dict["cover"] == "journal":
        paint(slide, theme_dict["accent"])
        title_color = theme_dict["light"]
        body = theme_dict["light"]
        kicker = theme_dict["accent2"]
        num_bg = theme_dict["dark"]
        num_fg = theme_dict["accent2"]
    else:
        paint(slide, theme_dict["dark"])
        title_color = theme_dict["light"] if theme_dict["ussr"] else "FFFFFF"
        body = theme_dict["light"] if theme_dict["ussr"] else "F4F4F4"
        kicker = theme_dict["accent2"] if theme_dict["ussr"] else theme_dict["kicker"]
        num_bg = theme_dict["accent"]
        num_fg = ink_on(num_bg)
    add_text(
        slide, 0.7, 0.42, 10, 0.32, spec.get("kicker", "ИТОГ").upper(), theme_dict["font"], 13,
        kicker, True, spacing=180,
    )
    add_text(
        slide, 0.68, 0.85, 12, 1.15, spec.get("title", "Что запомнить"), theme_dict["display"],
        36, title_color, display_bold(theme_dict),
    )
    items = spec["items"]
    for i, item in enumerate(items):
        y = 2.25 + i * 1.05
        rect(slide, 0.72, y, 0.62, 0.62, num_bg)
        add_text(slide, 0.72, y, 0.62, 0.62, f"{i + 1:02d}", theme_dict["font"], 14, num_fg, True, align="center", anchor="middle")
        add_text(slide, 1.6, y, 10.8, 0.7, item, theme_dict["font"], 18, body, anchor="middle", line_spacing=1.05)
    add_text(
        slide, 0.72, 6.85, 8, 0.3, deck["series"], theme_dict["font"], 12,
        mix(body, "000000", 0.25) if light_close else mix(title_color, "000000" if light_close else theme_dict["dark"], 0.15),
    )
    add_text(
        slide, 9.5, 6.85, 3.1, 0.3, f"{page:02d}   /   {total:02d}", theme_dict["font"], 12,
        kicker, True, align="right",
    )


def render(slide, deck, spec, page, total):
    theme_dict = THEMES[deck["theme"]]
    layout = spec["layout"]
    if layout == "cover":
        draw_cover(slide, theme_dict, deck, spec, total)
    elif layout == "statement":
        draw_statement(slide, theme_dict, deck, spec, page, total)
    elif layout == "close":
        draw_close(slide, theme_dict, deck, spec, page, total)
    else:
        box = chrome(slide, theme_dict, deck, spec, page, total)
        {
            "bullets": draw_bullets,
            "stats": draw_stats,
            "split": draw_split,
            "timeline": draw_timeline,
            "cards": draw_cards,
            "steps": draw_steps,
            "compare": draw_compare,
            "quote": draw_quote,
        }[layout](slide, theme_dict, spec, box)


def build_deck(deck, path):
    prs = Presentation()
    prs.slide_width = Inches(W)
    prs.slide_height = Inches(H)
    prs.core_properties.title = deck["slides"][0]["title"].replace("\n", " ")
    prs.core_properties.subject = deck["series"]
    prs.core_properties.category = "Лекция"
    blank = prs.slide_layouts[6]
    total = len(deck["slides"])
    for index, spec in enumerate(deck["slides"], start=1):
        render(prs.slides.add_slide(blank), deck, spec, index, total)
    prs.save(path)
    return total
