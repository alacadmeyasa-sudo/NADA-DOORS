# -*- coding: utf-8 -*-
"""
مولّد قالب صفحة هبوط "معرض نادا دورز - فرع نجران".
ينتج ملفين:
  1) template/nada-doors-najran-elementor.json  -> قالب قابل للاستيراد في Elementor
  2) index.html                                 -> نسخة معاينة فورية (RTL)
كل البيانات (الهاتف / رابط الواتساب / النصوص) معرّفة في الأعلى لسهولة التعديل.
"""

import json
import random
import string
from urllib.parse import quote

# ------------------------------------------------------------------
# 1) البيانات الأساسية القابلة للتعديل
# ------------------------------------------------------------------
COMPANY        = "معرض نادا دورز"
BRANCH         = "فرع نجران"
PHONE_LOCAL    = "0544072610"
PHONE_INTL     = "966544072610"          # الصيغة الدولية لرابط الواتساب
WA_MESSAGE     = ("السلام عليكم، تواصلت معكم عبر صفحة "
                  + BRANCH + " 🌟 "
                  "وأرغب بالاستفسار عن الأبواب والأسعار المتوفرة")
WA_LINK        = "https://wa.me/" + PHONE_INTL + "?text=" + quote(WA_MESSAGE)
TEL_LINK       = "tel:+" + PHONE_INTL
MAPS_LINK      = "https://www.google.com/maps/search/?api=1&query=" + quote("معرض نادا دورز نجران")

# الألوان (هوية فاخرة تناسب معارض الأبواب)
C_DARK   = "#1c160f"   # بني داكن فاخر
C_DARK2  = "#2b2117"
C_GOLD   = "#c9a24b"   # ذهبي
C_GOLD2  = "#e3c478"
C_CREAM  = "#f7f3ec"
C_TEXT   = "#3a332a"
C_WA     = "#25D366"   # أخضر الواتساب

# أنواع الأبواب المعروضة
PRODUCTS = [
    ("أبواب خشبية فاخرة", "أبواب من خشب طبيعي مصمّمة بأناقة تمنح منزلك دفئاً وفخامة.", "🚪"),
    ("أبواب أمان مصفّحة", "حماية قصوى لمنزلك بأبواب مصفّحة عالية المتانة ومقاومة للكسر.", "🛡️"),
    ("أبواب حديد وليزر", "تصاميم حديد وقص ليزر عصرية تجمع بين القوة والجمال.", "✨"),
    ("أبواب داخلية", "خيارات واسعة من الأبواب الداخلية بألوان وأشكال تناسب كل ديكور.", "🏠"),
    ("أبواب الرئيسية (المدخل)", "أبواب مداخل فخمة تعكس ذوقك من أول لمسة.", "👑"),
    ("أبواب الحمامات (HDF)", "أبواب مقاومة للرطوبة عملية وأنيقة لدورات المياه.", "💧"),
]

FEATURES = [
    ("جودة مضمونة", "خامات أصلية وتشطيب احترافي يدوم لسنوات.", "★"),
    ("تركيب احترافي", "فريق متخصص يضمن لك تركيباً دقيقاً وسريعاً.", "🔧"),
    ("ضمان حقيقي", "ضمان على المنتج والتركيب لراحة بالك.", "✔"),
    ("أسعار منافسة", "أفضل قيمة مقابل السعر في منطقة نجران.", "💎"),
]

# ------------------------------------------------------------------
# 2) أدوات بناء Elementor
# ------------------------------------------------------------------
def eid():
    return "".join(random.choice("0123456789abcdef") for _ in range(7))

def widget(wtype, settings):
    return {"id": eid(), "elType": "widget", "settings": settings,
            "elements": [], "widgetType": wtype}

def column(width, elements, settings=None):
    s = {"_column_size": width, "_inline_size": None}
    if settings:
        s.update(settings)
    return {"id": eid(), "elType": "column", "settings": s, "elements": elements}

def section(columns, settings=None):
    return {"id": eid(), "elType": "section", "settings": settings or {},
            "elements": columns, "isInner": False}

def heading(text, tag="h2", color=C_DARK, size=None, align="center"):
    s = {"title": text, "header_size": tag, "align": align,
         "title_color": color}
    if size:
        s["typography_typography"] = "custom"
        s["typography_font_size"] = {"unit": "px", "size": size, "sizes": []}
        s["typography_font_weight"] = "700"
    return widget("heading", s)

def text(content, color=C_TEXT, align="center", size=16):
    return widget("text-editor", {
        "editor": "<p>" + content + "</p>",
        "align": align,
        "text_color": color,
        "typography_typography": "custom",
        "typography_font_size": {"unit": "px", "size": size, "sizes": []},
    })

def button(label, link, bg=C_GOLD, color=C_DARK, align="center", icon=None):
    s = {
        "text": label,
        "link": {"url": link, "is_external": "true", "nofollow": "",
                 "custom_attributes": ""},
        "align": align,
        "background_color": bg,
        "button_text_color": color,
        "border_radius": {"unit": "px", "top": 50, "right": 50,
                          "bottom": 50, "left": 50, "isLinked": True},
        "text_padding": {"unit": "px", "top": 16, "right": 38,
                         "bottom": 16, "left": 38, "isLinked": False},
        "typography_typography": "custom",
        "typography_font_size": {"unit": "px", "size": 18, "sizes": []},
        "typography_font_weight": "700",
    }
    if icon:
        s["selected_icon"] = {"value": icon, "library": "fa-brands"}
        s["icon_align"] = "right"
    return widget("button", s)

def icon_box(title, desc, emoji):
    """صندوق ميزة/منتج باستخدام نص (يبقى قابلاً للتعديل بسهولة في إليمنتور)."""
    inner = [
        widget("heading", {"title": emoji, "header_size": "div",
                           "align": "center",
                           "typography_typography": "custom",
                           "typography_font_size": {"unit": "px", "size": 46, "sizes": []}}),
        heading(title, tag="h3", color=C_DARK, size=22, align="center"),
        text(desc, color=C_TEXT, align="center", size=15),
    ]
    col_bg = {
        "background_background": "classic",
        "background_color": "#ffffff",
        "border_radius": {"unit": "px", "top": 18, "right": 18,
                          "bottom": 18, "left": 18, "isLinked": True},
        "margin": {"unit": "px", "top": 10, "right": 10, "bottom": 10,
                   "left": 10, "isLinked": True},
        "padding": {"unit": "px", "top": 32, "right": 22, "bottom": 32,
                    "left": 22, "isLinked": False},
        "box_shadow_box_shadow_type": "yes",
        "box_shadow_box_shadow": {"horizontal": 0, "vertical": 12, "blur": 30,
                                  "spread": 0, "color": "rgba(28,22,15,0.10)"},
    }
    return column(33, inner, col_bg)


def grid_section(items, builder, cols_per_row=3, bg=C_CREAM):
    """يبني قسماً يحتوي شبكة من الأعمدة."""
    width = int(100 / cols_per_row)
    columns = []
    for it in items:
        c = builder(*it)
        c["settings"]["_column_size"] = width
        columns.append(c)
    return section(columns, {
        "background_background": "classic",
        "background_color": bg,
        "padding": {"unit": "px", "top": 30, "right": 10, "bottom": 50,
                    "left": 10, "isLinked": False},
        "gap": "extended",
    })


# ------------------------------------------------------------------
# 3) بناء أقسام الصفحة
# ------------------------------------------------------------------
content = []

# --- القسم 1: الهيرو (الواجهة) ---
hero_col = column(100, [
    heading(COMPANY, tag="h1", color="#ffffff", size=54, align="center"),
    heading(BRANCH, tag="h2", color=C_GOLD2, size=30, align="center"),
    text("وجهتك الأولى لأبواب فاخرة بجودة عالية وأسعار تنافسية في منطقة نجران — "
         "تصاميم عصرية، خامات أصلية، وتركيب احترافي بضمان.",
         color="#f0e8d8", align="center", size=19),
    section([  # صف الأزرار
        column(50, [button("تواصل عبر واتساب", WA_LINK, bg=C_WA,
                           color="#ffffff", icon="fab fa-whatsapp")]),
        column(50, [button("اتصل الآن " + PHONE_LOCAL, TEL_LINK, bg=C_GOLD,
                           color=C_DARK)]),
    ], {"gap": "default", "structure": "20"}),
])
content.append(section([hero_col], {
    "background_background": "gradient",
    "background_color": C_DARK,
    "background_color_b": C_DARK2,
    "background_gradient_angle": {"unit": "deg", "size": 135, "sizes": []},
    "padding": {"unit": "px", "top": 90, "right": 20, "bottom": 90,
                "left": 20, "isLinked": False},
    "border_color": C_GOLD,
    "border_border": "solid",
    "border_width": {"unit": "px", "top": 0, "right": 0, "bottom": 5,
                     "left": 0, "isLinked": False},
}))

# --- القسم 2: عنوان المميزات ---
content.append(section([column(100, [
    heading("لماذا تختار " + COMPANY + "؟", tag="h2", color=C_DARK, size=36),
    text("نقدّم لك تجربة متكاملة من الاختيار حتى التركيب", color=C_TEXT, size=18),
])], {"padding": {"unit": "px", "top": 55, "right": 20, "bottom": 10,
                  "left": 20, "isLinked": False},
      "background_background": "classic", "background_color": C_CREAM}))

# --- القسم 3: شبكة المميزات (4 أعمدة) ---
content.append(grid_section(FEATURES, icon_box, cols_per_row=4, bg=C_CREAM))

# --- القسم 4: عنوان المنتجات ---
content.append(section([column(100, [
    heading("منتجاتنا", tag="h2", color=C_DARK, size=36),
    text("تشكيلة واسعة من الأبواب تناسب كل الأذواق والميزانيات",
         color=C_TEXT, size=18),
])], {"padding": {"unit": "px", "top": 55, "right": 20, "bottom": 10,
                  "left": 20, "isLinked": False},
      "background_background": "classic", "background_color": "#ffffff"}))

# --- القسم 5: شبكة المنتجات (3 أعمدة) ---
content.append(grid_section(PRODUCTS, icon_box, cols_per_row=3, bg="#ffffff"))

# --- القسم 6: شريط دعوة للتواصل (CTA) ---
content.append(section([column(100, [
    heading("هل أعجبك تصميم معين؟ تواصل معنا الآن", tag="h2",
            color="#ffffff", size=32),
    text("فريق فرع نجران جاهز للرد على استفساراتك وتقديم أفضل العروض",
         color="#f0e8d8", size=18),
    button("راسلنا على واتساب — " + BRANCH, WA_LINK, bg=C_WA,
           color="#ffffff", icon="fab fa-whatsapp"),
])], {
    "background_background": "gradient",
    "background_color": C_GOLD,
    "background_color_b": "#a9863a",
    "background_gradient_angle": {"unit": "deg", "size": 135, "sizes": []},
    "padding": {"unit": "px", "top": 55, "right": 20, "bottom": 55,
                "left": 20, "isLinked": False},
}))

# --- القسم 7: التواصل والموقع ---
content.append(section([
    column(50, [
        heading("تواصل معنا", tag="h2", color=C_DARK, size=32, align="right"),
        text("📞 الهاتف / واتساب: <a href='" + TEL_LINK + "' style='color:" + C_GOLD + "'>"
             + PHONE_LOCAL + "</a>", color=C_TEXT, align="right", size=18),
        text("📍 الموقع: " + COMPANY + " - " + BRANCH + "، منطقة نجران",
             color=C_TEXT, align="right", size=18),
        text("🕐 أوقات العمل: يومياً من 9 صباحاً حتى 11 مساءً",
             color=C_TEXT, align="right", size=18),
        button("افتح الموقع على الخريطة", MAPS_LINK, bg=C_DARK,
               color="#ffffff", align="right"),
    ]),
    column(50, [
        heading("تواصل سريع", tag="h3", color=C_DARK, size=24, align="center"),
        button("محادثة واتساب فورية", WA_LINK, bg=C_WA, color="#ffffff",
               icon="fab fa-whatsapp"),
        button("اتصال هاتفي مباشر", TEL_LINK, bg=C_GOLD, color=C_DARK),
    ], {
        "background_background": "classic", "background_color": C_CREAM,
        "border_radius": {"unit": "px", "top": 18, "right": 18,
                          "bottom": 18, "left": 18, "isLinked": True},
        "padding": {"unit": "px", "top": 30, "right": 25, "bottom": 30,
                    "left": 25, "isLinked": False},
    }),
], {"padding": {"unit": "px", "top": 55, "right": 20, "bottom": 55,
                "left": 20, "isLinked": False},
    "background_background": "classic", "background_color": "#ffffff"}))

# --- القسم 8: الفوتر ---
content.append(section([column(100, [
    heading(COMPANY + " — " + BRANCH, tag="h3", color=C_GOLD2, size=22),
    text("جميع الحقوق محفوظة © " + COMPANY + " " + BRANCH + " 2026",
         color="#cdbfa6", size=14),
])], {
    "background_background": "classic", "background_color": C_DARK,
    "padding": {"unit": "px", "top": 35, "right": 20, "bottom": 35,
                "left": 20, "isLinked": False},
}))


# ------------------------------------------------------------------
# 4) كتابة قالب Elementor
# ------------------------------------------------------------------
template = {
    "version": "0.4",
    "title": "نادا دورز - فرع نجران (صفحة هبوط)",
    "type": "page",
    "content": content,
    "page_settings": {
        "template": "elementor_canvas",
        "hide_title": "yes",
    },
}

with open("template/nada-doors-najran-elementor.json", "w", encoding="utf-8") as f:
    json.dump(template, f, ensure_ascii=False, indent=2)

print("✓ تم إنشاء قالب Elementor")
print("WhatsApp link:", WA_LINK)
