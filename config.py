# random -> مكتبة بتخليك تختار عشوائي سواء كانت من ليستاية او رقم واستعملناها في اللابات
# time -> بتحسب الوقت اللي بيعدي هنحتاجها في الواجهة 
# tkinter -> دي مكتبة بتاعت بايثون استخدمناها عشان نعمل الواجهة الاساسية لو محدش غيرها
N, TIME_LIMIT, NUM_WORDS, MAX_EFFORT = 8, 300, 10, 1000
# N -> grid size aka 8*8 , TIME_LIMIT -> literally time limit in seconds
# NUM_WORDS ->  عدد الكلام المستعمل في اللعبة انا شايف انو 10 احسن حاجة عشان هتوضح ليه بنفضل ستايلات على ستايلات تانية 
# MAX_EFFORT -> اعلى عدد من محاولات انك تحط كلمة في اماكن مختلفة 
HINT_COST = 5   # points taken off for each hint
POOL = ["HOUSE", "WATER", "APPLE", "TABLE", "CHAIR", "MUSIC", "LIGHT", "PHONE", "BREAD",
        "GREEN", "SMILE", "RIVER", "CLOUD", "PLANT", "TRAIN", "SUGAR", "MONEY", "HAPPY",
        "SUMMER", "WINTER", "GARDEN", "FRIEND", "FAMILY", "SCHOOL", "WINDOW", "DOCTOR",
        "ORANGE", "KITCHEN", "MORNING", "COUNTRY", "BIRTHDAY", "MOUNTAIN", "ANIMAL"]
# هنا زود كلام براحتك في الليستاية دي اهم حاجة الكلمة متعديش ال 8 حروف
DIRS = [(0, 1), (1, 0), (1, 1), (-1, 1), (0, -1), (-1, 0), (-1, -1), (1, -1)]
# دي الاتجهات هنحتاجها في المعادلة تحت على طول

# ---- الألوان: كلها هنا وتقدر تغيّر أي واحد ----
BG          = "#faf7f1"   # خلفية الشاشة (كريمي)
TILE        = "#ebe3d2"   # الخانة العادية
TILE_EDGE   = "#d6cbb3"
TILE_HOVER  = "#e2d8c3"   # لما الماوس يعدي على خانة
INK         = "#2a2118"   # لون الكلام
MUTED       = "#8a7f6f"
GREEN       = "#6cbb8a"   # الكلمة اللي اتلقت
GREEN_DARK  = "#4f9b6d"
ORANGE      = "#f0a35e"   # السحب
BTN         = "#d96a1f"   # زرار New Game
BTN_HOVER   = "#c25a14"
HINT_FILL   = "#fbe3c4"   # الحرف الأول بتاع التلميح
HINT_EDGE   = "#e8944a"
MISS_FILL   = "#f9d6d6"   # الكلمات اللي متلقتش بعد ما الوقت يخلص
MISS_EDGE   = "#d64545"
PANEL       = "#e6e9ef"   # بانل الكلمات
PANEL_EDGE  = "#c8cfdb"
TRACK       = "#e8e0d4"
NAVY        = "#1f2937"
RED         = "#d64545"
WHITE       = "#ffffff"

# ألوان مختلفة لكل كلمة تتلقي
WORD_COLORS = [
    "#57b880",  #green
    "#4c9be8",  #blue
    "#e06c75",  #red
    "#9b72cf",  #purple
    "#3aa89e",  #teal
    "#d97b38",  #orange
    "#d4609c",  #pink
    "#6d8ce8",  #sky blue
    "#82ad49",  #lime
    "#c98a2c",  #yellow
]

BALLOON_COLORS = ["#f0a35e", "#6cbb8a", "#e86a6a", "#6ab0f0", "#f2d45c", "#b48be8"]

# ---- الفونت ----
FONT = "Segoe UI"         # بدائل: "Bahnschrift", "Trebuchet MS"

# ---- المقاسات ----
T, G, PAD = 56, 6, 4      # حجم الخانة، المسافة بين الخانات، الهامش
BOARD_W = N * T + (N - 1) * G + 2 * PAD
CONTENT_W = 620           # عرض بانل الكلمات
COLS = 5                  # عدد الكلمات في الصف
