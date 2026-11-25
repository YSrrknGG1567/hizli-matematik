import flet as ft, random, asyncio, json, urllib.request, gc

FIREBASE_URL = "https://" + "hizli-matematik-10492-default-rtdb" + ".europe-west1.firebasedatabase.app"

async def main(page: ft.Page):
    page.title = "Hizli Matematik"
    page.bgcolor = "#121225"
    page.padding = 0

    uno = ("#e74c3c", "#2980b9", "#27ae60", "#f39c12")
    d = {
        "mod": "solo", "isim": "Oyuncu", "puan": 0, "can": 3, "svy": 1, "dc": 0,
        "kalan": 7.0, "max": 7.0, "donma": 0.0, "aktif": False, "dur": False,
        "altin": 50, "rekor": 0, "kombo": 0, "jd": 1, "js": 0, "ja": 1, "jc": 0,
        "girdi": "", "soru": "12 + 8", "simge": "+", "renk": "#e74c3c",
        "yerel_skorlar": list(), "online_ok": False,
        "dogru": 0, "yanlis": 0, "bos": 0, "top_sure": 0.0,
        "vs_sira": 1, "vs_atla": 3, "p1": dict(), "p2": dict(), "soru_sayac": 0
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

    menu_rekor_txt = ft.Text(f"EN YUKSEK SKORUN: {d['rekor']}", size=16, weight=ft.FontWeight.BOLD, color="#ffd32a")

    def mod_sec_ac(e=None):
        dlg = ft.AlertDialog(
            bgcolor="#1e1e3f",
            title=ft.Text("Oyun Modu Sec", color="white"),
            content=ft.Column(
                [
                    ft.Button("Tek Kisilik (Skor Tablosu)", bgcolor="#0984e3", color="white", width=240, on_click=lambda _: (page.pop_dialog(), isim_sor_ac("solo"))),
                    ft.Button("1v1 VS Modu (2 Kisi - 15sn)", bgcolor="#e17055", color="white", width=240, on_click=lambda _: (page.pop_dialog(), isim_sor_ac("vs"))),
                ],
                tight=True,
            ),
            actions=[ft.TextButton("Iptal", on_click=lambda _: page.pop_dialog())],
        )
        page.show_dialog(dlg)

    def isim_sor_ac(mod):
        d["mod"] = mod
        if mod == "solo":
            isim_input = ft.TextField(label="Name:", hint_text="Adini yaz (Max 20 karakter)", max_length=20, value="" if d["isim"] == "Oyuncu" else d["isim"], autofocus=True, color="white", border_color="#0984e3")
            uyari = ft.Text("", color="#ff7675", size=12)

            def onayla(ev=None):
                girilen = (isim_input.value or "").strip()[:20]
                if not girilen:
                    uyari.value = "Lutfen bir isim yaz!"
                    page.update()
                    return
                d["isim"] = girilen
                page.pop_dialog()
                ekran_degistir("oyun")
                oyunu_baslat()

            dlg = ft.AlertDialog(
                bgcolor="#1e1e3f",
                title=ft.Text("Oyuncu Adi", color="white"),
                content=ft.Column([isim_input, uyari], tight=True),
                actions=[
                    ft.TextButton("Iptal", on_click=lambda _: page.pop_dialog()),
                    ft.Button("Basla", bgcolor="#00b894", color="white", on_click=onayla),
                ],
            )
            page.show_dialog(dlg)
        else:
            ad1 = ft.TextField(label="1. Oyuncu Name:", max_length=20, autofocus=True, color="white", border_color="#0984e3")
            ad2 = ft.TextField(label="2. Oyuncu Name:", max_length=20, color="white", border_color="#e17055")
            uyari = ft.Text("", color="#ff7675", size=12)

            def vs_onayla(ev=None):
                i1 = (ad1.value or "").strip()[:20]
                i2 = (ad2.value or "").strip()[:20]
                if not i1 or not i2:
                    uyari.value = "Iki oyuncu adini da yaz!"
                    page.update()
                    return
                d["p1"] = {"isim": i1, "puan": 0, "dogru": 0, "yanlis": 0, "bos": 0, "ort": 99.0}
                d["p2"] = {"isim": i2, "puan": 0, "dogru": 0, "yanlis": 0, "bos": 0, "ort": 99.0}
                d["vs_sira"] = 1
                page.pop_dialog()
                ekran_degistir("oyun")
                oyunu_baslat()

            dlg = ft.AlertDialog(
                bgcolor="#1e1e3f",
                title=ft.Text("1v1 VS Oyunculari", color="white"),
                content=ft.Column([ad1, ad2, uyari], tight=True),
                actions=[
                    ft.TextButton("Iptal", on_click=lambda _: page.pop_dialog()),
                    ft.Button("Kapismayi Baslat", bgcolor="#00b894", color="white", on_click=vs_onayla),
                ],
            )
            page.show_dialog(dlg)

    def skor_tablosu_ac(e=None):
        kayitlar = skorlari_getir()
        satir_listesi = list()
        if not kayitlar:
            satir_listesi.append(ft.Text("Henuz kayitli skor yok. Ilk rekoru sen kir!", color="#a2a8d3"))
        else:
            for idx, item in enumerate(kayitlar, 1):
                renk = "#ffd32a" if idx == 1 else ("#dfe6e9" if idx == 2 else ("#e17055" if idx == 3 else "white"))
                satir_listesi.append(
                    ft.Row(
                        [
                            ft.Text(f"{idx}. {item['isim']}", color=renk, weight=ft.FontWeight.BOLD, size=14),
                            ft.Text(f"{item['skor']} P", color="#00b894", weight=ft.FontWeight.BOLD, size=14),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        width=250,
                    )
                )
        durum_yazi = "Online Bulut Bagli" if d["online_ok"] else "Baglanti Hatasi (Interneti Kontrol Et)"
        satir_listesi.append(ft.Text(durum_yazi, size=11, color="#00b894" if d["online_ok"] else "#ff7675"))

        dlg = ft.AlertDialog(
            bgcolor="#1e1e3f",
            title=ft.Text("Skor Tablosu (Top 10)", color="#ffd32a"),
            content=ft.Column(satir_listesi, tight=True, spacing=6),
            actions=[ft.TextButton("Kapat", on_click=lambda _: page.pop_dialog())],
        )
        page.show_dialog(dlg)
    vs_banner = ft.Container(content=ft.Text("", size=12, weight=ft.FontWeight.BOLD, color="white"), bgcolor="#e17055", padding=5, border_radius=8, visible=False)
    ust_txt = ft.Text("Can:3 P:0 S:1", size=11, weight=ft.FontWeight.BOLD, color="#ff6b81")
    altin_txt = ft.Text("Altin:50", size=11, weight=ft.FontWeight.BOLD, color="#ffd32a")
    bar = ft.ProgressBar(value=1.0, width=310, height=11, color="#00b894", bgcolor="#1e1e3f")
    kose1 = ft.Text("?", size=15, weight=ft.FontWeight.BOLD, color="white")
    kose2 = ft.Text("?", size=15, weight=ft.FontWeight.BOLD, color="white")
    soru_txt = ft.Text("HIZLI MAT", size=22, weight=ft.FontWeight.BOLD, color="#121225", text_align=ft.TextAlign.CENTER)
    cevap_txt = ft.Text("UNO", size=20, weight=ft.FontWeight.BOLD, color="#0f3460", text_align=ft.TextAlign.CENTER)

    kart_ic = ft.Container(
        content=ft.Column(
            [
                ft.Row([kose1], alignment=ft.MainAxisAlignment.START, width=215),
                ft.Container(
                    content=ft.Column([soru_txt, cevap_txt], horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER, spacing=2),
                    bgcolor="white", border_radius=36, width=175, height=82, alignment=ft.Alignment(0, 0),
                ),
                ft.Row([kose2], alignment=ft.MainAxisAlignment.END, width=215),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN, horizontal_alignment=ft.CrossAxisAlignment.CENTER, width=215, height=145,
        ),
        bgcolor="#e74c3c", border_radius=14, padding=10, width=235, height=165, alignment=ft.Alignment(0, 0),
    )
    kart_dis = ft.Container(content=kart_ic, bgcolor="white", border_radius=18, padding=6)
    msg_txt = ft.Text("Hazir!", size=13, weight=ft.FontWeight.BOLD, color="#ffd32a", text_align=ft.TextAlign.CENTER)
    karne_txt = ft.Text("", size=11, weight=ft.FontWeight.BOLD, color="white", text_align=ft.TextAlign.CENTER)
    karne_kutu = ft.Container(content=karne_txt, bgcolor="#1e1e3f", padding=8, border_radius=10, visible=False)

    def guncelle():
        ust_txt.value = f"Can:{d['can']} P:{d['puan']} S:{d['svy']}"
        altin_txt.value = f"Altin:{d['altin']}"
        menu_rekor_txt.value = f"EN YUKSEK SKORUN: {d['rekor']}"
        d_btn.content = f"Dondur ({d['jd']})"
        s_btn.content = f"+10sn ({d['js']})"
        a_btn.content = f"Atla ({d['vs_atla']})" if d["mod"] == "vs" else f"Atla ({d['ja']})"
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

    def geri_tikla(e=None):
        onceki_dur = d["dur"]
        d["dur"] = True

        def secim(kaydet_mi):
            if kaydet_mi and d["mod"] == "solo":
                if d["puan"] > d["rekor"]:
                    d["rekor"] = d["puan"]
                skoru_kaydet_bulut(d["isim"], d["puan"])
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
            dlg = ft.AlertDialog(
                bgcolor="#1e1e3f", title=ft.Text("VS'den Cik", color="white"),
                content=ft.Text("Mevcut kapisma iptal edilsin mi?", color="#dfe6e9"),
                actions=[ft.Button("Menuye Don", bgcolor="#ff4757", color="white", on_click=lambda _: secim(False)), ft.TextButton("Iptal", on_click=vazgec)],
            )
        else:
            dlg = ft.AlertDialog(
                bgcolor="#1e1e3f", title=ft.Text("Menuye Don", color="white"),
                content=ft.Text(f"{d['isim']} - Mevcut Puan: {d['puan']}\nSkorun kaydedilsin mi?", color="#dfe6e9"),
                actions=[
                    ft.Button("Skoru Kaydet", bgcolor="#00b894", color="white", on_click=lambda _: secim(True)),
                    ft.Button("Kaydetme", bgcolor="#ff4757", color="white", on_click=lambda _: secim(False)),
                    ft.TextButton("Iptal", on_click=vazgec),
                ],
            )
        page.show_dialog(dlg)

    def yeni_soru():
        d["aktif"] = True
        d["soru_sayac"] += 1
        if d["soru_sayac"] % 15 == 0:
            gc.collect()
        ys = 1 if d["puan"] < 50 else (2 if d["puan"] < 100 else 3)
        if ys > d["svy"]:
            d["svy"] = ys
        d["kalan"] = 15.0 if d["mod"] == "vs" else 7.0 + (d["svy"] - 1) * 3.0
        d["max"] = d["kalan"]
        d["donma"] = 0.0
        d["girdi"] = ""

        if d["svy"] == 1:
            isl = random.choice(("+", "-"))
            s1, s2 = random.randint(1, 10), random.randint(1, 10)
        elif d["svy"] == 2:
            isl = random.choice(("+", "-", "*"))
            if isl == "*":
                s1, s2 = random.randint(2, 9), random.randint(2, 9)
            else:
                s1, s2 = random.randint(10, 25), random.randint(10, 25)
        else:
            isl = random.choice(("+", "-", "*"))
            if isl == "*":
                s1, s2 = random.randint(11, 25), random.randint(11, 25)
            else:
                s1, s2 = random.randint(25, 60), random.randint(20, 50)

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
        try:
            page.pop_dialog()
        except Exception:
            pass
        d["aktif"] = False
        d["kombo"] = 0
        d["donma"] = 0.0
        kart_ic.bgcolor = "#e74c3c"
        soru_txt.value = "OYUN BITTI"
        cevap_txt.value = f"{d['puan']} P"
        kose1.value = "X"
        kose2.value = "X"
        if d["mod"] == "vs":
            ort = (d["top_sure"] / d["dogru"]) if d["dogru"] > 0 else 99.0
            if d["vs_sira"] == 1:
                d["p1"] = {"isim": d["p1"]["isim"], "puan": d["puan"], "dogru": d["dogru"], "yanlis": d["yanlis"], "bos": d["bos"], "ort": ort}
                d["vs_sira"] = 2
                guncelle()
                ort_yazi = f"{ort:.1f}sn" if ort < 90 else "-"
                dlg = ft.AlertDialog(
                    bgcolor="#1e1e3f", title=ft.Text(f"{d['p1']['isim']} Turunu Bitirdi!", color="#ffd32a"),
                    content=ft.Text(f"Puan: {d['p1']['puan']} P (Ort. Hiz: {ort_yazi})\nDogru: {d['p1']['dogru']} | Yanlis: {d['p1']['yanlis']} | Bos: {d['p1']['bos']}\nSira {d['p2']['isim']} oyuncusunda!", color="white"),
                    actions=[ft.Button(f"{d['p2']['isim']} Baslasin", bgcolor="#00b894", color="white", on_click=lambda _: (page.pop_dialog(), oyunu_baslat()))],
                )
                page.show_dialog(dlg)
                return
            else:
                d["p2"] = {"isim": d["p2"]["isim"], "puan": d["puan"], "dogru": d["dogru"], "yanlis": d["yanlis"], "bos": d["bos"], "ort": ort}
                hiz_kutusu = ft.Container(visible=False)
                if d["p1"]["ort"] < 90 and d["p2"]["ort"] < 90 and abs(d["p1"]["ort"] - d["p2"]["ort"]) > 0.1:
                    hizli = d["p1"] if d["p1"]["ort"] < d["p2"]["ort"] else d["p2"]
                    yavas = d["p2"] if d["p1"]["ort"] < d["p2"]["ort"] else d["p1"]
                    hediye_sec = random.choice(("d", "s", "a"))
                    if hediye_sec == "d":
                        d["jd"] += 1
                        hediye_ad = "Zaman Dondurucu (5sn)"
                    elif hediye_sec == "s":
                        d["js"] += 1
                        hediye_ad = "+10 Saniye Jokeri"
                    else:
                        d["ja"] += 1
                        hediye_ad = "Soru Atla Jokeri"
                    yavas["puan"] = max(0, yavas["puan"] - 10)
                    hiz_kutusu = ft.Container(
                        content=ft.Text(f"En Hizli: {hizli['isim']} ({hizli['ort']:.1f}sn) -> Bedava {hediye_ad}!\nEn Yavas: {yavas['isim']} ({yavas['ort']:.1f}sn) -> -10 Skor", size=11, color="#00cec9", text_align=ft.TextAlign.CENTER),
                        bgcolor="#121225", padding=6, border_radius=8,
                    )
                if d["p1"]["puan"] != d["p2"]["puan"]:
                    page.run_task(konfeti_patlat)
                    kaz = d["p1"] if d["p1"]["puan"] > d["p2"]["puan"] else d["p2"]
                    kay = d["p2"] if d["p1"]["puan"] > d["p2"]["puan"] else d["p1"]
                    kaz_yeni = kaz["puan"] + 25
                    kay_yeni = max(0, kay["puan"] - 30)
                    d["altin"] += 50
                    if kaz_yeni > d["rekor"]:
                        d["rekor"] = kaz_yeni
                    skoru_kaydet_bulut(kaz["isim"], kaz_yeni)
                    sonuc_icerik = ft.Column(
                        [
                            hiz_kutusu,
                            ft.Container(
                                content=ft.Column([
                                    ft.Text("KAZANDIN!", size=20, weight=ft.FontWeight.BOLD, color="#ffd32a"),
                                    ft.Text(f"{kaz['isim']}", size=15, weight=ft.FontWeight.BOLD, color="white"),
                                    ft.Text(f"{kaz['puan']} + 25 Skor = {kaz_yeni} P | +50 Altin", size=12, color="#00b894", weight=ft.FontWeight.BOLD),
                                    ft.Text(f"Dogru: {kaz['dogru']} | Yanlis: {kaz['yanlis']} | Bos: {kaz['bos']}", size=11, color="#dfe6e9"),
                                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
                                bgcolor="#121225", padding=10, border_radius=10,
                            ),
                            ft.Container(
                                content=ft.Column([
                                    ft.Text("KAYBETTIN BIR DAHAKI SEFERE", size=12, weight=ft.FontWeight.BOLD, color="#ff7675"),
                                    ft.Text(f"{kay['isim']}", size=15, weight=ft.FontWeight.BOLD, color="white"),
                                    ft.Text(f"{kay['puan']} - 30 Skor = {kay_yeni} P | 0 Altin", size=12, color="#ff7675", weight=ft.FontWeight.BOLD),
                                    ft.Text(f"Dogru: {kay['dogru']} | Yanlis: {kay['yanlis']} | Bos: {kay['bos']}", size=11, color="#dfe6e9"),
                                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
                                bgcolor="#121225", padding=10, border_radius=10,
                            ),
                        ],
                        tight=True, spacing=6,
                    )
                else:
                    sonuc_icerik = ft.Column([hiz_kutusu, ft.Text(f"BERABERE!\n{d['p1']['isim']}: {d['p1']['puan']} P | {d['p2']['isim']}: {d['p2']['puan']} P", color="#ffd32a", weight=ft.FontWeight.BOLD)], tight=True)
                dlg = ft.AlertDialog(bgcolor="#1e1e3f", title=ft.Text("VS Sonucu", color="white"), content=sonuc_icerik, actions=[ft.Button("Tamam", bgcolor="#0984e3", color="white", on_click=lambda _: page.pop_dialog())])
                page.show_dialog(dlg)
                msg_txt.value = "VS Kapismasi Tamamlandi!"
                msg_txt.color = "#ffd32a"
                d["vs_sira"] = 1
        else:
            kayip_sayisi = d["yanlis"] + d["bos"]
            ceza = 10 if kayip_sayisi > d["dogru"] else 0
            final_skor = max(0, d["puan"] - ceza)
            if final_skor > d["rekor"]:
                d["rekor"] = final_skor
            skoru_kaydet_bulut(d["isim"], final_skor)
            msg_txt.value = f"{sebep} | Rekor: {d['rekor']}"
            msg_txt.color = "#ff7675"
            ceza_ek = f"\nKayip Soru Fazla ({kayip_sayisi}>{d['dogru']}): -10 Ceza -> Net: {final_skor} P" if ceza > 0 else ""
            karne_txt.value = f"Kazanilan: {d['puan']} P | Dogru: {d['dogru']} | Yanlis: {d['yanlis']} | Bos: {d['bos']}{ceza_ek}"
            karne_kutu.visible = True
        oyna_btn.visible = False
        gonder_btn.visible = False
        tekrar_btn.visible = True
        gc.collect()
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
            if d["mod"] == "vs":
                if d["vs_atla"] <= 0:
                    msg_txt.value = "VS Modunda Atla hakkin bitti!"
                    msg_txt.color = "#ff7675"
                    guncelle()
                    return
                d["vs_atla"] -= 1
            else:
                if d["ja"] <= 0:
                    msg_txt.value = "Atla hakkin kalmadi! Magazadan al (70 Altin)"
                    msg_txt.color = "#ffd32a"
                    guncelle()
                    return
                d["ja"] -= 1
            d["bos"] += 1
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
        m_txt = ft.Text(f"Mevcut Altin: {d['altin']} | Ekstra Can: +{d['jc']}", color="#ffd32a", weight=ft.FontWeight.BOLD)
        uyari_txt = ft.Text("Dikkat: Magazada sure akmaya devam eder!", size=11, color="#ff7675", visible=d["aktif"])

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
            elif t == "a":
                d["ja"] += 1
                m_txt.value = "Soru Atla jokeri alindi!"
            elif t == "c":
                d["jc"] += 1
                if d["can"] > 0:
                    d["can"] += 1
                m_txt.value = f"+1 Can! Baslangic: {3 + d['jc']}"
            m_txt.color = "#00b894"
            guncelle()

        dlg = ft.AlertDialog(
            bgcolor="#1e1e3f", title=ft.Text("Magaza", color="white"),
            content=ft.Column([
                m_txt, uyari_txt,
                ft.Button("Zaman Dondur (5sn) - 30 Altin", bgcolor="#0984e3", color="white", width=240, on_click=lambda _: al("d", 30)),
                ft.Button("Ekstra Sure (+10sn) - 50 Altin", bgcolor="#6c5ce7", color="white", width=240, on_click=lambda _: al("s", 50)),
                ft.Button("Kalici +1 Can - 60 Altin", bgcolor="#e94560", color="white", width=240, on_click=lambda _: al("c", 60)),
                ft.Button("Soru Atla (1x) - 70 Altin", bgcolor="#e17055", color="white", width=240, on_click=lambda _: al("a", 70)),
            ], tight=True),
            actions=[ft.TextButton("Kapat", on_click=lambda _: page.pop_dialog())],
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
            d["top_sure"] += (d["max"] - d["kalan"])
            d["dogru"] += 1
            d["kombo"] += 1
            kaz = 10 + (d["kombo"] - 1) * 2
            d["puan"] += kaz
            if d["mod"] == "solo":
                d["altin"] += 10
            kt = f" | {d['kombo']}x KOMBO!" if d["kombo"] > 1 else ""
            msg_txt.value = f"Harika! +{kaz} Puan{kt}"
            msg_txt.color = "#00b894"
            yeni_soru()
        else:
            d["yanlis"] += 1
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
        d["svy"] = 1
        d["kombo"] = 0
        d["dur"] = False
        d["dogru"] = 0
        d["yanlis"] = 0
        d["bos"] = 0
        d["top_sure"] = 0.0
        karne_kutu.visible = False
        p_btn.content = "II"
        p_btn.bgcolor = "#636e72"
        oyna_btn.visible = False
        tekrar_btn.visible = False
        gonder_btn.visible = True
        if d["mod"] == "vs":
            d["can"] = 3
            d["vs_atla"] = 3
            d_btn.visible = False
            s_btn.visible = False
            mag_btn.visible = False
            aktif_ad = d["p1"]["isim"] if d["vs_sira"] == 1 else d["p2"]["isim"]
            vs_banner.content.value = f"1v1 VS (15sn) | Sira: {aktif_ad} ({d['vs_sira']}/2)"
            vs_banner.visible = True
            msg_txt.value = f"{aktif_ad} Basladi! (3 Can | 3 Atla)"
        else:
            d["can"] = 3 + d["jc"]
            d_btn.visible = True
            s_btn.visible = True
            mag_btn.visible = True
            vs_banner.visible = False
            msg_txt.value = f"Iyi sanslar {d['isim']}! ({d['can']} Can)"
        msg_txt.color = "#00b894"
        yeni_soru()

    geri_btn = ft.Button("<-", bgcolor="#ff4757", color="white", width=44, on_click=geri_tikla)
    p_btn = ft.Button("II", bgcolor="#636e72", color="white", width=40, on_click=duraklat_degis)
    mag_btn = ft.Button("Magaza", bgcolor="#ffd32a", color="#121225", width=82, on_click=magaza)
    d_btn = ft.Button("Dondur (1)", bgcolor="#0984e3", color="white", on_click=lambda _: joker("d"))
    s_btn = ft.Button("+10sn (0)", bgcolor="#6c5ce7", color="white", on_click=lambda _: joker("s"))
    a_btn = ft.Button("Atla (1)", bgcolor="#e17055", color="white", on_click=lambda _: joker("a"))
    oyna_btn = ft.Button("OYNA", bgcolor="#0984e3", color="white", width=260, height=48, on_click=oyunu_baslat)
    gonder_btn = ft.Button("GONDER", bgcolor="#00b894", color="white", width=260, height=46, visible=False, on_click=kontrol)
    tekrar_btn = ft.Button("TEKRAR OYNA", bgcolor="#ff4757", color="white", width=260, height=46, visible=False, on_click=oyunu_baslat)

    s_renk = ("#c0392b", "#1f618d", "#1e8449", "#d68910")
    satirlar = list()
    for r, s in enumerate((("7", "8", "9"), ("4", "5", "6"), ("1", "2", "3"), ("-", "0", "SIL"))):
        btns = [ft.Button(t, bgcolor=("#ff4757" if t == "SIL" else ("#6c5ce7" if t == "-" else s_renk[r])), color="white", width=82, height=46, on_click=lambda _, x=t: tus(x)) for t in s]
        satirlar.append(ft.Row(btns, alignment=ft.MainAxisAlignment.CENTER, spacing=8))

    ust_bar = ft.Container(content=ft.Row([geri_btn, p_btn, ust_txt, altin_txt, mag_btn], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER, spacing=2), bgcolor="#1e1e3f", padding=6, border_radius=10, width=340)

    menu_ekrani = ft.Column([
        ft.Container(height=40),
        ft.Container(content=menu_rekor_txt, bgcolor="#1e1e3f", padding=14, border_radius=12),
        ft.Container(height=45),
        ft.Text("HIZLI MATEMATIK", size=28, weight=ft.FontWeight.BOLD, color="white"),
        ft.Text("UNO Kartli Zeka Yarisi", size=13, color="#a2a8d3"),
        ft.Container(height=25),
        ft.Button("OYNA", bgcolor="#0984e3", color="white", width=240, height=56, on_click=mod_sec_ac),
        ft.Container(height=10),
        ft.Button("MAGAZA", bgcolor="#ffd32a", color="#121225", width=240, height=48, on_click=magaza),
        ft.Container(height=35),
        ft.Button("SKOR TABLOSU", bgcolor="#6c5ce7", color="white", width=240, height=48, on_click=skor_tablosu_ac),
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.SPACE_BETWEEN, visible=True)

    oyun_ekrani = ft.Column([
        ft.Container(height=20),
        vs_banner,
        ust_bar,
        bar,
        kart_dis,
        ft.Row([d_btn, s_btn, a_btn], alignment=ft.MainAxisAlignment.CENTER, spacing=6),
        msg_txt,
        karne_kutu,
        ft.Column(satirlar, spacing=6, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        oyna_btn,
        gonder_btn,
        tekrar_btn,
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER, spacing=6, visible=False)

    def ekran_degistir(hedef):
        menu_ekrani.visible = (hedef == "menu")
        oyun_ekrani.visible = (hedef == "oyun")
        page.update()

    ana_icerik = ft.Row([ft.Column([menu_ekrani, oyun_ekrani], horizontal_alignment=ft.CrossAxisAlignment.CENTER)], alignment=ft.MainAxisAlignment.CENTER, expand=True)
    page.add(ft.Stack([ana_icerik, konfeti_katman], expand=True))

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
                            bitti("SURE DOLDU!")
                        else:
                            msg_txt.value = f"SURE DOLDU! Dogrusu {d['dc']} idi"
                            msg_txt.color = "#ff7675"
                            yeni_soru()
                page.update()

    page.run_task(sayac)

ft.run(main)
