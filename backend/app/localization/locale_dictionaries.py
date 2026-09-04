"""
ExamHub Multilingual Internationalization (i18n) Engine
Provides localized translation dictionaries across 6 global languages
for candidate examination rooms, proctoring alerts, and grading rubrics.
"""

from typing import Dict, Any

LOCALE_TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "en": {
        "portal_title": "ExamHub Institutional Examination Portal",
        "exam_session_active": "Assessment Session In Progress",
        "time_remaining": "Time Remaining",
        "fullscreen_required": "Fullscreen lockdown mode is mandatory for this assessment.",
        "submit_exam": "Submit Examination",
        "confirm_submission": "Are you sure you want to finalize and submit your assessment?",
        "unanswered_questions_warning": "You have {count} unanswered questions remaining.",
        "trust_score_label": "Proctoring Integrity Index",
        "anomaly_detected": "Proctoring anomaly detected. Please face the camera.",
        "camera_required": "Webcam streaming must remain active at all times.",
        "microphone_required": "Microphone monitoring active.",
        "screen_share_active": "Desktop display lockdown active.",
        "multiple_faces_warning": "Multiple human faces detected in examination field of view.",
        "face_missing_warning": "No face detected in video stream. Return to center.",
        "tab_switch_warning": "Window focus loss detected. Infraction logged.",
        "calculator_title": "Integrated Scientific Calculator",
        "formula_sheet": "Reference Formulas & Periodic Constants",
        "scratchpad": "Digital Examination Scratchpad",
        "certificate_issued": "Certificate of Completion Issued",
        "verification_hash": "Cryptographic Verification Fingerprint",
        "download_pdf": "Download Official Transcript (PDF)",
        "grade_scale": "Grading Scale & Distribution Curve",
        "inter_rater_agreement": "Marker Consensus Reliability (Fleiss' Kappa)",
        "plagiarism_collusion_alert": "Academic Integrity Alert: Similarity threshold exceeded.",
        "offline_cached": "Network disconnected: responses cached securely in local encrypted store.",
        "offline_synced": "Network restored: cached responses successfully synchronized."
    },
    "es": {
        "portal_title": "Portal de Exámenes Institucionales ExamHub",
        "exam_session_active": "Sesión de Evaluación en Curso",
        "time_remaining": "Tiempo Restante",
        "fullscreen_required": "El modo de pantalla completa es obligatorio para esta evaluación.",
        "submit_exam": "Enviar Examen",
        "confirm_submission": "¿Está seguro de que desea finalizar y enviar su evaluación?",
        "unanswered_questions_warning": "Tiene {count} preguntas sin responder pendientes.",
        "trust_score_label": "Índice de Integridad de Supervisión",
        "anomaly_detected": "Anomalía de supervisión detectada. Mire hacia la cámara.",
        "camera_required": "La transmisión de la cámara web debe permanecer activa en todo momento.",
        "microphone_required": "Monitoreo de micrófono activo.",
        "screen_share_active": "Bloqueo de pantalla de escritorio activo.",
        "multiple_faces_warning": "Múltiples rostros detectados en el campo visual del examen.",
        "face_missing_warning": "No se detecta ningún rostro en el video. Regrese al centro.",
        "tab_switch_warning": "Pérdida de foco de ventana detectada. Infracción registrada.",
        "calculator_title": "Calculadora Científica Integrada",
        "formula_sheet": "Fórmulas de Referencia y Constantes",
        "scratchpad": "Borrador Digital de Examen",
        "certificate_issued": "Certificado de Finalización Emitido",
        "verification_hash": "Huella Criptográfica de Verificación",
        "download_pdf": "Descargar Certificado Oficial (PDF)",
        "grade_scale": "Escala de Calificación y Curva de Distribución",
        "inter_rater_agreement": "Confiabilidad del Consenso entre Evaluadores (Kappa de Fleiss)",
        "plagiarism_collusion_alert": "Alerta de Integridad Académica: Umbral de similitud superado.",
        "offline_cached": "Red desconectada: respuestas guardadas en almacenamiento seguro local.",
        "offline_synced": "Red restaurada: respuestas sincronizadas con éxito."
    },
    "fr": {
        "portal_title": "Portail d'Évaluation Institutionnelle ExamHub",
        "exam_session_active": "Session d'Évaluation en Cours",
        "time_remaining": "Temps Restant",
        "fullscreen_required": "Le mode plein écran est obligatoire pour cette évaluation.",
        "submit_exam": "Soumettre l'Examen",
        "confirm_submission": "Êtes-vous sûr de vouloir finaliser et soumettre votre examen ?",
        "unanswered_questions_warning": "Il vous reste {count} questions sans réponse.",
        "trust_score_label": "Indice d'Intégrité de Surveillance",
        "anomaly_detected": "Anomalie de surveillance détectée. Veuillez regarder la caméra.",
        "camera_required": "La webcam doit rester active en permanence.",
        "microphone_required": "Surveillance audio active.",
        "screen_share_active": "Verrouillage de l'affichage de bureau actif.",
        "multiple_faces_warning": "Plusieurs visages détectés dans le champ visuel.",
        "face_missing_warning": "Aucun visage détecté. Veuillez vous recentrer.",
        "tab_switch_warning": "Perte de focus de la fenêtre détectée. Infraction enregistrée.",
        "calculator_title": "Calculatrice Scientifique Intégrée",
        "formula_sheet": "Formules de Référence et Constantes",
        "scratchpad": "Brouillon Numérique d'Examen",
        "certificate_issued": "Certificat de Réussite Délivré",
        "verification_hash": "Empreinte Cryptographique de Vérification",
        "download_pdf": "Télécharger le Relevé Officiel (PDF)",
        "grade_scale": "Échelle de Notation et Courbe de Gauss",
        "inter_rater_agreement": "Consensus des Correcteurs (Kappa de Fleiss)",
        "plagiarism_collusion_alert": "Alerte Intégrité: Seuil de similarité dépassé.",
        "offline_cached": "Réseau déconnecté: réponses stockées localement de manière chiffrée.",
        "offline_synced": "Réseau rétabli: réponses synchronisées avec succès."
    },
    "de": {
        "portal_title": "ExamHub Institutionelles Prüfungsportal",
        "exam_session_active": "Prüfungssitzung Aktiv",
        "time_remaining": "Verbleibende Zeit",
        "fullscreen_required": "Der Vollbildmodus ist für diese Prüfung obligatorisch.",
        "submit_exam": "Prüfung Abgeben",
        "confirm_submission": "Möchten Sie Ihre Prüfung wirklich abschließen und einreichen?",
        "unanswered_questions_warning": "Sie haben noch {count} unbeantwortete Fragen.",
        "trust_score_label": "Aufsichts-Integritätsindex",
        "anomaly_detected": "Aufsichtsanomalie festgestellt. Bitte in die Kamera blicken.",
        "camera_required": "Die Webcam-Übertragung muss durchgehend aktiviert bleiben.",
        "microphone_required": "Mikrofonüberwachung aktiv.",
        "screen_share_active": "Bildschirmsperre aktiv.",
        "multiple_faces_warning": "Mehrere Gesichter im Erfassungsbereich erkannt.",
        "face_missing_warning": "Kein Gesicht erkannt. Bitte zur Bildmitte zurückkehren.",
        "tab_switch_warning": "Fensterfokus verloren. Regelverstoß protokolliert.",
        "calculator_title": "Integrierter Wissenschaftlicher Taschenrechner",
        "formula_sheet": "Formelsammlung & Konstanten",
        "scratchpad": "Digitaler Notizblock",
        "certificate_issued": "Abschlusszertifikat Ausgestellt",
        "verification_hash": "Kryptografischer Verifizierungs-Hash",
        "download_pdf": "Offizielles Zeugnis Herunterladen (PDF)",
        "grade_scale": "Notenskala & Gaußsche Normalverteilung",
        "inter_rater_agreement": "Korrektoren-Übereinstimmung (Fleiss' Kappa)",
        "plagiarism_collusion_alert": "Akademischer Integritätsalarm: Ähnlichkeitsschwelle überschritten.",
        "offline_cached": "Netzwerk getrennt: Antworten lokal verschlüsselt zwischengespeichert.",
        "offline_synced": "Netzwerk wiederhergestellt: Antworten synchronisiert."
    },
    "ja": {
        "portal_title": "ExamHub 教育機関向けオンライン試験ポータル",
        "exam_session_active": "試験セッション実施中",
        "time_remaining": "残り時間",
        "fullscreen_required": "本試験では全画面ロックダウンモードが必須です。",
        "submit_exam": "試験を提出する",
        "confirm_submission": "試験を終了して解答を提出してもよろしいですか？",
        "unanswered_questions_warning": "未解答の問題がまだ {count} 問あります。",
        "trust_score_label": "不正監視整合性スコア",
        "anomaly_detected": "異常動作が検出されました。カメラの正面を向いてください。",
        "camera_required": "ウェブカメラは常に有効にしておく必要があります。",
        "microphone_required": "マイクによる音声監視が作動しています。",
        "screen_share_active": "デスクトップ画面の固定ロックダウンが有効です。",
        "multiple_faces_warning": "画面内に複数の人物の顔が検出されました。",
        "face_missing_warning": "カメラ映像内に顔が検出されません。中央に戻ってください。",
        "tab_switch_warning": "ウィンドウのフォーカスが外れました。違反が記録されました。",
        "calculator_title": "組み込み関数電卓",
        "formula_sheet": "公式集・物理定数表",
        "scratchpad": "計算用デジタルメモ帳",
        "certificate_issued": "修了証明書が発行されました",
        "verification_hash": "暗号化照合ハッシュ値",
        "download_pdf": "公式成績証明書をダウンロード (PDF)",
        "grade_scale": "評点スケール・標準正規分布曲線",
        "inter_rater_agreement": "採点者間一致度信頼性 (フライスのカッパ係数)",
        "plagiarism_collusion_alert": "学術的整合性警告: 類似性基準値を超過しました。",
        "offline_cached": "ネットワーク切断: 解答は安全にローカル暗号化保存されました。",
        "offline_synced": "ネットワーク復旧: キャッシュされた解答の同期が完了しました。"
    },
    "hi": {
        "portal_title": "एग्जामहब संस्थागत परीक्षा पोर्टल",
        "exam_session_active": "मूल्यांकन सत्र प्रगति पर है",
        "time_remaining": "शेष समय",
        "fullscreen_required": "इस परीक्षा के लिए पूर्ण स्क्रीन लॉकडाउन मोड अनिवार्य है।",
        "submit_exam": "परीक्षा जमा करें",
        "confirm_submission": "क्या आप वाकई अपनी परीक्षा समाप्त करके जमा करना चाहते हैं?",
        "unanswered_questions_warning": "आपके {count} अनुत्तरित प्रश्न शेष हैं।",
        "trust_score_label": "प्रॉक्टरिंग अखंडता सूचकांक",
        "anomaly_detected": "असामान्यता का पता चला। कृपया कैमरे की ओर देखें।",
        "camera_required": "वेबकैम हर समय सक्रिय रहना चाहिए।",
        "microphone_required": "माइक्रोफ़ोन निगरानी सक्रिय है।",
        "screen_share_active": "डेस्कटॉप स्क्रीन लॉकडाउन सक्रिय है।",
        "multiple_faces_warning": "कैमरे के दृश्य में एक से अधिक चेहरे पाए गए।",
        "face_missing_warning": "वीडियो में कोई चेहरा नहीं मिला। कृपया केंद्र में आएं।",
        "tab_switch_warning": "विंडो फोकस हटने का पता चला। उल्लंघन दर्ज किया गया।",
        "calculator_title": "एकीकृत वैज्ञानिक कैलकुलेटर",
        "formula_sheet": "संदर्भ सूत्र और नियतांक",
        "scratchpad": "डिजिटल रफ़ कार्य पैड",
        "certificate_issued": "समाप्ति प्रमाणपत्र जारी किया गया",
        "verification_hash": "क्रिप्टोग्राफ़िक सत्यापन फिंगरप्रिंट",
        "download_pdf": "आधिकारिक प्रतिलेख डाउनलोड करें (PDF)",
        "grade_scale": "ग्रेडिंग पैमाना और वितरण वक्र",
        "inter_rater_agreement": "मूल्यांकनकर्ता सहमति विश्वसनीयता (फ्लीस का कप्पा)",
        "plagiarism_collusion_alert": "अकादमिक अखंडता चेतावनी: समानता सीमा पार हो गई।",
        "offline_cached": "इंटरनेट बंद: उत्तर सुरक्षित स्थानीय एन्क्रिप्टेड मेमोरी में सहेजे गए।",
        "offline_synced": "इंटरनेट बहाल: सहेजे गए उत्तर सफलतापूर्वक सिंक्रनाइज़ हो गए।"
    }
}


class LocalizationService:
    """
    Retrieves localized strings with fallback to English.
    """

    @classmethod
    def get_text(cls, key: str, lang: str = "en", **kwargs) -> str:
        lang_dict = LOCALE_TRANSLATIONS.get(lang.lower(), LOCALE_TRANSLATIONS["en"])
        template = lang_dict.get(key) or LOCALE_TRANSLATIONS["en"].get(key, key)
        if kwargs:
            try:
                return template.format(**kwargs)
            except Exception:
                return template
        return template
