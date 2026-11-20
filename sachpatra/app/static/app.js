/**
 * SachPatra: Frontend Application Core
 * Vanilla JS, no build steps, no external CDN dependencies.
 * Full multilingual support (EN, HI, PA) with local speech synthesis.
 */

(function () {
  'use strict';

  // =========================================================================
  // UI Translations (EN / HI / PA)
  // =========================================================================
  const I18N = {
    en: {
      app_title: 'सचपत्र <span class="brand-sub">SachPatra</span>',
      app_tagline: 'Citizen Digital Arrest & Cyber Extortion Shield',
      tab_check: 'Check',
      tab_dashboard: 'Dashboard',
      tab_how_it_works: 'How It Works',
      gov_warning_title: 'Supreme Court of India Ruling:',
      gov_warning_body: '"Digital Arrest" has zero legal validity in India. Police, CBI, ED, and courts NEVER arrest citizens online or demand money on video calls.',
      mode_text: 'Paste Message',
      mode_image: 'Upload Notice Photo',
      mode_call: 'Describe a Call',
      samples_label: 'Quick Test:',
      sample_scam_cbi: '🚨 CBI Digital Arrest',
      sample_scam_parcel: '📦 FedEx Narcotics',
      sample_benign_otp: '✅ Normal Bank OTP',
      sample_benign_bill: '💡 Electricity Bill',
      text_input_label: 'Notice text, message, or call description',
      text_placeholder: 'Paste the message, chat screenshot text, or describe what the caller said...',
      call_placeholder: 'Describe the call: Who called? What agency did they claim to be from? Did they demand to stay on video call or transfer money to a safe account?',
      clear_btn: 'Clear',
      dropzone_main: 'Tap to select or drop notice photo',
      dropzone_sub: 'JPG, PNG, WebP up to 5MB. EXIF stripped in memory.',
      btn_analyze: 'Check for Digital Arrest',
      score_likely: 'Likely Scam',
      score_suspicious: 'Suspicious',
      score_cannot_verify: 'Cannot Verify',
      plain_summary_title: 'Simple Explanation for Citizens',
      read_aloud: 'Read Aloud',
      stop_reading: 'Stop',
      voice_unavailable: 'Voice speech output is not supported by your current browser engine.',
      action_plan_title: 'Do this in the next 10 minutes',
      action_plan_subtitle: 'Step-by-step emergency protection protocol. Check each as you finish.',
      why_title: 'Why We Think So (Detected Red Flags)',
      why_subtitle: 'Transparent rules matched in your input with authoritative citations.',
      drafts_title: 'Ready-to-Use Emergency Drafts',
      drafts_subtitle: 'Pre-filled with extracted facts ready to copy or share immediately.',
      draft_tab_complaint: 'Portal Complaint',
      draft_tab_script: '1930 Call Script',
      draft_tab_family: 'Family WhatsApp Alert',
      btn_copy: 'Copy Draft',
      btn_share_family: 'Share Family Alert',
      dash_title: 'Anonymized Live Dashboard',
      dash_sub: 'Aggregate community metrics. Only counters stored; zero message content or PII is ever retained.',
      stat_total: 'Total Screenings',
      stat_scams: 'Likely Scams',
      stat_suspicious: 'Suspicious Cases',
      stat_cannot_verify: 'Unverified / Benign',
      chart_verdicts: 'Screening Verdicts Breakdown',
      chart_rules: 'Top Triggered Red Flags',
      chart_languages: 'Language Distribution',
      chart_timeline: 'Last 14 Days Activity Volume',
      trans_title: 'Transparency & How SachPatra Works',
      trans_sub: 'Open audit: Complete architecture, rules, and privacy commitments.',
      g1_title: '1. Deterministic Rule Engine',
      g1_body: 'Verdicts come ONLY from transparent deterministic rules. AI never decides the verdict and cannot hallucinate a scam status.',
      g2_title: '2. Absolute Privacy',
      g2_body: 'Zero content logging. Neither notice texts nor uploaded images are saved to disk or database. Only anonymous counters are kept.',
      g3_title: '3. AI Only Reads & Explains',
      g3_body: 'Multimodal AI is used exclusively as an optional reader for notice images and for simple explanations. If offline, the core rules still work 100%.',
      g4_title: '4. Grounded in Law',
      g4_body: "Backed by the Supreme Court of India's landmark suo motu order (17 Oct 2025) confirming digital arrest has no legal authority.",
      public_rules_title: 'Public Rule Inventory (14 Rules)',
      public_rules_sub: 'Every rule evaluated in the deterministic engine is publicly listed below with weights and rationale.',
      toast_copied: 'Draft copied to clipboard!',
      toast_empty_text: 'Please paste message text or upload an image first.',
      toast_offline: 'Connection error. Please check your internet or retry.',
      toast_image_reading_offline: 'Image reading is currently offline; please paste the text.',
      source_link_label: 'Official Reference',
      plain_summary_likely_scam: "Warning: This message shows clear signs of a digital arrest scam. Real police or court officials never arrest people over video calls or demand money. Please hang up immediately, speak with your family, and call helpline 1930.",
      plain_summary_suspicious: "Caution: This message contains suspicious official claims or urgent payment demands. Do not transfer any money or disclose private information without independently verifying directly with local authorities.",
      plain_summary_cannot_verify: "Notice: Common digital arrest patterns were not found, but always remain vigilant. Government agencies will never rush you or ask for secret money transfers. If pressured, dial 1930."
    },
    hi: {
      app_title: 'सचपत्र <span class="brand-sub">SachPatra</span>',
      app_tagline: 'डिजिटल अरेस्ट व साइबर जबरन वसूली से नागरिक सुरक्षा',
      tab_check: 'जांचें',
      tab_dashboard: 'डैशबोर्ड',
      tab_how_it_works: 'यह कैसे काम करता है',
      gov_warning_title: 'सुप्रीम कोर्ट का महत्वपूर्ण आदेश:',
      gov_warning_body: 'भारत में "डिजिटल अरेस्ट" का कोई कानूनी अस्तित्व नहीं है। पुलिस, सीबीआई, ईडी या अदालतें कभी भी वीडियो कॉल पर गिरफ्तारी नहीं करतीं और न ही पैसे मांगती हैं।',
      mode_text: 'संदेश पेस्ट करें',
      mode_image: 'नोटिस फोटो अपलोड करें',
      mode_call: 'कॉल का विवरण दें',
      samples_label: 'नमूना जांचें:',
      sample_scam_cbi: '🚨 सीबीआई डिजिटल अरेस्ट',
      sample_scam_parcel: '📦 फेडेक्स पार्सल घोटाला',
      sample_benign_otp: '✅ सामान्य बैंक ओटीपी',
      sample_benign_bill: '💡 बिजली बिल रिमाइंडर',
      text_input_label: 'नोटिस या कॉल का विवरण',
      text_placeholder: 'संदेश, व्हाट्सएप चैट या नोटिस का टेक्स्ट यहां पेस्ट करें...',
      call_placeholder: 'कॉल का विवरण दें: फोन किसने किया था? खुद को किस एजेंसी का बताया? क्या उन्होंने वीडियो कॉल पर रहने या पैसे भेजने को कहा?',
      clear_btn: 'हटाएं',
      dropzone_main: 'नोटिस की फोटो चुनने के लिए टैप करें',
      dropzone_sub: 'JPG, PNG, WebP (अधिकतम 5MB)। फोन से सीधे अपलोड करें।',
      btn_analyze: 'डिजिटल अरेस्ट की जांच करें',
      score_likely: 'घोटाले की पूरी संभावना',
      score_suspicious: 'संदिग्ध',
      score_cannot_verify: 'पुष्टि नहीं हो सकी',
      plain_summary_title: 'बुजुर्गों और परिवारों के लिए सरल भाषा में',
      read_aloud: 'बोलकर सुनाएं',
      stop_reading: 'रोकें',
      voice_unavailable: 'आपके ब्राउज़र में बोलकर सुनाने की सुविधा उपलब्ध नहीं है।',
      action_plan_title: 'अगले 10 मिनट में यह जरूरी काम करें',
      action_plan_subtitle: 'तुरंत सुरक्षा के 6 कदम। काम पूरा होने पर टिक करें।',
      why_title: 'हमें ऐसा क्यों लगा (पहचाने गए खतरे)',
      why_subtitle: 'संदेश में मिले संदिग्ध पैटर्न और सरकारी कानूनी संदर्भ।',
      drafts_title: 'शिकायत व चेतावनी के तैयार संदेश',
      drafts_subtitle: 'ज़रूरी जानकारियों के साथ तैयार प्रारूप, तुरंत कॉपी या शेयर करें।',
      draft_tab_complaint: 'पोर्टल शिकायत ड्राफ्ट',
      draft_tab_script: '1930 कॉल स्क्रिप्ट',
      draft_tab_family: 'परिवार हेतु व्हाट्सएप अलर्ट',
      btn_copy: 'कॉपी करें',
      btn_share_family: 'व्हाट्सएप पर शेयर करें',
      dash_title: 'सार्वजनिक लाइव डैशबोर्ड',
      dash_sub: 'सामूहिक सुरक्षा आंकड़े। केवल संख्याओं की गिनती रखी जाती है; कोई निजी डेटा नहीं रखा जाता।',
      stat_total: 'कुल जांच',
      stat_scams: 'पहचाने गए घोटाले',
      stat_suspicious: 'संदिग्ध मामले',
      stat_cannot_verify: 'सामान्य / असत्यापित',
      chart_verdicts: 'परिणामों का वितरण',
      chart_rules: 'सबसे ज्यादा मिलने वाले खतरे',
      chart_languages: 'भाषाओं का वितरण',
      chart_timeline: 'पिछले 14 दिनों की गतिविधि',
      trans_title: 'पारदर्शिता और सचपत्र की कार्यप्रणाली',
      trans_sub: 'खुली व्यवस्था: नियम, तकनीक और गोपनीयता की पूरी गारंटी।',
      g1_title: '1. निश्चित नियमों द्वारा निर्णय',
      g1_body: 'फैसले केवल सार्वजनिक व पारदर्शी नियमों द्वारा लिए जाते हैं। एआई कभी भी अपनी मर्जी से फैसला नहीं लेता।',
      g2_title: '2. पूर्ण गोपनीयता',
      g2_body: 'कोई निजी संदेश या फोटो सर्वर पर सेव नहीं होता। केवल अनाम संख्याओं की गिनती सुरक्षित रहती है।',
      g3_title: '3. एआई केवल पढ़ने व समझाने के लिए',
      g3_body: 'फोटो से टेक्स्ट पढ़ने और सरल भाषा में समझाने के लिए ही एआई का उपयोग होता है। नियम हमेशा काम करते हैं।',
      g4_title: '4. कानूनी मान्यता पर आधारित',
      g4_body: 'सुप्रीम कोर्ट के 17 अक्टूबर 2025 के आदेश पर आधारित, जिसमें डिजिटल अरेस्ट को पूरी तरह गैरकानूनी ठहराया गया है।',
      public_rules_title: 'सार्वजनिक नियम सूची (14 नियम)',
      public_rules_sub: 'स्क्रीनिंग में इस्तेमाल होने वाले सभी 14 नियम नीचे विवरण सहित दिए गए हैं।',
      toast_copied: 'ड्राफ्ट कॉपी हो गया!',
      toast_empty_text: 'कृपया पहले कोई संदेश लिखें या फोटो अपलोड करें।',
      toast_offline: 'इंटरनेट कनेक्शन में समस्या है। कृपया दोबारा प्रयास करें।',
      toast_image_reading_offline: 'इमेज पढ़ने की सेवा ऑफलाइन है; कृपया टेक्स्ट पेस्ट करें।',
      source_link_label: 'आधिकारिक संदर्भ',
      plain_summary_likely_scam: "जरूरी चेतावनी: इस संदेश में डिजिटल अरेस्ट धोखाधड़ी के पक्के लक्षण हैं। असली पुलिस या जज कभी भी वीडियो कॉल पर गिरफ्तारी नहीं करते और न ही पैसे मांगते हैं। कृपया तुरंत फोन काटें, अपने परिवार को बताएं और 1930 पर फोन करें।",
      plain_summary_suspicious: "सावधानी: इस संदेश में संदिग्ध सरकारी दावे या पैसों की जल्दबाजी भरी मांग है। स्थानीय अधिकारियों या बैंक से सीधे जांच किए बिना कोई पैसा न भेजें और न ही अपनी निजी जानकारी साझा करें।",
      plain_summary_cannot_verify: "सूचना: सामान्य धोखाधड़ी के संकेत नहीं मिले हैं, फिर भी सतर्क रहें। सरकारी विभाग कभी भी फोन पर जल्दबाजी नहीं कराते और न ही किसी गोपनीय खाते में पैसे मांगते हैं। यदि कोई दबाव डाले तो 1930 मिलाएं।"
    },
    pa: {
      app_title: 'ਸੱਚਪੱਤਰ <span class="brand-sub">SachPatra</span>',
      app_tagline: 'ਡਿਜੀਟਲ ਅਰੈਸਟ ਅਤੇ ਸਾਈਬਰ ਠੱਗੀ ਤੋਂ ਨਾਗਰਿਕ ਸੁਰੱਖਿਆ',
      tab_check: 'ਜਾਂਚੋ',
      tab_dashboard: 'ਡੈਸ਼ਬੋਰਡ',
      tab_how_it_works: 'ਇਹ ਕਿਵੇਂ ਕੰਮ ਕਰਦਾ ਹੈ',
      gov_warning_title: 'ਸੁਪਰੀਮ ਕੋਰਟ ਦਾ ਵੱਡਾ ਫੈਸਲਾ:',
      gov_warning_body: 'ਭਾਰਤ ਵਿੱਚ "ਡਿਜੀਟਲ ਅਰੈਸਟ" ਦਾ ਕੋਈ ਕਾਨੂੰਨੀ ਆਧਾਰ ਨਹੀਂ ਹੈ। ਪੁਲਿਸ, ਸੀਬੀਆਈ, ਈਡੀ ਜਾਂ ਅਦਾਲਤਾਂ ਕਦੇ ਵੀ ਵੀਡੀਓ ਕਾਲ \'ਤੇ ਗ੍ਰਿਫ਼ਤਾਰੀ ਨਹੀਂ ਕਰਦੀਆਂ ਅਤੇ ਨਾ ਹੀ ਪੈਸੇ ਮੰਗਦੀਆਂ ਹਨ।',
      mode_text: 'ਸੁਨੇਹਾ ਪੇਸਟ ਕਰੋ',
      mode_image: 'ਨੋਟਿਸ ਦੀ ਫੋਟੋ ਅਪਲੋਡ ਕਰੋ',
      mode_call: 'ਕਾਲ ਦਾ ਵੇਰਵਾ ਦਿਓ',
      samples_label: 'ਨਮੂਨਾ ਪਰਖੋ:',
      sample_scam_cbi: '🚨 ਸੀਬੀਆਈ ਡਿਜੀਟਲ ਅਰੈਸਟ',
      sample_scam_parcel: '📦 ਫੈਡਐਕਸ ਪਾਰਸਲ ਠੱਗੀ',
      sample_benign_otp: '✅ ਆਮ ਬੈਂਕ ਓਟੀਪੀ',
      sample_benign_bill: '💡 ਬਿਜਲੀ ਬਿੱਲ ਰਿਮਾਈਂਡਰ',
      text_input_label: 'ਸੁਨੇਹਾ ਜਾਂ ਕਾਲ ਦਾ ਵੇਰਵਾ',
      text_placeholder: 'ਸੁਨੇਹਾ, ਵਟਸਐਪ ਚੈਟ ਜਾਂ ਨੋਟਿਸ ਦਾ ਟੈਕਸਟ ਇੱਥੇ ਪੇਸਟ ਕਰੋ...',
      call_placeholder: 'ਕਾਲ ਦਾ ਵੇਰਵਾ ਦਿਓ: ਕਿਸਨੇ ਫੋਨ ਕੀਤਾ ਸੀ? ਕਿਹੜੀ ਏਜੰਸੀ ਦਾ ਨਾਮ ਲਿਆ? ਕੀ ਵੀਡੀਓ ਕਾਲ \'ਤੇ ਰਹਿਣ ਜਾਂ ਪੈਸੇ ਭੇਜਣ ਲਈ ਕਿਹਾ?',
      clear_btn: 'ਸਾਫ਼ ਕਰੋ',
      dropzone_main: 'ਨੋਟਿਸ ਦੀ ਤਸਵੀਰ ਚੁਣਨ ਲਈ ਟੈਪ ਕਰੋ',
      dropzone_sub: 'JPG, PNG, WebP (ਵੱਧ ਤੋਂ ਵੱਧ 5MB)। ਫੋਨ ਤੋਂ ਸਿੱਧਾ ਅਪਲੋਡ ਕਰੋ।',
      btn_analyze: 'ਡਿਜੀਟਲ ਅਰੈਸਟ ਦੀ ਜਾਂਚ ਕਰੋ',
      score_likely: 'ਠੱਗੀ ਦੀ ਪੂਰੀ ਸੰਭਾਵਨਾ',
      score_suspicious: 'ਸ਼ੱਕੀ',
      score_cannot_verify: 'ਪੁਸ਼ਟੀ ਨਹੀਂ ਹੋ ਸਕੀ',
      plain_summary_title: 'ਬਜ਼ੁਰਗਾਂ ਅਤੇ ਪਰਿਵਾਰਾਂ ਲਈ ਸੌਖੀ ਬੋਲੀ ਵਿੱਚ',
      read_aloud: 'ਬੋਲ ਕੇ ਸੁਣਾਓ',
      stop_reading: 'ਰੋਕੋ',
      voice_unavailable: 'ਤੁਹਾਡੇ ਬ੍ਰਾਊਜ਼ਰ ਵਿੱਚ ਬੋਲ ਕੇ ਸੁਣਾਉਣ ਦੀ ਸੁਵਿਧਾ ਉਪਲਬਧ ਨਹੀਂ ਹੈ।',
      action_plan_title: 'ਅਗਲੇ 10 ਮਿੰਟਾਂ ਵਿੱਚ ਇਹ ਜ਼ਰੂਰੀ ਕਦਮ ਚੁੱਕੋ',
      action_plan_subtitle: 'ਤੁਰੰਤ ਬਚਾਅ ਦੇ 6 ਕਦਮ। ਕੰਮ ਪੂਰਾ ਹੋਣ \'ਤੇ ਟਿੱਕ ਕਰੋ।',
      why_title: 'ਸਾਨੂੰ ਅਜਿਹਾ ਕਿਉਂ ਲੱਗਿਆ (ਫੜੇ ਗਏ ਖ਼ਤਰੇ)',
      why_subtitle: 'ਸੁਨੇਹੇ ਵਿੱਚ ਮਿਲੇ ਸ਼ੱਕੀ ਪੈਟਰਨ ਅਤੇ ਸਰਕਾਰੀ ਕਾਨੂੰਨੀ ਹਵਾਲੇ।',
      drafts_title: 'ਸ਼ਿਕਾਇਤ ਅਤੇ ਚੇਤਾਵਨੀ ਦੇ ਤਿਆਰ ਖਰੜੇ',
      drafts_subtitle: 'ਜ਼ਰੂਰੀ ਵੇਰਵਿਆਂ ਨਾਲ ਤਿਆਰ ਸੰਦੇਸ਼, ਤੁਰੰਤ ਕਾਪੀ ਜਾਂ ਸ਼ੇਅਰ ਕਰੋ।',
      draft_tab_complaint: 'ਪੋਰਟਲ ਸ਼ਿਕਾਇਤ ਡਰਾਫਟ',
      draft_tab_script: '1930 ਕਾਲ ਸਕ੍ਰਿਪਟ',
      draft_tab_family: 'ਪਰਿਵਾਰ ਲਈ ਵਟਸਐਪ ਅਲਰਟ',
      btn_copy: 'ਕਾਪੀ ਕਰੋ',
      btn_share_family: 'ਵਟਸਐਪ \'ਤੇ ਸ਼ੇਅਰ ਕਰੋ',
      dash_title: 'ਲਾਈਵ ਡੈਸ਼ਬੋਰਡ',
      dash_sub: 'ਜਨਤਕ ਸੁਰੱਖਿਆ ਅੰਕੜੇ। ਸਿਰਫ਼ ਸੰਖਿਆਵਾਂ ਦੀ ਗਿਣਤੀ ਰੱਖੀ ਜਾਂਦੀ ਹੈ; ਕੋਈ ਨਿੱਜੀ ਜਾਣਕਾਰੀ ਨਹੀਂ ਰੱਖੀ ਜਾਂਦੀ।',
      stat_total: 'ਕੁੱਲ ਜਾਂਚਾਂ',
      stat_scams: 'ਫੜੀਆਂ ਗਈਆਂ ਠੱਗੀਆਂ',
      stat_suspicious: 'ਸ਼ੱਕੀ ਮਾਮਲੇ',
      stat_cannot_verify: 'ਆਮ / ਅਣਪ੍ਰਮਾਣਿਤ',
      chart_verdicts: 'ਨਤੀਜਿਆਂ ਦੀ ਵੰਡ',
      chart_rules: 'ਸਭ ਤੋਂ ਵੱਧ ਸਾਹਮਣੇ ਆਏ ਖ਼ਤਰੇ',
      chart_languages: 'ਭਾਸ਼ਾਵਾਂ ਦੀ ਵੰਡ',
      chart_timeline: 'ਪਿਛਲੇ 14 ਦਿਨਾਂ ਦੀ ਗਤੀਵਿਧੀ',
      trans_title: 'ਪਾਰਦਰਸ਼ਤਾ ਅਤੇ ਸੱਚਪੱਤਰ ਦੀ ਕਾਰਜਪ੍ਰਣਾਲੀ',
      trans_sub: 'ਖੁੱਲ੍ਹਾ ਪ੍ਰਬੰਧ: ਨਿਯਮ, ਤਕਨੀਕ ਅਤੇ ਗੁਪਤਤਾ ਦੀ ਪੂਰੀ ਗਰੰਟੀ।',
      g1_title: '1. ਪੱਕੇ ਨਿਯਮਾਂ ਦੁਆਰਾ ਫੈਸਲਾ',
      g1_body: 'ਨਤੀਜੇ ਕੇਵਲ ਪਾਰਦਰਸ਼ੀ ਨਿਯਮਾਂ ਤੋਂ ਤੈਅ ਹੁੰਦੇ ਹਨ। ਏਆਈ ਕਦੇ ਵੀ ਆਪਣੀ ਮਰਜ਼ੀ ਨਾਲ ਫੈਸਲਾ ਨਹੀਂ ਕਰਦਾ।',
      g2_title: '2. ਮੁਕੰਮਲ ਗੁਪਤਤਾ',
      g2_body: 'ਕੋਈ ਨਿੱਜੀ ਸੁਨੇਹਾ ਜਾਂ ਫੋਟੋ ਸਰਵਰ \'ਤੇ ਸੇਵ ਨਹੀਂ ਹੁੰਦੀ। ਸਿਰਫ਼ ਗੁਮਨਾਮ ਅੰਕੜੇ ਰੱਖੇ ਜਾਂਦੇ ਹਨ।',
      g3_title: '3. ਏਆਈ ਸਿਰਫ਼ ਪੜ੍ਹਨ ਅਤੇ ਸਮਝਾਉਣ ਲਈ',
      g3_body: 'ਫੋਟੋ ਤੋਂ ਟੈਕਸਟ ਪੜ੍ਹਨ ਅਤੇ ਸਰਲ ਭਾਸ਼ਾ ਵਿੱਚ ਦੱਸਣ ਲਈ ਹੀ ਏਆਈ ਵਰਤਿਆ ਜਾਂਦਾ ਹੈ। ਨਿਯਮ ਹਮੇਸ਼ਾ ਚੱਲਦੇ ਹਨ।',
      g4_title: '4. ਕਾਨੂੰਨੀ ਮਾਨਤਾ \'ਤੇ ਆਧਾਰਿਤ',
      g4_body: "ਸੁਪਰੀਮ ਕੋਰਟ ਦੇ 17 ਅਕਤੂਬਰ 2025 ਦੇ ਹੁਕਮਾਂ 'ਤੇ ਆਧਾਰਿਤ, ਜਿਸ ਵਿੱਚ ਡਿਜੀਟਲ ਅਰੈਸਟ ਨੂੰ ਪੂਰੀ ਤਰ੍ਹਾਂ ਗੈਰ-ਕਾਨੂੰਨੀ ਐਲਾਨਿਆ ਗਿਆ ਹੈ।",
      public_rules_title: 'ਜਨਤਕ ਨਿਯਮ ਸੂਚੀ (14 ਨਿਯਮ)',
      public_rules_sub: 'ਸਕ੍ਰੀਨਿੰਗ ਵਿੱਚ ਵਰਤੇ ਜਾਂਦੇ ਸਾਰੇ 14 ਨਿਯਮ ਹੇਠਾਂ ਵੇਰਵੇ ਸਹਿਤ ਦਿੱਤੇ ਗਏ ਹਨ।',
      toast_copied: 'ਡਰਾਫਟ ਕਾਪੀ ਹੋ ਗਿਆ!',
      toast_empty_text: 'ਕਿਰਪਾ ਕਰਕੇ ਪਹਿਲਾਂ ਕੋਈ ਸੁਨੇਹਾ ਲਿਖੋ ਜਾਂ ਫੋਟੋ ਅਪਲੋਡ ਕਰੋ।',
      toast_offline: 'ਇੰਟਰਨੈੱਟ ਕਨੈਕਸ਼ਨ ਵਿੱਚ ਸਮੱਸਿਆ ਹੈ। ਕਿਰਪਾ ਕਰਕੇ ਦੁਬਾਰਾ ਕੋਸ਼ਿਸ਼ ਕਰੋ।',
      toast_image_reading_offline: 'ਤਸਵੀਰ ਪੜ੍ਹਨ ਦੀ ਸੇਵਾ ਆਫ਼ਲਾਈਨ ਹੈ; ਕਿਰਪਾ ਕਰਕੇ ਟੈਕਸਟ ਪੇਸਟ ਕਰੋ।',
      source_link_label: 'ਸਰਕਾਰੀ ਹਵਾਲਾ',
      plain_summary_likely_scam: "ਜ਼ਰੂਰੀ ਚੇਤਾਵਨੀ: ਇਸ ਸੁਨੇਹੇ ਵਿੱਚ ਡਿਜੀਟਲ ਅਰੈਸਟ ਠੱਗੀ ਦੇ ਪੱਕੇ ਲੱਛਣ ਹਨ। ਅਸਲੀ ਪੁਲਿਸ ਜਾਂ ਜੱਜ ਕਦੇ ਵੀ ਵੀਡੀਓ ਕਾਲ 'ਤੇ ਗ੍ਰਿਫ਼ਤਾਰੀ ਨਹੀਂ ਕਰਦੇ ਅਤੇ ਨਾ ਹੀ ਪੈਸੇ ਮੰਗਦੇ ਹਨ। ਕਿਰਪਾ ਕਰਕੇ ਤੁਰੰਤ ਫੋਨ ਕੱਟੋ, ਆਪਣੇ ਪਰਿਵਾਰ ਨੂੰ ਦੱਸੋ ਅਤੇ 1930 'ਤੇ ਫੋਨ ਕਰੋ।",
      plain_summary_suspicious: "ਸਾਵਧਾਨੀ: ਇਸ ਸੁਨੇਹੇ ਵਿੱਚ ਸ਼ੱਕੀ ਸਰਕਾਰੀ ਦਾਅਵੇ ਜਾਂ ਪੈਸਿਆਂ ਦੀ ਕਾਹਲੀ ਭਰੀ ਮੰਗ ਹੈ। ਸਥਾਨਕ ਅਧਿਕਾਰੀਆਂ ਜਾਂ ਬੈਂਕ ਤੋਂ ਸਿੱਧੀ ਜਾਂਚ ਕੀਤੇ ਬਿਨਾਂ ਕੋਈ ਪੈਸੇ ਨਾ ਭੇਜੋ ਅਤੇ ਨਾ ਹੀ ਨਿੱਜੀ ਜਾਣਕਾਰੀ ਦਿਓ।",
      plain_summary_cannot_verify: "ਸੂਚਨਾ: ਆਮ ਠੱਗੀ ਦੇ ਸੰਕੇਤ ਨਹੀਂ ਮਿਲੇ, ਫਿਰ ਵੀ ਹਮੇਸ਼ਾ ਚੌਕਸ ਰਹੋ। ਸਰਕਾਰੀ ਵਿਭਾਗ ਕਦੇ ਵੀ ਫੋਨ 'ਤੇ ਕਾਹਲੀ ਨਹੀਂ ਕਰਵਾਉਂਦੇ ਅਤੇ ਨਾ ਹੀ ਕਿਸੇ ਗੁਪਤ ਖਾਤੇ ਵਿੱਚ ਪੈਸੇ ਮੰਗਦੇ ਹਨ। ਜੇਕਰ ਕੋਈ ਦਬਾਅ ਪਾਵੇ ਤਾਂ 1930 ਡਾਇਲ ਕਰੋ।"
    }
  };

  // Sample texts for chips
  const SAMPLES = {
    scam_cbi: {
      en: "You are under digital arrest by CBI officer. Stay on video call and do not disconnect. Transfer 50000 rupees verification amount to safe account.",
      hi: "केंद्रीय जांच ब्यूरो सीबीआई: आप पर डिजिटल अरेस्ट लगाया गया है। वीडियो कॉल पर रहें और कैमरा चालू रखें। जमानत राशि तुरंत सुरक्षित खाते में ट्रांसफर करें।",
      pa: "ਸੀਬੀਆਈ ਹੈੱਡਕੁਆਰਟਰ: ਤੁਹਾਨੂੰ ਡਿਜੀਟਲ ਗ੍ਰਿਫ਼ਤਾਰੀ ਅਧੀਨ ਲਿਆ ਗਿਆ ਹੈ। ਵੀਡੀਓ ਕਾਲ 'ਤੇ ਰਹੋ ਅਤੇ ਕੈਮਰਾ ਆਨ ਰੱਖੋ। ਜ਼ਮਾਨਤ ਰਾਸ਼ੀ ਤੁਰੰਤ ਸੁਰੱਖਿਅਤ ਖਾਤੇ ਵਿੱਚ ਭੇਜੋ।"
    },
    scam_parcel: {
      en: "Mumbai Police Cyber Cell: Your FedEx courier package was intercepted containing MDMA drugs and fake passports. Pay bail amount to clear charges.",
      hi: "मुंबई पुलिस साइबर सेल: आपके फेडेक्स पार्सल में नशीली दवाएं और पासपोर्ट जब्त किए गए हैं। गिरफ्तारी वारंट से बचने के लिए जुर्माना भरें।",
      pa: "ਮੁੰਬਈ ਪੁਲਿਸ: ਤੁਹਾਡੇ ਪਾਰਸਲ ਵਿੱਚ ਨਸ਼ੀਲੀਆਂ ਦਵਾਈਆਂ ਅਤੇ ਪਾਸਪੋਰਟ ਫੜੇ ਗਏ ਹਨ। 2 ਘੰਟਿਆਂ ਵਿੱਚ ਗ੍ਰਿਫ਼ਤਾਰੀ ਵਾਰੰਟ ਜਾਰੀ ਹੋਵੇਗਾ, ਜੁਰਮਾਨਾ ਭਰੋ।"
    },
    benign_otp: {
      en: "Dear customer, your OTP for transaction of Rs 450 at Swiggy is 849201. Valid for 10 minutes. Do not share this OTP with anyone.",
      hi: "प्रिय ग्राहक, फ्लिपकार्ट पर 750 रुपये के ऑर्डर के लिए आपका ओटीपी 394812 है। यह किसी के साथ साझा न करें।",
      pa: "ਪਿਆਰੇ ਗਾਹਕ, ਤੁਹਾਡੇ ਖਾਤੇ ਦੇ ਲੈਣ-ਦੇਣ ਲਈ ਓਟੀਪੀ 394812 ਹੈ। ਇਹ ਕਿਸੇ ਨਾਲ ਸਾਂਝਾ ਨਾ ਕਰੋ।"
    },
    benign_bill: {
      en: "Electricity bill reminder: Your bill of Rs 1420 for consumer account 98210 is due on 25-Nov. Pay on the state electricity board portal.",
      hi: "बिजली बिल सूचना: उपभोक्ता खाता 98210 के लिए 1420 रुपये का बिल 25 नवंबर तक देय है। बिजली विभाग के पोर्टल पर भुगतान करें।",
      pa: "ਬਿਜਲੀ ਬਿੱਲ ਸੂਚਨਾ: ਉਪਭੋਗਤਾ ਖਾਤਾ 98210 ਲਈ 1420 ਰੁਪਏ ਦਾ ਬਿੱਲ 25 ਨਵੰਬਰ ਤੱਕ ਭਰਨਯੋਗ ਹੈ। ਬਿਜਲੀ ਬੋਰਡ ਦੇ ਪੋਰਟਲ 'ਤੇ ਭੁਗਤਾਨ ਕਰੋ।"
    }
  };

  // State Management
  const state = {
    lang: 'en',
    activeTab: 'tab-check',
    inputMode: 'text', // 'text', 'image', 'call'
    selectedFile: null,
    currentResult: null,
    activeDraft: 'complaint',
    speechUtterance: null,
    isSpeaking: false
  };

  // DOM Elements
  const elements = {
    html: document.documentElement,
    langBtns: document.querySelectorAll('.lang-btn'),
    navTabs: document.querySelectorAll('.nav-tab'),
    tabPanes: document.querySelectorAll('.tab-pane'),
    modeBtns: document.querySelectorAll('.mode-btn'),
    sampleChips: document.querySelectorAll('.chip'),
    textInputArea: document.getElementById('text-input-area'),
    imageInputArea: document.getElementById('image-input-area'),
    inputText: document.getElementById('input-text'),
    charCount: document.getElementById('char-count'),
    btnClearText: document.getElementById('btn-clear-text'),
    dropZone: document.getElementById('drop-zone'),
    fileInput: document.getElementById('file-input'),
    imagePreviewWrapper: document.getElementById('image-preview-wrapper'),
    imagePreview: document.getElementById('image-preview'),
    previewFilename: document.getElementById('preview-filename'),
    previewFilesize: document.getElementById('preview-filesize'),
    btnRemoveImage: document.getElementById('btn-remove-image'),
    btnAnalyze: document.getElementById('btn-analyze'),
    loadingSkeleton: document.getElementById('loading-skeleton'),
    resultContainer: document.getElementById('result-container'),
    toastContainer: document.getElementById('toast-container'),
    // Result elements
    verdictCard: document.getElementById('verdict-card'),
    verdictIcon: document.getElementById('verdict-icon'),
    verdictBadge: document.getElementById('verdict-badge'),
    verdictTitle: document.getElementById('verdict-title'),
    verdictSummary: document.getElementById('verdict-summary'),
    scoreValue: document.getElementById('score-value'),
    scoreBar: document.getElementById('score-bar'),
    engineTag: document.getElementById('engine-tag'),
    plainSummaryText: document.getElementById('plain-summary-text'),
    btnReadAloud: document.getElementById('btn-read-aloud'),
    voiceBtnText: document.getElementById('voice-btn-text'),
    voiceUnavailableNote: document.getElementById('voice-unavailable-note'),
    actionStepsList: document.getElementById('action-steps-list'),
    reasonsAccordion: document.getElementById('reasons-accordion'),
    draftTabs: document.querySelectorAll('.draft-tab'),
    draftText: document.getElementById('draft-text'),
    btnCopyDraft: document.getElementById('btn-copy-draft'),
    btnShareFamily: document.getElementById('btn-share-family'),
    resultDisclaimer: document.getElementById('result-disclaimer'),
    // Dashboard elements
    statTotalScans: document.getElementById('stat-total-scans'),
    statScams: document.getElementById('stat-scams'),
    statSuspicious: document.getElementById('stat-suspicious'),
    statCannotVerify: document.getElementById('stat-cannot-verify'),
    chartVerdictsContainer: document.getElementById('chart-verdicts-container'),
    chartRulesContainer: document.getElementById('chart-rules-container'),
    chartLanguagesContainer: document.getElementById('chart-languages-container'),
    chartTimelineContainer: document.getElementById('chart-timeline-container'),
    // Transparency elements
    rulesListContainer: document.getElementById('rules-list-container')
  };

  // =========================================================================
  // Initialisation & Language Switching
  // =========================================================================
  function initLanguage() {
    let saved = localStorage.getItem('sachpatra_lang');
    if (!saved) {
      const navLang = (navigator.language || navigator.userLanguage || 'en').toLowerCase();
      if (navLang.startsWith('hi')) saved = 'hi';
      else if (navLang.startsWith('pa')) saved = 'pa';
      else saved = 'en';
    }
    setLanguage(saved);
  }

  function setLanguage(lang) {
    if (!I18N[lang]) lang = 'en';
    state.lang = lang;
    localStorage.setItem('sachpatra_lang', lang);
    elements.html.setAttribute('lang', lang);

    // Update active button
    elements.langBtns.forEach(btn => {
      const isActive = btn.dataset.lang === lang;
      btn.classList.toggle('active', isActive);
      btn.setAttribute('aria-pressed', isActive ? 'true' : 'false');
    });

    // Translate all static nodes
    document.querySelectorAll('[data-i18n]').forEach(el => {
      const key = el.dataset.i18n;
      if (I18N[lang] && I18N[lang][key]) {
        el.innerHTML = I18N[lang][key];
      }
    });

    // Update placeholders based on mode
    updatePlaceholder();

    // If the input box contains a known sample, switch it to the new language
    for (const [key, variants] of Object.entries(SAMPLES)) {
      if (Object.values(variants).includes(elements.inputText.value.trim())) {
        elements.inputText.value = variants[lang] || variants['en'];
        updateCharCount();
        break;
      }
    }

    // If result is currently visible, re-render localized sections
    if (state.currentResult) {
      renderResult(state.currentResult);
    }
  }

  function updatePlaceholder() {
    if (state.inputMode === 'call') {
      elements.inputText.placeholder = I18N[state.lang].call_placeholder;
    } else {
      elements.inputText.placeholder = I18N[state.lang].text_placeholder;
    }
  }

  // =========================================================================
  // Toast Notifications
  // =========================================================================
  function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast ${type === 'error' ? 'toast-error' : (type === 'success' ? 'toast-success' : '')}`;
    toast.textContent = message;
    elements.toastContainer.appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateY(8px)';
      toast.style.transition = 'all 0.25s ease';
      setTimeout(() => toast.remove(), 250);
    }, 4000);
  }

  // =========================================================================
  // Tab Navigation (Check, Dashboard, How It Works)
  // =========================================================================
  function setTab(tabId) {
    state.activeTab = tabId;
    elements.navTabs.forEach(tab => {
      const isActive = tab.dataset.tab === tabId;
      tab.classList.toggle('active', isActive);
      tab.setAttribute('aria-selected', isActive ? 'true' : 'false');
    });

    elements.tabPanes.forEach(pane => {
      const isTarget = pane.id === tabId;
      pane.classList.toggle('hidden', !isTarget);
      pane.classList.toggle('active', isTarget);
    });

    if (tabId === 'tab-dashboard') {
      loadDashboard();
    } else if (tabId === 'tab-transparency') {
      loadTransparencyRules();
    }
  }

  // =========================================================================
  // Input Modes (Text, Image, Call) & Samples
  // =========================================================================
  function setInputMode(mode) {
    state.inputMode = mode;
    elements.modeBtns.forEach(btn => {
      const isActive = btn.dataset.mode === mode;
      btn.classList.toggle('active', isActive);
      btn.setAttribute('aria-selected', isActive ? 'true' : 'false');
    });

    if (mode === 'image') {
      elements.textInputArea.classList.add('hidden');
      elements.imageInputArea.classList.remove('hidden');
    } else {
      elements.textInputArea.classList.remove('hidden');
      elements.imageInputArea.classList.add('hidden');
      updatePlaceholder();
      elements.inputText.focus();
    }
  }

  const SAMPLE_IMAGES = {
    scam_cbi: { file: '/samples/sample_01_arrest_warrant.png', name: 'sample_01_arrest_warrant.png' },
    scam_parcel: { file: '/samples/sample_03_courier_notice.png', name: 'sample_03_courier_notice.png' },
    benign_otp: { file: '/samples/sample_04_bank_otp.png', name: 'sample_04_bank_otp.png' },
    benign_bill: { file: '/samples/sample_02_freeze_order.png', name: 'sample_02_freeze_order.png' }
  };

  async function loadSampleImage(sampleKey) {
    const meta = SAMPLE_IMAGES[sampleKey] || SAMPLE_IMAGES.scam_cbi;
    try {
      const resp = await fetch(meta.file);
      if (!resp.ok) throw new Error('Failed to load sample image');
      const blob = await resp.blob();
      const file = new File([blob], meta.name, { type: 'image/png' });
      await handleFileSelect(file);
      elements.imageInputArea.scrollIntoView({ behavior: 'smooth', block: 'center' });
    } catch (err) {
      showToast('Could not load sample document', 'error');
    }
  }

  function fillSample(sampleKey) {
    if (state.inputMode === 'image') {
      loadSampleImage(sampleKey);
      return;
    }
    const sampleSet = SAMPLES[sampleKey];
    if (sampleSet) {
      elements.inputText.value = sampleSet[state.lang] || sampleSet.en;
      updateCharCount();
      elements.inputText.focus();
      // Scroll smoothly to checker box
      elements.inputText.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  }

  function updateCharCount() {
    const len = elements.inputText.value.length;
    elements.charCount.textContent = `${len} / 6000`;
  }

  // =========================================================================
  // Image Handling (Downscaling & EXIF Stripping)
  // =========================================================================
  async function handleFileSelect(file) {
    if (!file) return;

    const validTypes = ['image/jpeg', 'image/png', 'image/webp'];
    if (!validTypes.includes(file.type)) {
      showToast('Invalid file format. Please upload JPG, PNG, or WebP.', 'error');
      return;
    }

    if (file.size > 5 * 1024 * 1024) {
      showToast('File size exceeds 5MB limit.', 'error');
      return;
    }

    // Client-side canvas downscale if excessively large (> 2000px)
    try {
      const processedBlob = await downscaleImageIfNeeded(file);
      state.selectedFile = new File([processedBlob], file.name, { type: file.type });

      // Display preview
      const reader = new FileReader();
      reader.onload = (e) => {
        elements.imagePreview.src = e.target.result;
        elements.previewFilename.textContent = file.name;
        elements.previewFilesize.textContent = `${(state.selectedFile.size / 1024).toFixed(1)} KB`;
        elements.imagePreviewWrapper.classList.remove('hidden');
      };
      reader.readAsDataURL(state.selectedFile);
    } catch (err) {
      state.selectedFile = file;
    }
  }

  function downscaleImageIfNeeded(file, maxDimension = 2000) {
    return new Promise((resolve) => {
      const img = new Image();
      img.onload = () => {
        let width = img.width;
        let height = img.height;

        if (width <= maxDimension && height <= maxDimension) {
          resolve(file);
          return;
        }

        if (width > height) {
          height = Math.round((height * maxDimension) / width);
          width = maxDimension;
        } else {
          width = Math.round((width * maxDimension) / height);
          height = maxDimension;
        }

        const canvas = document.createElement('canvas');
        canvas.width = width;
        canvas.height = height;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(img, 0, 0, width, height);
        canvas.toBlob((blob) => resolve(blob || file), file.type, 0.92);
      };
      img.onerror = () => resolve(file);
      img.src = URL.createObjectURL(file);
    });
  }

  function removeSelectedImage() {
    state.selectedFile = null;
    elements.fileInput.value = '';
    elements.imagePreview.src = '';
    elements.imagePreviewWrapper.classList.add('hidden');
  }

  // =========================================================================
  // Analysis API Execution
  // =========================================================================
  async function performAnalysis() {
    stopReadAloud();

    let endpoint = '/api/analyze';
    let bodyData = null;
    let isMultipart = false;

    if (state.inputMode === 'image') {
      if (!state.selectedFile) {
        showToast(I18N[state.lang].toast_empty_text, 'error');
        return;
      }
      endpoint = '/api/analyze-image';
      isMultipart = true;
      bodyData = new FormData();
      bodyData.append('file', state.selectedFile);
      bodyData.append('language', state.lang);
      bodyData.append('channel', 'document');
    } else {
      const text = elements.inputText.value.trim();
      if (!text) {
        showToast(I18N[state.lang].toast_empty_text, 'error');
        elements.inputText.focus();
        return;
      }
      bodyData = JSON.stringify({
        text: text,
        language: state.lang,
        channel: state.inputMode === 'call' ? 'call' : 'message'
      });
    }

    // Show loading skeleton
    elements.btnAnalyze.disabled = true;
    elements.btnAnalyze.querySelector('.btn-spinner').classList.remove('hidden');
    elements.loadingSkeleton.classList.remove('hidden');
    elements.resultContainer.classList.add('hidden');

    try {
      const options = {
        method: 'POST',
        headers: isMultipart ? {} : { 'Content-Type': 'application/json' },
        body: bodyData
      };

      const res = await fetch(endpoint, options);

      if (res.status === 429) {
        showToast('Rate limit reached (20 requests/min). Please wait a moment.', 'error');
        return;
      }

      if (res.status === 503 && state.inputMode === 'image') {
        showToast(I18N[state.lang].toast_image_reading_offline, 'error');
        return;
      }

      if (!res.ok) {
        const errJson = await res.json().catch(() => ({}));
        showToast(errJson.detail || 'Analysis could not be completed.', 'error');
        return;
      }

      const data = await res.json();
      state.currentResult = data;
      renderResult(data);
    } catch (err) {
      showToast(I18N[state.lang].toast_offline, 'error');
    } finally {
      elements.btnAnalyze.disabled = false;
      elements.btnAnalyze.querySelector('.btn-spinner').classList.add('hidden');
      elements.loadingSkeleton.classList.add('hidden');
    }
  }

  // =========================================================================
  // Result Rendering
  // =========================================================================
  function renderResult(data) {
    elements.resultContainer.classList.remove('hidden');

    // 1. Verdict & Color Cards
    const verdict = data.verdict;
    elements.verdictCard.className = `verdict-card verdict-${verdict}`;

    let iconText = '🚨';
    let badgeText = 'Likely Scam';
    let titleText = 'High Risk of Digital Arrest Extortion';
    let barColor = 'var(--scam-red)';

    if (verdict === 'likely_scam') {
      iconText = '🚨';
      badgeText = state.lang === 'hi' ? 'घोटाले की पूरी संभावना' : (state.lang === 'pa' ? 'ਠੱਗੀ ਦੀ ਪੂਰੀ ਸੰਭਾਵਨਾ' : 'Likely Scam');
      titleText = state.lang === 'hi' ? 'डिजिटल अरेस्ट धोखाधड़ी के पक्के संकेत' : (state.lang === 'pa' ? 'ਡਿਜੀਟਲ ਅਰੈਸਟ ਠੱਗੀ ਦੇ ਪੱਕੇ ਸੰਕੇਤ' : 'Digital Arrest Coercion Detected');
      barColor = 'var(--scam-red)';
    } else if (verdict === 'suspicious') {
      iconText = '⚠️';
      badgeText = state.lang === 'hi' ? 'संदिग्ध गतिविधि' : (state.lang === 'pa' ? 'ਸ਼ੱਕੀ ਗਤੀਵਿਧੀ' : 'Suspicious');
      titleText = state.lang === 'hi' ? 'संदिग्ध सरकारी दावे या मांग' : (state.lang === 'pa' ? 'ਸ਼ੱਕੀ ਸਰਕਾਰੀ ਦਾਅਵੇ ਜਾਂ ਮੰਗ' : 'Suspicious Coercion Elements Detected');
      barColor = 'var(--suspicious-amber)';
    } else {
      iconText = 'ℹ️';
      badgeText = state.lang === 'hi' ? 'पुष्टि नहीं हो सकी' : (state.lang === 'pa' ? 'ਪੁਸ਼ਟੀ ਨਹੀਂ ਹੋ ਸਕੀ' : 'Cannot Verify');
      titleText = state.lang === 'hi' ? 'डिजिटल अरेस्ट का कोई ज्ञात पैटर्न नहीं' : (state.lang === 'pa' ? 'ਡਿਜੀਟਲ ਅਰੈਸਟ ਦਾ ਕੋਈ ਜਾਣਿਆ ਪੈਟਰਨ ਨਹੀਂ' : 'No Clear Scam Patterns Found');
      barColor = 'var(--safe-grey)';
    }

    elements.verdictIcon.textContent = iconText;
    elements.verdictBadge.textContent = badgeText;
    elements.verdictTitle.textContent = titleText;
    elements.engineTag.textContent = `Engine: ${data.engine === 'rules+gemini' ? 'Rules + Gemini' : 'Rules'}`;

    // 2. Score Meter
    const score = Math.max(0, Math.min(100, data.score));
    elements.scoreValue.textContent = score;

    // Circumference = 2 * PI * 42 ~= 263.89
    const circumference = 264;
    const offset = circumference - (score / 100) * circumference;
    elements.scoreBar.style.stroke = barColor;
    elements.scoreBar.style.strokeDashoffset = offset;

    // 3. Plain Summary
    const fallbackSummary = I18N[state.lang] && I18N[state.lang]['plain_summary_' + verdict];
    if (state.lang !== data.language && fallbackSummary) {
      elements.plainSummaryText.textContent = fallbackSummary;
    } else {
      elements.plainSummaryText.textContent = data.plain_summary || fallbackSummary || '';
    }

    // 4. Action Steps Checklist
    renderActionSteps(data.action_plan || []);

    // 5. Reasons Accordion
    renderReasons(data.reasons || []);

    // 6. Drafts
    setDraftTab(state.activeDraft);

    // 7. Disclaimer
    elements.resultDisclaimer.textContent = data.disclaimer || '';

    // Scroll to results
    elements.resultContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  function renderActionSteps(steps) {
    elements.actionStepsList.innerHTML = '';
    steps.forEach((step) => {
      const item = document.createElement('div');
      item.className = 'action-step-item';

      const checkbox = document.createElement('input');
      checkbox.type = 'checkbox';
      checkbox.className = 'step-checkbox';
      checkbox.id = `step-check-${step.step}`;
      checkbox.setAttribute('aria-label', `Mark step ${step.step} complete: ${step.title}`);

      checkbox.addEventListener('change', () => {
        item.classList.toggle('checked', checkbox.checked);
      });

      const content = document.createElement('div');
      content.className = 'step-content';

      const header = document.createElement('div');
      header.className = 'step-header';

      const title = document.createElement('h4');
      title.className = 'step-title';
      title.textContent = `${step.step}. ${step.title}`;

      header.appendChild(title);

      if (step.timebox_min) {
        const timeBadge = document.createElement('span');
        timeBadge.className = 'timebox-badge';
        timeBadge.textContent = `${step.timebox_min} Min`;
        header.appendChild(timeBadge);
      }

      const desc = document.createElement('p');
      desc.className = 'step-desc';
      desc.textContent = step.description;

      content.appendChild(header);
      content.appendChild(desc);

      item.appendChild(checkbox);
      item.appendChild(content);
      elements.actionStepsList.appendChild(item);
    });
  }

  function renderReasons(reasons) {
    elements.reasonsAccordion.innerHTML = '';
    if (!reasons || reasons.length === 0) {
      const emptyNote = document.createElement('p');
      emptyNote.style.color = 'var(--text-muted)';
      emptyNote.style.padding = '12px';
      emptyNote.textContent = state.lang === 'hi' 
        ? 'कोई विशिष्ट नियम ट्रिगर नहीं हुआ।' 
        : (state.lang === 'pa' ? 'ਕੋਈ ਖਾਸ ਨਿਯਮ ਟ੍ਰਿਗਰ ਨਹੀਂ ਹੋਇਆ।' : 'No specific red flags triggered.');
      elements.reasonsAccordion.appendChild(emptyNote);
      return;
    }

    reasons.forEach((r, idx) => {
      const item = document.createElement('div');
      item.className = `accordion-item ${idx === 0 ? 'open' : ''}`; // First one open by default

      const headerBtn = document.createElement('button');
      headerBtn.type = 'button';
      headerBtn.className = 'accordion-header';
      headerBtn.setAttribute('aria-expanded', idx === 0 ? 'true' : 'false');

      const titleWrap = document.createElement('div');
      titleWrap.className = 'accordion-title-wrap';

      const idBadge = document.createElement('span');
      idBadge.className = 'rule-id-badge';
      idBadge.textContent = r.id;

      const titleSpan = document.createElement('span');
      titleSpan.textContent = r.title;

      const weightBadge = document.createElement('span');
      weightBadge.className = 'rule-weight-badge';
      weightBadge.textContent = `+${r.weight}`;

      titleWrap.appendChild(idBadge);
      titleWrap.appendChild(titleSpan);
      titleWrap.appendChild(weightBadge);

      const arrow = document.createElement('span');
      arrow.className = 'accordion-arrow';
      arrow.textContent = '▼';

      headerBtn.appendChild(titleWrap);
      headerBtn.appendChild(arrow);

      const body = document.createElement('div');
      body.className = 'accordion-body';

      const whyP = document.createElement('p');
      whyP.textContent = r.why;
      body.appendChild(whyP);

      if (r.snippet) {
        const snippetBox = document.createElement('div');
        snippetBox.className = 'snippet-box';
        snippetBox.textContent = `Matched: "${r.snippet}"`;
        body.appendChild(snippetBox);
      }

      if (r.source_url) {
        const link = document.createElement('a');
        link.className = 'source-link';
        link.href = r.source_url;
        link.target = '_blank';
        link.rel = 'noopener noreferrer';
        link.textContent = `↗ ${I18N[state.lang].source_link_label}`;
        body.appendChild(link);
      }

      headerBtn.addEventListener('click', () => {
        const isOpen = item.classList.contains('open');
        item.classList.toggle('open', !isOpen);
        headerBtn.setAttribute('aria-expanded', !isOpen ? 'true' : 'false');
      });

      item.appendChild(headerBtn);
      item.appendChild(body);
      elements.reasonsAccordion.appendChild(item);
    });
  }

  // =========================================================================
  // Drafts & Social Sharing
  // =========================================================================
  function setDraftTab(draftKey) {
    state.activeDraft = draftKey;
    elements.draftTabs.forEach(tab => {
      const isActive = tab.dataset.draft === draftKey;
      tab.classList.toggle('active', isActive);
      tab.setAttribute('aria-selected', isActive ? 'true' : 'false');
    });

    if (!state.currentResult || !state.currentResult.drafts) return;
    const drafts = state.currentResult.drafts;

    if (draftKey === 'complaint') {
      elements.draftText.textContent = drafts.complaint_text || '';
    } else if (draftKey === 'script') {
      elements.draftText.textContent = drafts.script_1930 || '';
    } else if (draftKey === 'family') {
      elements.draftText.textContent = drafts.family_alert || '';
    }
  }

  async function copyActiveDraft() {
    const text = elements.draftText.textContent;
    if (!text) return;

    try {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        await navigator.clipboard.writeText(text);
      } else {
        const ta = document.createElement('textarea');
        ta.value = text;
        document.body.appendChild(ta);
        ta.select();
        document.execCommand('copy');
        document.body.removeChild(ta);
      }
      showToast(I18N[state.lang].toast_copied, 'success');
    } catch (e) {
      showToast('Could not copy automatically. Please select and copy.', 'info');
    }
  }

  async function shareFamilyAlert() {
    if (!state.currentResult || !state.currentResult.drafts) return;
    const alertMsg = state.currentResult.drafts.family_alert || '';
    if (!alertMsg) return;

    if (navigator.share) {
      try {
        await navigator.share({
          title: '🚨 Digital Arrest Scam Alert',
          text: alertMsg
        });
        return;
      } catch (err) {
        // Fallback to WhatsApp link if share dismissed or unsupported
      }
    }

    // Direct WhatsApp share fallback
    const waUrl = `https://wa.me/?text=${encodeURIComponent(alertMsg)}`;
    window.open(waUrl, '_blank', 'noopener,noreferrer');
  }

  // =========================================================================
  // Local Speech Synthesis (Read Aloud)
  // =========================================================================
  function toggleReadAloud() {
    if (state.isSpeaking) {
      stopReadAloud();
      return;
    }

    if (!('speechSynthesis' in window)) {
      elements.voiceUnavailableNote.classList.remove('hidden');
      return;
    }

    const textToRead = elements.plainSummaryText.textContent.trim();
    if (!textToRead) return;

    window.speechSynthesis.cancel();

    const utter = new SpeechSynthesisUtterance(textToRead);
    state.speechUtterance = utter;

    // Set voice language code
    const langCode = state.lang === 'hi' ? 'hi-IN' : (state.lang === 'pa' ? 'pa-IN' : 'en-IN');
    utter.lang = langCode;

    // Pick a voice matching language if available
    const voices = window.speechSynthesis.getVoices();
    const matchedVoice = voices.find(v => v.lang.startsWith(state.lang) || v.lang === langCode);
    if (matchedVoice) {
      utter.voice = matchedVoice;
    }

    utter.onstart = () => {
      state.isSpeaking = true;
      elements.btnReadAloud.classList.add('playing');
      elements.voiceBtnText.textContent = I18N[state.lang].stop_reading;
      elements.voiceUnavailableNote.classList.add('hidden');
    };

    utter.onend = () => {
      stopReadAloud();
    };

    utter.onerror = () => {
      stopReadAloud();
      elements.voiceUnavailableNote.classList.remove('hidden');
    };

    window.speechSynthesis.speak(utter);
  }

  function stopReadAloud() {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
    }
    state.isSpeaking = false;
    if (elements.btnReadAloud) {
      elements.btnReadAloud.classList.remove('playing');
      elements.voiceBtnText.textContent = I18N[state.lang].read_aloud;
    }
  }

  // =========================================================================
  // Dashboard & Inline SVG Charts
  // =========================================================================
  async function loadDashboard() {
    try {
      const res = await fetch('/api/stats');
      if (!res.ok) return;
      const data = await res.json();
      renderDashboard(data);
    } catch (e) {
      // Offline fallback
    }
  }

  function renderDashboard(data) {
    elements.statTotalScans.textContent = data.total_scans || 0;
    elements.statScams.textContent = (data.totals_by_verdict && data.totals_by_verdict.likely_scam) || 0;
    elements.statSuspicious.textContent = (data.totals_by_verdict && data.totals_by_verdict.suspicious) || 0;
    elements.statCannotVerify.textContent = (data.totals_by_verdict && data.totals_by_verdict.cannot_verify) || 0;

    // Render Charts
    renderVerdictsChart(data.totals_by_verdict || {});
    renderTopRulesChart(data.top_rules || []);
    renderLanguagesChart(data.by_language || {});
    renderTimelineChart(data.last_14_days || []);
  }

  function renderVerdictsChart(verdicts) {
    const total = (verdicts.likely_scam || 0) + (verdicts.suspicious || 0) + (verdicts.cannot_verify || 0);
    const container = elements.chartVerdictsContainer;
    container.innerHTML = '';

    if (total === 0) {
      container.innerHTML = '<p style="color:var(--text-muted);padding:20px;text-align:center;">No scans recorded yet.</p>';
      return;
    }

    const items = [
      { label: 'Likely Scam', count: verdicts.likely_scam || 0, color: 'var(--scam-red)' },
      { label: 'Suspicious', count: verdicts.suspicious || 0, color: 'var(--suspicious-amber)' },
      { label: 'Cannot Verify', count: verdicts.cannot_verify || 0, color: 'var(--safe-grey)' }
    ];

    let svg = '<svg viewBox="0 0 340 160" width="100%" height="160" style="overflow:visible;" role="img" aria-label="Verdicts bar chart">';
    items.forEach((item, i) => {
      const pct = total > 0 ? (item.count / total) : 0;
      const barWidth = Math.max(4, pct * 220);
      const y = 20 + i * 45;

      svg += `<text x="0" y="${y + 14}" fill="var(--text-secondary)" font-size="12" font-weight="600">${item.label}</text>`;
      svg += `<rect x="95" y="${y}" width="${barWidth}" height="20" rx="4" fill="${item.color}" />`;
      svg += `<text x="${105 + barWidth}" y="${y + 15}" fill="#ffffff" font-size="12" font-weight="700">${item.count} (${(pct * 100).toFixed(0)}%)</text>`;
    });
    svg += '</svg>';
    container.innerHTML = svg;
  }

  function renderTopRulesChart(topRules) {
    const container = elements.chartRulesContainer;
    container.innerHTML = '';

    if (!topRules || topRules.length === 0) {
      container.innerHTML = '<p style="color:var(--text-muted);padding:20px;text-align:center;">No red flags logged yet.</p>';
      return;
    }

    const maxCount = Math.max(...topRules.map(r => r.count), 1);
    const displayed = topRules.slice(0, 5);

    let svg = `<svg viewBox="0 0 340 ${displayed.length * 36 + 20}" width="100%" height="${displayed.length * 36 + 20}" role="img" aria-label="Top red flags chart">`;
    displayed.forEach((r, i) => {
      const barWidth = Math.max(4, (r.count / maxCount) * 200);
      const y = 10 + i * 36;
      svg += `<text x="0" y="${y + 16}" fill="var(--saffron-hover)" font-size="13" font-weight="700" font-family="var(--font-mono)">${r.rule_id}</text>`;
      svg += `<rect x="50" y="${y}" width="${barWidth}" height="20" rx="4" fill="var(--saffron-main)" />`;
      svg += `<text x="${60 + barWidth}" y="${y + 15}" fill="#ffffff" font-size="12" font-weight="700">${r.count}</text>`;
    });
    svg += '</svg>';
    container.innerHTML = svg;
  }

  function renderLanguagesChart(langMap) {
    const container = elements.chartLanguagesContainer;
    container.innerHTML = '';

    const total = Object.values(langMap).reduce((a, b) => a + b, 0);
    if (total === 0) {
      container.innerHTML = '<p style="color:var(--text-muted);padding:20px;text-align:center;">No language data yet.</p>';
      return;
    }

    const items = [
      { label: 'English', count: langMap.en || 0, color: '#38bdf8' },
      { label: 'हिन्दी (Hindi)', count: langMap.hi || 0, color: '#f97316' },
      { label: 'ਪੰਜਾਬੀ (Punjabi)', count: langMap.pa || 0, color: '#a855f7' }
    ];

    let svg = '<svg viewBox="0 0 340 140" width="100%" height="140" role="img" aria-label="Languages breakdown">';
    items.forEach((item, i) => {
      const pct = total > 0 ? (item.count / total) : 0;
      const barWidth = Math.max(4, pct * 180);
      const y = 15 + i * 40;
      svg += `<text x="0" y="${y + 14}" fill="var(--text-secondary)" font-size="12" font-weight="600">${item.label}</text>`;
      svg += `<rect x="110" y="${y}" width="${barWidth}" height="18" rx="4" fill="${item.color}" />`;
      svg += `<text x="${120 + barWidth}" y="${y + 14}" fill="#ffffff" font-size="12" font-weight="700">${item.count} (${(pct * 100).toFixed(0)}%)</text>`;
    });
    svg += '</svg>';
    container.innerHTML = svg;
  }

  function renderTimelineChart(dailyList) {
    const container = elements.chartTimelineContainer;
    container.innerHTML = '';

    if (!dailyList || dailyList.length === 0) {
      container.innerHTML = '<p style="color:var(--text-muted);padding:20px;text-align:center;">No timeline records in last 14 days.</p>';
      return;
    }

    const maxVal = Math.max(...dailyList.map(d => d.total), 1);
    const count = dailyList.length;
    const chartHeight = 120;
    const barWidth = Math.max(12, Math.floor(280 / count) - 4);

    let svg = '<svg viewBox="0 0 340 150" width="100%" height="150" role="img" aria-label="14 days activity trend">';
    dailyList.forEach((d, i) => {
      const barH = Math.max(4, (d.total / maxVal) * 90);
      const x = 20 + i * (barWidth + 4);
      const y = 110 - barH;
      const shortDate = d.date.slice(5); // MM-DD

      svg += `<rect x="${x}" y="${y}" width="${barWidth}" height="${barH}" rx="3" fill="#38bdf8" />`;
      svg += `<text x="${x + barWidth / 2}" y="${y - 4}" text-anchor="middle" fill="#ffffff" font-size="10" font-weight="700">${d.total}</text>`;
      svg += `<text x="${x + barWidth / 2}" y="130" text-anchor="middle" fill="var(--text-muted)" font-size="9">${shortDate}</text>`;
    });
    svg += '</svg>';
    container.innerHTML = svg;
  }

  // =========================================================================
  // Transparency & Public Rules Inventory
  // =========================================================================
  async function loadTransparencyRules() {
    try {
      const res = await fetch('/api/rules');
      if (!res.ok) return;
      const data = await res.json();
      renderPublicRules(data.rules || []);
    } catch (e) {
      // Offline fallback
    }
  }

  function renderPublicRules(rules) {
    elements.rulesListContainer.innerHTML = '';
    rules.forEach(r => {
      const item = document.createElement('div');
      item.className = 'public-rule-item';

      const titleObj = r.title || {};
      const whyObj = r.why || {};
      const title = titleObj[state.lang] || titleObj.en || `Rule ${r.id}`;
      const why = whyObj[state.lang] || whyObj.en || '';

      item.innerHTML = `
        <div class="public-rule-head">
          <div style="display:flex;align-items:center;gap:8px;">
            <span class="rule-id-badge">${r.id}</span>
            <strong class="public-rule-title">${escapeHTML(title)}</strong>
          </div>
          <span class="rule-weight-badge">+${r.weight} Weight ${r.hard ? '(Hard Rule)' : ''}</span>
        </div>
        <p class="public-rule-why">${escapeHTML(why)}</p>
        ${r.source_url ? `<a href="${r.source_url}" target="_blank" rel="noopener noreferrer" class="source-link" style="margin-top:4px;">↗ ${I18N[state.lang].source_link_label}</a>` : ''}
      `;
      elements.rulesListContainer.appendChild(item);
    });
  }

  function escapeHTML(str) {
    if (!str) return '';
    return str.replace(/[&<>'"]/g, 
      tag => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[tag] || tag)
    );
  }

  // =========================================================================
  // Event Listeners Setup
  // =========================================================================
  function setupEventListeners() {
    // Language buttons
    elements.langBtns.forEach(btn => {
      btn.addEventListener('click', () => setLanguage(btn.dataset.lang));
    });

    // Navigation tabs
    elements.navTabs.forEach(tab => {
      tab.addEventListener('click', () => setTab(tab.dataset.tab));
    });

    // Mode buttons
    elements.modeBtns.forEach(btn => {
      btn.addEventListener('click', () => setInputMode(btn.dataset.mode));
    });

    // Sample chips
    elements.sampleChips.forEach(chip => {
      chip.addEventListener('click', () => fillSample(chip.dataset.sample));
    });

    // Text area inputs
    elements.inputText.addEventListener('input', updateCharCount);
    elements.btnClearText.addEventListener('click', () => {
      elements.inputText.value = '';
      updateCharCount();
      elements.inputText.focus();
    });

    // Dropzone & File picker
    elements.dropZone.addEventListener('click', () => elements.fileInput.click());
    elements.dropZone.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        elements.fileInput.click();
      }
    });

    elements.fileInput.addEventListener('change', (e) => {
      if (e.target.files && e.target.files[0]) {
        handleFileSelect(e.target.files[0]);
      }
    });

    // Drag and drop
    elements.dropZone.addEventListener('dragover', (e) => {
      e.preventDefault();
      elements.dropZone.classList.add('dragover');
    });

    elements.dropZone.addEventListener('dragleave', () => {
      elements.dropZone.classList.remove('dragover');
    });

    elements.dropZone.addEventListener('drop', (e) => {
      e.preventDefault();
      elements.dropZone.classList.remove('dragover');
      if (e.dataTransfer.files && e.dataTransfer.files[0]) {
        handleFileSelect(e.dataTransfer.files[0]);
      }
    });

    elements.btnRemoveImage.addEventListener('click', removeSelectedImage);

    // Primary analyze trigger
    elements.btnAnalyze.addEventListener('click', performAnalysis);

    // Read aloud button
    elements.btnReadAloud.addEventListener('click', toggleReadAloud);

    // Draft sub-tabs
    elements.draftTabs.forEach(tab => {
      tab.addEventListener('click', () => setDraftTab(tab.dataset.draft));
    });

    // Copy draft
    elements.btnCopyDraft.addEventListener('click', copyActiveDraft);

    // Share Family Alert
    elements.btnShareFamily.addEventListener('click', shareFamilyAlert);
  }

  // DOM Content Loaded Execution
  document.addEventListener('DOMContentLoaded', () => {
    initLanguage();
    setupEventListeners();
  });

})();
