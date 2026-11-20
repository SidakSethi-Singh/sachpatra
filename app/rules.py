"""Rule definitions and text normalisation for SachPatra.
Deterministic rule engine with 14 rules covering coercion, impersonation,
financial demands, technical abuse, and fraudulent evidence patterns.
"""

import re
import unicodedata
from dataclasses import dataclass
from typing import Callable, Dict, List, Optional, Tuple
from urllib.parse import urlparse


HOMOGLYPH_MAP: Dict[str, str] = {
    # Cyrillic lookalikes to Latin
    "\u0430": "a", "\u0441": "c", "\u0435": "e", "\u0456": "i", "\u0458": "j",
    "\u043e": "o", "\u0440": "p", "\u0455": "s", "\u0445": "x", "\u0443": "y",
    "\u0410": "a", "\u0412": "b", "\u0421": "c", "\u0415": "e", "\u041d": "h",
    "\u0406": "i", "\u0408": "j", "\u041a": "k", "\u041c": "m", "\u041e": "o",
    "\u0420": "p", "\u0422": "t", "\u0425": "x",
    # Greek lookalikes
    "\u03bf": "o", "\u03bd": "v", "\u03c1": "p"
}


def clean_spaced_letters(text: str) -> str:
    """De-obfuscate spaced characters or emoji-spaced letters:
    e.g. 'd i g i t a l   a r r e s t' -> 'digital arrest'
    'd🚨i🚨g🚨i🚨t🚨a🚨l' -> 'digital'
    Preserves natural multi-word phrases and normal single-letter English words.
    """
    # 1. Strip symbols/emojis positioned strictly between single latin letters: 'd🚨i' -> 'di'
    t = re.sub(r"(?<=\b[a-zA-Z])[\-_.*~|•\U00010000-\U0010ffff](?=[a-zA-Z]\b)", "", text)
    # 2. De-space single letters within individual words (separated by 2+ spaces)
    parts = re.split(r"\s{2,}", t)
    new_parts = []
    for p in parts:
        # Join sequences of 3+ single letters separated by single space: e.g. 'c b i' -> 'cbi'
        p2 = re.sub(
            r"\b([a-zA-Z])\s+([a-zA-Z])\s+([a-zA-Z](?:\s+[a-zA-Z])*)\b",
            lambda m: re.sub(r"\s+", "", m.group(0)),
            p
        )
        new_parts.append(p2)
    return " ".join(new_parts)


def normalize_text(text: str) -> str:
    """Normalise text: lowercase, NFKC, de-homoglyph, de-obfuscate spaced letters,
    collapse spaces, strip zero-width chars, and map Devanagari/Gurmukhi digits to ASCII.
    """
    if not text:
        return ""
    # 1. NFKC normalization
    text = unicodedata.normalize("NFKC", text)
    # 2. Lowercase
    text = text.lower()
    # 3. Strip zero-width & invisible formatting characters
    text = re.sub(r"[\u200b\u200c\u200d\u200e\u200f\ufeff\u202a-\u202e]", "", text)
    # 4. Map homoglyphs (Cyrillic / Greek visually identical confusables to ASCII)
    text = "".join(HOMOGLYPH_MAP.get(c, c) for c in text)
    # 5. Map Devanagari (0x0966-0x096F) and Gurmukhi (0x0A66-0x0A6F) digits to ASCII
    for i in range(10):
        dev_char = chr(0x0966 + i)
        gur_char = chr(0x0A66 + i)
        ascii_char = str(i)
        text = text.replace(dev_char, ascii_char)
        text = text.replace(gur_char, ascii_char)
    # 6. De-obfuscate spaced/emoji-separated letters (e.g. 'd i g i t a l' or 'd🚨i🚨g...')
    text = clean_spaced_letters(text)
    # 7. Collapse multiple whitespace characters into single space
    text = re.sub(r"\s+", " ", text).strip()
    return text


SHORTENER_DOMAINS = {
    "bit.ly", "tinyurl.com", "t.co", "cutt.ly", "rb.gy", "is.gd",
    "ow.ly", "rebrand.ly", "shorturl.at", "gg.gg", "v.gd"
}

GOV_KEYWORDS = (
    "cbi", "police", "court", "cyber", "rbi", "trai", "echallan",
    "parivahan", "incometax", "gov-in", "gov-india", "highcourt"
)


def check_suspicious_links(text: str) -> Optional[Tuple[int, int]]:
    """R11 Link check by code:
    Detects shortened URLs (bit.ly, tinyurl, etc.) or government-looking domains
    that do NOT end in legitimate Indian official TLDs (.gov.in or .nic.in).
    Returns (start, end) span of first match if found.
    """
    url_pattern = re.compile(
        r"(https?://[^\s<>\"'()]+|www\.[^\s<>\"'()]+|[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(?:/[^\s<>\"'()]*)?)",
        re.IGNORECASE
    )
    for match in url_pattern.finditer(text):
        raw_url = match.group(0).rstrip(".,;:!?)'\"")
        start = match.start()
        end = start + len(raw_url)

        # Parse host
        parse_target = raw_url if raw_url.startswith(("http://", "https://")) else "http://" + raw_url
        try:
            parsed = urlparse(parse_target)
            host = (parsed.hostname or "").lower().rstrip(".")
        except Exception:
            host = raw_url.split("/")[0].lower().rstrip(".")

        if not host:
            continue

        # Condition 1: URL shortener
        for short in SHORTENER_DOMAINS:
            if host == short or host.endswith("." + short):
                return (start, end)

        # Condition 2: Impersonates government keywords but is NOT .gov.in or .nic.in
        has_gov_keyword = any(k in host for k in GOV_KEYWORDS)
        is_official = host.endswith(".gov.in") or host.endswith(".nic.in")
        if has_gov_keyword and not is_official:
            return (start, end)

    return None


@dataclass
class Rule:
    id: str
    category: str
    weight: int
    patterns: Dict[str, str]  # keys: "en", "hi", "pa", "hinglish"
    hard: bool = False
    custom_checker: Optional[Callable[[str], Optional[Tuple[int, int]]]] = None


RULES: List[Rule] = [
    Rule(
        id="R01",
        category="coercion",
        weight=40,
        hard=True,
        patterns={
            "en": r"\b(?:digital|virtual|online)\s*(?:arrest(?:ed)?|custody|detention)\b",
            "hi": r"(?:डिजिटल|वर्चुअल|ऑनलाइन)\s*(?:अरेस्ट|गिरफ्तारी|नज़रबंदी|हिरासत)",
            "pa": r"(?:ਡਿਜੀਟਲ|ਵਰਚੁਅਲ|ਆਨਲਾਈਨ)\s*(?:ਗ੍ਰਿਫ਼ਤਾਰੀ|ਗ੍ਰਿਫਤਾਰੀ|ਅਰੈਸਟ|ਨਜ਼ਰਬੰਦੀ|ਹਿਰਾਸਤ)",
            "hinglish": r"\b(?:digital|virtual|online)\s*(?:arrest(?:ed)?|giraftari|giraftaari|hiraasat|nazarbandi|custody)\b",
        }
    ),
    Rule(
        id="R02",
        category="coercion",
        weight=25,
        hard=False,
        patterns={
            "en": r"\b(?:stay\s+on\s+(?:the\s+)?(?:video|skype|whatsapp)?\s*call|do\s+not\s+(?:disconnect|cut|hang\s*up)\s+(?:the\s+)?(?:video|skype|whatsapp|voice)?\s*call|keep\s+(?:your\s+)?camera\s+(?:on|open)|remain\s+on\s+(?:the\s+)?(?:line|call)|continuous\s+video\s+monitoring)\b",
            "hi": r"(?:वीडियो\s*कॉल\s*(?:पर\s*रहें|चालू\s*रखें|काटना\s*मत)|कैमरा\s*(?:ऑन|चालू)\s*रखें|कॉल\s*(?:डिस्कनेक्ट|कट|काटना|बंद)\s*(?:मत|ना)\s*(?:करना)?|लाइन\s*पर\s*बने\s*रहें)",
            "pa": r"(?:ਵੀਡੀਓ\s*ਕਾਲ\s*(?:'ਤੇ|ਤੇ)\s*ਰਹੋ|ਕੈਮਰਾ\s*(?:ਆਨ|ਚਾਲੂ)\s*ਰੱਖੋ|ਕਾਲ\s*(?:ਨਾ\s*ਕੱਟੋ|ਬੰਦ\s*ਨਾ\s*ਕਰੋ)|ਲਾਈਨ\s*'ਤੇ\s*ਬਣੇ\s*ਰਹੋ)",
            "hinglish": r"(?:video\s*call\s*(?:pe\s*raho|chalu\s*rakho|par\s*raho|pe\s*bane\s*raho)|call\s*(?:cut\s*mat\s*karna|disconnect\s*mat\s*karo|mat\s*kaatna|mat\s*karna)|camera\s*(?:on\s*rakho|chalu\s*rakho))",
        }
    ),
    Rule(
        id="R03",
        category="impersonation",
        weight=15,
        hard=False,
        patterns={
            "en": r"\b(?:cbi|central\s+bureau\s+of\s+investigation|enforcement\s+directorate|\bed\s+officer\b|\bed\s+directorate\b|ncb|narcotics\s+control\s+bureau|trai|telecom\s+regulatory\s+authority|telecom\s+department|\brbi\b|\brbi\s+offic(?:er|ial|account)?\b|customs\s+department|customs\s+offic(?:er|ial)|cyber\s+crime\s+cell|cyber\s+cell|delhi\s+police|mumbai\s+police|crime\s+branch|dsp\b|supreme\s+court(?:\s+of\s+india)?|narcotics\s+(?:department|cell)|nia|national\s+investigation\s+agency)\b",
            "hi": r"(?:सीबीआई|केंद्रीय\s*जांच\s*ब्यूरो|प्रवर्तन\s*निदेशालय|ईडी\s*अधिकारी|नारकोटिक्स\s*(?:कंट्रोल\s*ब्यूरो|सेल|विभाग)|एनसीबी|ट्राई|दूरसंचार\s*विभाग|आरबीआई|कस्टम\s*विभाग|सीमा\s*शुल्क|साइबर\s*(?:क्राइम\s*)?सेल|सुप्रीम\s*कोर्ट|दिल्ली\s*पुलिस|मुंबई\s*पुलिस|क्राइम\s*ब्रांच|डीएसपी|पुलिस\s*(?:विभाग|अधिकारी)?)",
            "pa": r"(?:ਸੀਬੀਆਈ|ਇਨਫੋਰਸਮੈਂਟ\s*ਡਾਇਰੈਕਟੋਰੇਟ|ਈਡੀ|ਨਾਰਕੋਟਿਕਸ\s*(?:ਬਿਊਰੋ|ਸੈੱਲ|ਵਿਭਾਗ)|ਐਨਸੀਬੀ|ਟਰਾਈ|ਦੂਰਸੰਚਾਰ\s*ਵਿਭਾਗ|ਆਰਬੀਆਈ|ਕਸਟਮ\s*ਵਿਭਾਗ|ਸਾਈਬਰ\s*ਸੈੱਲ|ਸੁਪਰੀਮ\s*ਕੋਰਟ|ਦਿੱਲੀ\s*ਪੁਲਿਸ|ਮੁੰਬਈ\s*ਪੁਲਿਸ|ਕ੍ਰਾਈਮ\s*ਬ੍ਰਾਂਚ|ਡੀਐਸਪੀ|ਪੁਲਿਸ)",
            "hinglish": r"\b(?:cbi\s*(?:officer|dept|branch)?|ed\s*officer|ncb\s*officer|trai\s*(?:official|department)?|telecom\s*department|customs\s*department|cyber\s*crime\s*cell|cyber\s*cell|delhi\s*police|mumbai\s*police|crime\s*branch|dsp|supreme\s*court)\b",
        }
    ),
    Rule(
        id="R04",
        category="allegation",
        weight=20,
        hard=False,
        patterns={
            "en": r"(?:\b(?:parcel|courier|shipment|consignment|package)\b.*?\b(?:drugs|narcotics|mdma|contraband|illegal\s+items|fake\s+passports|passports)\b|\b(?:drugs|mdma|contraband|narcotics)\b.*?\b(?:parcel|courier|package|shipment)\b|\b(?:fedex|dhl|india\s+post)\s+(?:parcel|package|courier)\s+(?:detained|seized|intercepted)\b)",
            "hi": r"(?:(?:पार्सल|कूरियर|पैकेट).*?(?:ड्रग्स|नशीली\s*दवा|नशीले\s*पदार्थ|एमडीएमए|पासपोर्ट|अवैध\s*सामान|प्रतिबंधित)|(?:ड्रग्स|नशीली\s*दवा|नशीले\s*पदार्थ).*?(?:पार्सल|कूरियर|पैकेट)|(?:फेडेक्स|डीएचएल|कूरियर)\s*(?:जब्त|पकड़ा\s*गया))",
            "pa": r"(?:(?:ਪਾਰਸਲ|ਕੋਰੀਅਰ|ਪੈਕਟ).*?(?:ਨਸ਼ੀਲੀਆਂ\s*ਦਵਾਈਆਂ|ਨਸ਼ੀਲਾ\s*ਸਾਮਾਨ|ਡਰੱਗਜ਼|ਪਾਸਪੋਰਟ|ਗੈਰ-ਕਾਨੂੰਨੀ\s*ਸਾਮਾਨ)|(?:ਨਸ਼ੀਲੀਆਂ\s*ਦਵਾਈਆਂ|ਡਰੱਗਜ਼).*?(?:ਪਾਰਸਲ|ਕੋਰੀਅਰ)|(?:ਫੈਡਐਕਸ|ਕੋਰੀਅਰ)\s*(?:ਜ਼ਬਤ|ਫੜਿਆ\s*ਗਿਆ))",
            "hinglish": r"(?:(?:parcel|courier)\s*(?:me|mai)\s*(?:drugs|nasha|passport|contraband|illegal\s*saman)|(?:parcel|courier)\s*(?:pakda\s*gaya|seize\s*hua|detain\s*hua|intercept))",
        }
    ),
    Rule(
        id="R05",
        category="payment",
        weight=30,
        hard=True,
        patterns={
            "en": r"\b(?:(?:pay|transfer)\s+.*?\b(?:safe|rbi|government|verification|clearance|holding)\b.*?\baccount|pay\s+(?:[\d,]+\s*(?:rupees|inr|rs\.?)|(?:rs\.?|inr|₹)\s*[\d,]+|fine|bail|penalty|verification\s+fee|security\s+deposit|amount|charges)|transfer\s+.*?\baccount|refundable\s+(?:security\s+)?deposit|security\s+bond\s+amount|bail\s+(?:money|amount|fee)|settlement\s+amount|verification\s+amount|clearance\s+fund)\b",
            "hi": r"(?:(?:जुर्माना|जमानत\s*राशि|सत्यापन\s*शुल्क|सुरक्षा\s*राशि|सत्यापन\s*राशि).*?(?:भरें|जमा|भुगतान|ट्रांसफर|भेजें)|(?:सुरक्षित\s*खाते|आरबीआई\s*खाते|सरकारी\s*खाते).*?(?:ट्रांसफर|पैसे|जमा|भेजें)|(?:रिफंडेबल|सिक्योरिटी)\s*डिपॉजिट|क्लियरेंस\s*फंड)",
            "pa": r"(?:(?:ਜੁਰਮਾਨਾ|ਜ਼ਮਾਨਤ\s*ਰਾਸ਼ੀ|ਤਸਦੀਕ\s*ਫੀਸ).*?(?:ਭਰੋ|ਜਮ੍ਹਾਂ|ਭੁਗਤਾਨ|ਟਰਾਂਸਫਰ|ਭੇਜੋ)|(?:ਸੁਰੱਖਿਅਤ\s*ਖਾਤੇ|ਆਰਬੀਆਈ\s*ਖਾਤੇ|ਸਰਕਾਰੀ\s*ਖਾਤੇ).*?(?:ਟਰਾਂਸਫਰ|ਪੈਸੇ|ਭੇਜੋ|ਜਮ੍ਹਾਂ)|ਰਿਫੰਡੇਬਲ\s*ਡਿਪਾਜ਼ਿਟ)",
            "hinglish": r"(?:(?:fine|bail\s*(?:amount|fee)|penalty|verification\s*fee|security\s*deposit|verification\s*amount).*?(?:bharo|pay\s*karo|dena\s*hoga|jama\s*karo|pay\s*karna|deposit\s*(?:kijiye|karo))|(?:safe\s*account|rbi\s*account|government\s*account).*?(?:me\s*transfer|me\s*bhejo|mai\s*daalo))",
        }
    ),
    Rule(
        id="R06",
        category="coercion",
        weight=20,
        hard=False,
        patterns={
            "en": r"\b(?:do\s+not\s+tell\s+(?:anyone|your\s+family|family|friends)|keep\s+(?:this\s+)?(?:matter\s+)?(?:confidential|secret)|secret\s+from\s+family|strictly\s+confidential|national\s+security\s+secret|close\s+(?:the\s+)?door|isolated\s+room|stay\s+alone\s+in\s+(?:the\s+)?room)\b",
            "hi": r"(?:किसी\s*को\s*(?:मत|नहीं|न|ना)\s*(?:बताना|बताएं|बताओ|बताइए)|परिवार\s*को\s*(?:मत|नहीं|न|ना)\s*(?:बताओ|बताएं|जानकारी\s*न\s*दें)|गोपनीय\s*(?:मामला|केस)|कमरा\s*बंद\s*(?:रखें|करके\s*रहें|करो)|कमरे\s*का\s*दरवाज़?ा\s*बंद|अकेले\s*(?:कमरे\s*में\s*)?रहें)",
            "pa": r"(?:ਕਿਸੇ\s*ਨੂੰ\s*(?:ਨਾ\s*ਦੱਸੋ|ਨਹੀਂ\s*ਦੱਸਣਾ)|ਪਰਿਵਾਰ\s*ਨੂੰ\s*(?:ਕੁਝ\s*ਵੀ\s*|ਬਿਲਕੁਲ\s*)?ਨਾ\s*ਦੱਸੋ|ਗੁਪਤ\s*(?:ਕੇਸ|ਮਾਮਲਾ)|ਕਮਰਾ\s*ਬੰਦ\s*(?:ਰੱਖੋ|ਕਰਕੇ\s*ਰਹੋ)|ਇਕੱਲੇ\s*(?:ਕਮਰੇ\s*ਵਿੱਚ\s*)?ਰਹੋ)",
            "hinglish": r"(?:kisi\s*ko\s*(?:mat\s*(?:batana|bataye)|nahi\s*batana)|family\s*ko\s*(?:mat\s*batao|kuch\s*mat\s*bolna)|confidential\s*(?:case|matter|call)|room\s*ka\s*door\s*close\s*rakho|akela\s*raho)",
        }
    ),
    Rule(
        id="R07",
        category="urgency",
        weight=15,
        hard=False,
        patterns={
            "en": r"\b(?:arrest\s+(?:warrant\s+issued|within\s+\d+\s+hours?|in\s+\d+\s+hours?)|immediate\s+arrest|non-bailable\s+warrant|(?:sim|number|mobile)\s+.*?\b(?:blocked|disconnected|terminated)\s+(?:within|in)\s+\d+\s+hours?|disconnected\s+within\s+\d+\s+hours?|within\s+1\s+hour)\b",
            "hi": r"(?:गिरफ्तारी\s*वारंट|तत्काल\s*गिरफ्तारी|(?:अगले\s*)?\d+\s*घंटे\s*में\s*(?:गिरफ्तारी|ब्लॉक|बंद|घर\s*पहुंचेगी)|(?:सिम|मोबाइल|नंबर)\s*.*?(?:अगले\s*)?\d+\s*घंटे\s*में\s*(?:ब्लॉक|बंद)|गैर-जमानती\s*वारंट|तुरंत\s*कार्रवाई|वारंट\s*जारी)",
            "pa": r"(?:ਗ੍ਰਿਫ਼ਤਾਰੀ\s*ਵਾਰੰਟ|ਤੁਰੰਤ\s*ਗ੍ਰਿਫ਼ਤਾਰੀ|\d+\s*ਘੰਟਿਆਂ\s*ਵਿੱਚ\s*(?:ਗ੍ਰਿਫ਼ਤਾਰੀ|ਬਲਾਕ|ਜੁਰਮਾਨਾ)|(?:ਸਿਮ|ਮੋਬਾਈਲ|ਨੰਬਰ)\s*.*?\d+\s*ਘੰਟਿਆਂ\s*ਵਿੱਚ\s*(?:ਬਲਾਕ|ਬੰਦ)|ਗੈਰ-ਜ਼ਮਾਨਤੀ\s*ਵਾਰੰਟ)",
            "hinglish": r"(?:arrest\s*warrant\s*(?:nikla|jari|nikal\s*rahi|issue\s*ho)|turant\s*arrest|(?:sim|mobile|phone|number)\s*.*?(?:block|band|terminate).*?(?:in\s*\d+\s*hours?|\d+\s*ghante\s*me)|(?:in|\d+)\s*(?:ghante|hours?)\s*(?:me\s*)?(?:arrest|sim\s*block|phone\s*band|block\s*ho)|non-bailable\s*warrant)",
        }
    ),
    Rule(
        id="R08",
        category="allegation",
        weight=15,
        hard=False,
        patterns={
            "en": r"\b(?:aadhaar\s+(?:card\s+)?.*?\b(?:misused|used\s+in|linked\s+to)\b.*?\b(?:crime|fraud|terror|money\s+laundering|cyber)|sim\s+(?:card\s+)?.*?\b(?:used\s+in|linked\s+to|registered\s+for)\b.*?\b(?:crime|illegal|fraud|terror|cyber)|bank\s+account\s+opened\s+in\s+your\s+name)\b",
            "hi": r"(?:आधार\s*(?:कार्ड\s*)?.*?(?:दुरुपयोग|शामिल|जुड़ा)|आपका\s*सिम\s*.*?(?:अपराध|धोखाधड़ी|साइबर)\s*में\s*शामिल|आपके\s*नाम\s*पर\s*(?:फर्जी|अवैध)\s*बैंक\s*खाता)",
            "pa": r"(?:ਆਧਾਰ\s*(?:ਕਾਰਡ\s*)?.*?(?:ਦੁਰਵਰਤੋਂ|ਸ਼ਾਮਲ)|ਤੁਹਾਡਾ\s*ਸਿਮ\s*.*?(?:ਅਪਰਾਧ|ਧੋਖਾਧੜੀ)\s*ਵਿੱਚ\s*ਸ਼ਾਮਲ|ਤੁਹਾਡੇ\s*ਨਾਮ\s*'ਤੇ\s*ਜਾਅਲੀ\s*ਬੈਂਕ\s*ਖਾਤਾ)",
            "hinglish": r"(?:aadhaar\s*(?:card\s*)?.*?(?:misuse\s*hua|fraud\s*me|used)|aapka\s*sim\s*.*?(?:crime\s*me|fraud\s*me)|farzi\s*bank\s*account\s*khula)",
        }
    ),
    Rule(
        id="R09",
        category="payment",
        weight=25,
        hard=False,
        patterns={
            "en": r"\b(?:pay\s+.*?\bupi\b|transfer\s+to\s+(?:personal|private)\s+account|send\s+money\s+to\s+upi|upi\s+id\b|gpay|phonepe\s+number)\b",
            "hi": r"(?:यूपीआई\s*(?:आईडी\s*)?(?:पर|में).*?(?:पैसे\s*भेजें|भुगतान|भेजें|जमानत)|(?:निजी|व्यक्तिगत)\s*(?:बैंक\s*)?(?:खाते|यूपीआई)\s*में.*?ट्रांसफर|व्यक्तिगत\s*(?:खाते|यूपीआई)\s*में)",
            "pa": r"(?:ਯੂਪੀਆਈ\s*ਆਈਡੀ\s*'ਤੇ.*?(?:ਪੈਸੇ\s*ਭੇਜੋ|ਟਰਾਂਸਫਰ)|ਨਿੱਜੀ\s*(?:ਬੈਂਕ\s*)?ਖਾਤੇ\s*ਵਿੱਚ.*?ਟਰਾਂਸਫਰ)",
            "hinglish": r"(?:personal\s*upi|upi\s*id\s*(?:pe\s*bhejo|par\s*transfer|pe\s*pay)|personal\s*account\s*me\s*(?:transfer|daalo)|gpay\s*karo|phonepe\s*karo)",
        }
    ),
    Rule(
        id="R10",
        category="tech_abuse",
        weight=30,
        hard=True,
        patterns={
            "en": r"\b(?:(?:share|tell|give|provide)\s+(?:the\s+)?(?:otp|\d+-digit\s+code)|download\s+(?:anydesk|teamviewer|quicksupport|rustdesk)|install\s+(?:anydesk|teamviewer|quicksupport|rustdesk)|remote\s+access\s+app|screen\s+sharing\s+app)\b",
            "hi": r"(?:ओटीपी\s*(?:बताएं|शेयर\s*करें|दें)|\d+\s*अंकों\s*का\s*कोड\s*बताएं|एनीडेस्क|टीमव्यूअर|रस्टडेस्क\s*(?:डाउनलोड|इंस्टॉल)|स्क्रीन\s*शेयर|रिमोट\s*(?:सपोर्ट|एक्सेस)\s*(?:ऐप)?)",
            "pa": r"(?:ਓਟੀਪੀ\s*(?:ਦੱਸੋ|ਦਿਓ|ਸਾਂਝਾ\s*ਕਰੋ)|\d+\s*ਅੰਕਾਂ\s*ਦਾ\s*ਕੋਡ|ਐਨੀਡੈਸਕ|ਟੀਮਵਿਊਅਰ\s*(?:ਡਾਊਨਲੋਡ|ਇੰਸਟਾਲ)|ਸਕ੍ਰੀਨ\s*ਸ਼ੇਅਰ)",
            "hinglish": r"(?:otp\s*(?:batao|share\s*karo|do|send\s*karo)|(?:anydesk|teamviewer|quicksupport|rustdesk)\s*(?:download|install)\s*karo)",
        }
    ),
    Rule(
        id="R11",
        category="suspicious_link",
        weight=20,
        hard=False,
        patterns={},
        custom_checker=check_suspicious_links
    ),
    Rule(
        id="R12",
        category="impersonation",
        weight=15,
        hard=False,
        patterns={
            "en": r"\b(?:contacting\s+.*?\b(?:whatsapp|skype|telegram)|police\s+officer\s+on\s+whatsapp|officer\s+calling\s+from\s+skype|telegram\s+.*?\bcall\s+from\s+officer|whatsapp\s+video\s+statement|connect\s+with\s+.*?\bofficer\s+on\s+skype|notice\s+(?:sent\s+)?via\s+(?:whatsapp|skype|telegram))\b",
            "hi": r"(?:व्हाट्सएप\s*(?:पर\s*(?:पुलिस\s*)?(?:कॉल|संपर्क|वीडियो\s*कॉल))|स्काइप\s*पर\s*(?:पुलिस|अधिकारी)\s*कॉल|टेलीग्राम\s*पर\s*(?:अधिकारी|कॉल))",
            "pa": r"(?:ਵਟਸਐਪ\s*(?:'ਤੇ\s*(?:ਪੁਲਿਸ\s*)?(?:ਸੰਪਰਕ|ਵੀਡੀਓ\s*ਕਾਲ|ਕਾਲ))|ਸਕਾਈਪ\s*'ਤੇ\s*ਪੁਲਿਸ\s*ਕਾਲ|ਟੈਲੀਗ੍ਰਾਮ\s*'ਤੇ\s*ਕਾਲ)",
            "hinglish": r"(?:whatsapp\s*(?:pe\s*call|par\s*officer|video\s*call\s*pe\s*statement)|skype\s*pe\s*police|telegram\s*call|notice\s*(?:via|pe)\s*whatsapp)",
        }
    ),
    Rule(
        id="R13",
        category="forgery",
        weight=15,
        hard=False,
        patterns={
            "en": r"\b(?:(?:account\s+)?freeze\s+order|asset\s+seizure\s+order|arrest\s+warrant\s+copy|surveillance\s+order|official\s+seal\s+attached|order\s+sent\s+on\s+(?:whatsapp|chat|telegram)|court\s+clearance\s+certificate|summons\s+sent\s+via\s+whatsapp)\b",
            "hi": r"(?:खाता\s*(?:सीज|फ्रीज)\s*आदेश|जब्ती\s*का\s*आदेश|व्हाट्सएप\s*पर\s*(?:वारंट|नोटिस|आदेश)|सील\s*लगा\s*(?:पत्र|दस्तावेज)|गिरफ्तारी\s*वारंट\s*की\s*कॉपी)",
            "pa": r"(?:ਖਾਤਾ\s*ਫਰੀਜ਼\s*ਆਰਡਰ|ਜ਼ਬਤੀ\s*ਦਾ\s*ਹੁਕਮ|ਵਟਸਐਪ\s*'ਤੇ\s*(?:ਨੋਟਿਸ|ਵਾਰੰਟ)|ਮੋਹਰ\s*ਵਾਲਾ\s*ਪੱਤਰ|ਗ੍ਰਿਫ਼ਤਾਰੀ\s*ਵਾਰੰਟ\s*ਦੀ\s*ਕਾਪੀ)",
            "hinglish": r"(?:freeze\s*order|arrest\s*warrant\s*copy|whatsapp\s*pe\s*(?:notice|order\s*bheja)|official\s*seal\s*laga\s*hua|attachment\s*order)",
        }
    ),
    Rule(
        id="R14",
        category="allegation",
        weight=15,
        hard=False,
        patterns={
            "en": r"\b(?:money\s+laundering|\bpmla(?:\s+act)?\b|canara\s+bank\s+(?:\w+\s+)?(?:fraud|case|scam)|naresh\s+goyal|jet\s+airways\s+scam|hawala\s+(?:racket|transactions?|money)|illegal\s+foreign\s+remittance)\b",
            "hi": r"(?:मनी\s*लॉन्ड्रिंग|केनरा\s*बैंक\s*(?:घोटाला|फ्रॉड|केस)|नरेश\s*गोयल|हवाला\s*(?:लेनदेन|कारोबार)|अवैध\s*विदेशी\s*लेन-देन)",
            "pa": r"(?:ਮਨੀ\s*ਲਾਂਡਰਿੰਗ|ਕੈਨਰਾ\s*ਬੈਂਕ\s*(?:ਘੁਟਾਲਾ|ਫਰਾਡ)|ਨਰੇਸ਼\s*ਗੋਇਲ|ਹਵਾਲਾ\s*(?:ਲੈਣ-ਦੇਣ|ਕਾਰੋਬਾਰ))",
            "hinglish": r"(?:money\s*laundering|canara\s*bank\s*(?:fraud|scam|case)|naresh\s*goyal|hawala\s*(?:ka\s*paisa|transaction))",
        }
    ),
]
