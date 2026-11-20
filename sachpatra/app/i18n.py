"""Internationalization resources for SachPatra.
Supported languages: en (English), hi (Hindi), pa (Punjabi).
All user-facing text, rule descriptions, action plans, drafts, and disclaimers live here.
Refined for natural, simple, respectful phrasing accessible to elderly and non-technical citizens.
"""

from typing import Any, Dict, List

DISCLAIMER: Dict[str, str] = {
    "en": "Automated screening, not legal advice. If in doubt, call 1930.",
    "hi": "यह एक स्वचालित जांच है, कानूनी सलाह नहीं। किसी भी संदेह या दबाव में तुरंत 1930 पर कॉल करें।",
    "pa": "ਇਹ ਕੰਪਿਊਟਰ ਆਧਾਰਿਤ ਜਾਂਚ ਹੈ, ਕਾਨੂੰਨੀ ਸਲਾਹ ਨਹੀਂ। ਕਿਸੇ ਵੀ ਸ਼ੱਕ ਜਾਂ ਦਬਾਅ ਦੀ ਹਾਲਤ ਵਿੱਚ ਤੁਰੰਤ 1930 'ਤੇ ਫੋਨ ਕਰੋ।"
}

CANNOT_VERIFY_ADVICE: Dict[str, str] = {
    "en": "Automated screening could not detect typical digital arrest scam patterns. Verify via official channels, and if pressured or in doubt, call 1930.",
    "hi": "स्वचालित जांच में डिजिटल अरेस्ट के जाने-माने लक्षण नहीं मिले। किसी भी अनजान व्यक्ति के कहने पर पैसे न भेजें, और दबाव होने पर 1930 पर संपर्क करें।",
    "pa": "ਕੰਪਿਊਟਰ ਜਾਂਚ ਵਿੱਚ ਡਿਜੀਟਲ ਅਰੈਸਟ ਦੇ ਆਮ ਲੱਛਣ ਨਹੀਂ ਮਿਲੇ। ਕਿਸੇ ਵੀ ਅਣਜਾਣ ਵਿਅਕਤੀ ਦੇ ਕਹਿਣ 'ਤੇ ਪੈਸੇ ਨਾ ਭੇਜੋ, ਅਤੇ ਦਬਾਅ ਹੋਣ 'ਤੇ 1930 'ਤੇ ਸੰਪਰਕ ਕਰੋ।"
}

IMAGE_OFFLINE_MESSAGE: Dict[str, str] = {
    "en": "Image reading is offline; please paste the text.",
    "hi": "इमेज पढ़ने की सेवा अभी ऑफलाइन है; कृपया संदेश का टेक्स्ट कॉपी करके पेस्ट करें।",
    "pa": "ਤਸਵੀਰ ਪੜ੍ਹਨ ਦੀ ਸੇਵਾ ਹਾਲੇ ਆਫ਼ਲਾਈਨ ਹੈ; ਕਿਰਪਾ ਕਰਕੇ ਸੁਨੇਹੇ ਦਾ ਟੈਕਸਟ ਕਾਪੀ ਕਰਕੇ ਪੇਸਟ ਕਰੋ।"
}

PLAIN_SUMMARY_FALLBACK: Dict[str, Dict[str, str]] = {
    "likely_scam": {
        "en": "Warning: This message shows clear signs of a digital arrest scam. Real police or court officials never arrest people over video calls or demand money. Please hang up immediately, speak with your family, and call helpline 1930.",
        "hi": "जरूरी चेतावनी: इस संदेश में डिजिटल अरेस्ट धोखाधड़ी के पक्के लक्षण हैं। असली पुलिस या जज कभी भी वीडियो कॉल पर गिरफ्तारी नहीं करते और न ही पैसे मांगते हैं। कृपया तुरंत फोन काटें, अपने परिवार को बताएं और 1930 पर फोन करें।",
        "pa": "ਜ਼ਰੂਰੀ ਚੇਤਾਵਨੀ: ਇਸ ਸੁਨੇਹੇ ਵਿੱਚ ਡਿਜੀਟਲ ਅਰੈਸਟ ਠੱਗੀ ਦੇ ਪੱਕੇ ਲੱਛਣ ਹਨ। ਅਸਲੀ ਪੁਲਿਸ ਜਾਂ ਜੱਜ ਕਦੇ ਵੀ ਵੀਡੀਓ ਕਾਲ 'ਤੇ ਗ੍ਰਿਫ਼ਤਾਰੀ ਨਹੀਂ ਕਰਦੇ ਅਤੇ ਨਾ ਹੀ ਪੈਸੇ ਮੰਗਦੇ ਹਨ। ਕਿਰਪਾ ਕਰਕੇ ਤੁਰੰਤ ਫੋਨ ਕੱਟੋ, ਆਪਣੇ ਪਰਿਵਾਰ ਨੂੰ ਦੱਸੋ ਅਤੇ 1930 'ਤੇ ਫੋਨ ਕਰੋ।"
    },
    "suspicious": {
        "en": "Caution: This message contains suspicious official claims or urgent payment demands. Do not transfer any money or disclose private information without independently verifying directly with local authorities.",
        "hi": "सावधानी: इस संदेश में संदिग्ध सरकारी दावे या पैसों की जल्दबाजी भरी मांग है। स्थानीय अधिकारियों या बैंक से सीधे जांच किए बिना कोई पैसा न भेजें और न ही अपनी निजी जानकारी साझा करें।",
        "pa": "ਸਾਵਧਾਨੀ: ਇਸ ਸੁਨੇਹੇ ਵਿੱਚ ਸ਼ੱਕੀ ਸਰਕਾਰੀ ਦਾਅਵੇ ਜਾਂ ਪੈਸਿਆਂ ਦੀ ਕਾਹਲੀ ਭਰੀ ਮੰਗ ਹੈ। ਸਥਾਨਕ ਅਧਿਕਾਰੀਆਂ ਜਾਂ ਬੈਂਕ ਤੋਂ ਸਿੱਧੀ ਜਾਂਚ ਕੀਤੇ ਬਿਨਾਂ ਕੋਈ ਪੈਸੇ ਨਾ ਭੇਜੋ ਅਤੇ ਨਾ ਹੀ ਨਿੱਜੀ ਜਾਣਕਾਰੀ ਦਿਓ।"
    },
    "cannot_verify": {
        "en": "Notice: Common digital arrest patterns were not found, but always remain vigilant. Government agencies will never rush you or ask for secret money transfers. If pressured, dial 1930.",
        "hi": "सूचना: सामान्य धोखाधड़ी के संकेत नहीं मिले हैं, फिर भी सतर्क रहें। सरकारी विभाग कभी भी फोन पर जल्दबाजी नहीं कराते और न ही किसी गोपनीय खाते में पैसे मांगते हैं। यदि कोई दबाव डाले तो 1930 मिलाएं।",
        "pa": "ਸੂਚਨਾ: ਆਮ ਠੱਗੀ ਦੇ ਸੰਕੇਤ ਨਹੀਂ ਮਿਲੇ, ਫਿਰ ਵੀ ਹਮੇਸ਼ਾ ਚੌਕਸ ਰਹੋ। ਸਰਕਾਰੀ ਵਿਭਾਗ ਕਦੇ ਵੀ ਫੋਨ 'ਤੇ ਕਾਹਲੀ ਨਹੀਂ ਕਰਵਾਉਂਦੇ ਅਤੇ ਨਾ ਹੀ ਕਿਸੇ ਗੁਪਤ ਖਾਤੇ ਵਿੱਚ ਪੈਸੇ ਮੰਗਦੇ ਹਨ। ਜੇਕਰ ਕੋਈ ਦਬਾਅ ਪਾਵੇ ਤਾਂ 1930 ਡਾਇਲ ਕਰੋ।"
    }
}

VERDICT_SUMMARIES: Dict[str, Dict[str, str]] = {
    "likely_scam": {
        "en": "High probability of digital arrest fraud detected. Immediate protective action required.",
        "hi": "डिजिटल अरेस्ट धोखाधड़ी की पूरी संभावना। तुरंत बात बंद करें और सुरक्षात्मक कदम उठाएं।",
        "pa": "ਡਿਜੀਟਲ ਅਰੈਸਟ ਧੋਖਾਧੜੀ ਦੀ ਪੂਰੀ ਸੰਭਾਵਨਾ। ਤੁਰੰਤ ਗੱਲਬਾਤ ਬੰਦ ਕਰੋ ਅਤੇ ਬਚਾਅ ਦੇ ਕਦਮ ਚੁੱਕੋ।"
    },
    "suspicious": {
        "en": "Suspicious coercion or impersonation elements detected. Do not comply without official verification.",
        "hi": "संदिग्ध दबाव और फर्जी पहचान के संकेत मिले हैं। बिना आधिकारिक पुष्टि के कोई कदम न उठाएं।",
        "pa": "ਸ਼ੱਕੀ ਦਬਾਅ ਅਤੇ ਨਕਲੀ ਪਛਾਣ ਦੇ ਸੰਕੇਤ ਮਿਲੇ ਹਨ। ਬਿਨਾਂ ਸਰਕਾਰੀ ਪੁਸ਼ਟੀ ਦੇ ਕੋਈ ਕੰਮ ਨਾ ਕਰੋ।"
    },
    "cannot_verify": {
        "en": "No clear digital arrest patterns identified. Exercise caution and verify via 1930 if unsure.",
        "hi": "डिजिटल अरेस्ट का कोई स्पष्ट पैटर्न नहीं मिला। सतर्क रहें और असमंजस होने पर 1930 पर कॉल करें।",
        "pa": "ਡਿਜੀਟਲ ਅਰੈਸਟ ਦਾ ਕੋਈ ਸਪੱਸ਼ਟ ਪੈਟਰਨ ਨਹੀਂ ਮਿਲਿਆ। ਚੌਕਸ ਰਹੋ ਅਤੇ ਸ਼ੱਕ ਹੋਣ 'ਤੇ 1930 'ਤੇ ਕਾਲ ਕਰੋ।"
    }
}

OFFICIAL_SOURCES = {
    "supreme_court": "https://api.sci.gov.in/supremecourt/2025/59769/59769_2025_2_7_65003_Order_17-Oct-2025.pdf",
    "cybercrime": "https://cybercrime.gov.in",
    "sancharsaathi": "https://sancharsaathi.gov.in",
    "helpline": "tel:1930"
}

RULES_METADATA: Dict[str, Dict[str, Any]] = {
    "R01": {
        "title": {
            "en": "Fictitious 'Digital Arrest' Threat",
            "hi": "'डिजिटल अरेस्ट' का फर्जी दावा",
            "pa": "'ਡਿਜੀਟਲ ਅਰੈਸਟ' ਦੀ ਝੂਠੀ ਧਮਕੀ"
        },
        "why": {
            "en": "'Digital arrest' has zero legal basis in Indian law. The Supreme Court of India took suo motu cognisance on 17 Oct 2025, confirming no agency can arrest anyone online or over video calls.",
            "hi": "भारतीय कानून में 'डिजिटल अरेस्ट' नाम की कोई चीज नहीं है। सुप्रीम कोर्ट (17 अक्टूबर 2025) ने साफ किया है कि कोई भी पुलिस या जांच एजेंसी वीडियो कॉल पर कभी गिरफ्तारी नहीं कर सकती।",
            "pa": "ਭਾਰਤੀ ਕਾਨੂੰਨ ਵਿੱਚ 'ਡਿਜੀਟਲ ਅਰੈਸਟ' ਨਾਂ ਦਾ ਕੋਈ ਕਾਨੂੰਨ ਨਹੀਂ ਹੈ। ਸੁਪਰੀਮ ਕੋਰਟ (17 ਅਕਤੂਬਰ 2025) ਨੇ ਸਾਫ਼ ਕੀਤਾ ਹੈ ਕਿ ਕੋਈ ਵੀ ਜਾਂਚ ਏਜੰਸੀ ਵੀਡੀਓ ਕਾਲ 'ਤੇ ਕਦੇ ਗ੍ਰਿਫ਼ਤਾਰੀ ਨਹੀਂ ਕਰ ਸਕਦੀ।"
        },
        "source_url": OFFICIAL_SOURCES["supreme_court"]
    },
    "R02": {
        "title": {
            "en": "Forced Video Call / Continuous Surveillance",
            "hi": "वीडियो कॉल पर रहने या कैमरा चालू रखने का दबाव",
            "pa": "ਵੀਡੀਓ ਕਾਲ 'ਤੇ ਰਹਿਣ ਜਾਂ ਕੈਮਰਾ ਚਾਲੂ ਰੱਖਣ ਦਾ ਦਬਾਅ"
        },
        "why": {
            "en": "Law enforcement agencies never demand citizens remain on 24x7 Skype/WhatsApp video calls or keep cameras turned on.",
            "hi": "असली पुलिस या जांच अधिकारी कभी भी नागरिकों को वीडियो कॉल पर बंधक नहीं बनाते और न ही कैमरा चालू रखने का दबाव डालते हैं।",
            "pa": "ਅਸਲੀ ਪੁਲਿਸ ਜਾਂ ਜਾਂਚ ਅਧਿਕਾਰੀ ਕਦੇ ਵੀ ਨਾਗਰਿਕਾਂ ਨੂੰ ਵੀਡੀਓ ਕਾਲ 'ਤੇ ਬੰਧਕ ਨਹੀਂ ਬਣਾਉਂਦੇ ਅਤੇ ਨਾ ਹੀ ਕੈਮਰਾ ਚਾਲੂ ਰੱਖਣ ਲਈ ਮਜਬੂਰ ਕਰਦੇ ਹਨ।"
        },
        "source_url": OFFICIAL_SOURCES["cybercrime"]
    },
    "R03": {
        "title": {
            "en": "Agency Impersonation (CBI/ED/Police/TRAI/Customs)",
            "hi": "जांच एजेंसी का फर्जी रूप धारण करना (CBI/ED/पुलिस/TRAI)",
            "pa": "ਜਾਂਚ ਏਜੰਸੀ ਦਾ ਨਕਲੀ ਰੂਪ ਧਾਰਨਾ (CBI/ED/ਪੁਲਿਸ/TRAI)"
        },
        "why": {
            "en": "Fraudsters impersonate high-profile agencies (CBI, ED, Narcotics, Police, TRAI) to create overwhelming psychological pressure.",
            "hi": "धोखेबाज डर और घबराहट पैदा करने के लिए सीबीआई, ईडी, नारकोटिक्स, पुलिस या ट्राई जैसी शीर्ष एजेंसियों के फर्जी अधिकारी बनते हैं।",
            "pa": "ਠੱਗ ਡਰ ਪੈਦਾ ਕਰਨ ਲਈ ਸੀਬੀਆਈ, ਈਡੀ, ਨਾਰਕੋਟਿਕਸ, ਪੁਲਿਸ ਜਾਂ ਟਰਾਈ ਵਰਗੀਆਂ ਵੱਡੀਆਂ ਏਜੰਸੀਆਂ ਦੇ ਨਕਲੀ ਅਧਿਕਾਰੀ ਬਣ ਕੇ ਗੱਲ ਕਰਦੇ ਹਨ।"
        },
        "source_url": OFFICIAL_SOURCES["cybercrime"]
    },
    "R04": {
        "title": {
            "en": "Illegal Parcel / Contraband Courier Claim",
            "hi": "पार्सल में नशीला सामान या अवैध पासपोर्ट मिलने का झूठा दावा",
            "pa": "ਪਾਰਸਲ ਵਿੱਚ ਨਸ਼ੀਲੀਆਂ ਦਵਾਈਆਂ ਜਾਂ ਗੈਰ-ਕਾਨੂੰਨੀ ਪਾਸਪੋਰਟ ਦਾ ਝੂਠਾ ਦਾਅਵਾ"
        },
        "why": {
            "en": "Scammers falsely claim a courier parcel (FedEx/DHL/India Post) in your name contained narcotics, passports, or contraband to initiate extortion.",
            "hi": "धोखेबाज झूठा दावा करते हैं कि आपके नाम से भेजे गए कूरियर पार्सल में ड्रग्स या पासपोर्ट जब्त हुए हैं ताकि आपसे जबरन वसूली की जा सके।",
            "pa": "ਠੱਗ ਝੂਠਾ ਦਾਅਵਾ ਕਰਦੇ ਹਨ ਕਿ ਤੁਹਾਡੇ ਨਾਮ 'ਤੇ ਭੇਜੇ ਗਏ ਕੋਰੀਅਰ ਪਾਰਸਲ ਵਿੱਚ ਨਸ਼ੀਲਾ ਸਾਮਾਨ ਜਾਂ ਪਾਸਪੋਰਟ ਮਿਲਿਆ ਹੈ ਤਾਂ ਜੋ ਪੈਸੇ ਠੱਗੇ ਜਾ ਸਕਣ।"
        },
        "source_url": OFFICIAL_SOURCES["sancharsaathi"]
    },
    "R05": {
        "title": {
            "en": "Financial Demand (Bail / Safe Account / Verification)",
            "hi": "पैसे की मांग (जमानत राशि / सुरक्षित खाता / सत्यापन शुल्क)",
            "pa": "ਪੈਸਿਆਂ ਦੀ ਮੰਗ (ਜ਼ਮਾਨਤ ਰਾਸ਼ੀ / ਸੁਰੱਖਿਅਤ ਖਾਤਾ / ਤਸਦੀਕ ਫੀਸ)"
        },
        "why": {
            "en": "No Indian court or police agency ever demands money transfer to a 'safe account' or takes bail/clearance fee over phone/UPI.",
            "hi": "भारत की कोई भी अदालत या पुलिस एजेंसी फोन या चैट पर किसी 'सुरक्षित खाते' में पैसे ट्रांसफर करने या सत्यापन शुल्क की मांग नहीं करती।",
            "pa": "ਭਾਰਤ ਦੀ ਕੋਈ ਵੀ ਅਦਾਲਤ ਜਾਂ ਪੁਲਿਸ ਫ਼ੋਨ ਜਾਂ ਚੈਟ 'ਤੇ ਕਿਸੇ 'ਸੁਰੱਖਿਅਤ ਖਾਤੇ' ਵਿੱਚ ਪੈਸੇ ਟਰਾਂਸਫਰ ਕਰਨ ਜਾਂ ਜ਼ਮਾਨਤ ਰਾਸ਼ੀ ਮੰਗਣ ਦਾ ਕੰਮ ਨਹੀਂ ਕਰਦੀ।"
        },
        "source_url": OFFICIAL_SOURCES["cybercrime"]
    },
    "R06": {
        "title": {
            "en": "Isolation & Secrecy Mandate",
            "hi": "गोपनीयता और परिवार को न बताने का दबाव",
            "pa": "ਗੁਪਤਤਾ ਅਤੇ ਪਰਿਵਾਰ ਤੋਂ ਗੱਲ ਲੁਕਾਉਣ ਦਾ ਦਬਾਅ"
        },
        "why": {
            "en": "Scammers forbid telling family or closing the room door to isolate you psychologically and prevent third-party intervention.",
            "hi": "धोखेबाज पीड़ित को परिवार या दोस्तों से अलग-थलग करने के लिए गोपनीयता और कमरे का दरवाजा बंद रखने का दबाव बनाते हैं।",
            "pa": "ਠੱਗ ਪੀੜਤ ਨੂੰ ਇਕੱਲਾ ਕਰਨ ਲਈ ਪਰਿਵਾਰ ਨੂੰ ਨਾ ਦੱਸਣ ਅਤੇ ਕਮਰਾ ਬੰਦ ਰੱਖਣ ਦਾ ਦਬਾਅ ਪਾਉਂਦੇ ਹਨ ਤਾਂ ਜੋ ਕੋਈ ਮਦਦ ਨਾ ਕਰ ਸਕੇ।"
        },
        "source_url": OFFICIAL_SOURCES["cybercrime"]
    },
    "R07": {
        "title": {
            "en": "Artificial Urgency & Arrest Deadline",
            "hi": "तत्काल गिरफ्तारी या सिम ब्लॉक करने की झूठी समयसीमा",
            "pa": "ਤੁਰੰਤ ਗ੍ਰਿਫ਼ਤਾਰੀ ਜਾਂ ਸਿਮ ਬਲਾਕ ਕਰਨ ਦੀ ਝੂਠੀ ਸਮਾਂ ਸੀਮਾ"
        },
        "why": {
            "en": "Imposing artificial deadlines (e.g. 'arrest in 2 hours', 'SIM disconnection in 1 hour') aims to bypass rational thinking.",
            "hi": "कुछ ही घंटों में गिरफ्तारी या सिम ब्लॉक होने की झूठी समयसीमा इसलिए दी जाती है ताकि व्यक्ति घबराकर बिना सोचे पैसे दे दे।",
            "pa": "ਕੁਝ ਘੰਟਿਆਂ ਵਿੱਚ ਗ੍ਰਿਫ਼ਤਾਰੀ ਜਾਂ ਸਿਮ ਬੰਦ ਹੋਣ ਦੀ ਧਮਕੀ ਇਸ ਲਈ ਦਿੱਤੀ ਜਾਂਦੀ ਹੈ ਤਾਂ ਜੋ ਵਿਅਕਤੀ ਘਬਰਾ ਕੇ ਪੈਸੇ ਦੇ ਦੇਵੇ।"
        },
        "source_url": OFFICIAL_SOURCES["sancharsaathi"]
    },
    "R08": {
        "title": {
            "en": "Identity Misuse Allegation (Aadhaar/SIM/Bank)",
            "hi": "पहचान के दुरुपयोग का आरोप (आधार/सिम/बैंक खाता)",
            "pa": "ਪਛਾਣ ਦੀ ਦੁਰਵਰਤੋਂ ਦਾ ਦੋਸ਼ (ਆਧਾਰ/ਸਿਮ/ਬੈਂਕ ਖਾਤਾ)"
        },
        "why": {
            "en": "Scammers claim your Aadhaar or phone number was used in terrorist funding or criminal rings to make you feel legally vulnerable.",
            "hi": "धोखेबाज दावा करते हैं कि आपके आधार या सिम का इस्तेमाल किसी आपराधिक गिरोह द्वारा हुआ है ताकि आप दोषी महसूस करने लगें।",
            "pa": "ਠੱਗ ਦਾਅਵਾ ਕਰਦੇ ਹਨ ਕਿ ਤੁਹਾਡਾ ਆਧਾਰ ਜਾਂ ਸਿਮ ਕਿਸੇ ਗੰਭੀਰ ਅਪਰਾਧ ਵਿੱਚ ਵਰਤਿਆ ਗਿਆ ਹੈ ਤਾਂ ਜੋ ਤੁਸੀਂ ਦਬਾਅ ਵਿੱਚ ਆ ਜਾਵੋ।"
        },
        "source_url": OFFICIAL_SOURCES["sancharsaathi"]
    },
    "R09": {
        "title": {
            "en": "Payment via Personal UPI / Phone / Private Account",
            "hi": "निजी यूपीआई, फोन या बैंक खाते में भुगतान की मांग",
            "pa": "ਨਿੱਜੀ ਯੂਪੀਆਈ, ਫ਼ੋਨ ਜਾਂ ਬੈਂਕ ਖਾਤੇ ਵਿੱਚ ਭੁਗਤਾਨ ਦੀ ਮੰਗ"
        },
        "why": {
            "en": "Official government revenues go only to consolidated treasury portals (Bharatkosh/e-Challan), never individual UPI IDs or private accounts.",
            "hi": "सरकारी राजस्व केवल आधिकारिक राजकोष पोर्टलों (भारतकोश/ई-चालान) में जमा होता है, किसी निजी यूपीआई आईडी या बैंक खाते में नहीं।",
            "pa": "ਸਰਕਾਰੀ ਫੀਸਾਂ ਕੇਵਲ ਸਰਕਾਰੀ ਖਜ਼ਾਨਾ ਪੋਰਟਲ (ਭਾਰਤਕੋਸ਼) ਵਿੱਚ ਜਾਂਦੀਆਂ ਹਨ, ਕਿਸੇ ਨਿੱਜੀ ਯੂਪੀਆਈ ਜਾਂ ਨਿੱਜੀ ਖਾਤੇ ਵਿੱਚ ਨਹੀਂ।"
        },
        "source_url": OFFICIAL_SOURCES["cybercrime"]
    },
    "R10": {
        "title": {
            "en": "OTP Demand / Remote Desktop Software (AnyDesk/TeamViewer)",
            "hi": "ओटीपी की मांग या स्क्रीन शेयरिंग ऐप (AnyDesk/TeamViewer)",
            "pa": "ਓਟੀਪੀ ਦੀ ਮੰਗ ਜਾਂ ਸਕ੍ਰੀਨ ਸ਼ੇਅਰਿੰਗ ਐਪ (AnyDesk/TeamViewer)"
        },
        "why": {
            "en": "No authentic police or bank personnel will ever ask for OTPs or instruct you to install AnyDesk, TeamViewer, or QuickSupport.",
            "hi": "कोई भी असली पुलिस या बैंक अधिकारी कभी फोन पर ओटीपी नहीं मांगता और न ही AnyDesk या TeamViewer जैसे ऐप इंस्टॉल करने को कहता है।",
            "pa": "ਕੋਈ ਵੀ ਅਸਲੀ ਪੁਲਿਸ ਜਾਂ ਬੈਂਕ ਅਧਿਕਾਰੀ ਕਦੇ ਫੋਨ 'ਤੇ ਓਟੀਪੀ ਨਹੀਂ ਮੰਗਦਾ ਅਤੇ ਨਾ ਹੀ AnyDesk ਜਾਂ TeamViewer ਵਰਗੇ ਐਪ ਇੰਸਟਾਲ ਕਰਨ ਲਈ ਕਹਿੰਦਾ ਹੈ।"
        },
        "source_url": OFFICIAL_SOURCES["cybercrime"]
    },
    "R11": {
        "title": {
            "en": "Suspicious Link (Shortened URL or Fake Non-Gov Domain)",
            "hi": "संदिग्ध लिंक (शॉर्ट यूआरएल या फर्जी गैर-सरकारी डोमेन)",
            "pa": "ਸ਼ੱਕੀ ਲਿੰਕ (ਛੋਟਾ ਯੂਆਰਐਲ ਜਾਂ ਨਕਲੀ ਗੈਰ-ਸਰਕਾਰੀ ਡੋਮੇਨ)"
        },
        "why": {
            "en": "Legitimate Indian government departments use exclusively .gov.in or .nic.in domains. Shorteners and .com/.org/.xyz domains are fraudulent.",
            "hi": "भारत सरकार के आधिकारिक पोर्टल केवल .gov.in या .nic.in पर चलते हैं। शॉर्ट लिंक या .com/.net/.xyz वाले डोमेन फर्जी होते हैं।",
            "pa": "ਭਾਰਤ ਸਰਕਾਰ ਦੇ ਅਧਿਕਾਰਤ ਪੋਰਟਲ ਸਿਰਫ਼ .gov.in ਜਾਂ .nic.in 'ਤੇ ਚੱਲਦੇ ਹਨ। ਸ਼ਾਰਟ ਲਿੰਕ ਜਾਂ .com/.org ਵਾਲੀਆਂ ਸਾਈਟਾਂ ਜਾਅਲੀ ਹੁੰਦੀਆਂ ਹਨ।"
        },
        "source_url": OFFICIAL_SOURCES["sancharsaathi"]
    },
    "R12": {
        "title": {
            "en": "Official Contact via WhatsApp / Skype / Telegram",
            "hi": "व्हाट्सएप, स्काइप या टेलीग्राम पर पुलिस संपर्क का दावा",
            "pa": "ਵਟਸਐਪ, ਸਕਾਈਪ ਜਾਂ ਟੈਲੀਗ੍ਰਾਮ 'ਤੇ ਪੁਲਿਸ ਸੰਪਰਕ ਦਾ ਦਾਅਵਾ"
        },
        "why": {
            "en": "Indian law enforcement never sends summons, takes statements, or issues court orders over WhatsApp or Skype personal messages.",
            "hi": "भारतीय कानून प्रवर्तन एजेंसियां कभी भी व्हाट्सएप, स्काइप या टेलीग्राम पर कानूनी नोटिस नहीं भेजतीं और न ही बयान दर्ज करती हैं।",
            "pa": "ਭਾਰਤੀ ਜਾਂਚ ਏਜੰਸੀਆਂ ਕਦੇ ਵੀ ਵਟਸਐਪ, ਸਕਾਈਪ ਜਾਂ ਟੈਲੀਗ੍ਰਾਮ ਰਾਹੀਂ ਕਾਨੂੰਨੀ ਨੋਟਿਸ ਨਹੀਂ ਭੇਜਦੀਆਂ ਅਤੇ ਨਾ ਹੀ ਬਿਆਨ ਲੈਂਦੀਆਂ ਹਨ।"
        },
        "source_url": OFFICIAL_SOURCES["cybercrime"]
    },
    "R13": {
        "title": {
            "en": "Forged Notice / Arrest Warrant Sent via Chat",
            "hi": "व्हाट्सएप चैट पर भेजा गया फर्जी जब्ती या गिरफ्तारी वारंट",
            "pa": "ਵਟਸਐਪ ਚੈਟ 'ਤੇ ਭੇਜਿਆ ਗਿਆ ਜਾਅਲੀ ਜ਼ਬਤੀ ਜਾਂ ਗ੍ਰਿਫ਼ਤਾਰੀ ਵਾਰੰਟ"
        },
        "why": {
            "en": "Warrants and bank freeze orders are served physically through legal summons, never as PDFs or images transmitted over social chat apps.",
            "hi": "अदालत या पुलिस के गिरफ्तारी वारंट और खाता सीज आदेश डाक या पुलिस द्वारा व्यक्तिगत रूप से दिए जाते हैं, व्हाट्सएप चैट पर फोटो भेजकर नहीं।",
            "pa": "ਅਦਾਲਤੀ ਵਾਰੰਟ ਅਤੇ ਖਾਤਾ ਫਰੀਜ਼ ਕਰਨ ਦੇ ਹੁਕਮ ਵਿਅਕਤੀਗਤ ਤੌਰ 'ਤੇ ਦਿੱਤੇ ਜਾਂਦੇ ਹਨ, ਵਟਸਐਪ ਚੈਟ 'ਤੇ ਫੋਟੋਆਂ ਭੇਜ ਕੇ ਨਹੀਂ।"
        },
        "source_url": OFFICIAL_SOURCES["cybercrime"]
    },
    "R14": {
        "title": {
            "en": "Money Laundering / High-Profile Financial Scam Allegation",
            "hi": "मनी लॉन्ड्रिंग या बड़े बैंक घोटाले का झूठा आरोप",
            "pa": "ਮਨੀ ਲਾਂਡਰਿੰਗ ਜਾਂ ਵੱਡੇ ਬੈਂਕ ਘੁਟਾਲੇ ਦਾ ਝੂਠਾ ਦੋਸ਼"
        },
        "why": {
            "en": "Scammers fabricate links to high-profile cases (e.g. Canara Bank, Naresh Goyal, hawala rackets) to frighten targets into compliance.",
            "hi": "धोखेबाज डराने के लिए मशहूर वित्तीय घोटालों (जैसे केनरा बैंक, नरेश गोयल, हवाला) के फर्जी संबंध जोड़ते हैं।",
            "pa": "ਠੱਗ ਡਰਾਉਣ ਲਈ ਮਸ਼ਹੂਰ ਘੁਟਾਲਿਆਂ (ਜਿਵੇਂ ਕੈਨਰਾ ਬੈਂਕ, ਨਰੇਸ਼ ਗੋਇਲ, ਹਵਾਲਾ) ਦੇ ਝੂਠੇ ਸੰਬੰਧ ਜੋੜਦੇ ਹਨ।"
        },
        "source_url": OFFICIAL_SOURCES["cybercrime"]
    }
}

ACTION_STEPS: Dict[str, List[Dict[str, Any]]] = {
    "en": [
        {
            "step": 1,
            "title": "Hang up and cut connection immediately",
            "description": "Disconnect the video call or chat right now. Do not speak further, do not pay any amount, and never share OTPs or download any apps.",
            "timebox_min": 2
        },
        {
            "step": 2,
            "title": "Call National Cybercrime Helpline 1930",
            "description": "Dial 1930 from your phone immediately. Inform the officer that someone is attempting a digital arrest fraud against you.",
            "timebox_min": 3
        },
        {
            "step": 3,
            "title": "Register formal report at cybercrime.gov.in",
            "description": "Visit cybercrime.gov.in and log a formal complaint under the Financial/Cyber Fraud category with call details.",
            "timebox_min": 5
        },
        {
            "step": 4,
            "title": "Confide in a family member or trusted friend",
            "description": "Break the isolation immediately. Speak to a trusted family member or neighbour. Fraudsters thrive on keeping you alone.",
            "timebox_min": None
        },
        {
            "step": 5,
            "title": "Alert your bank to freeze transactions if any money was sent",
            "description": "If you paid money or shared bank/card details, call your bank's emergency helpline immediately to block transfers and cards.",
            "timebox_min": None
        },
        {
            "step": 6,
            "title": "Preserve all evidence securely",
            "description": "Take screenshots of WhatsApp/Skype chats, copy caller phone numbers, keep forged PDFs, and note UPI transaction IDs for the police.",
            "timebox_min": None
        }
    ],
    "hi": [
        {
            "step": 1,
            "title": "तुरंत कॉल काटें और बातचीत बंद करें",
            "description": "वीडियो कॉल या चैट को तुरंत बंद करें। आगे कोई बात न करें, कोई पैसा न भेजें, ओटीपी न बताएं और कोई ऐप डाउनलोड न करें।",
            "timebox_min": 2
        },
        {
            "step": 2,
            "title": "राष्ट्रीय साइबर हेल्पलाइन 1930 पर तुरंत कॉल करें",
            "description": "अपने फोन से तुरंत 1930 डायल करें और बताएं कि आपके साथ डिजिटल अरेस्ट धोखाधड़ी की कोशिश हो रही है।",
            "timebox_min": 3
        },
        {
            "step": 3,
            "title": "cybercrime.gov.in पर आधिकारिक शिकायत दर्ज करें",
            "description": "cybercrime.gov.in पोर्टल पर जाएं और घटना का पूरा विवरण देते हुए साइबर फ्रॉड की आधिकारिक शिकायत दर्ज करें।",
            "timebox_min": 5
        },
        {
            "step": 4,
            "title": "परिवार के किसी सदस्य या मित्र को तुरंत बताएं",
            "description": "अकेले न रहें। तुरंत अपने परिवार या किसी भरोसेमंद व्यक्ति को पूरी बात बताएं। धोखेबाज आपको अकेला रखकर डराते हैं।",
            "timebox_min": None
        },
        {
            "step": 5,
            "title": "यदि पैसे भेजे हैं तो तुरंत बैंक को सूचित करें",
            "description": "यदि आपने कोई पैसा भेजा है या बैंक विवरण साझा किया है, तो तुरंत अपने बैंक की हेल्पलाइन पर कॉल कर लेन-देन रुकवाएं।",
            "timebox_min": None
        },
        {
            "step": 6,
            "title": "सभी सबूत सुरक्षित रखें",
            "description": "व्हाट्सएप/स्काइप चैट के स्क्रीनशॉट लें, कॉलर का फोन नंबर नोट करें और फर्जी नोटिस व यूपीआई आईडी सुरक्षित रखें।",
            "timebox_min": None
        }
    ],
    "pa": [
        {
            "step": 1,
            "title": "ਤੁਰੰਤ ਕਾਲ ਕੱਟੋ ਅਤੇ ਸੰਪਰਕ ਬੰਦ ਕਰੋ",
            "description": "ਵੀਡੀਓ ਕਾਲ ਜਾਂ ਚੈਟ ਨੂੰ ਤੁਰੰਤ ਬੰਦ ਕਰੋ। ਅੱਗੇ ਕੋਈ ਗੱਲ ਨਾ ਕਰੋ, ਕੋਈ ਪੈਸੇ ਨਾ ਭੇਜੋ, ਓਟੀਪੀ ਨਾ ਦੱਸੋ ਅਤੇ ਕੋਈ ਐਪ ਡਾਊਨਲੋਡ ਨਾ ਕਰੋ।",
            "timebox_min": 2
        },
        {
            "step": 2,
            "title": "ਰਾਸ਼ਟਰੀ ਸਾਈਬਰ ਹੈਲਪਲਾਈਨ 1930 'ਤੇ ਤੁਰੰਤ ਕਾਲ ਕਰੋ",
            "description": "ਆਪਣੇ ਫੋਨ ਤੋਂ ਤੁਰੰਤ 1930 ਡਾਇਲ ਕਰੋ ਅਤੇ ਦੱਸੋ ਕਿ ਤੁਹਾਡੇ ਨਾਲ ਡਿਜੀਟਲ ਅਰੈਸਟ ਧੋਖਾਧੜੀ ਦੀ ਕੋਸ਼ਿਸ਼ ਹੋ ਰਹੀ ਹੈ।",
            "timebox_min": 3
        },
        {
            "step": 3,
            "title": "cybercrime.gov.in 'ਤੇ ਸ਼ਿਕਾਇਤ ਦਰਜ ਕਰੋ",
            "description": "cybercrime.gov.in ਪੋਰਟਲ 'ਤੇ ਜਾਓ ਅਤੇ ਪੂਰੇ ਵੇਰਵਿਆਂ ਨਾਲ ਸਾਈਬਰ ਅਪਰਾਧ ਦੀ ਸ਼ਿਕਾਇਤ ਦਰਜ ਕਰੋ।",
            "timebox_min": 5
        },
        {
            "step": 4,
            "title": "ਪਰਿਵਾਰ ਜਾਂ ਭਰੋਸੇਯੋਗ ਦੋਸਤ ਨੂੰ ਤੁਰੰਤ ਦੱਸੋ",
            "description": "ਇਕੱਲੇ ਨਾ ਰਹੋ। ਤੁਰੰਤ ਆਪਣੇ ਪਰਿਵਾਰ ਦੇ ਮੈਂਬਰ ਜਾਂ ਦੋਸਤ ਨੂੰ ਪੂਰੀ ਗੱਲ ਦੱਸੋ। ਠੱਗ ਤੁਹਾਨੂੰ ਇਕੱਲੇ ਰੱਖ ਕੇ ਡਰਾਉਂਦੇ ਹਨ।",
            "timebox_min": None
        },
        {
            "step": 5,
            "title": "ਜੇਕਰ ਪੈਸੇ ਭੇਜੇ ਹਨ ਤਾਂ ਤੁਰੰਤ ਬੈਂਕ ਨੂੰ ਖਾਤਾ ਰੋਕਣ ਲਈ ਕਹੋ",
            "description": "ਜੇਕਰ ਤੁਸੀਂ ਕੋਈ ਰਕਮ ਟਰਾਂਸਫਰ ਕੀਤੀ ਹੈ, ਤਾਂ ਤੁਰੰਤ ਆਪਣੇ ਬੈਂਕ ਦੀ ਐਮਰਜੈਂਸੀ ਹੈਲਪਲਾਈਨ 'ਤੇ ਕਾਲ ਕਰਕੇ ਲੈਣ-ਦੇਣ ਰੋਕੋ।",
            "timebox_min": None
        },
        {
            "step": 6,
            "title": "ਸਾਰੇ ਸਬੂਤ ਸੁਰੱਖਿਅਤ ਰੱਖੋ",
            "description": "ਚੈਟਾਂ ਦੇ ਸਕ੍ਰੀਨਸ਼ਾਟ ਲਓ, ਫੋਨ ਨੰਬਰ ਸੰਭਾਲੋ ਅਤੇ ਜਾਅਲੀ ਨੋਟਿਸ ਤੇ ਯੂਪੀਆਈ ਆਈਡੀ ਪੁਲਿਸ ਰਿਪੋਰਟ ਲਈ ਰੱਖੋ।",
            "timebox_min": None
        }
    ]
}

DRAFT_TEMPLATES: Dict[str, Dict[str, str]] = {
    "en": {
        "complaint_text": (
            "COMPLAINT OF ATTEMPTED DIGITAL ARREST / CYBER EXTORTION\n"
            "Date of Incident: {date}\n"
            "Impersonated Agency: {agency}\n"
            "Modus Operandi: Perpetrators initiated contact claiming to be law enforcement officers, "
            "falsely alleging criminal involvement and threatening 'digital arrest' over video call. "
            "They exerted severe psychological intimidation and demanded financial transfer for verification/bail.\n"
            "Financial Demand / Details: {amount_or_details}\n"
            "Fraudster Contact / UPI ID: {caller_or_upi}\n"
            "Action Taken: I disconnected the call in accordance with Supreme Court guidelines and reported to 1930. "
            "Please investigate and take strict action."
        ),
        "script_1930": (
            "1. Hello, I am reporting an active 'digital arrest' extortion attempt against me.\n"
            "2. The fraudster called claiming to be an officer from {agency}.\n"
            "3. They threatened immediate arrest over video call and demanded money/verification.\n"
            "4. Suspect details: Contact/UPI: {caller_or_upi}, Amount demanded: {amount_or_details}.\n"
            "5. I have disconnected the call without paying, and I request urgent registration and advisory assistance."
        ),
        "family_alert": (
            "⚠️ URGENT FRAUD ALERT: I just received a fraudulent video/voice call claiming to be from {agency} "
            "threatening a 'digital arrest'. 'Digital arrest' is completely fake and illegal under Supreme Court rulings. "
            "I have safely disconnected the call and called the 1930 Cyber Helpline. "
            "Please be alert: never stay on video calls with such fraudsters, never share OTPs, and never transfer money."
        )
    },
    "hi": {
        "complaint_text": (
            "डिजिटल अरेस्ट / साइबर जबरन वसूली की शिकायत\n"
            "घटना की तिथि: {date}\n"
            "फर्जी जांच एजेंसी: {agency}\n"
            "घटना का विवरण: अज्ञात व्यक्तियों ने जांच अधिकारी बनकर संपर्क किया और वीडियो कॉल पर 'डिजिटल अरेस्ट' की धमकी दी। "
            "उन्होंने मुझ पर झूठे आरोप लगाए और सत्यापन/जमानत के नाम पर पैसे की मांग की।\n"
            "मांगी गई राशि/वित्तीय विवरण: {amount_or_details}\n"
            "धोखेबाज का संपर्क / यूपीआई आईडी: {caller_or_upi}\n"
            "की गई कार्रवाई: मैंने सुप्रीम कोर्ट के दिशानिर्देशों के अनुसार कॉल काट दी और 1930 पर सूचित किया। "
            "कृपया मामले की त्वरित जांच कर सख्त कानूनी कार्रवाई करें।"
        ),
        "script_1930": (
            "1. नमस्ते, मैं 'डिजिटल अरेस्ट' के नाम पर हो रही जबरन वसूली की शिकायत दर्ज कराना चाहता/चाहती हूँ।\n"
            "2. फोन करने वाले ने खुद को {agency} का अधिकारी बताया।\n"
            "3. उसने वीडियो कॉल पर तत्काल गिरफ्तारी की धमकी देकर पैसे और सत्यापन की मांग की।\n"
            "4. धोखेबाज का विवरण: फोन/यूपीआई: {caller_or_upi}, मांगी गई राशि: {amount_or_details}।\n"
            "5. मैंने बिना कोई भुगतान किए कॉल काट दी है, कृपया इसे पोर्टल पर दर्ज करें और सहायता प्रदान करें।"
        ),
        "family_alert": (
            "⚠️ जरूरी सूचना: मुझे अभी {agency} का फर्जी अधिकारी बनकर 'डिजिटल अरेस्ट' की धमकी भरा कॉल आया था। "
            "सुप्रीम कोर्ट के अनुसार 'डिजिटल अरेस्ट' पूरी तरह फर्जी और गैरकानूनी है। "
            "मैंने तुरंत कॉल काट दी है और 1930 साइबर हेल्पलाइन को सूचित कर दिया है। "
            "आप सभी सावधान रहें: ऐसे वीडियो कॉल पर न रुकें, कोई ओटीपी न दें और किसी को पैसे न भेजें।"
        )
    },
    "pa": {
        "complaint_text": (
            "ਡਿਜੀਟਲ ਅਰੈਸਟ / ਸਾਈਬਰ ਜਬਰੀ ਵਸੂਲੀ ਦੀ ਸ਼ਿਕਾਇਤ\n"
            "ਘਟਨਾ ਦੀ ਮਿਤੀ: {date}\n"
            "ਨਕਲੀ ਜਾਂਚ ਏਜੰਸੀ: {agency}\n"
            "ਘਟਨਾ ਦਾ ਵੇਰਵਾ: ਅਣਪਛਾਤੇ ਵਿਅਕਤੀਆਂ ਨੇ ਅਧਿਕਾਰੀ ਬਣ ਕੇ ਸੰਪਰਕ ਕੀਤਾ ਅਤੇ ਵੀਡੀਓ ਕਾਲ 'ਤੇ 'ਡਿਜੀਟਲ ਅਰੈਸਟ' ਦੀ ਧਮਕੀ ਦਿੱਤੀ। "
            "ਉਨ੍ਹਾਂ ਨੇ ਝੂਠੇ ਦੋਸ਼ ਲਗਾ ਕੇ ਜ਼ਮਾਨਤ/ਤਸਦੀਕ ਦੇ ਨਾਮ 'ਤੇ ਪੈਸਿਆਂ ਦੀ ਮੰਗ ਕੀਤੀ।\n"
            "ਮੰਗੀ ਗਈ ਰਕਮ/ਵੇਰਵਾ: {amount_or_details}\n"
            "ਠੱਗ ਦਾ ਫੋਨ / ਯੂਪੀਆਈ ਆਈਡੀ: {caller_or_upi}\n"
            "ਕੀਤੀ ਗਈ ਕਾਰਵਾਈ: ਮੈਂ ਸੁਪਰੀਮ ਕੋਰਟ ਦੇ ਹੁਕਮਾਂ ਅਨੁਸਾਰ ਕਾਲ ਕੱਟ ਦਿੱਤੀ ਅਤੇ 1930 'ਤੇ ਜਾਣਕਾਰੀ ਦਿੱਤੀ। "
            "ਕ੍ਰਿਪਾ ਕਰਕੇ ਤੁਰੰਤ ਕਾਰਵਾਈ ਕੀਤੀ ਜਾਵੇ।"
        ),
        "script_1930": (
            "1. ਸਤਿ ਸ੍ਰੀ ਅਕਾਲ ਜੀ, ਮੈਂ ਇੱਕ ਫਰਜ਼ੀ 'ਡਿਜੀਟਲ ਅਰੈਸਟ' ਦੀ ਸ਼ਿਕਾਇਤ ਦਰਜ ਕਰਵਾਉਣੀ ਹੈ।\n"
            "2. ਫੋਨ ਕਰਨ ਵਾਲੇ ਨੇ ਖੁਦ ਨੂੰ {agency} ਦਾ ਅਧਿਕਾਰੀ ਦੱਸਿਆ।\n"
            "3. ਉਸਨੇ ਵੀਡੀਓ ਕਾਲ 'ਤੇ ਤੁਰੰਤ ਗ੍ਰਿਫ਼ਤਾਰੀ ਦੀ ਧਮਕੀ ਦੇ ਕੇ ਪੈਸਿਆਂ ਦੀ ਮੰਗ ਕੀਤੀ।\n"
            "4. ਠੱਗ ਦੇ ਵੇਰਵੇ: ਫੋਨ/ਯੂਪੀਆਈ: {caller_or_upi}, ਮੰਗੀ ਗਈ ਰਕਮ: {amount_or_details}।\n"
            "5. ਮੈਂ ਬਿਨਾਂ ਪੈਸੇ ਦਿੱਤੇ ਕਾਲ ਕੱਟ ਦਿੱਤੀ ਹੈ, ਕ੍ਰਿਪਾ ਕਰਕੇ ਮੇਰੀ ਰਿਪੋਰਟ ਦਰਜ ਕਰੋ।"
        ),
        "family_alert": (
            "⚠️ ਜ਼ਰੂਰੀ ਸਾਵਧਾਨੀ: ਮੈਨੂੰ ਹੁਣੇ {agency} ਦਾ ਨਕਲੀ ਅਧਿਕਾਰੀ ਬਣ ਕੇ 'ਡਿਜੀਟਲ ਅਰੈਸਟ' ਦੀ ਧਮਕੀ ਭਰੀ ਕਾਲ ਆਈ ਸੀ। "
            "ਸੁਪਰੀਮ ਕੋਰਟ ਮੁਤਾਬਕ 'ਡਿਜੀਟਲ ਅਰੈਸਟ' ਪੂਰੀ ਤਰ੍ਹਾਂ ਨਕਲੀ ਅਤੇ ਗੈਰ-ਕਾਨੂੰਨੀ ਹੈ। "
            "ਮੈਂ ਤੁਰੰਤ ਕਾਲ ਕੱਟ ਦਿੱਤੀ ਹੈ ਅਤੇ 1930 ਸਾਈਬਰ ਹੈਲਪਲਾਈਨ 'ਤੇ ਦੱਸ ਦਿੱਤਾ ਹੈ। "
            "ਕ੍ਰਿਪਾ ਕਰਕੇ ਸਾਰੇ ਸਾਵਧਾਨ ਰਹੋ: ਅਜਿਹੀ ਵੀਡੀਓ ਕਾਲ ਨਾ ਸੁਣੋ, ਓਟੀਪੀ ਨਾ ਦਿਓ ਅਤੇ ਕੋਈ ਪੈਸੇ ਨਾ ਭੇਜੋ।"
        )
    }
}
