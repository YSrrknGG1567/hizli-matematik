import flet as ft, random, asyncio

async def main(page: ft.Page):
    page.title = "Hizli Matematik"
    page.bgcolor = "#121225"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 12
    uno = ["#e74c3c", "#2980b9", "#27ae60", "#f39c12"]
    d = {"puan": 0, "can": 3, "svy": 1, "dc": 0, "kalan": 7.0, "max": 7.0, "donma": 0.0, "aktif": True, "dur": False, "altin": 50, "rekor": 0, "kombo": 0, "jd": 1, "js": 0, "jc": 0, "girdi": "", "soru": "12 + 8", "simge": "+", "renk": "#e74c3c"}
    ust_txt = ft.Text("Can: 3 | Puan: 0 | Svy: 1", size=13, weight=ft.FontWeight.BOLD, color="#ff6b81")
    altin_txt = ft.Text("Altin: 50", size=13, weight=ft.FontWeight.BOLD, color="#ffd32a")
    bar = ft.ProgressBar(value=1.0, width=340, height=11, color="#00b894", bgcolor="#1e1e3f")
    kose1 = ft.Text("+", size=16, weight=ft.FontWeight.BOLD, color="white")
    kose2 = ft.Text("+", size=16, weight=ft.FontWeight.BOLD, color="white")
    soru_txt = ft.Text("12 + 8", size=28, weight=ft.FontWeight.BOLD, color="#121225")
    cevap_txt = ft.Text("?", size=24, weight=ft.FontWeight.BOLD, color="#0f3460")
    kart_ic = ft.Container(ft.Column([ft.Row([kose1], alignment=ft.MainAxisAlignment.START), ft.Container(ft.Column([soru_txt, cevap_txt], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2), bgcolor="white", border_radius=40, padding=ft.padding.symmetric(horizontal=26, vertical=10)), ft.Row([kose2], alignment=ft.MainAxisAlignment.END)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN), bgcolor="#e74c3c", border_radius=14, padding=10, width=230, height=165)
    kart_dis = ft.Container(kart_ic, bgcolor="white", border_radius=18, padding=6, shadow=ft.BoxShadow(blur_radius=12, color="#000000"))
    msg_txt = ft.Text("UNO Kartlari ve Magaza Aktif!", size=12, weight=ft.FontWeight.BOLD, color="#a2a8d3", text_align=ft.TextAlign.CENTER)
    def guncelle():
        ust_txt.value = f"Can: {d['can']} | Puan: {d['puan']} | Svy: {d['svy']}"
        altin_txt.value = f"Altin: {d['altin']}"
        d_btn.text = f"Dondur 5s ({d['jd']})"
        s_btn.text = f"+10sn ({d['js']})"
        cevap_txt.value = d["girdi"] if d["girdi"] != "" else "?"
        page.update()
    def duraklat_degis(e=None):
        if not d["aktif"] or d["can"] <= 0: return
        d["dur"] = not d["dur"]
        if d["dur"]:
            p_btn.text = "> Devam"; p_btn.bgcolor = "#00b894"
            kart_ic.bgcolor = "#636e72"; soru_txt.value = "DURAKLATILDI"; kose1.value = "II"; kose2.value = "II"
        else:
            p_btn.text = "II"; p_btn.bgcolor = "#636e72"
            kart_ic.bgcolor = d["renk"]; soru_txt.value = d["soru"]; kose1.value = d["simge"]; kose2.value = d["simge"]
        guncelle()
    def yeni_soru():
        d["aktif"] = True; d["kalan"] = 7.0; d["max"] = 7.0; d["donma"] = 0.0; d["girdi"] = ""
        ys = 1 if d["puan"] < 50 else (2 if d["puan"] < 100 else 3)
        if ys > d["svy"]: d["svy"] = ys
        ust = 10 if d["svy"] == 1 else (20 if d["svy"] == 2 else 50)
        s1, s2 = random.randint(1, ust), random.randint(1, ust)
        isl = random.choice(["+", "-", "*"])
        d["dc"] = s1 + s2 if isl == "+" else (s1 - s2 if isl == "-" else s1 * s2)
        d["simge"] = "x" if isl == "*" else isl
        d["soru"] = f"{s1} {d['simge']} {s2}"
        d["renk"] = random.choice(uno)
        kart_ic.bgcolor = d["renk"]; soru_txt.value = d["soru"]; kose1.value = d["simge"]; kose2.value = d["simge"]
        guncelle()
    def bitti(sebep):
        d["aktif"] = False; d["kombo"] = 0; d["donma"] = 0.0
        if d["puan"] > d["rekor"]: d["rekor"] = d["puan"]
        kart_ic.bgcolor = "#e74c3c"; soru_txt.value = "OYUN BITTI"; kose1.value = "X"; kose2.value = "X"
        msg_txt.value = f"{sebep} | Puan: {d['puan']} | Rekor: {d['rekor']}"; msg_txt.color = "#ff7675"
        tekrar_btn.visible = True; guncelle()
    def joker(t):
        if not d["aktif"] or d["dur"] or d["can"] <= 0: return
        if t == "d" and d["jd"] > 0:
            d["jd"] -= 1; d["donma"] += 5.0; msg_txt.value = "ZAMAN DONDU! (5 saniye)"; msg_txt.color = "#00cec9"
        elif t == "s" and d["js"] > 0:
            d["js"] -= 1; d["kalan"] += 10.0; d["max"] = max(d["max"], d["kalan"]); msg_txt.value = "+10 Saniye Eklendi!"; msg_txt.color = "#a29bfe"
        else: msg_txt.value = "Joker kalmadi! Magazadan al"; msg_txt.color = "#ffd32a"
        guncelle()
    def magaza(e):
        if d["dur"]: return
        d["dur"] = True
        m_txt = ft.Text(f"Mevcut Altin: {d['altin']} | Ekstra Can: +{d['jc']}", color="#ffd32a", weight=ft.FontWeight.BOLD)
        def al(t, f):
            if d["altin"] < f: m_txt.value = "Yetersiz altin!"; m_txt.color = "#ff7675"; page.update(); return
            d["altin"] -= f
            if t == "d": d["jd"] += 1; m_txt.value = "Zaman Dondurucu alindi!"
            elif t == "s": d["js"] += 1; m_txt.value = "+10 Saniye alindi!"
            elif t == "c":
                d["jc"] += 1
                if d["can"] > 0: d["can"] += 1
                m_txt.value = f"+1 Can! Baslangic: {3 + d['jc']}"
            m_txt.color = "#00b894"; guncelle()
        def kapat(e=None): d["dur"] = False; dlg.open = False; page.update()
        dlg = ft.AlertDialog(bgcolor="#1e1e3f", title=ft.Text("Magaza", color="white"), content=ft.Column([m_txt, ft.ElevatedButton("Zaman Dondur (5sn) - 30 Altin", bgcolor="#0984e3", color="white", width=250, on_click=lambda _: al("d", 30)), ft.ElevatedButton("Ekstra Sure (+10sn) - 50 Altin", bgcolor="#6c5ce7", color="white", width=250, on_click=lambda _: al("s", 50)), ft.ElevatedButton("Kalici +1 Can - 60 Altin", bgcolor="#e94560", color="white", width=250, on_click=lambda _: al("c", 60))], tight=True), actions=[ft.TextButton("Oyuna Don", on_click=kapat)], on_dismiss=kapat)
        page.overlay.append(dlg); dlg.open = True; page.update()
    def tus(t):
        if d["can"] <= 0 or d["dur"]: return
        if t == "SIL": d["girdi"] = d["girdi"][:-1]
        elif t == "-": d["girdi"] = d["girdi"][1:] if d["girdi"].startswith("-") else "-" + d["girdi"]
        else: d["girdi"] += t
        guncelle()
    def kontrol(e=None):
        if d["can"] <= 0 or d["dur"]: return
        try: cvp = int(d["girdi"])
        except ValueError: msg_txt.value = "Once bir sayi tusla!"; msg_txt.color = "#ffd32a"; guncelle(); return
        if cvp == d["dc"]:
            d["kombo"] += 1; kaz = 10 + (d["kombo"] - 1) * 2; d["puan"] += kaz; d["altin"] += 10
            kt = f" | {d['kombo']}x KOMBO!" if d["kombo"] > 1 else ""
            msg_txt.value = f"Harika! +{kaz} Puan | +10 Altin{kt}"; msg_txt.color = "#00b894"; yeni_soru()
        else:
            d["can"] -= 1; d["kombo"] = 0
            if d["can"] == 0: bitti(f"Dogrusu {d['dc']} idi")
            else: msg_txt.value = f"Yanlis! Dogrusu {d['dc']} idi"; msg_txt.color = "#ff7675"; yeni_soru()
    def tekrar(e=None):
        d["puan"] = 0; d["can"] = 3 + d["jc"]; d["svy"] = 1; d["kombo"] = 0
        tekrar_btn.visible = False; msg_txt.value = f"Yeni oyun! ({d['can']} Can)"; msg_txt.color = "#a2a8d3"; yeni_soru()
    p_btn = ft.ElevatedButton("II", bgcolor="#636e72", color="white", width=45, on_click=duraklat_degis)
    d_btn = ft.ElevatedButton("Dondur 5s (1)", bgcolor="#0984e3", color="white", on_click=lambda _: joker("d"))
    s_btn = ft.ElevatedButton("+10sn (0)", bgcolor="#6c5ce7", color="white", on_click=lambda _: joker("s"))
    tekrar_btn = ft.ElevatedButton("TEKRAR OYNA", bgcolor="#ff4757", color="white", width=220, height=44, visible=False, on_click=tekrar)
    s_renk = ["#c0392b", "#1f618d", "#1e8449", "#d68910"]
    satirlar = []
    for r, s in enumerate([["7", "8", "9"], ["4", "5", "6"], ["1", "2", "3"], ["-", "0", "SIL"]]):
        btns = [ft.ElevatedButton(t, bgcolor=("#ff4757" if t=="SIL" else ("#6c5ce7" if t=="-" else s_renk[r])), color="white", width=85, height=48, on_click=lambda _, x=t: tus(x)) for t in s]
        satirlar.append(ft.Row(btns, alignment=ft.MainAxisAlignment.CENTER))
    page.add(ft.Container(ft.Row([p_btn, ust_txt, altin_txt, ft.ElevatedButton("Magaza", bgcolor="#ffd32a", color="#121225", on_click=magaza)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN), bgcolor="#1e1e3f", padding=8, border_radius=8), bar, kart_dis, ft.Row([d_btn, s_btn], alignment=ft.MainAxisAlignment.CENTER), msg_txt, ft.Column(satirlar, spacing=5), ft.ElevatedButton("GONDER", bgcolor="#00b894", color="white", width=270, height=46, on_click=kontrol), tekrar_btn)
    async def sayac():
        while True:
            await asyncio.sleep(0.05)
            if d["aktif"] and not d["dur"] and d["can"] > 0:
                if d["donma"] > 0: d["donma"] -= 0.05; bar.color = "#00cec9"
                else:
                    d["kalan"] -= 0.05; o = max(0.0, min(1.0, d["kalan"] / d["max"]))
                    bar.value = o; bar.color = "#00b894" if o > 0.5 else ("#ffd32a" if o > 0.25 else "#ff4757")
                    if d["kalan"] <= 0:
                        d["can"] -= 1; d["kombo"] = 0
                        if d["can"] == 0: bitti("SURE DOLDU!")
                        else: msg_txt.value = f"SURE DOLDU! Dogrusu {d['dc']} idi"; msg_txt.color = "#ff7675"; yeni_soru()
                page.update()
    yeni_soru(); page.run_task(sayac)

ft.app(target=main)
