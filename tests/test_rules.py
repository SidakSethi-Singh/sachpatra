"""Unit tests for deterministic rules across English, Hindi, Punjabi, and Hinglish."""

import pytest
from app.engine import evaluate_rules, normalize_text
from app.rules import RULES, check_suspicious_links


def run_rule(rule_id: str, text: str) -> bool:
    norm = normalize_text(text)
    fired = evaluate_rules(text, norm)
    return any(r.id == rule_id for r, _ in fired)


class TestRulesMultilingual:
    # R01: Digital arrest
    def test_r01_positive(self):
        assert run_rule("R01", "You are under digital arrest by the cyber cell.")
        assert run_rule("R01", "आपको तुरंत डिजिटल अरेस्ट किया जाता है।")
        assert run_rule("R01", "ਤੁਹਾਨੂੰ ਡਿਜੀਟਲ ਗ੍ਰਿਫ਼ਤਾਰੀ ਅਧੀਨ ਲਿਆ ਗਿਆ ਹੈ।")
        assert run_rule("R01", "Aap par digital arrest laga diya gaya hai.")

    def test_r01_negative(self):
        assert not run_rule("R01", "This is a digital signature on your invoice.")
        assert not run_rule("R01", "डिजिटल इंडिया कार्यक्रम की प्रगति।")
        assert not run_rule("R01", "ਡਿਜੀਟਲ ਪੰਜਾਬ ਮਿਸ਼ਨ ਤਹਿਤ ਸੇਵਾਵਾਂ।")

    # R02: Stay on video call
    def test_r02_positive(self):
        assert run_rule("R02", "Stay on the video call and keep your camera on.")
        assert run_rule("R02", "वीडियो कॉल पर रहें और कैमरा चालू रखें।")
        assert run_rule("R02", "ਵੀਡੀਓ ਕਾਲ 'ਤੇ ਰਹੋ ਅਤੇ ਕੈਮਰਾ ਆਨ ਰੱਖੋ।")
        assert run_rule("R02", "Video call pe raho aur call cut mat karna.")

    def test_r02_negative(self):
        assert not run_rule("R02", "Let us schedule a normal Zoom meeting next week.")

    # R03: Impersonated agency
    def test_r03_positive(self):
        assert run_rule("R03", "This is Officer Sharma from CBI headquarters.")
        assert run_rule("R03", "केंद्रीय जांच ब्यूरो सीबीआई के विशेष अधिकारी।")
        assert run_rule("R03", "ਸੀਬੀਆਈ ਹੈੱਡਕੁਆਰਟਰ ਵੱਲੋਂ ਜ਼ਰੂਰੀ ਸੂਚਨਾ।")
        assert run_rule("R03", "Main Mumbai Police cyber cell se baat kar raha hoon.")

    def test_r03_negative(self):
        assert not run_rule("R03", "Looking for jobs at a private firm.")

    # R04: Parcel with drugs / illegal items
    def test_r04_positive(self):
        assert run_rule("R04", "Your FedEx parcel containing 140 grams of MDMA drugs has been seized.")
        assert run_rule("R04", "आपके पार्सल में 5 पासपोर्ट और नशीली दवाएं जब्त हुई हैं।")
        assert run_rule("R04", "ਤੁਹਾਡੇ ਪਾਰਸਲ ਵਿੱਚ ਨਸ਼ੀਲੀਆਂ ਦਵਾਈਆਂ ਫੜੀਆਂ ਗਈਆਂ ਹਨ।")
        assert run_rule("R04", "Aapke courier me contraband drugs mila hai.")

    def test_r04_negative(self):
        assert not run_rule("R04", "Your Amazon parcel has been dispatched and will arrive today.")

    # R05: Payment demand (fine, bail, safe account)
    def test_r05_positive(self):
        assert run_rule("R05", "You must transfer refundable security deposit to the safe account.")
        assert run_rule("R05", "आपको जमानत राशि तुरंत सरकारी खाते में जमा करनी होगी।")
        assert run_rule("R05", "ਜ਼ਮਾਨਤ ਰਾਸ਼ੀ ਸੁਰੱਖਿਅਤ ਖਾਤੇ ਵਿੱਚ ਜਮ੍ਹਾਂ ਕਰੋ।")
        assert run_rule("R05", "Bail amount pay karo safe account me verification fee jama karo.")

    def test_r05_negative(self):
        assert not run_rule("R05", "Your monthly electricity bill of Rs 500 is generated.")

    # R06: Secrecy & isolation
    def test_r06_positive(self):
        assert run_rule("R06", "This is a strictly confidential case, do not tell your family.")
        assert run_rule("R06", "गोपनीय मामला है, परिवार को मत बताना और कमरे का दरवाजा बंद रखो।")
        assert run_rule("R06", "ਗੁਪਤ ਮਾਮਲਾ ਹੈ, ਪਰਿਵਾਰ ਨੂੰ ਨਾ ਦੱਸੋ ਅਤੇ ਕਮਰਾ ਬੰਦ ਰੱਖੋ।")
        assert run_rule("R06", "Kisi ko mat batana family ko bilkul mat bolna.")

    def test_r06_negative(self):
        assert not run_rule("R06", "Please share this exciting festival greeting with everyone.")

    # R07: Urgency & arrest threat
    def test_r07_positive(self):
        assert run_rule("R07", "Non-bailable arrest warrant issued, immediate arrest within 2 hours.")
        assert run_rule("R07", "2 घंटे में सिम ब्लॉक और गैर-जमानती गिरफ्तारी वारंट जारी।")
        assert run_rule("R07", "2 ਘੰਟਿਆਂ ਵਿੱਚ ਸਿਮ ਬਲਾਕ ਅਤੇ ਗ੍ਰਿਫ਼ਤਾਰੀ ਵਾਰੰਟ ਜਾਰੀ।")
        assert run_rule("R07", "2 ghante me sim block ho jayega aur turant arrest warrant niklega.")

    def test_r07_negative(self):
        assert not run_rule("R07", "Your doctor appointment is confirmed for tomorrow.")

    # R08: Aadhaar/SIM misused
    def test_r08_positive(self):
        assert run_rule("R08", "Your Aadhaar card was linked to financial fraud and terror activities.")
        assert run_rule("R08", "आपके आधार कार्ड का दुरुपयोग साइबर अपराध में हुआ है।")
        assert run_rule("R08", "ਤੁਹਾਡਾ ਸਿਮ ਅਪਰਾਧ ਵਿੱਚ ਸ਼ਾਮਲ ਪਾਇਆ ਗਿਆ ਹੈ।")
        assert run_rule("R08", "Aapka aadhaar card misuse hua hai crime me.")

    def test_r08_negative(self):
        assert not run_rule("R08", "Aadhaar update completed at the enrollment center.")

    # R09: Personal UPI / Account payment
    def test_r09_positive(self):
        assert run_rule("R09", "Pay via UPI to officer.verify@oksbi right now.")
        assert run_rule("R09", "निजी बैंक खाते में तुरंत ट्रांसफर करें।")
        assert run_rule("R09", "ਯੂਪੀਆਈ ਆਈਡੀ 'ਤੇ ਪੈਸੇ ਭੇਜੋ ਤੁਰੰਤ।")
        assert run_rule("R09", "UPI id pe bhejo personal account me transfer karo.")

    def test_r09_negative(self):
        assert not run_rule("R09", "Paid Rs 30 for tea.")

    # R10: OTP or remote access app
    def test_r10_positive(self):
        assert run_rule("R10", "Download AnyDesk and share the 6-digit code for verification.")
        assert run_rule("R10", "एनीडेस्क डाउनलोड करें और तुरंत ओटीपी बताएं।")
        assert run_rule("R10", "ਟੀਮਵਿਊਅਰ ਇੰਸਟਾਲ ਕਰੋ ਅਤੇ ਓਟੀਪੀ ਦੱਸੋ।")
        assert run_rule("R10", "AnyDesk download karo aur otp batao.")

    def test_r10_negative(self):
        assert not run_rule("R10", "Download our official game from Google Play Store.")

    # R11: Suspicious link code check
    def test_r11_positive(self):
        assert run_rule("R11", "Click http://bit.ly/cbi-warrant to view your summons.")
        assert run_rule("R11", "Open http://cbi-verification.com/case to verify.")
        assert run_rule("R11", "Check https://tinyurl.com/police-notice for court details.")

    def test_r11_negative(self):
        # Legitimate government domains must NOT trigger R11
        assert not run_rule("R11", "File complaint at https://cybercrime.gov.in or https://sci.gov.in")
        assert not run_rule("R11", "Check services at https://sancharsaathi.gov.in")

    # R12: WhatsApp/Skype officer contact
    def test_r12_positive(self):
        assert run_rule("R12", "Officer calling from Skype for statement.")
        assert run_rule("R12", "व्हाट्सएप पर पुलिस कॉल आई है।")
        assert run_rule("R12", "ਵਟਸਐਪ 'ਤੇ ਪੁਲਿਸ ਕਾਲ ਆਈ ਹੈ।")
        assert run_rule("R12", "Whatsapp pe call par officer baat karega.")

    def test_r12_negative(self):
        assert not run_rule("R12", "Sent photos to my friend on WhatsApp.")

    # R13: Forged order sent via chat
    def test_r13_positive(self):
        assert run_rule("R13", "Arrest warrant copy sent on WhatsApp with official seal attached.")
        assert run_rule("R13", "खाता सीज आदेश व्हाट्सएप पर भेजा गया है।")
        assert run_rule("R13", "ਖਾਤਾ ਫਰੀਜ਼ ਆਰਡਰ ਵਟਸਐਪ 'ਤੇ ਭੇਜਿਆ ਗਿਆ ਹੈ।")
        assert run_rule("R13", "Freeze order aur arrest warrant copy bheja hai.")

    def test_r13_negative(self):
        assert not run_rule("R13", "Court closed today for public holiday.")

    # R14: Money laundering / Canara bank allegation
    def test_r14_positive(self):
        assert run_rule("R14", "Your name appeared in Naresh Goyal Jet Airways money laundering case.")
        assert run_rule("R14", "केनरा बैंक घोटाला और मनी लॉन्ड्रिंग में आपका नाम आया है।")
        assert run_rule("R14", "ਮਨੀ ਲਾਂਡਰਿੰਗ ਅਤੇ ਹਵਾਲਾ ਲੈਣ-ਦੇਣ ਦਾ ਕੇਸ ਦਰਜ ਹੈ।")
        assert run_rule("R14", "Canara bank scam me hawala transaction mila hai.")

    def test_r14_negative(self):
        assert not run_rule("R14", "Opened a new recurring deposit at bank branch.")
