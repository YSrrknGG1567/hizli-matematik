 import flet as ft, random, asyncio, json, urllib.request, gc

FIREBASE_URL = "https://" + "hizli-matematik-10492-default-rtdb" + ".europe-west1.firebasedatabase.app"

T = {
    "tr": {"ad": "Turkce", "baslik": "HIZLI MATEMATIK", "alt": "UNO Kartli Ders & Zeka Yarisi", "oyna": "OYNA", "magaza": "MAGAZA", "skor": "SKOR TABLOSU", "diller": "DILLER", "rekor": "EN YUKSEK SKORUN", "profDegis": "Profili Degistir", "profBas": "Oyuncu Profili", "adYer": "Adin (Max 20)", "kaydet": "KAYDET", "iptal": "Iptal", "kapat": "Kapat", "tamam": "Tamam", "tekrar": "TEKRAR OYNA", "can": "Can", "altin": "Altin", "dondur": "Dondur", "atla": "Atla", "durak": "DURAKLATILDI", "bitti": "OYUN BITTI", "puan": "PUAN", "dogru": "Dogru", "yanlis": "Yanlis", "bos": "Bos", "seviye": "Seviye", "kazandin": "KAZANDIN!", "kaybettin": "KAYBETTIN BIR DAHAKI SEFERE", "berabere": "BERABERE!", "sureDoldu": "SURE DOLDU!", "dogrusu": "Dogrusu", "harika": "Dogru!", "tek": "Tek Kisilik", "vs": "1v1 VS (15sn)", "sira": "Sira", "baslasin": "Baslasin", "kaydetSor": "Skor kaydedilsin mi?", "kaydetBtn": "Skoru Kaydet", "kaydetmeBtn": "Kaydetme", "yetersiz": "Yetersiz altin!", "sureAkar": "Dikkat: Sure akmaya devam ediyor!", "kad": ("Ilkokul", "Ortaokul", "Lise", "Universite"), "sinif": ". Sinif", "modlar": ("Kolay", "Orta", "Zor", "Cok Zor"), "dersler": ("Matematik", "Fen & Bilim", "Tarih & Cografya", "Genel Kultur & Mantik"), "magItem": ("Zaman Dondur (5s)", "50/50 Sik Eleme", "Ekstra Sure (+10s)", "Kalici +1 Can", "Soru Atla (1x)", "3 Soru 2X Puan"), "soruEk": "isleminin sonucu kactir?", "xBul": "ise x kactir?"},
    "en": {"ad": "English", "baslik": "FAST MATH", "alt": "UNO Card Subject & Brain Race", "oyna": "PLAY", "magaza": "SHOP", "skor": "LEADERBOARD", "diller": "LANGUAGES", "rekor": "HIGH SCORE", "profDegis": "Change Profile", "profBas": "Player Profile", "adYer": "Name (Max 20)", "kaydet": "SAVE", "iptal": "Cancel", "kapat": "Close", "tamam": "OK", "tekrar": "PLAY AGAIN", "can": "HP", "altin": "Gold", "dondur": "Freeze", "atla": "Skip", "durak": "PAUSED", "bitti": "GAME OVER", "puan": "PTS", "dogru": "Correct", "yanlis": "Wrong", "bos": "Empty", "seviye": "Level", "kazandin": "YOU WON!", "kaybettin": "YOU LOST BETTER LUCK NEXT TIME", "berabere": "DRAW!", "sureDoldu": "TIME IS UP!", "dogrusu": "Correct answer", "harika": "Correct!", "tek": "Single Player", "vs": "1v1 VS (15s)", "sira": "Turn", "baslasin": "Start", "kaydetSor": "Save your score?", "kaydetBtn": "Save Score", "kaydetmeBtn": "Don't Save", "yetersiz": "Not enough gold!", "sureAkar": "Warning: Timer keeps running!", "kad": ("Primary", "Middle School", "High School", "University"), "sinif": " Grade", "modlar": ("Easy", "Medium", "Hard", "Extreme"), "dersler": ("Mathematics", "Science", "History & Geography", "General Knowledge & Logic"), "magItem": ("Freeze Time (5s)", "50/50 Eliminate", "Extra Time (+10s)", "Permanent +1 HP", "Skip Question (1x)", "2X Score (3 Qs)"), "soruEk": "what is the result?", "xBul": "find x:"},
    "ru": {"ad": "Русский", "baslik": "БЫСТРАЯ МАТЕМАТИКА", "alt": "Викторина и дуэль UNO", "oyna": "ИГРАТЬ", "magaza": "МАГАЗИН", "skor": "РЕЙТИНГ", "diller": "ЯЗЫКИ", "rekor": "РЕКОРД", "profDegis": "Изменить профиль", "profBas": "Профиль игрока", "adYer": "Имя (Макс 20)", "kaydet": "СОХРАНИТЬ", "iptal": "Отмена", "kapat": "Закрыть", "tamam": "ОК", "tekrar": "ЗАНОВО", "can": "Жизни", "altin": "Золото", "dondur": "Заморозка", "atla": "Пропуск", "durak": "ПАУЗА", "bitti": "ИГРА ОКОНЧЕНА", "puan": "ОЧКОВ", "dogru": "Верно", "yanlis": "Неверно", "bos": "Пропущено", "seviye": "Уровень", "kazandin": "ПОБЕДА!", "kaybettin": "ВЫ ПРОИГРАЛИ", "berabere": "НИЧЬЯ!", "sureDoldu": "ВРЕМЯ ВЫШЛО!", "dogrusu": "Правильный ответ", "harika": "Верно!", "tek": "Одиночная", "vs": "1на1 VS (15с)", "sira": "Ход", "baslasin": "Начать", "kaydetSor": "Сохранить счет?", "kaydetBtn": "Сохранить", "kaydetmeBtn": "Не сохранять", "yetersiz": "Недостаточно золота!", "sureAkar": "Внимание: время идет!", "kad": ("Начальная", "Средняя школа", "Старшая школа", "Университет"), "sinif": " класс", "modlar": ("Легко", "Средне", "Сложно", "Эксперт"), "dersler": ("Математика", "Наука", "История и География", "Логика и Эрудиция"), "magItem": ("Заморозка (5с)", "50/50 Убрать 2", "Время (+10с)", "+1 Жизнь навсегда", "Пропустить (1x)", "2X Очки (3 вопр.)"), "soruEk": "чему равно?", "xBul": "найдите x:"},
    "ko": {"ad": "한국어", "baslik": "빠른 수학", "alt": "UNO 카드 과목 & 두뇌 퀴즈", "oyna": "게임 시작", "magaza": "상점", "skor": "순위표", "diller": "언어", "rekor": "최고 점수", "profDegis": "프로필 변경", "profBas": "플레이어 프로필", "adYer": "이름 (최대 20자)", "kaydet": "저장", "iptal": "취소", "kapat": "닫기", "tamam": "확인", "tekrar": "다시 하기", "can": "생명", "altin": "골드", "dondur": "얼리기", "atla": "건너뛰기", "durak": "일시정지", "bitti": "게임 종료", "puan": "점", "dogru": "정답", "yanlis": "오답", "bos": "패스", "seviye": "레벨", "kazandin": "승리했습니다!", "kaybettin": "패배했습니다 다음 기회에", "berabere": "무승부!", "sureDoldu": "시간 초과!", "dogrusu": "정답", "harika": "정답!", "tek": "싱글 플레이", "vs": "1대1 대전 (15초)", "sira": "차례", "baslasin": "시작", "kaydetSor": "점수를 저장할까요?", "kaydetBtn": "점수 저장", "kaydetmeBtn": "저장 안 함", "yetersiz": "골드가 부족합니다!", "sureAkar": "주의: 시간이 계속 흐릅니다!", "kad": ("초등학교", "중학교", "고등학교", "대학교"), "sinif": "학년", "modlar": ("쉬움", "보통", "어려움", "매우 어려움"), "dersler": ("수학", "과학", "역사 & 지리", "일반 상식 & 논리"), "magItem": ("시간 정지 (5초)", "50/50 보기 제거", "시간 추가 (+10초)", "영구 생명 +1", "문제 건너뛰기", "3문제 2배 점수"), "soruEk": "계산 결과는?", "xBul": "x의 값은?"},
    "ja": {"ad": "日本語", "baslik": "高速数学", "alt": "UNOカード教科＆頭脳バトル", "oyna": "プレイ", "magaza": "ショップ", "skor": "ランキング", "diller": "言語", "rekor": "ハイスコア", "profDegis": "プロフィール変更", "profBas": "プレイヤー設定", "adYer": "名前 (最大20文字)", "kaydet": "保存", "iptal": "キャンセル", "kapat": "閉じる", "tamam": "OK", "tekrar": "もう一度", "can": "ライフ", "altin": "ゴールド", "dondur": "フリーズ", "atla": "スキップ", "durak": "一時停止", "bitti": "ゲームオーバー", "puan": "点", "dogru": "正解", "yanlis": "不正解", "bos": "スキップ", "seviye": "レベル", "kazandin": "勝利！", "kaybettin": "敗北！次は頑張ろう", "berabere": "引き分け！", "sureDoldu": "時間切れ！", "dogrusu": "正解", "harika": "正解！", "tek": "シングル", "vs": "1対1 対戦 (15秒)", "sira": "順番", "baslasin": "スタート", "kaydetSor": "スコアを保存しますか？", "kaydetBtn": "保存する", "kaydetmeBtn": "保存しない", "yetersiz": "ゴールド不足！", "sureAkar": "注意：時間は進んでいます！", "kad": ("小学校", "中学校", "高校", "大学"), "sinif": "年生", "modlar": ("簡単", "普通", "難しい", "激ムズ"), "dersler": ("数学", "理科", "歴史・地理", "一般常識・論理"), "magItem": ("時間停止 (5秒)", "50/50 二択化", "時間延長 (+10秒)", "ライフ +1", "スキップ (1回)", "3問スコア2倍"), "soruEk": "計算結果は？", "xBul": "xの値は？"},
    "zh": {"ad": "中文", "baslik": "快速数学", "alt": "UNO卡牌学科智力竞赛", "oyna": "开始游戏", "magaza": "商店", "skor": "排行榜", "diller": "语言", "rekor": "最高分", "profDegis": "修改资料", "profBas": "玩家资料", "adYer": "名字 (最多20字)", "kaydet": "保存", "iptal": "取消", "kapat": "关闭", "tamam": "确定", "tekrar": "再玩一次", "can": "生命", "altin": "金币", "dondur": "冻结", "atla": "跳过", "durak": "已暂停", "bitti": "游戏结束", "puan": "分", "dogru": "正确", "yanlis": "错误", "bos": "跳过", "seviye": "等级", "kazandin": "你赢了！", "kaybettin": "你输了 下次加油", "berabere": "平局！", "sureDoldu": "时间到！", "dogrusu": "正确答案", "harika": "正确！", "tek": "单人模式", "vs": "1v1 对战 (15秒)", "sira": "回合", "baslasin": "开始", "kaydetSor": "是否保存分数？", "kaydetBtn": "保存分数", "kaydetmeBtn": "不保存", "yetersiz": "金币不足！", "sureAkar": "注意：时间仍在流逝！", "kad": ("小学", "初中", "高中", "大学"), "sinif": "年级", "modlar": ("简单", "中等", "困难", "地狱"), "dersler": ("数学", "科学", "历史与地理", "常识与逻辑"), "magItem": ("冻结时间 (5秒)", "50/50 排除两项", "加时 (+10秒)", "永久生命 +1", "跳过题目 (1次)", "3题双倍积分"), "soruEk": "结果是多少？", "xBul": "求x的值："},
    "de": {"ad": "Deutsch", "baslik": "SCHNELLMATHE", "alt": "UNO-Karten Quizduell", "oyna": "SPIELEN", "magaza": "SHOP", "skor": "RANGLISTE", "diller": "SPRACHEN", "rekor": "BESTLEISTUNG", "profDegis": "Profil andern", "profBas": "Spielerprofil", "adYer": "Name (Max 20)", "kaydet": "SPEICHERN", "iptal": "Abbrechen", "kapat": "Schliessen", "tamam": "OK", "tekrar": "NOCHMAL", "can": "Leben", "altin": "Gold", "dondur": "Einfrieren", "atla": "Uberspr.", "durak": "PAUSIERT", "bitti": "SPIEL VORBEI", "puan": "PKT", "dogru": "Richtig", "yanlis": "Falsch", "bos": "Leer", "seviye": "Stufe", "kazandin": "GEWONNEN!", "kaybettin": "VERLOREN VIEL GLUCK NACHSTES MAL", "berabere": "UNENTSCHIEDEN!", "sureDoldu": "ZEIT ABGELAUFEN!", "dogrusu": "Richtige Antwort", "harika": "Richtig!", "tek": "Einzelspieler", "vs": "1vs1 Duell (15s)", "sira": "Zug", "baslasin": "Starten", "kaydetSor": "Punkte speichern?", "kaydetBtn": "Speichern", "kaydetmeBtn": "Nicht speichern", "yetersiz": "Nicht genug Gold!", "sureAkar": "Achtung: Zeit lauft weiter!", "kad": ("Grundschule", "Mittelstufe", "Gymnasium", "Universitat"), "sinif": ". Klasse", "modlar": ("Leicht", "Mittel", "Schwer", "Extrem"), "dersler": ("Mathematik", "Wissenschaft", "Geschichte & Geografie", "Allgemeinwissen & Logik"), "magItem": ("Zeit einfrieren (5s)", "50/50 Joker", "Extra Zeit (+10s)", "Dauerhaft +1 Leben", "Frage uberspringen", "3 Fragen 2X Punkte"), "soruEk": "was ist das Ergebnis?", "xBul": "berechne x:"},
    "fr": {"ad": "Francais", "baslik": "MATHS RAPIDES", "alt": "Quiz & Duel Cartes UNO", "oyna": "JOUER", "magaza": "BOUTIQUE", "skor": "CLASSEMENT", "diller": "LANGUES", "rekor": "MEILLEUR SCORE", "profDegis": "Changer profil", "profBas": "Profil Joueur", "adYer": "Nom (Max 20)", "kaydet": "ENREGISTRER", "iptal": "Annuler", "kapat": "Fermer", "tamam": "OK", "tekrar": "REJOUER", "can": "Vie", "altin": "Or", "dondur": "Geler", "atla": "Passer", "durak": "PAUSE", "bitti": "FIN DE PARTIE", "puan": "PTS", "dogru": "Juste", "yanlis": "Faux", "bos": "Passe", "seviye": "Niveau", "kazandin": "GAGNE !", "kaybettin": "PERDU A LA PROCHAINE FOIS", "berabere": "EGALITE !", "sureDoldu": "TEMPS ECOULE !", "dogrusu": "Bonne reponse", "harika": "Bravo !", "tek": "Solo", "vs": "Duel 1v1 (15s)", "sira": "Tour", "baslasin": "Commencer", "kaydetSor": "Sauvegarder le score ?", "kaydetBtn": "Sauvegarder", "kaydetmeBtn": "Ne pas sauver", "yetersiz": "Or insuffisant !", "sureAkar": "Attention : le temps continue !", "kad": ("Primaire", "College", "Lycee", "Universite"), "sinif": "e Annee", "modlar": ("Facile", "Moyen", "Difficile", "Extreme"), "dersler": ("Mathematiques", "Sciences", "Histoire & Geographie", "Culture & Logique"), "magItem": ("Geler le temps (5s)", "50/50 Eliminer 2", "Temps (+10s)", "+1 Vie permanente", "Passer (1x)", "Score 2X (3 Qs)"), "soruEk": "quel est le resultat ?", "xBul": "trouve x :"},
    "it": {"ad": "Italiano", "baslik": "MATEMATICA VELOCE", "alt": "Sfida Quiz Carte UNO", "oyna": "GIOCA", "magaza": "NEGOZIO", "skor": "CLASSIFICA", "diller": "LINGUE", "rekor": "RECORD", "profDegis": "Cambia Profilo", "profBas": "Profilo Giocatore", "adYer": "Nome (Max 20)", "kaydet": "SALVA", "iptal": "Annulla", "kapat": "Chiudi", "tamam": "OK", "tekrar": "RIGIOCA", "can": "Vite", "altin": "Oro", "dondur": "Congela", "atla": "Salta", "durak": "IN PAUSA", "bitti": "GAME OVER", "puan": "PTI", "dogru": "Esatte", "yanlis": "Errate", "bos": "Saltate", "seviye": "Livello", "kazandin": "HAI VINTO!", "kaybettin": "HAI PERSO RITENTA", "berabere": "PAREGGIO!", "sureDoldu": "TEMPO SCADUTO!", "dogrusu": "Risposta esatta", "harika": "Esatto!", "tek": "Giocatore Singolo", "vs": "Sfida 1v1 (15s)", "sira": "Turno", "baslasin": "Inizia", "kaydetSor": "Salvare il punteggio?", "kaydetBtn": "Salva", "kaydetmeBtn": "Non salvare", "yetersiz": "Oro insufficiente!", "sureAkar": "Attenzione: il tempo scorre!", "kad": ("Elementari", "Medie", "Superiori", "Universita"), "sinif": " Anno", "modlar": ("Facile", "Medio", "Difficile", "Estremo"), "dersler": ("Matematica", "Scienze", "Storia e Geografia", "Cultura e Logica"), "magItem": ("Congela Tempo (5s)", "50/50 Elimina 2", "Tempo Extra (+10s)", "+1 Vita permanente", "Salta Domanda (1x)", "Punti 2X (3 Dom.)"), "soruEk": "qual e il risultato?", "xBul": "trova x:"},
    "es": {"ad": "Espanol", "baslik": "MATE RAPIDA", "alt": "Duelo Mental Cartas UNO", "oyna": "JUGAR", "magaza": "TIENDA", "skor": "CLASIFICACION", "diller": "IDIOMAS", "rekor": "RECORD", "profDegis": "Cambiar Perfil", "profBas": "Perfil de Jugador", "adYer": "Nombre (Max 20)", "kaydet": "GUARDAR", "iptal": "Cancelar", "kapat": "Cerrar", "tamam": "OK", "tekrar": "JUGAR DE NUEVO", "can": "Vida", "altin": "Oro", "dondur": "Congelar", "atla": "Saltar", "durak": "PAUSADO", "bitti": "FIN DEL JUEGO", "puan": "PTS", "dogru": "Correctas", "yanlis": "Incorrectas", "bos": "Saltadas", "seviye": "Nivel", "kazandin": "GANASTE!", "kaybettin": "PERDISTE SUERTE LA PROXIMA", "berabere": "EMPATE!", "sureDoldu": "TIEMPO AGOTADO!", "dogrusu": "Respuesta correcta", "harika": "Correcto!", "tek": "Un Jugador", "vs": "Duelo 1v1 (15s)", "sira": "Turno", "baslasin": "Empezar", "kaydetSor": "Guardar puntuacion?", "kaydetBtn": "Guardar", "kaydetmeBtn": "No guardar", "yetersiz": "Oro insuficiente!", "sureAkar": "Atencion: el tiempo sigue!", "kad": ("Primaria", "Secundaria", "Bachillerato", "Universidad"), "sinif": " Grado", "modlar": ("Facil", "Medio", "Dificil", "Extremo"), "dersler": ("Matematicas", "Ciencias", "Historia y Geografia", "Cultura y Logica"), "magItem": ("Congelar Tiempo (5s)", "50/50 Eliminar 2", "Tiempo Extra (+10s)", "+1 Vida permanente", "Saltar Pregunta (1x)", "Puntos 2X (3 Preg.)"), "soruEk": "cual es el resultado?", "xBul": "halla x:"}
}

async def main(page: ft.Page):
    page.title = "Fast Math & Global Quiz"
    page.bgcolor = "#121225"
    page.padding = 0

    uno = ("#e74c3c", "#2980b9", "#27ae60", "#f39c12")
    sik_renk = ("#c0392b", "#1f618d", "#1e8449", "#d68910")
    harfler = ("A", "B", "C", "D")

    prof = {"isim": "", "kadIdx": 1, "sinIdx": 1, "kayitli": False, "dil": "tr"}
    try:
        kp = await page.client_storage.get_async("hm_prof")
        if isinstance(kp, dict) and kp.get("kayitli"):
            prof.update(kp)
    except Exception:
        pass

    def L():
        return T.get(prof["dil"], T["tr"])

    d = {
        "mod": "solo", "zorIdx": 1, "dersIdx": 0, "puan": 0, "can": 3, "svy": 1,
        "dc": "", "kalan": 12.0, "max": 12.0, "donma": 0.0, "aktif": False,
        "dur": False, "altin": 50, "rekor": 0, "kombo": 0, "jd": 1, "js": 0,
        "ja": 1, "je": 1, "jc": 0, "cift_puan": 0, "soru": "12 + 8 = ?",
        "simge": "M", "renk": "#e74c3c", "yerel_skorlar": list(), "online_ok": False,
        "dogru": 0, "yanlis": 0, "bos": 0, "top_sure": 0.0, "vs_sira": 1,
        "vs_atla": 3, "p1": dict(), "p2": dict(), "soru_sayac": 0,
        "siklar": list(), "sorulanlar": set()
    }

    konfeti_katman = ft.Stack(width=360, height=640)
    konfeti_renkler = ("#ff4757", "#ffd32a", "#00b894", "#0984e3", "#a29bfe", "#ff6b81", "#00cec9", "#fdcb6e")

    async def konfeti_patlat():
        konfeti_katman.controls.clear()
        parcalar = list()
        for _ in range(45):
            x = 180 + random.uniform(-60, 60)
            y = 610.0
            vx = random.uniform(-7.5, 7.5)
            vy = random.uniform(-19.0, -10.0)
            boy = random.uniform(6, 12)
            renk = random.choice(konfeti_renkler)
            kutu = ft.Container(width=boy, height=boy, bgcolor=renk, border_radius=2 if random.random() > 0.5 else 10, left=x, top=y)
            konfeti_katman.controls.append(kutu)
            parcalar.append({"k": kutu, "x": x, "y": y, "vx": vx, "vy": vy})
        page.update()
        for _ in range(38):
            await asyncio.sleep(0.03)
            for p in parcalar:
                p["x"] += p["vx"]
                p["y"] += p["vy"]
                p["vy"] += 0.78
                p["k"].left = p["x"]
                p["k"].top = p["y"]
            page.update()
        konfeti_katman.controls.clear()
        parcalar.clear()
        gc.collect()
        page.update()

    def skoru_kaydet_bulut(isim, skor):
        if skor <= 0:
            return
        d["yerel_skorlar"].append({"isim": isim, "skor": skor})
        d["yerel_skorlar"] = sorted(d["yerel_skorlar"], key=lambda x: x["skor"], reverse=True)[:10]
        try:
            url = FIREBASE_URL + "/skorlar.json"
            veri = json.dumps({"isim": isim, "skor": skor}).encode("utf-8")
            req = urllib.request.Request(url, data=veri, headers={"Content-Type": "application/json"}, method="POST")
            urllib.request.urlopen(req, timeout=6)
            d["online_ok"] = True
        except Exception:
            d["online_ok"] = False

    def skorlari_getir():
        liste = list(d["yerel_skorlar"])
        try:
            url = FIREBASE_URL + "/skorlar.json"
            res = urllib.request.urlopen(url, timeout=6).read().decode("utf-8")
            ham = json.loads(res)
            d["online_ok"] = True
            if isinstance(ham, dict):
                en_iyiler = dict()
                for v in ham.values():
                    if isinstance(v, dict) and "isim" in v and "skor" in v:
                        ad = str(v["isim"])
                        sk = int(v["skor"])
                        if ad not in en_iyiler or sk > en_iyiler[ad]:
                            en_iyiler[ad] = sk
                liste = [{"isim": k, "skor": v} for k, v in en_iyiler.items()]
        except Exception:
            d["online_ok"] = False
        return sorted(liste, key=lambda x: x["skor"], reverse=True)[:10]
    t0 = L()
    menu_rekor_txt = ft.Text(f"{t0['rekor']}: {d['rekor']}", size=15, weight=ft.FontWeight.BOLD, color="#ffd32a")
    m_baslik_txt = ft.Text(t0["baslik"], size=26, weight=ft.FontWeight.BOLD, color="white")
    m_alt_txt = ft.Text(t0["alt"], size=13, color="#a2a8d3")
    btn_oyna = ft.Button(t0["oyna"], bgcolor="#0984e3", color="white", width=240, height=52, on_click=lambda _: oyna_tikla())
    btn_magaza = ft.Button(t0["magaza"], bgcolor="#ffd32a", color="#121225", width=240, height=44, on_click=lambda e: magaza(e))
    btn_skor = ft.Button(t0["skor"], bgcolor="#6c5ce7", color="white", width=240, height=44, on_click=lambda e: skor_tablosu_ac(e))
    btn_dil = ft.Button(f"{t0['diller']} ({t0['ad']})", bgcolor="#00b894", color="white", width=240, height=44, on_click=lambda _: dil_ac())

    def prof_metin_yap():
        t = L()
        bas = 1 if prof["kadIdx"] == 0 else (5 if prof["kadIdx"] == 1 else (9 if prof["kadIdx"] == 2 else 1))
        return f"{prof['isim']} | {t['kad'][prof['kadIdx']]} - {bas + prof['sinIdx']}{t['sinif']}"

    prof_bilgi_txt = ft.Text(prof_metin_yap() if prof["kayitli"] else "", size=12, color="#00cec9", weight=ft.FontWeight.BOLD, visible=prof["kayitli"])
    prof_degis_btn = ft.Button(t0["profDegis"], bgcolor="#636e72", color="white", width=240, visible=prof["kayitli"], on_click=lambda _: profil_ac())

    def dil_uygula():
        t = L()
        menu_rekor_txt.value = f"{t['rekor']}: {d['rekor']}"
        m_baslik_txt.value = t["baslik"]
        m_alt_txt.value = t["alt"]
        btn_oyna.content = t["oyna"]
        btn_magaza.content = t["magaza"]
        btn_skor.content = t["skor"]
        btn_dil.content = f"{t['diller']} ({t['ad']})"
        prof_degis_btn.content = t["profDegis"]
        mag_btn.content = t["magaza"]
        tekrar_btn.content = t["tekrar"]
        if prof["kayitli"]:
            prof_bilgi_txt.value = prof_metin_yap()
        page.update()

    def dil_ac():
        async def dil_sec(kod):
            prof["dil"] = kod
            try:
                await page.client_storage.set_async("hm_prof", prof)
            except Exception:
                pass
            page.pop_dialog()
            dil_uygula()

        satirlar_dil = list()
        kodlar = list(T.keys())
        for i in range(0, len(kodlar), 2):
            k1 = kodlar[i]
            b1 = ft.Button(T[k1]["ad"], bgcolor="#00b894" if prof["dil"] == k1 else "#121225", color="white", width=122, on_click=lambda _, c=k1: page.run_task(dil_sec, c))
            row_btns = [b1]
            if i + 1 < len(kodlar):
                k2 = kodlar[i + 1]
                b2 = ft.Button(T[k2]["ad"], bgcolor="#00b894" if prof["dil"] == k2 else "#121225", color="white", width=122, on_click=lambda _, c=k2: page.run_task(dil_sec, c))
                row_btns.append(b2)
            satirlar_dil.append(ft.Row(row_btns, alignment=ft.MainAxisAlignment.CENTER, spacing=6))

        dlg = ft.AlertDialog(bgcolor="#1e1e3f", title=ft.Text(L()["diller"], color="white"), content=ft.Column(satirlar_dil, tight=True, spacing=5), actions=[ft.TextButton(L()["kapat"], on_click=lambda _: page.pop_dialog())])
        page.show_dialog(dlg)

    def oyna_tikla():
        if prof["kayitli"]:
            mod_ve_ders_ac()
        else:
            profil_ac()

    def profil_ac():
        t = L()
        g_kad = [prof["kadIdx"]]
        g_sin = [prof["sinIdx"]]
        sinif_kolon = ft.Column(spacing=4, tight=True)
        ad_input = ft.TextField(label=t["adYer"], max_length=20, value=prof["isim"], autofocus=True, color="white", border_color="#0984e3")

        def sinif_yenile():
            sinif_kolon.controls.clear()
            bas = 1 if g_kad == 0 else (5 if g_kad == 1 else (9 if g_kad == 2 else 1))
            for i in range(4):
                sinif_kolon.controls.append(ft.Button(f"{bas + i}{t['sinif']}", bgcolor="#0984e3" if g_sin == i else "#121225", color="white", width=240, on_click=lambda _, idx=i: (g_sin.__setitem__(0, idx), sinif_yenile(), page.update())))

        def kad_sec(idx):
            g_kad = idx
            sinif_yenile()
            page.update()

        kad_satir1 = ft.Row([ft.Button(t["kad"], bgcolor="#00b894", color="white", width=116, on_click=lambda _: kad_sec(0)), ft.Button(t["kad"], bgcolor="#0984e3", color="white", width=116, on_click=lambda _: kad_sec(1))], alignment=ft.MainAxisAlignment.CENTER, spacing=6)
        kad_satir2 = ft.Row([ft.Button(t["kad"], bgcolor="#e17055", color="white", width=116, on_click=lambda _: kad_sec(2)), ft.Button(t["kad"], bgcolor="#6c5ce7", color="white", width=116, on_click=lambda _: kad_sec(3))], alignment=ft.MainAxisAlignment.CENTER, spacing=6)

        async def kaydet_tikla(ev=None):
            ad = (ad_input.value or "").strip()[:20]
            if not ad:
                return
            prof.update({"isim": ad, "kadIdx": g_kad, "sinIdx": g_sin, "kayitli": True})
            try:
                await page.client_storage.set_async("hm_prof", prof)
            except Exception:
                pass
            prof_bilgi_txt.value = prof_metin_yap()
            prof_bilgi_txt.visible = True
            prof_degis_btn.visible = True
            page.pop_dialog()
            mod_ve_ders_ac()

        sinif_yenile()
        dlg = ft.AlertDialog(bgcolor="#1e1e3f", title=ft.Text(t["profBas"], color="white"), content=ft.Column([ad_input, kad_satir1, kad_satir2, sinif_kolon], tight=True, spacing=6), actions=[ft.TextButton(t["iptal"], on_click=lambda _: page.pop_dialog()), ft.Button(t["kaydet"], bgcolor="#ffd32a", color="#121225", on_click=kaydet_tikla)])
        page.show_dialog(dlg)

    def mod_ve_ders_ac():
        t = L()
        durum_txt = ft.Text(f"{t['modlar'][d['zorIdx']]} | {t['dersler'][d['dersIdx']]}", size=11, color="#ffd32a", weight=ft.FontWeight.BOLD)

        def zor_sec(i):
            d["zorIdx"] = i
            durum_txt.value = f"{t['modlar'][d['zorIdx']]} | {t['dersler'][d['dersIdx']]}"
            page.update()

        def ders_sec(i):
            d["dersIdx"] = i
            durum_txt.value = f"{t['modlar'][d['zorIdx']]} | {t['dersler'][d['dersIdx']]}"
            page.update()

        zor_row1 = ft.Row([ft.Button(t["modlar"], bgcolor="#00b894", color="white", width=116, on_click=lambda _: zor_sec(0)), ft.Button(t["modlar"], bgcolor="#0984e3", color="white", width=116, on_click=lambda _: zor_sec(1))], alignment=ft.MainAxisAlignment.CENTER, spacing=6)
        zor_row2 = ft.Row([ft.Button(t["modlar"], bgcolor="#e17055", color="white", width=116, on_click=lambda _: zor_sec(2)), ft.Button(t["modlar"], bgcolor="#d63031", color="white", width=116, on_click=lambda _: zor_sec(3))], alignment=ft.MainAxisAlignment.CENTER, spacing=6)
        kat_row1 = ft.Row([ft.Button(t["dersler"], bgcolor="#e74c3c", color="white", width=116, height=48, on_click=lambda _: ders_sec(0)), ft.Button(t["dersler"], bgcolor="#2980b9", color="white", width=116, height=48, on_click=lambda _: ders_sec(1))], alignment=ft.MainAxisAlignment.CENTER, spacing=6)
        kat_row2 = ft.Row([ft.Button(t["dersler"], bgcolor="#27ae60", color="white", width=116, height=48, on_click=lambda _: ders_sec(2)), ft.Button(t["dersler"], bgcolor="#f39c12", color="white", width=116, height=48, on_click=lambda _: ders_sec(3))], alignment=ft.MainAxisAlignment.CENTER, spacing=6)

        dlg = ft.AlertDialog(bgcolor="#1e1e3f", title=ft.Text(prof_metin_yap(), size=13, color="white"), content=ft.Column([durum_txt, zor_row1, zor_row2, kat_row1, kat_row2, ft.Row([ft.Button(t["tek"], bgcolor="#0984e3", color="white", width=116, on_click=lambda _: (page.pop_dialog(), oyun_basla_mod("solo"))), ft.Button(t["vs"], bgcolor="#e17055", color="white", width=116, on_click=lambda _: (page.pop_dialog(), oyun_basla_mod("vs")))], alignment=ft.MainAxisAlignment.CENTER, spacing=6)], tight=True, spacing=5), actions=[ft.TextButton(t["iptal"], on_click=lambda _: page.pop_dialog())])
        page.show_dialog(dlg)
    def oyun_basla_mod(mod):
        d["mod"] = mod
        t = L()
        if mod == "solo":
            ekran_degistir("oyun")
            oyunu_baslat()
        else:
            ad1 = ft.TextField(label="1.", max_length=20, value=prof["isim"], color="white", border_color="#0984e3")
            ad2 = ft.TextField(label="2.", max_length=20, autofocus=True, color="white", border_color="#e17055")

            def vs_onayla(ev=None):
                i1 = (ad1.value or "").strip()[:20]
                i2 = (ad2.value or "").strip()[:20]
                if not i1 or not i2:
                    return
                d["p1"] = {"isim": i1, "puan": 0, "dogru": 0, "yanlis": 0, "bos": 0, "ort": 99.0}
                d["p2"] = {"isim": i2, "puan": 0, "dogru": 0, "yanlis": 0, "bos": 0, "ort": 99.0}
                d["vs_sira"] = 1
                page.pop_dialog()
                ekran_degistir("oyun")
                oyunu_baslat()

            dlg = ft.AlertDialog(bgcolor="#1e1e3f", title=ft.Text(t["vs"], color="white"), content=ft.Column([ad1, ad2], tight=True), actions=[ft.TextButton(t["iptal"], on_click=lambda _: page.pop_dialog()), ft.Button(t["baslasin"], bgcolor="#00b894", color="white", on_click=vs_onayla)])
            page.show_dialog(dlg)

    def skor_tablosu_ac(e=None):
        t = L()
        kayitlar = skorlari_getir()
        satir_listesi = [ft.Text("-", color="#a2a8d3")] if not kayitlar else [ft.Row([ft.Text(f"{idx}. {item['isim']}", color="#ffd32a" if idx == 1 else "white", weight=ft.FontWeight.BOLD, size=14), ft.Text(f"{item['skor']} {t['puan']}", color="#00b894", weight=ft.FontWeight.BOLD, size=14)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, width=250) for idx, item in enumerate(kayitlar, 1)]
        page.show_dialog(ft.AlertDialog(bgcolor="#1e1e3f", title=ft.Text(f"{t['skor']} (Top 10)", color="#ffd32a"), content=ft.Column(satir_listesi, tight=True, spacing=6), actions=[ft.TextButton(t["kapat"], on_click=lambda _: page.pop_dialog())]))

    vs_banner = ft.Container(content=ft.Text("", size=12, weight=ft.FontWeight.BOLD, color="white"), bgcolor="#e17055", padding=5, border_radius=8, visible=False)
    ust_txt = ft.Text("Can:3 P:0 S:1", size=11, weight=ft.FontWeight.BOLD, color="#ff6b81")
    altin_txt = ft.Text("Altin:50", size=11, weight=ft.FontWeight.BOLD, color="#ffd32a")
    bar = ft.ProgressBar(value=1.0, width=310, height=11, color="#00b894", bgcolor="#1e1e3f")
    kose1 = ft.Text("?", size=14, weight=ft.FontWeight.BOLD, color="white")
    ders_etiket = ft.Text("Matematik", size=10, weight=ft.FontWeight.BOLD, color="white")
    kose2 = ft.Text("?", size=14, weight=ft.FontWeight.BOLD, color="white")
    soru_txt = ft.Text("12 + 8 = ?", size=18, weight=ft.FontWeight.BOLD, color="#121225", text_align=ft.TextAlign.CENTER)

    kart_ic = ft.Container(content=ft.Column([ft.Row([kose1, ders_etiket], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, width=240), ft.Container(content=soru_txt, bgcolor="white", border_radius=0, width=236, height=106, padding=8, alignment=ft.Alignment(0, 0)), ft.Row([kose2], alignment=ft.MainAxisAlignment.END, width=240)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, horizontal_alignment=ft.CrossAxisAlignment.CENTER, width=240, height=160), bgcolor="#e74c3c", border_radius=12, padding=8, width=258, height=176, alignment=ft.Alignment(0, 0))
    kart_dis = ft.Container(content=kart_ic, bgcolor="white", border_radius=16, padding=6)
    msg_txt = ft.Text("", size=12, weight=ft.FontWeight.BOLD, color="#ffd32a", text_align=ft.TextAlign.CENTER)
    karne_txt = ft.Text("", size=11, weight=ft.FontWeight.BOLD, color="white", text_align=ft.TextAlign.CENTER)
    karne_kutu = ft.Container(content=karne_txt, bgcolor="#1e1e3f", padding=8, border_radius=10, visible=False)

    sik_butonlar = [ft.Button(f"{harfler[i]}) ?", bgcolor=sik_renk[i], color="white", width=155, height=52, on_click=lambda _, idx=i: sik_sec(idx)) for i in range(4)]
    sik_kolon = ft.Column([ft.Row([sik_butonlar, sik_butonlar], alignment=ft.MainAxisAlignment.CENTER, spacing=8), ft.Row([sik_butonlar, sik_butonlar], alignment=ft.MainAxisAlignment.CENTER, spacing=8)], spacing=8, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    def guncelle():
        t = L()
        ust_txt.value = f"{t['can']}:{d['can']} P:{d['puan']} S:{d['svy']}"
        altin_txt.value = f"{t['altin']}:{d['altin']}"
        menu_rekor_txt.value = f"{t['rekor']}: {d['rekor']}"
        d_btn.content = f"{t['dondur']} ({d['jd']})"
        s_btn.content = f"+10s ({d['js']})"
        e_btn.content = f"50/50 ({d['je']})"
        a_btn.content = f"{t['atla']} ({d['vs_atla']})" if d["mod"] == "vs" else f"{t['atla']} ({d['ja']})"
        page.update()

    def duraklat_degis(e=None):
        if not d["aktif"] or d["can"] <= 0:
            return
        d["dur"] = not d["dur"]
        p_btn.content = ">" if d["dur"] else "II"
        p_btn.bgcolor = "#00b894" if d["dur"] else "#636e72"
        kart_ic.bgcolor = "#636e72" if d["dur"] else d["renk"]
        soru_txt.value = L()["durak"] if d["dur"] else d["soru"]
        guncelle()

    def geri_tikla(e=None):
        onceki_dur = d["dur"]
        d["dur"] = True
        t = L()

        def secim(kaydet_mi):
            if kaydet_mi and d["mod"] == "solo":
                if d["puan"] > d["rekor"]:
                    d["rekor"] = d["puan"]
                skoru_kaydet_bulut(prof["isim"] or "Player", d["puan"])
            d["aktif"] = False
            d["dur"] = False
            page.pop_dialog()
            gc.collect()
            guncelle()
            ekran_degistir("menu")

        def vazgec(ev=None):
            d["dur"] = onceki_dur
            page.pop_dialog()

        if d["mod"] == "vs":
            page.show_dialog(ft.AlertDialog(bgcolor="#1e1e3f", title=ft.Text(t["vs"], color="white"), actions=[ft.Button(t["tamam"], bgcolor="#ff4757", color="white", on_click=lambda _: secim(False)), ft.TextButton(t["iptal"], on_click=vazgec)]))
        else:
            page.show_dialog(ft.AlertDialog(bgcolor="#1e1e3f", title=ft.Text(t["kaydetSor"], color="white"), content=ft.Text(f"{prof['isim']}: {d['puan']} {t['puan']}", color="#dfe6e9"), actions=[ft.Button(t["kaydetBtn"], bgcolor="#00b894", color="white", on_click=lambda _: secim(True)), ft.Button(t["kaydetmeBtn"], bgcolor="#ff4757", color="white", on_click=lambda _: secim(False)), ft.TextButton(t["iptal"], on_click=vazgec)]))

    def soru_uret():
        t = L()
        if d["dersIdx"] == 1:
            m, a = random.randint(2, 15), random.randint(2, 10)
            f = m * a
            siklar = [f"{f} N", f"{f + m} N", f"{max(1, f - a)} N", f"{f * 2} N"]
            random.shuffle(siklar)
            return f"F = m . a (m={m}kg, a={a}m/s2) => F=?", f"{f} N", "F", siklar
        if d["dersIdx"] == 2:
            yil = random.randint(11, 20) * 100 + random.randint(1, 95)
            yy = ((yil - 1) // 100) + 1
            siklar = [str(yy), str(yy - 1), str(yy + 1), str(yy + 2)]
            random.shuffle(siklar)
            return f"{yil} => Century / YY = ?", str(yy), "H", siklar
        if d["dersIdx"] == 3:
            b = random.randint(2, 8)
            cv = b * 32 - 1
            siklar = [str(cv), str(cv + 4), str(cv - 4), str(cv + 8)]
            random.shuffle(siklar)
            return f"{b - 1}, {b * 2 - 1}, {b * 4 - 1}, {b * 8 - 1}, ?", str(cv), "L", siklar

        guc = (d["zorIdx"] + 1) + prof["kadIdx"] + (d["svy"] - 1)
        while True:
            if guc <= 2:
                s1, s2 = random.randint(4, 15), random.randint(3, 14)
                cvp, metin, simge = (s1 + s2, f"{s1} + {s2} = ?", "+") if random.random() < 0.5 else (s1 * s2, f"{s1} x {s2} = ?", "x")
            elif guc <= 4:
                a, x, b = random.randint(3, 9), random.randint(4, 15), random.randint(5, 20)
                cvp, metin, simge = x, f"{a}x + {b} = {a * x + b} ({t['xBul']})", "X"
            else:
                s1, s2 = random.randint(28, 82), random.randint(24, 88)
                cvp, metin, simge = s1 * s2, f"{s1} x {s2} ({t['soruEk']})", "x"
            if metin not in d["sorulanlar"]:
                d["sorulanlar"].add(metin)
                break

        sik_set = {str(cvp)}
        while len(sik_set) < 4:
            fark = random.randint(1, 5) * (10 if abs(cvp) > 100 else 2)
            aday = cvp + (fark if random.random() < 0.5 else -fark)
            if aday != cvp and aday >= 0:
                sik_set.add(str(aday))
        siklar = list(sik_set)
        random.shuffle(siklar)
        return metin, str(cvp), simge, siklar

    def yeni_soru():
        d["aktif"] = True
        t = L()
        ys = 1 if d["puan"] < 40 else (2 if d["puan"] < 90 else (3 if d["puan"] < 150 else 4))
        if ys > d["svy"]:
            d["svy"] = ys
        d["kalan"] = 15.0 if d["mod"] == "vs" else 12.0
        d["max"] = d["kalan"]
        d["donma"] = 0.0
        metin, cvp, simge, siklar = soru_uret()
        d["dc"], d["simge"], d["soru"], d["siklar"] = cvp, simge, metin, siklar
        d["renk"] = random.choice(uno)
        soru_txt.size = 14 if len(metin) > 35 else 19
        kart_ic.bgcolor = d["renk"]
        ders_etiket.value = f"{t['dersler'][d['dersIdx']]} | {t['modlar'][d['zorIdx']]}"
        soru_txt.value = d["soru"]
        kose1.value = simge
        kose2.value = simge
        for i in range(4):
            sik_butonlar[i].content = f"{harfler[i]}) {siklar[i]}"
            sik_butonlar[i].visible = True
        sik_kolon.visible = True
        guncelle()

    def sik_sec(idx):
        if not d["aktif"] or d["dur"] or d["can"] <= 0:
            return
        t = L()
        if d["siklar"][idx] == d["dc"]:
            d["top_sure"] += (d["max"] - d["kalan"])
            d["dogru"] += 1
            d["kombo"] += 1
            carpan = 2 if d["cift_puan"] > 0 else 1
            if d["cift_puan"] > 0:
                d["cift_puan"] -= 1
            kaz = (10 + (d["kombo"] - 1) * 2) * carpan
            d["puan"] += kaz
            if d["mod"] == "solo":
                d["altin"] += 10 * carpan
            msg_txt.value = f"{t['harika']} +{kaz} {t['puan']}"
            msg_txt.color = "#00b894"
            yeni_soru()
        else:
            d["yanlis"] += 1
            d["can"] -= 1
            d["kombo"] = 0
            if d["can"] == 0:
                bitti(f"{t['dogrusu']}: {d['dc']}")
            else:
                msg_txt.value = f"{t['yanlis']}! {t['dogrusu']}: {d['dc']}"
                msg_txt.color = "#ff7675"
                yeni_soru()

    def bitti(sebep):
        try:
            page.pop_dialog()
        except Exception:
            pass
        t = L()
        d["aktif"] = False
        d["kombo"] = 0
        sik_kolon.visible = False
        kart_ic.bgcolor = "#e74c3c"
        soru_txt.value = f"{t['bitti']}\n{d['puan']} {t['puan']}"
        if d["mod"] == "vs":
            ort = (d["top_sure"] / d["dogru"]) if d["dogru"] > 0 else 99.0
            if d["vs_sira"] == 1:
                d["p1"] = {"isim": d["p1"]["isim"], "puan": d["puan"], "dogru": d["dogru"], "yanlis": d["yanlis"], "bos": d["bos"], "ort": ort}
                d["vs_sira"] = 2
                guncelle()
                page.show_dialog(ft.AlertDialog(bgcolor="#1e1e3f", title=ft.Text(d["p1"]["isim"], color="#ffd32a"), content=ft.Text(f"{d['p1']['puan']} {t['puan']}\n{t['sira']}: {d['p2']['isim']}", color="white"), actions=[ft.Button(t["baslasin"], bgcolor="#00b894", color="white", on_click=lambda _: (page.pop_dialog(), oyunu_baslat()))]))
                return
            d["p2"] = {"isim": d["p2"]["isim"], "puan": d["puan"], "dogru": d["dogru"], "yanlis": d["yanlis"], "bos": d["bos"], "ort": ort}
            if d["p1"]["puan"] != d["p2"]["puan"]:
                page.run_task(konfeti_patlat)
                kaz = d["p1"] if d["p1"]["puan"] > d["p2"]["puan"] else d["p2"]
                kay = d["p2"] if d["p1"]["puan"] > d["p2"]["puan"] else d["p1"]
                kaz_yeni, kay_yeni = kaz["puan"] + 25, max(0, kay["puan"] - 30)
                d["altin"] += 50
                skoru_kaydet_bulut(kaz["isim"], kaz_yeni)
                icerik = ft.Column([ft.Text(f"{t['kazandin']} {kaz['isim']} ({kaz_yeni} {t['puan']}, +50 {t['altin']})", color="#ffd32a", weight=ft.FontWeight.BOLD), ft.Text(f"{t['kaybettin']} {kay['isim']} ({kay_yeni} {t['puan']})", color="#ff7675")], tight=True)
            else:
                icerik = ft.Text(t["berabere"], color="#ffd32a")
            page.show_dialog(ft.AlertDialog(bgcolor="#1e1e3f", title=ft.Text(t["vs"], color="white"), content=icerik, actions=[ft.Button(t["tamam"], bgcolor="#0984e3", color="white", on_click=lambda _: page.pop_dialog())]))
            d["vs_sira"] = 1
        else:
            final_skor = max(0, d["puan"] - (10 if (d["yanlis"] + d["bos"]) > d["dogru"] else 0))
            if final_skor > d["rekor"]:
                d["rekor"] = final_skor
            skoru_kaydet_bulut(prof["isim"] or "Player", final_skor)
            karne_txt.value = f"{t['seviye']} {d['svy']}: {d['puan']} {t['puan']}\n{t['dogru']}:{d['dogru']} | {t['yanlis']}:{d['yanlis']} | {t['bos']}:{d['bos']}"
            karne_kutu.visible = True
        tekrar_btn.visible = True
        guncelle()

    def joker(tp):
        if not d["aktif"] or d["dur"] or d["can"] <= 0:
            return
        if tp == "d" and d["jd"] > 0:
            d["jd"] -= 1
            d["donma"] += 5.0
            guncelle()
        elif tp == "s" and d["js"] > 0:
            d["js"] -= 1
            d["kalan"] += 10.0
            d["max"] = max(d["max"], d["kalan"])
            guncelle()
        elif tp == "e" and d["je"] > 0:
            d["je"] -= 1
            silinen = 0
            for i in range(4):
                if d["siklar"][i] != d["dc"] and silinen < 2:
                    sik_butonlar[i].visible = False
                    silinen += 1
            guncelle()
        elif tp == "a":
            if d["mod"] == "vs" and d["vs_atla"] > 0:
                d["vs_atla"] -= 1
                d["bos"] += 1
                yeni_soru()
            elif d["mod"] == "solo" and d["ja"] > 0:
                d["ja"] -= 1
                d["bos"] += 1
                yeni_soru()

    def magaza(e):
        if d["dur"]:
            return
        t = L()
        m_txt = ft.Text(f"{t['altin']}: {d['altin']}", color="#ffd32a", weight=ft.FontWeight.BOLD)

        def al(tp, f):
            if d["altin"] < f:
                m_txt.value = t["yetersiz"]
                page.update()
                return
            d["altin"] -= f
            if tp == "d":
                d["jd"] += 1
            elif tp == "s":
                d["js"] += 1
            elif tp == "e":
                d["je"] += 1
            elif tp == "a":
                d["ja"] += 1
            elif tp == "2x":
                d["cift_puan"] += 3
            elif tp == "c":
                d["jc"] += 1
                if d["can"] > 0:
                    d["can"] += 1
            m_txt.value = f"{t['altin']}: {d['altin']}"
            guncelle()

        page.show_dialog(ft.AlertDialog(bgcolor="#1e1e3f", title=ft.Text(t["magaza"], color="white"), content=ft.Column([m_txt, ft.Button(f"{t['magItem']} - 30", bgcolor="#0984e3", color="white", width=240, on_click=lambda _: al("d", 30)), ft.Button(f"{t['magItem']} - 40", bgcolor="#00b894", color="white", width=240, on_click=lambda _: al("e", 40)), ft.Button(f"{t['magItem']} - 50", bgcolor="#6c5ce7", color="white", width=240, on_click=lambda _: al("s", 50)), ft.Button(f"{t['magItem']} - 60", bgcolor="#e94560", color="white", width=240, on_click=lambda _: al("c", 60)), ft.Button(f"{t['magItem']} - 70", bgcolor="#e17055", color="white", width=240, on_click=lambda _: al("a", 70)), ft.Button(f"{t['magItem']} - 80", bgcolor="#fdcb6e", color="#121225", width=240, on_click=lambda _: al("2x", 80))], tight=True, spacing=4), actions=[ft.TextButton(t["kapat"], on_click=lambda _: page.pop_dialog())]))

    def oyunu_baslat(e=None):
        d.update({"puan": 0, "svy": 1, "kombo": 0, "dur": False, "dogru": 0, "yanlis": 0, "bos": 0, "top_sure": 0.0, "cift_puan": 0})
        d["sorulanlar"].clear()
        karne_kutu.visible = False
        tekrar_btn.visible = False
        if d["mod"] == "vs":
            d["can"], d["vs_atla"] = 3, 3
            d_btn.visible = s_btn.visible = e_btn.visible = mag_btn.visible = False
            vs_banner.visible = True
        else:
            d["can"] = 3 + d["jc"]
            d_btn.visible = s_btn.visible = e_btn.visible = mag_btn.visible = True
            vs_banner.visible = False
        yeni_soru()

    geri_btn = ft.Button("<-", bgcolor="#ff4757", color="white", width=44, on_click=geri_tikla)
    p_btn = ft.Button("II", bgcolor="#636e72", color="white", width=40, on_click=duraklat_degis)
    mag_btn = ft.Button(t0["magaza"], bgcolor="#ffd32a", color="#121225", width=82, on_click=magaza)
        d_btn = ft.Button(f"{t0['dondur']} (1)", bgcolor="#0984e3", color="white", on_click=lambda _: joker("d"))
    s_btn = ft.Button("+10s (0)", bgcolor="#6c5ce7", color="white", on_click=lambda _: joker("s"))
    e_btn = ft.Button("50/50 (1)", bgcolor="#00b894", color="white", on_click=lambda _: joker("e"))
    a_btn = ft.Button(f"{t0['atla']} (1)", bgcolor="#e17055", color="white", on_click=lambda _: joker("a"))
    tekrar_btn = ft.Button(t0["tekrar"], bgcolor="#ff4757", color="white", width=260, height=46, visible=False, on_click=oyunu_baslat)

    ust_bar = ft.Container(content=ft.Row([geri_btn, p_btn, ust_txt, altin_txt, mag_btn], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, spacing=2), bgcolor="#1e1e3f", padding=6, border_radius=10, width=340)
    menu_ekrani = ft.Column([ft.Container(height=20), ft.Container(content=menu_rekor_txt, bgcolor="#1e1e3f", padding=12, border_radius=12), prof_bilgi_txt, ft.Container(height=16), m_baslik_txt, m_alt_txt, ft.Container(height=14), btn_oyna, ft.Container(height=6), btn_magaza, ft.Container(height=6), btn_skor, ft.Container(height=6), btn_dil, prof_degis_btn], horizontal_alignment=ft.CrossAxisAlignment.CENTER, visible=True)
    oyun_ekrani = ft.Column([ft.Container(height=18), vs_banner, ust_bar, bar, kart_dis, ft.Row([d_btn, s_btn, e_btn, a_btn], alignment=ft.MainAxisAlignment.CENTER, spacing=4), msg_txt, karne_kutu, sik_kolon, tekrar_btn], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=6, visible=False)

    def ekran_degistir(hedef):
        menu_ekrani.visible = (hedef == "menu")
        oyun_ekrani.visible = (hedef == "oyun")
        page.update()

    page.add(ft.Stack([ft.Row([ft.Column([menu_ekrani, oyun_ekrani], horizontal_alignment=ft.CrossAxisAlignment.CENTER)], alignment=ft.MainAxisAlignment.CENTER, expand=True), konfeti_katman], expand=True))

    async def sayac():
        while True:
            await asyncio.sleep(0.05)
            if d["aktif"] and not d["dur"] and d["can"] > 0:
                if d["donma"] > 0:
                    d["donma"] -= 0.05
                    bar.color = "#00cec9"
                else:
                    d["kalan"] -= 0.05
                    o = max(0.0, min(1.0, d["kalan"] / d["max"]))
                    bar.value = o
                    bar.color = "#00b894" if o > 0.5 else ("#ffd32a" if o > 0.25 else "#ff4757")
                    if d["kalan"] <= 0:
                        d["bos"] += 1
                        d["can"] -= 1
                        d["kombo"] = 0
                        if d["can"] == 0:
                            bitti(L()["sureDoldu"])
                        else:
                            yeni_soru()
                page.update()

    page.run_task(sayac)

ft.run(main)

