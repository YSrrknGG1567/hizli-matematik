import flet as ft, random, asyncio, json, urllib.request, gc

FIREBASE_URL = "https://" + "hizli-matematik-10492-default-rtdb" + ".europe-west1.firebasedatabase.app"

async def main(page: ft.Page):
    page.title = "Hizli Matematik"
    page.bgcolor = "#121225"
    page.padding = 0

    uno = ("#e74c3c", "#2980b9", "#27ae60", "#f39c12")
    sik_renk = ("#c0392b", "#1f618d", "#1e8449", "#d68910")
    harfler = ("A", "B", "C", "D")

    prof = {"isim": "", "kademe": "Ortaokul", "sinif": "6. Sinif", "kayitli": False}
    try:
        kayitli_prof = await page.client_storage.get_async("hm_prof")
        if isinstance(kayitli_prof, dict) and kayitli_prof.get("kayitli"):
            prof.update(kayitli_prof)
    except Exception:
        pass

    d = {
        "mod": "solo", "zorluk": "Orta", "ders": "Tam Sayilar & Islem",
        "puan": 0, "can": 3, "svy": 1, "dc": 0, "kalan": 12.0, "max": 12.0,
        "donma": 0.0, "aktif": False, "dur": False, "altin": 50, "rekor": 0,
        "kombo": 0, "jd": 1, "js": 0, "ja": 1, "je": 1, "jc": 0, "cift_puan": 0,
        "soru": "12 + 8 = ?", "simge": "+", "renk": "#e74c3c",
        "yerel_skorlar": list(), "online_ok": False,
        "dogru": 0, "yanlis": 0, "bos": 0, "top_sure": 0.0,
        "vs_sira": 1, "vs_atla": 3, "p1": dict(), "p2": dict(),
        "soru_sayac": 0, "siklar": list()
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
    prof_bilgi_txt = ft.Text(
        f"{prof['isim']} | {prof['kademe']} - {prof['sinif']}" if prof["kayitli"] else "",
        size=12, color="#00cec9", weight=ft.FontWeight.BOLD, visible=prof["kayitli"]
    )
    prof_degis_btn = ft.Button("Profili Degistir", bgcolor="#636e72", color="white", width=240, visible=prof["kayitli"], on_click=lambda _: profil_ac())

    def oyna_tikla(e=None):
        if prof["kayitli"]:
            mod_ve_ders_ac()
        else:
            profil_ac()

    def profil_ac():
        secili_kad = [prof["kademe"] or "Ortaokul"]
        secili_sin = [prof["sinif"] or "6. Sinif"]
        sinif_kolon = ft.Column(spacing=4, tight=True)
        uyari_txt = ft.Text("", color="#ff7675", size=12)
        ad_input = ft.TextField(label="Name:", hint_text="Adini yaz (Max 20 karakter)", max_length=20, value=prof["isim"], autofocus=True, color="white", border_color="#0984e3")

        sinif_haritasi = {
            "Ilkokul": ("1. Sinif", "2. Sinif", "3. Sinif", "4. Sinif"),
            "Ortaokul": ("5. Sinif", "6. Sinif", "7. Sinif", "8. Sinif"),
            "Lise": ("9. Sinif", "10. Sinif", "11. Sinif", "12. Sinif"),
            "Universite": ("1. Sinif (Uni)", "2. Sinif (Uni)", "3. Sinif (Uni)", "4. Sinif (Uni)"),
        }

        def sinif_yenile():
            sinif_kolon.controls.clear()
            liste = sinif_haritasi[secili_kad[0]]
            if secili_sin[0] not in liste:
                secili_sin[0] = liste[0]
            for s in liste:
                aktif_mi = (secili_sin[0] == s)
                sinif_kolon.controls.append(
                    ft.Button(
                        s,
                        bgcolor="#0984e3" if aktif_mi else "#121225",
                        color="white",
                        width=240,
                        on_click=lambda _, x=s: (secili_sin.__setitem__(0, x), sinif_yenile(), page.update())
                    )
                )

        def kad_sec(k):
            secili_kad[0] = k
            sinif_yenile()
            page.update()

        kad_satir1 = ft.Row([
            ft.Button("Ilkokul", bgcolor="#00b894", color="white", width=116, on_click=lambda _: kad_sec("Ilkokul")),
            ft.Button("Ortaokul", bgcolor="#0984e3", color="white", width=116, on_click=lambda _: kad_sec("Ortaokul")),
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=6)
        kad_satir2 = ft.Row([
            ft.Button("Lise", bgcolor="#e17055", color="white", width=116, on_click=lambda _: kad_sec("Lise")),
            ft.Button("Universite", bgcolor="#6c5ce7", color="white", width=116, on_click=lambda _: kad_sec("Universite")),
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=6)

        async def kaydet_tikla(ev=None):
            ad = (ad_input.value or "").strip()[:20]
            if not ad:
                uyari_txt.value = "Lutfen adini yaz!"
                page.update()
                return
            prof.update({"isim": ad, "kademe": secili_kad[0], "sinif": secili_sin[0], "kayitli": True})
            try:
                await page.client_storage.set_async("hm_prof", prof)
            except Exception:
                pass
            prof_bilgi_txt.value = f"{prof['isim']} | {prof['kademe']} - {prof['sinif']}"
            prof_bilgi_txt.visible = True
            prof_degis_btn.visible = True
            page.pop_dialog()
            mod_ve_ders_ac()

        sinif_yenile()
        dlg = ft.AlertDialog(
            bgcolor="#1e1e3f",
            title=ft.Text("Oyuncu Profili", color="white"),
            content=ft.Column([ad_input, kad_satir1, kad_satir2, sinif_kolon, uyari_txt], tight=True, spacing=6),
            actions=[
                ft.TextButton("Iptal", on_click=lambda _: page.pop_dialog()),
                ft.Button("KAYDET", bgcolor="#ffd32a", color="#121225", on_click=kaydet_tikla),
            ],
        )
        page.show_dialog(dlg)

    def ders_listesi_getir():
        k = prof["kademe"]
        if k == "Ilkokul":
            return (("Toplama & Cikarma", "#e74c3c"), ("Carpim Tablosu", "#2980b9"), ("Sayi Oruntuleri", "#27ae60"), ("Gunluk Problemler", "#f39c12"))
        elif k == "Ortaokul":
            return (("Tam Sayilar & Islem", "#e74c3c"), ("Denklem & Cebir", "#2980b9"), ("Oran & Yuzde", "#27ae60"), ("Sayisal Mantik", "#f39c12"))
        elif k == "Lise":
            return (("Uslu & Koklu Sayilar", "#e74c3c"), ("Fonksiyon & Polinom", "#2980b9"), ("Permutasyon & Olasilik", "#27ae60"), ("TYT / AYT Mantik", "#f39c12"))
        return (("Lineer Cebir & Matris", "#e74c3c"), ("Limit & Turev Temeli", "#2980b9"), ("Istatistik & Olasilik", "#27ae60"), ("ALES / Ileri Mantik", "#f39c12"))

    def mod_ve_ders_ac():
        dersler = ders_listesi_getir()
        if not any(x[0] == d["ders"] for x in dersler):
            d["ders"] = dersler[0][0]

        durum_txt = ft.Text(f"Mod: {d['zorluk']} | Ders: {d['ders']}", size=11, color="#ffd32a", weight=ft.FontWeight.BOLD)

        def zor_sec(z):
            d["zorluk"] = z
            durum_txt.value = f"Mod: {d['zorluk']} | Ders: {d['ders']}"
            page.update()

        def ders_sec(ad):
            d["ders"] = ad
            durum_txt.value = f"Mod: {d['zorluk']} | Ders: {d['ders']}"
            page.update()

        zor_row1 = ft.Row([
            ft.Button("Kolay", bgcolor="#00b894", color="white", width=116, on_click=lambda _: zor_sec("Kolay")),
            ft.Button("Orta", bgcolor="#0984e3", color="white", width=116, on_click=lambda _: zor_sec("Orta")),
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=6)
        zor_row2 = ft.Row([
            ft.Button("Zor", bgcolor="#e17055", color="white", width=116, on_click=lambda _: zor_sec("Zor")),
            ft.Button("Cok Zor", bgcolor="#d63031", color="white", width=116, on_click=lambda _: zor_sec("Cok Zor")),
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=6)

        kat_row1 = ft.Row([
            ft.Container(content=ft.Text(dersler[0][0], size=11, weight=ft.FontWeight.BOLD, color="white", text_align=ft.TextAlign.CENTER), bgcolor=dersler[0][1], width=116, height=54, border_radius=0, alignment=ft.Alignment(0, 0), padding=4, on_click=lambda _: ders_sec(dersler[0][0])),
            ft.Container(content=ft.Text(dersler[1][0], size=11, weight=ft.FontWeight.BOLD, color="white", text_align=ft.TextAlign.CENTER), bgcolor=dersler[1][1], width=116, height=54, border_radius=0, alignment=ft.Alignment(0, 0), padding=4, on_click=lambda _: ders_sec(dersler[1][0])),
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=6)
        kat_row2 = ft.Row([
            ft.Container(content=ft.Text(dersler[2][0], size=11, weight=ft.FontWeight.BOLD, color="white", text_align=ft.TextAlign.CENTER), bgcolor=dersler[2][1], width=116, height=54, border_radius=0, alignment=ft.Alignment(0, 0), padding=4, on_click=lambda _: ders_sec(dersler[2][0])),
            ft.Container(content=ft.Text(dersler[3][0], size=11, weight=ft.FontWeight.BOLD, color="white", text_align=ft.TextAlign.CENTER), bgcolor=dersler[3][1], width=116, height=54, border_radius=0, alignment=ft.Alignment(0, 0), padding=4, on_click=lambda _: ders_sec(dersler[3][0])),
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=6)

        dlg = ft.AlertDialog(
            bgcolor="#1e1e3f",
            title=ft.Text(f"Modlar & Dersler ({prof['sinif']})", size=15, color="white"),
            content=ft.Column([
                durum_txt,
                ft.Text("MODLAR:", size=11, color="#a2a8d3"),
                zor_row1, zor_row2,
                ft.Text("DERS KATEGORISI:", size=11, color="#a2a8d3"),
                kat_row1, kat_row2,
                ft.Row([
                    ft.Button("Tek Kisilik", bgcolor="#0984e3", color="white", width=116, on_click=lambda _: (page.pop_dialog(), oyun_basla_mod("solo"))),
                    ft.Button("1v1 VS (15sn)", bgcolor="#e17055", color="white", width=116, on_click=lambda _: (page.pop_dialog(), oyun_basla_mod("vs"))),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=6),
            ], tight=True, spacing=5),
            actions=[ft.TextButton("Iptal", on_click=lambda _: page.pop_dialog())],
        )
        page.show_dialog(dlg)
    def oyun_basla_mod(mod):
        d["mod"] = mod
        if mod == "solo":
            ekran_degistir("oyun")
            oyunu_baslat()
        else:
            ad1 = ft.TextField(label="1. Oyuncu Name:", max_length=20, value=prof["isim"], color="white", border_color="#0984e3")
            ad2 = ft.TextField(label="2. Oyuncu Name:", max_length=20, autofocus=True, color="white", border_color="#e17055")
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
    kose1 = ft.Text("?", size=14, weight=ft.FontWeight.BOLD, color="white")
    ders_etiket = ft.Text("Matematik", size=10, weight=ft.FontWeight.BOLD, color="white")
    kose2 = ft.Text("?", size=14, weight=ft.FontWeight.BOLD, color="white")
    soru_txt = ft.Text("HIZLI MAT", size=18, weight=ft.FontWeight.BOLD, color="#121225", text_align=ft.TextAlign.CENTER)

    kart_ic = ft.Container(
        content=ft.Column(
            [
                ft.Row([kose1, ders_etiket], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, width=240),
                ft.Container(
                    content=soru_txt,
                    bgcolor="white", border_radius=0, width=236, height=106, padding=8, alignment=ft.Alignment(0, 0),
                ),
                ft.Row([kose2], alignment=ft.MainAxisAlignment.END, width=240),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN, horizontal_alignment=ft.CrossAxisAlignment.CENTER, width=240, height=160,
        ),
        bgcolor="#e74c3c", border_radius=12, padding=8, width=258, height=176, alignment=ft.Alignment(0, 0),
    )
    kart_dis = ft.Container(content=kart_ic, bgcolor="white", border_radius=16, padding=6)
    msg_txt = ft.Text("Hazir!", size=12, weight=ft.FontWeight.BOLD, color="#ffd32a", text_align=ft.TextAlign.CENTER)
    karne_txt = ft.Text("", size=11, weight=ft.FontWeight.BOLD, color="white", text_align=ft.TextAlign.CENTER)
    karne_kutu = ft.Container(content=karne_txt, bgcolor="#1e1e3f", padding=8, border_radius=10, visible=False)

    sik_butonlar = list()
    for i in range(4):
        sik_butonlar.append(
            ft.Button(
                f"{harfler[i]}) ?",
                bgcolor=sik_renk[i],
                color="white",
                width=155,
                height=52,
                on_click=lambda _, idx=i: sik_sec(idx)
            )
        )
    sik_kolon = ft.Column(
        [
            ft.Row([sik_butonlar[0], sik_butonlar[1]], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
            ft.Row([sik_butonlar[2], sik_butonlar[3]], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
        ],
        spacing=8,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    def guncelle():
        ust_txt.value = f"Can:{d['can']} P:{d['puan']} S:{d['svy']}"
        altin_txt.value = f"Altin:{d['altin']}"
        menu_rekor_txt.value = f"EN YUKSEK SKORUN: {d['rekor']}"
        d_btn.content = f"Dondur ({d['jd']})"
        s_btn.content = f"+10sn ({d['js']})"
        e_btn.content = f"50/50 ({d['je']})"
        a_btn.content = f"Atla ({d['vs_atla']})" if d["mod"] == "vs" else f"Atla ({d['ja']})"
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
                skoru_kaydet_bulut(prof["isim"] or "Oyuncu", d["puan"])
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
                content=ft.Text(f"{prof['isim']} - Mevcut Puan: {d['puan']}\nSkorun kaydedilsin mi?", color="#dfe6e9"),
                actions=[
                    ft.Button("Skoru Kaydet", bgcolor="#00b894", color="white", on_click=lambda _: secim(True)),
                    ft.Button("Kaydetme", bgcolor="#ff4757", color="white", on_click=lambda _: secim(False)),
                    ft.TextButton("Iptal", on_click=vazgec),
                ],
            )
        page.show_dialog(dlg)

    def soru_uret():
        z_taban = {"Kolay": 1, "Orta": 2, "Zor": 3, "Cok Zor": 4}.get(d["zorluk"], 2)
        k_taban = {"Ilkokul": 0, "Ortaokul": 1, "Lise": 2, "Universite": 3}.get(prof["kademe"], 1)
        guc = z_taban + k_taban + (d["svy"] - 1)
        simge = "M"

        if guc <= 2:
            s1, s2 = random.randint(4, 15), random.randint(3, 13)
            if random.random() < 0.5:
                cvp, metin, simge = s1 + s2, f"{s1} + {s2} = ?", "+"
            else:
                cvp, metin, simge = s1 * s2, f"{s1} x {s2} = ?", "x"
        elif guc <= 4:
            tip = random.randint(0, 2)
            if tip == 0:
                s1, s2 = random.randint(14, 38), random.randint(12, 29)
                cvp, metin, simge = s1 * s2, f"{s1} x {s2} = ?", "x"
            elif tip == 1:
                a, x, b = random.randint(3, 8), random.randint(4, 12), random.randint(5, 16)
                cvp, metin = x, f"{a}x + {b} = {a * x + b} ise x kactir?"
            else:
                a, b = random.randint(2, 6), random.randint(3, 8)
                cvp, metin = a * 5 + b, f"Bir sepette {a * 10} ceviz var. Yarisinin {b} fazlasi kactir?"
        elif guc <= 6:
            tip = random.randint(0, 3)
            if tip == 0:
                s1, s2 = random.randint(28, 72), random.randint(24, 78)
                cvp, metin, simge = s1 * s2, f"{s1} x {s2} isleminin sonucu kactir?", "x"
            elif tip == 1:
                a, b = random.randint(5, 12), random.randint(3, 8)
                cvp, metin = a * b, f"x + y = {a + b} ve x - y = {a - b} ise x . y carpimi kactir?"
            elif tip == 2:
                n = random.randint(4, 10)
                cvp, metin = 2 * n + 3, f"Ardisik 3 tek sayinin toplami {3 * (2 * n + 1)} ise en buyuk sayi kactir?"
            else:
                h, t = random.randint(6, 10) * 10, random.randint(2, 5)
                cvp, metin = h * t * 2, f"Saatte {h} km hizla {t} saatte yolun yarisini giden aracin tum yolu kac km?"
        else:
            tip = random.randint(0, 3)
            if tip == 0:
                s1, s2 = random.randint(45, 94), random.randint(52, 96)
                cvp, metin, simge = s1 * s2, f"{s1} x {s2} carpiminin sonucu kactir?", "x"
            elif tip == 1:
                k = random.randint(3, 8)
                cvp, metin = k * k + 1, f"f(x) = x^2 + 1 fonksiyonunda f({k}) degeri kactir?"
            elif tip == 2:
                a = random.randint(4, 8)
                cvp, metin = (a * (a - 1)) // 2, f"{a} kisilik grupta herkes birbiriyle 1 kez tokalasirsa kac tokalasma olur?"
            else:
                b = random.randint(3, 7)
                cvp, metin = b * 32 - 1, f"{b - 1}, {b * 2 - 1}, {b * 4 - 1}, {b * 8 - 1}, ? Oruntude siradaki sayi kactir?"

        sik_set = {cvp}
        while len(sik_set) < 4:
            fark = random.randint(1, 4) * (10 if abs(cvp) > 100 else 2)
            aday = cvp + (fark if random.random() < 0.5 else -fark)
            if aday != cvp and aday >= 0:
                sik_set.add(aday)
        siklar = list(sik_set)
        random.shuffle(siklar)
        return metin, cvp, simge, siklar

    def yeni_soru():
        d["aktif"] = True
        d["soru_sayac"] += 1
        if d["soru_sayac"] % 15 == 0:
            gc.collect()
        ys = 1 if d["puan"] < 40 else (2 if d["puan"] < 90 else (3 if d["puan"] < 150 else 4))
        if ys > d["svy"]:
            d["svy"] = ys
        d["kalan"] = 15.0 if d["mod"] == "vs" else 12.0
        d["max"] = d["kalan"]
        d["donma"] = 0.0

        metin, cvp, simge, siklar = soru_uret()
        d["dc"], d["simge"], d["soru"], d["siklar"] = cvp, simge, metin, siklar
        d["renk"] = random.choice(uno)

        soru_txt.size = 13 if len(metin) > 55 else (15 if len(metin) > 30 else 20)
        kart_ic.bgcolor = d["renk"]
        ders_etiket.value = f"{d['ders']} | {d['zorluk']}"
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
        secilen = d["siklar"][idx]
        if secilen == d["dc"]:
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
            msg_txt.value = f"Dogru! +{kaz} Puan" + (" (2X BONUS!)" if carpan == 2 else "")
            msg_txt.color = "#00b894"
            yeni_soru()
        else:
            d["yanlis"] += 1
            d["can"] -= 1
            d["kombo"] = 0
            if d["can"] == 0:
                bitti(f"Dogru sik: {d['dc']}")
            else:
                msg_txt.value = f"Yanlis! Dogrusu: {d['dc']}"
                msg_txt.color = "#ff7675"
                yeni_soru()

    def bitti(sebep):
        try:
            page.pop_dialog()
        except Exception:
            pass
        d["aktif"] = False
        d["kombo"] = 0
        d["donma"] = 0.0
        sik_kolon.visible = False
        kart_ic.bgcolor = "#e74c3c"
        soru_txt.size = 19
        soru_txt.value = f"OYUN BITTI\n{d['puan']} PUAN"
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
                    hediye_sec = random.choice(("d", "s", "e", "a"))
                    if hediye_sec == "d":
                        d["jd"] += 1
                        hediye_ad = "Zaman Dondurucu (5sn)"
                    elif hediye_sec == "s":
                        d["js"] += 1
                        hediye_ad = "+10 Saniye Jokeri"
                    elif hediye_sec == "e":
                        d["je"] += 1
                        hediye_ad = "50/50 Sik Eleme"
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
            skoru_kaydet_bulut(prof["isim"] or "Oyuncu", final_skor)
            msg_txt.value = f"{sebep} | Ulasilan: Seviye {d['svy']}"
            msg_txt.color = "#ff7675"
            ceza_ek = f"\nKayip Soru Fazla ({kayip_sayisi}>{d['dogru']}): -10 Ceza -> Net: {final_skor} P" if ceza > 0 else ""
            karne_txt.value = f"SONUC (Seviye {d['svy']}): {d['puan']} P\nDogru: {d['dogru']} | Yanlis: {d['yanlis']} | Bos: {d['bos']}{ceza_ek}"
            karne_kutu.visible = True
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
        elif t == "e" and d["je"] > 0:
            d["je"] -= 1
            silinen = 0
            for i in range(4):
                if d["siklar"][i] != d["dc"] and silinen < 2:
                    sik_butonlar[i].visible = False
                    silinen += 1
            msg_txt.value = "50/50: Iki yanlis sik elendi!"
            msg_txt.color = "#00b894"
            guncelle()
        elif t == "a":
            if d["mod"] == "vs":
                if d["vs_atla"] <= 0:
                    msg_txt.value = "VS Atla hakkin bitti!"
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
            msg_txt.value = f"Soru atlandi! (Dogrusu: {d['dc']})"
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
            elif t == "e":
                d["je"] += 1
                m_txt.value = "50/50 Sik Eleme alindi!"
            elif t == "a":
                d["ja"] += 1
                m_txt.value = "Soru Atla jokeri alindi!"
            elif t == "2x":
                d["cift_puan"] += 3
                m_txt.value = "3 Soru 2X Puan aktif!"
            elif t == "c":
                d["jc"] += 1
                if d["can"] > 0:
                    d["can"] += 1
                m_txt.value = f"+1 Can! Baslangic: {3 + d['jc']}"
            m_txt.color = "#00b894"
            guncelle()

        dlg = ft.AlertDialog(
            bgcolor="#1e1e3f", title=ft.Text("Genisletilmis Magaza", color="white"),
            content=ft.Column([
                m_txt, uyari_txt,
                ft.Button("Zaman Dondur (5sn) - 30 Altin", bgcolor="#0984e3", color="white", width=240, on_click=lambda _: al("d", 30)),
                ft.Button("50/50 Sik Eleme (1x) - 40 Altin", bgcolor="#00b894", color="white", width=240, on_click=lambda _: al("e", 40)),
                ft.Button("Ekstra Sure (+10sn) - 50 Altin", bgcolor="#6c5ce7", color="white", width=240, on_click=lambda _: al("s", 50)),
                ft.Button("Kalici +1 Can - 60 Altin", bgcolor="#e94560", color="white", width=240, on_click=lambda _: al("c", 60)),
                ft.Button("Soru Atla (1x) - 70 Altin", bgcolor="#e17055", color="white", width=240, on_click=lambda _: al("a", 70)),
                ft.Button("3 Soru 2X Puan - 80 Altin", bgcolor="#fdcb6e", color="#121225", width=240, on_click=lambda _: al("2x", 80)),
            ], tight=True, spacing=4),
            actions=[ft.TextButton("Kapat", on_click=lambda _: page.pop_dialog())],
        )
        page.show_dialog(dlg)

    def oyunu_baslat(e=None):
        d["puan"] = 0
        d["svy"] = 1
        d["kombo"] = 0
        d["dur"] = False
        d["dogru"] = 0
        d["yanlis"] = 0
        d["bos"] = 0
        d["top_sure"] = 0.0
        d["cift_puan"] = 0
        karne_kutu.visible = False
        p_btn.content = "II"
        p_btn.bgcolor = "#636e72"
        tekrar_btn.visible = False
        if d["mod"] == "vs":
            d["can"] = 3
            d["vs_atla"] = 3
            d_btn.visible = False
            s_btn.visible = False
            e_btn.visible = False
            mag_btn.visible = False
            aktif_ad = d["p1"]["isim"] if d["vs_sira"] == 1 else d["p2"]["isim"]
            vs_banner.content.value = f"1v1 VS (15sn) | Sira: {aktif_ad} ({d['vs_sira']}/2)"
            vs_banner.visible = True
            msg_txt.value = f"{aktif_ad} Basladi! (3 Can | 3 Atla)"
        else:
            d["can"] = 3 + d["jc"]
            d_btn.visible = True
            s_btn.visible = True
            e_btn.visible = True
            mag_btn.visible = True
            vs_banner.visible = False
            msg_txt.value = f"Iyi sanslar {prof['isim']}! ({d['can']} Can)"
        msg_txt.color = "#00b894"
        yeni_soru()

    geri_btn = ft.Button("<-", bgcolor="#ff4757", color="white", width=44, on_click=geri_tikla)
    p_btn = ft.Button("II", bgcolor="#636e72", color="white", width=40, on_click=duraklat_degis)
    mag_btn = ft.Button("Magaza", bgcolor="#ffd32a", color="#121225", width=82, on_click=magaza)
    d_btn = ft.Button("Dondur (1)", bgcolor="#0984e3", color="white", on_click=lambda _: joker("d"))
    s_btn = ft.Button("+10sn (0)", bgcolor="#6c5ce7", color="white", on_click=lambda _: joker("s"))
    e_btn = ft.Button("50/50 (1)", bgcolor="#00b894", color="white", on_click=lambda _: joker("e"))
    a_btn = ft.Button("Atla (1)", bgcolor="#e17055", color="white", on_click=lambda _: joker("a"))
    tekrar_btn = ft.Button("TEKRAR OYNA", bgcolor="#ff4757", color="white", width=260, height=46, visible=False, on_click=oyunu_baslat)

    ust_bar = ft.Container(content=ft.Row([geri_btn, p_btn, ust_txt, altin_txt, mag_btn], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER, spacing=2), bgcolor="#1e1e3f", padding=6, border_radius=10, width=340)

    menu_ekrani = ft.Column([
        ft.Container(height=30),
        ft.Container(content=menu_rekor_txt, bgcolor="#1e1e3f", padding=14, border_radius=12),
        prof_bilgi_txt,
        ft.Container(height=30),
        ft.Text("HIZLI MATEMATIK", size=28, weight=ft.FontWeight.BOLD, color="white"),
        ft.Text("UNO Kartli Zeka Yarisi", size=13, color="#a2a8d3"),
        ft.Container(height=20),
        ft.Button("OYNA", bgcolor="#0984e3", color="white", width=240, height=56, on_click=oyna_tikla),
        ft.Container(height=8),
        ft.Button("MAGAZA", bgcolor="#ffd32a", color="#121225", width=240, height=48, on_click=magaza),
        ft.Container(height=20),
        ft.Button("SKOR TABLOSU", bgcolor="#6c5ce7", color="white", width=240, height=48, on_click=skor_tablosu_ac),
        prof_degis_btn,
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.SPACE_BETWEEN, visible=True)

    oyun_ekrani = ft.Column([
        ft.Container(height=18),
        vs_banner,
        ust_bar,
        bar,
        kart_dis,
        ft.Row([d_btn, s_btn, e_btn, a_btn], alignment=ft.MainAxisAlignment.CENTER, spacing=4),
        msg_txt,
        karne_kutu,
        sik_kolon,
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
                            msg_txt.value = f"SURE DOLDU! Dogrusu: {d['dc']}"
                            msg_txt.color = "#ff7675"
                            yeni_soru()
                page.update()

    page.run_task(sayac)

ft.run(main)
