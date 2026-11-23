import flet as ft, random, asyncio

async def main(page: ft.Page):
    page.title = "Hizli Matematik"
    page.bgcolor = "#121225"
    page.padding = 0

    uno = ["#e74c3c", "#2980b9", "#27ae60", "#f39c12"]
    d = {
        "puan": 0, "can": 3, "svy": 1, "dc": 0, "kalan": 7.0, "max": 7.0,
        "donma": 0.0, "aktif": False, "dur": False, "altin": 50, "rekor": 0,
        "kombo": 0, "jd": 1, "js": 0, "jc": 0, "girdi": "", "soru": "12 + 8",
        "simge": "+", "renk": "#e74c3c"
    }

    ust_txt = ft.Text("Can: 3 | P: 0 | Svy: 1", size=12, weight=ft.FontWeight.BOLD, color="#ff6b81")
    altin_txt = ft.Text("Altin: 50", size=12, weight=ft.FontWeight.BOLD, color="#ffd32a")
    bar = ft.ProgressBar(value=1.0, width=300, height=11, color="#00b894", bgcolor="#1e1e3f")
    kose1 = ft.Text("?", size=15, weight=ft.FontWeight.BOLD, color="white")
    kose2 = ft.Text("?", size=15, weight=ft.FontWeight.BOLD, color="white")
    soru_txt = ft.Text("HIZLI MAT", size=22, weight=ft.FontWeight.BOLD, color="#121225", text_align=ft.TextAlign.CENTER)
    cevap_txt = ft.Text("UNO", size=20, weight=ft.FontWeight.BOLD, color="#0f3460", text_align=ft.TextAlign.CENTER)

    kart_ic = ft.Container(
        content=ft.Column(
            [
                ft.Row([kose1], alignment=ft.MainAxisAlignment.START, width=215),
                ft.Container(
                    content=ft.Column(
                        [soru_txt, cevap_txt],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=2,
                    ),
                    bgcolor="white",
                    border_radius=36,
                    width=175,
                    height=82,
                    alignment=ft.Alignment(0, 0),
                ),
                ft.Row([kose2], alignment=ft.MainAxisAlignment.END, width=215),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            width=215,
            height=145,
        ),
        bgcolor="#e74c3c",
        border_radius=14,
        padding=10,
        width=235,
        height=165,
        alignment=ft.Alignment(0, 0),
    )
    kart_dis = ft.Container(content=kart_ic, bgcolor="white", border_radius=18, padding=6)
    msg_txt = ft.Text("Hazir oldugunda OYNA butonuna bas!", size=13, weight=ft.FontWeight.BOLD, color="#ffd32a", text_align=ft.TextAlign.CENTER)

    def guncelle():
        ust_txt.value = f"Can: {d['can']} | P: {d['puan']} | Svy: {d['svy']}"
        altin_txt.value = f"Altin: {d['altin']}"
        d_btn.content = f"Dondur ({d['jd']})"
        s_btn.content = f"+10sn ({d['js']})"
        if d["aktif"]:
            cevap_txt.value = d["girdi"] if d["girdi"] != "" else "?"
        page.update()

    def duraklat_degis(e=None):
        if not d["aktif"] or d["can"] <= 0:
            return
        d["dur"] = not d["dur"]
        if d["dur"]:
            p_btn.content = ">"
            p_btn.bgcolor = "#00b894"
            kart_ic.bgcolor = "#636e72"
            soru_txt.value = "DURAKLATILDI"
            kose1.value = "II"
            kose2.value = "II"
        else:
            p_btn.content = "II"
            p_btn.bgcolor = "#636e72"
            kart_ic.bgcolor = d["renk"]
            soru_txt.value = d["soru"]
            kose1.value = d["simge"]
            kose2.value = d["simge"]
        guncelle()

    def yeni_soru():
        d["aktif"] = True
        ys = 1 if d["puan"] < 50 else (2 if d["puan"] < 100 else 3)
        if ys > d["svy"]:
            d["svy"] = ys
        d["kalan"] = 7.0 + (d["svy"] - 1) * 3.0
        d["max"] = d["kalan"]
        d["donma"] = 0.0
        d["girdi"] = ""
        ust = 10 if d["svy"] == 1 else (20 if d["svy"] == 2 else 50)
        s1, s2 = random.randint(1, ust), random.randint(1, ust)
        isl = random.choice(["+", "-", "*"])
        d["dc"] = s1 + s2 if isl == "+" else (s1 - s2 if isl == "-" else s1 * s2)
        d["simge"] = "x" if isl == "*" else isl
        d["soru"] = f"{s1} {d['simge']} {s2}"
        d["renk"] = random.choice(uno)
        kart_ic.bgcolor = d["renk"]
        soru_txt.value = d["soru"]
        kose1.value = d["simge"]
        kose2.value = d["simge"]
        guncelle()

    def bitti(sebep):
        d["aktif"] = False
        d["kombo"] = 0
        d["donma"] = 0.0
        if d["puan"] > d["rekor"]:
            d["rekor"] = d["puan"]
        kart_ic.bgcolor = "#e74c3c"
        soru_txt.value = "OYUN BITTI"
        cevap_txt.value = f"{d['puan']} P"
        kose1.value = "X"
        kose2.value = "X"
        msg_txt.value = f"{sebep} | Rekor: {d['rekor']}"
        msg_txt.color = "#ff7675"
        oyna_btn.visible = False
        gonder_btn.visible = False
        tekrar_btn.visible = True
        guncelle()

    def joker(t):
        if not d["aktif"] or d["dur"] or d["can"] <= 0:
            return
        if t == "d" and d["jd"] > 0:
            d["jd"] -= 1
            d["donma"] += 5.0
            msg_txt.value = "ZAMAN DONDU! (5 saniye)"
            msg_txt.color = "#00cec9"
            guncelle()
        elif t == "s" and d["js"] > 0:
            d["js"] -= 1
            d["kalan"] += 10.0
            d["max"] = max(d["max"], d["kalan"])
            msg_txt.value = "+10 Saniye Eklendi!"
            msg_txt.color = "#a29bfe"
            guncelle()
        elif t == "a":
            msg_txt.value = f"Soru atlandi! (Cevap {d['dc']} idi)"
            msg_txt.color = "#fdcb6e"
            yeni_soru()
        else:
            msg_txt.value = "Joker kalmadi! Magazadan al"
            msg_txt.color = "#ffd32a"
            guncelle()

    def magaza(e):
        if d["dur"]:
            return
        zaten_pasif = not d["aktif"]
        d["dur"] = True
        m_txt = ft.Text(f"Mevcut Altin: {d['altin']} | Ekstra Can: +{d['jc']}", color="#ffd32a", weight=ft.FontWeight.BOLD)

        def al(t, f):
            if d["altin"] < f:
                m_txt.value = "Yetersiz altin!"
                m_txt.color = "#ff7675"
                page.update()
                return
            d["altin"] -= f
            if t == "d":
                d["jd"] += 1
                m_txt.value = "Zaman Dondurucu alindi!"
            elif t == "s":
                d["js"] += 1
                m_txt.value = "+10 Saniye alindi!"
            elif t == "c":
                d["jc"] += 1
                if d["can"] > 0:
                    d["can"] += 1
                m_txt.value = f"+1 Can! Baslangic: {3 + d['jc']}"
            m_txt.color = "#00b894"
            guncelle()

        def kapat(e=None):
            d["dur"] = False
            if zaten_pasif:
                d["aktif"] = False
            page.pop_dialog()

        dlg = ft.AlertDialog(
            bgcolor="#1e1e3f",
            title=ft.Text("Magaza", color="white"),
            content=ft.Column(
                [
                    m_txt,
                    ft.Button("Zaman Dondur (5sn) - 30 Altin", bgcolor="#0984e3", color="white", width=240, on_click=lambda _: al("d", 30)),
                    ft.Button("Ekstra Sure (+10sn) - 50 Altin", bgcolor="#6c5ce7", color="white", width=240, on_click=lambda _: al("s", 50)),
                    ft.Button("Kalici +1 Can - 60 Altin", bgcolor="#e94560", color="white", width=240, on_click=lambda _: al("c", 60)),
                ],
                tight=True,
            ),
            actions=[ft.TextButton("Oyuna Don", on_click=kapat)],
            on_dismiss=kapat,
        )
        page.show_dialog(dlg)

    def tus(t):
        if not d["aktif"] or d["can"] <= 0 or d["dur"]:
            return
        if t == "SIL":
            d["girdi"] = d["girdi"][:-1]
        elif t == "-":
            d["girdi"] = d["girdi"][1:] if d["girdi"].startswith("-") else "-" + d["girdi"]
        else:
            d["girdi"] += t
        guncelle()

    def kontrol(e=None):
        if not d["aktif"] or d["can"] <= 0 or d["dur"]:
            return
        try:
            cvp = int(d["girdi"])
        except ValueError:
            msg_txt.value = "Once bir sayi tusla!"
            msg_txt.color = "#ffd32a"
            guncelle()
            return
        if cvp == d["dc"]:
            d["kombo"] += 1
            kaz = 10 + (d["kombo"] - 1) * 2
            d["puan"] += kaz
            d["altin"] += 10
            kt = f" | {d['kombo']}x KOMBO!" if d["kombo"] > 1 else ""
            msg_txt.value = f"Harika! +{kaz} Puan | +10 Altin{kt}"
            msg_txt.color = "#00b894"
            yeni_soru()
        else:
            d["can"] -= 1
            d["kombo"] = 0
            if d["can"] == 0:
                bitti(f"Dogrusu {d['dc']} idi")
            else:
                msg_txt.value = f"Yanlis! Dogrusu {d['dc']} idi"
                msg_txt.color = "#ff7675"
                yeni_soru()

    def oyunu_baslat(e=None):
        d["puan"] = 0
        d["can"] = 3 + d["jc"]
        d["svy"] = 1
        d["kombo"] = 0
        oyna_btn.visible = False
        tekrar_btn.visible = False
        gonder_btn.visible = True
        msg_txt.value = f"Basladi! ({d['can']} Can) - Hizli Coz!"
        msg_txt.color = "#00b894"
        yeni_soru()

    p_btn = ft.Button("II", bgcolor="#636e72", color="white", width=40, on_click=duraklat_degis)
    d_btn = ft.Button("Dondur (1)", bgcolor="#0984e3", color="white", on_click=lambda _: joker("d"))
    s_btn = ft.Button("+10sn (0)", bgcolor="#6c5ce7", color="white", on_click=lambda _: joker("s"))
    a_btn = ft.Button("Atla", bgcolor="#e17055", color="white", on_click=lambda _: joker("a"))
    oyna_btn = ft.Button("OYNA", bgcolor="#0984e3", color="white", width=260, height=48, on_click=oyunu_baslat)
    gonder_btn = ft.Button("GONDER", bgcolor="#00b894", color="white", width=260, height=46, visible=False, on_click=kontrol)
    tekrar_btn = ft.Button("TEKRAR OYNA", bgcolor="#ff4757", color="white", width=260, height=46, visible=False, on_click=oyunu_baslat)

    s_renk = ["#c0392b", "#1f618d", "#1e8449", "#d68910"]
    satirlar = list()
    for r, s in enumerate([["7", "8", "9"], ["4", "5", "6"], ["1", "2", "3"], ["-", "0", "SIL"]]):
        btns = [
            ft.Button(
                t,
                bgcolor=("#ff4757" if t == "SIL" else ("#6c5ce7" if t == "-" else s_renk[r])),
                color="white",
                width=82,
                height=46,
                on_click=lambda _, x=t: tus(x),
            )
            for t in s
        ]
        satirlar.append(ft.Row(btns, alignment=ft.MainAxisAlignment.CENTER, spacing=8))

    ust_bar = ft.Container(
        content=ft.Row(
            [p_btn, ust_txt, altin_txt, ft.Button("Magaza", bgcolor="#ffd32a", color="#121225", on_click=magaza)],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor="#1e1e3f",
        padding=8,
        border_radius=10,
        width=320,
    )

    page.add(
        ft.Row(
            [
                ft.Column(
                    [
                        ft.Container(height=28),
                        ust_bar,
                        bar,
                        kart_dis,
                        ft.Row([d_btn, s_btn, a_btn], alignment=ft.MainAxisAlignment.CENTER, spacing=6),
                        msg_txt,
                        ft.Column(satirlar, spacing=6, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        oyna_btn,
                        gonder_btn,
                        tekrar_btn,
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=8,
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True,
        )
    )

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
                        d["can"] -= 1
                        d["kombo"] = 0
                        if d["can"] == 0:
                            bitti("SURE DOLDU!")
                        else:
                            msg_txt.value = f"SURE DOLDU! Dogrusu {d['dc']} idi"
                            msg_txt.color = "#ff7675"
                            yeni_soru()
                page.update()

    page.run_task(sayac)

ft.run(main)
