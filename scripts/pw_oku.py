#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bot korumalı / JavaScript'le oluşan sayfayı yerel Playwright (Chromium) ile okur ve JSON basar.
Bağlama token yazmaz (MCP Playwright'ın aksine sonuç betiğe döner). Önce headless, olmazsa headed denenir.

Kullanım: python3 pw_oku.py URL            # {"url","kaynak":"playwright","basliklar":[[H,metin]],"paragraflar":[...]}
"""
import json, sys, time


def oku(url, headless=True):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(headless=headless, args=["--disable-blink-features=AutomationControlled", "--disable-http2"])
        c = b.new_context(locale="tr-TR", viewport={"width": 1366, "height": 900},
                          user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36")
        pg = c.new_page()
        pg.goto(url, wait_until="domcontentloaded", timeout=45000)
        pg.wait_for_timeout(2500)
        for _ in range(4):                      # alttaki SEO metni kaydırınca yüklenir
            pg.mouse.wheel(0, 2500); pg.wait_for_timeout(500)
        d = pg.evaluate("""()=>{const hs=[...document.querySelectorAll('h1,h2,h3,h4')].map(e=>[e.tagName,e.innerText.trim()]).filter(x=>x[1].length>3&&x[1].length<140);
          const ps=[...document.querySelectorAll('p')].map(e=>e.innerText.trim()).filter(x=>x.split(/\\s+/).length>=12);
          return {title:document.title,hs,ps}}""")
        b.close()
        return d


if __name__ == "__main__":
    url = sys.argv[1]
    for hl in (True, False):
        try:
            d = oku(url, hl)
            print(json.dumps({"url": url, "kaynak": "playwright", "baslik_sayfa": d["title"], "basliklar": d["hs"],
                              "paragraflar": d["ps"][:80]}, ensure_ascii=False))
            break
        except Exception as e:
            err = str(e)[:150]
    else:
        print(json.dumps({"url": url, "kaynak": "playwright", "hata": err}))
