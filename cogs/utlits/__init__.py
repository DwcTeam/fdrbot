
times = {1800: "30m", 3600: "1h", 7200: "2h",
             21600: "6h", 43200: "12h", 86400: "24h"}

def convert_number_to_000(number: int) -> str:
    if number < 10:
        return "00" + str(number)
    elif number < 100:
        return "0" + str(number)
    else:
        return str(number)

def between_two_numbers(num: int, a: int, b: int):
    """
    True if the number is between the two numbers, False if not
    """
    if a < num and num < b: 
        return True
    else: 
        return False


HELP_DATA = {
    "main": {
        "title": "الصفحة الرئيسية",
        "description": ("**بسم الله الرحمن الرحيم**\n"
                    "بوت فاذكروني اول بوت عربي اسلامي للأذكار, البوت "
                    "يمكنه تشغيل القرآن الكريم بالقنوات الصوتيه و أرسال الأذكار"
                    "و الأدعية بشكل دوري, البوت غير ربحي و اهدافه خالصه لله عز و جل."
                    "\n\nيمكنك من الأسفل أختيار الأوامر"
                    ),
        "cog": None
    },
    "general": {
        "title": "الأوامر العامة",
        "description": "يمكن للعامة أستخدامها و متاحة للجميع",
        "cog": "general"
    },
    "moshaf": {
        "title": "أوامر المصحف الشريف", 
        "description": "يمكن ل أوامر المصحف الشريف فتح القرآن الكريم بالصور و أيضاً تثبيت رساله للمصحف",
        "cog": "moshaf"
    },
    "hijri": {
        "title": "أوامر التاريخ الهجري",
        "description": "يمكن ل أوامر التاريخ الهجري تحويل التاريخ الهجري إلى التاريخ الميلادي و عكسه",
        "cog": "hijri"
    },
    "quran_voice": {
        "title": "أوامر القرآن الكريم الصوتية",
        "description": "يمكن ل أوامر القرآن الكريم الصوتية تشغيل القرآن الكريم بالصوت بأكثر من 150 قارئ مختلف و تشغيل أكثر من 150 أذاعة مخصصة للقرآن الكريم",
        "cog": "quran"
    },
    "admin": {
        "title": "أوامر مشرفي السيرفر",
        "description": "يمكن ل أوامر مشرفي السيرفر تحديد تحديد قناة أرسال الأدعية و الأذان و العديد من الأمور **(للمشرفين فقط)**",
        "cog": "set"
    },
    "hadith": {
        "title": "أوامر الحديث النبوي الشريف",
        "description": "يمكن ل أوامر الحديث النبوي الشريف البحث عن الحديث و التحقق منه و الحصول على حديث بشكل عشوائي",
        "cog": "hadith"
    },
    "tafsir": {
        "title": "أوامر تفسير المصحف الشريف",
        "description": "يمكن ل أوامر تفسير المصحف الشريف فتح بطاقات تفسير سور القرآن الكريم و أيضاً البحث عن تفسير كلمة محددة",
        "cog": "tafsir"
    }
}
