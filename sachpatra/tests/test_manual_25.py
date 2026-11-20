"""Test suite for the 25 newly crafted scam/benign/advisory test cases in EN/HI/PA/Hinglish.
Asserts scam recall >= 95%, zero benign false alarms, and 100% advisory detection.
"""

import pytest
from app.engine import analyze_text
from app.schemas import AnalyzeRequest

MANUAL_25_TEST_CASES = [
    # 15 Scams
    ("EN", "scam", "This is DSP Sharma from Crime Branch Delhi. Your SIM card was used in illegal cyber extortion in Maharashtra. You are placed on virtual arrest. Do not cut the Skype call and transfer 35000 to government safe holding account."),
    ("EN", "scam", "TRAI telecom disconnection order: Your mobile number 9876543210 will be terminated within 2 hours due to 17 harassment complaints. Press 9 or download AnyDesk for verification."),
    ("EN", "scam", "Customs Department Delhi Airport: Parcel tracking DHL-98124 detained with illegal passport and banned narcotics. Pay clearance fee of 25,000 INR to UPI officer@okaxis to stop immediate arrest warrant."),
    ("EN", "scam", "Supreme Court registry summons: A non-bailable warrant issued under PMLA act in Canara Bank loan fraud. Join video session immediately. Keep this matter secret from family members."),
    ("HI", "scam", "अपराध शाखा मुख्यालय: आपके नाम से जारी आधार कार्ड का उपयोग मनी लॉन्ड्रिंग और बैंक खाते खोलने में हुआ है। आपको डिजिटल अरेस्ट में रखा जाता है। स्काइप पर कमरा बंद करके रहें और 40,000 रुपये सत्यापन शुल्क भेजें।"),
    ("HI", "scam", "ट्राई (TRAI) चेतावनी: आपका मोबाइल नंबर अगले 2 घंटे में बंद कर दिया जाएगा क्योंकि इससे अश्लील संदेश भेजे गए हैं। पुलिस जांच से बचने के लिए तुरंत रिमोट सपोर्ट ऐप डाउनलोड करें और 15,000 रुपये जमा करें।"),
    ("HI", "scam", "मुंबई नारकोटिक्स सेल: आपके नाम का कूरियर पार्सल पकड़ा गया है जिसमें विदेशी मुद्रा और नशीले पदार्थ मिले हैं। गिरफ्तारी से बचने के लिए हमारे अधिकारी के व्यक्तिगत यूपीआई 9811223344 पर जमानत राशि भेजें।"),
    ("HI", "scam", "सीबीआई हेडक्वार्टर नोटिस: आपके खिलाफ वित्तीय धोखाधड़ी का वारंट है। किसी को न बताएं और अभी वीडियो कॉल पर अपना कैमरा ऑन रखें, वरना स्थानीय पुलिस 1 घंटे में घर पहुंचेगी।"),
    ("PA", "scam", "ਪੁਲਿਸ ਸਾਈਬਰ ਸੈੱਲ: ਤੁਹਾਡੇ ਆਧਾਰ ਕਾਰਡ ਤੇ ਗੈਰ-ਕਾਨੂੰਨੀ ਸਿਮ ਕਾਰਡ ਚੱਲ ਰਹੇ ਹਨ ਜੋ ਦੇਸ਼ ਵਿਰੋਧੀ ਗਤੀਵਿਧੀਆਂ ਵਿੱਚ ਵਰਤੇ ਗਏ ਹਨ। ਤੁਹਾਨੂੰ ਡਿਜੀਟਲ ਅਰੈਸਟ ਕੀਤਾ ਗਿਆ ਹੈ। ਵੀਡੀਓ ਕਾਲ ਨਾ ਕੱਟੋ ਅਤੇ ਵੈਰੀਫਿਕੇਸ਼ਨ ਫੀਸ 50,000 ਰੁਪਏ ਭੇਜੋ।"),
    ("PA", "scam", "ਸੀਬੀਆਈ ਜਾਂਚ ਅਧਿਕਾਰੀ: ਕੈਨਰਾ ਬੈਂਕ ਘੁਟਾਲੇ ਵਿੱਚ ਤੁਹਾਡਾ ਨਾਮ ਆਇਆ ਹੈ। ਗੁਪਤ ਕੇਸ ਹੈ, ਪਰਿਵਾਰ ਨੂੰ ਬਿਲਕੁਲ ਨਾ ਦੱਸੋ। ਗ੍ਰਿਫ਼ਤਾਰੀ ਵਾਰੰਟ ਰੋਕਣ ਲਈ ਸਰਕਾਰੀ ਖਾਤੇ ਵਿੱਚ 25,000 ਰੁਪਏ ਜਮ੍ਹਾਂ ਕਰਵਾਓ।"),
    ("PA", "scam", "ਕਸਟਮ ਵਿਭਾਗ: ਤੁਹਾਡਾ ਪਾਰਸਲ ਏਅਰਪੋਰਟ ਤੇ ਰੋਕਿਆ ਗਿਆ ਹੈ ਜਿਸ ਵਿੱਚ ਪਾਬੰਦੀਸ਼ੁਦਾ ਨਸ਼ੀਲਾ ਸਾਮਾਨ ਹੈ। ਤੁਰੰਤ ਵਟਸਐਪ ਵੀਡੀਓ ਕਾਲ ਤੇ ਆਓ ਅਤੇ 2 ਘੰਟਿਆਂ ਅੰਦਰ ਜੁਰਮਾਨਾ ਭਰੋ।"),
    ("Hinglish", "scam", "CBI officer bol raha hu headquarters se. Aapke naam par money laundering case register hua hai. Aapko digital arrest kiya gaya hai, video call disconnect mat karna aur safe account me 50000 transfer karo."),
    ("Hinglish", "scam", "Police cyber crime branch alert: Aapka parcel courier me banned drugs mila hai. Warrant issue ho gaya hai, arrest se bachne ke liye RustDesk app install karo aur security deposit pay karo."),
    ("Hinglish", "scam", "TRAI department: Aapka mobile sim card block ho jayega in 2 hours. Police case file ho chuka hai. Bachne ke liye confidential call join kare aur kisi ko mat bataye."),
    ("Hinglish", "scam", "Enforcement Directorate notice via WhatsApp: Aapke bank account se hawala transaction hua hai. Immediate bail fee deposit kijiye personal UPI par to avoid raid in 2 hours."),
    # 7 Benign
    ("EN", "benign", "Dear customer, your electricity bill of Rs 2,340 for consumer number 90214 is due on 28-Nov-2026. Please pay via the official state discom mobile app."),
    ("EN", "benign", "State Bank of India: Your account XX4819 was credited with Rs 15,000 via NEFT on 19-Nov-2026. Ref: SBI981237190."),
    ("EN", "benign", "Your Indigo flight 6E-204 from Delhi to Mumbai is on time. Web check-in is open at goindigo.in."),
    ("HI", "benign", "प्रिय ग्राहक, आपका एचडीएफसी बैंक क्रेडिट कार्ड स्टेटमेंट तैयार है। न्यूनतम देय राशि 1,200 रुपये है। भुगतान की अंतिम तिथि 25 नवंबर है।"),
    ("HI", "benign", "रेलवे आरक्षण: पीएनआर 2419082314 के लिए आपकी सीट एस-4, 32 (लोअर बर्थ) कन्फर्म हो गई है। भारतीय रेल आपकी सुखद यात्रा की कामना करती है।"),
    ("PA", "benign", "ਪਿਆਰੇ ਗਾਹਕ, ਤੁਹਾਡੇ ਐਸਬੀਆਈ ਖਾਤੇ ਵਿੱਚੋਂ 500 ਰੁਪਏ ਏਟੀਐਮ ਰਾਹੀਂ ਕੱਢੇ ਗਏ ਹਨ। ਜੇਕਰ ਇਹ ਤੁਸੀਂ ਨਹੀਂ ਕੀਤਾ ਤਾਂ ਤੁਰੰਤ ਬੈਂਕ ਨੂੰ ਸੂਚਿਤ ਕਰੋ।"),
    ("Hinglish", "benign", "Bhai kal sham ko cricket match dekhne chal rahe hai kya? Ticket book kar di hai maine BookMyShow se."),
    # 3 Advisories
    ("EN", "advisory", "PIB Fact Check Press Release: Beware of fraudulent callers claiming to be from CBI or Police threatening digital arrest on Skype. Real police never demand money or conduct virtual arrests. Report to 1930."),
    ("HI", "advisory", "आरबीआई जनहित में चेतावनी: साइबर ठगों द्वारा डिजिटल अरेस्ट के नाम पर वीडियो कॉल कर पैसे ऐंठने की घटनाएं सामने आ रही हैं। सतर्क रहें, किसी अनजान को ओटीपी न दें और कोई राशि ट्रांसफर न करें।"),
    ("PA", "advisory", "ਪੰਜਾਬ ਪੁਲਿਸ ਚੇਤਾਵਨੀ: ਡਿਜੀਟਲ ਅਰੈਸਟ ਧੋਖਾਧੜੀ ਤੋਂ ਸਾਵਧਾਨ ਰਹੋ। ਪੁਲਿਸ ਕਦੇ ਵੀ ਵੀਡੀਓ ਕਾਲ ਤੇ ਪੈਸੇ ਨਹੀਂ ਮੰਗਦੀ। ਠੱਗੀ ਹੋਣ ਤੇ 1930 ਤੇ ਸ਼ਿਕਾਇਤ ਕਰੋ।")
]


@pytest.mark.parametrize("lang, true_label, text", MANUAL_25_TEST_CASES)
def test_manual_25_cases(lang, true_label, text):
    res = analyze_text(AnalyzeRequest(text=text, language="auto"))

    if true_label == "scam":
        assert res.verdict == "likely_scam", f"Failed scam detection for [{lang}]: {text}"
        assert res.score >= 60
    elif true_label == "benign":
        assert res.verdict != "likely_scam", f"Benign message wrongly flagged as likely_scam: {text}"
        assert res.score < 25
    elif true_label == "advisory":
        assert res.advisory is True, f"Advisory pattern was missed for: {text}"
        assert res.verdict != "likely_scam"
