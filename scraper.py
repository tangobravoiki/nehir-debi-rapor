#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Headless backend
from datetime import datetime
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

def scrape_dsi_data():
    """DSİ sitesinden nehir debi verilerini çeker"""
    url = "https://edirnenehir.dsi.gov.tr/"
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Tabloyu bul
        table = soup.find('table')
        if not table:
            print("Tablo bulunamadı!")
            return None
        
        # Başlıkları ve verileri ayıkla
        headers = []
        data_rows = []
        
        # Başlıkları al
        header_row = table.find('tr')
        if header_row:
            headers = [th.text.strip() for th in header_row.find_all(['th', 'td'])]
        
        # Veri satırlarını al
        for row in table.find_all('tr')[1:]:  # İlk satırı atla (başlık)
            cols = [td.text.strip() for td in row.find_all('td')]
            if cols:
                data_rows.append(cols)
        
        return {'headers': headers, 'data': data_rows}
    
    except Exception as e:
        print(f"Veri çekme hatası: {e}")
        return None

def create_chart(data_dict, output_path='output/debi_grafik.png'):
    """Debi verilerinden grafik oluşturur"""
    if not data_dict or not data_dict['data']:
        return None
    
    # Output dizinini oluştur
    os.makedirs('output', exist_ok=True)
    
    try:
        # Nehir isimleri ve debi değerlerini ayıkla
        nehirler = []
        debiler = []
        
        for row in data_dict['data']:
            if len(row) >= 4:
                nehir = row[0]
                try:
                    debi = float(row[3].replace(',', '.'))
                    nehirler.append(nehir)
                    debiler.append(debi)
                except ValueError:
                    continue
        
        if not nehirler:
            print("Grafik için veri yok!")
            return None
        
        # Grafik oluştur
        plt.figure(figsize=(12, 6))
        plt.bar(range(len(nehirler)), debiler, color='steelblue')
        plt.xlabel('Nehir İstasyonları', fontsize=12)
        plt.ylabel('Debi (m³/s)', fontsize=12)
        plt.title(f'DSİ 11. Bölge - Nehir Debi Verileri\n{datetime.now().strftime("%d.%m.%Y")}', fontsize=14, weight='bold')
        plt.xticks(range(len(nehirler)), nehirler, rotation=45, ha='right')
        plt.tight_layout()
        plt.grid(axis='y', alpha=0.3)
        
        # Kaydet
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return output_path
    
    except Exception as e:
        print(f"Grafik oluşturma hatası: {e}")
        return None

def create_html_report(data_dict, chart_path):
    """HTML rapor oluşturur"""
    tarih = datetime.now().strftime("%d.%m.%Y %H:%M")
    
    # Tablo HTML'i oluştur
    table_html = "<table border='1' style='border-collapse: collapse; width: 100%;'>\n"
    
    if data_dict and data_dict['headers']:
        table_html += "<tr style='background-color: #4CAF50; color: white;'>\n"
        for header in data_dict['headers']:
            table_html += f"<th style='padding: 10px;'>{header}</th>\n"
        table_html += "</tr>\n"
    
    if data_dict and data_dict['data']:
        for row in data_dict['data']:
            table_html += "<tr>\n"
            for cell in row:
                table_html += f"<td style='padding: 8px;'>{cell}</td>\n"
            table_html += "</tr>\n"
    
    table_html += "</table>"
    
    # HTML şablonu
    html = f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DSİ Nehir Debi Raporu - {tarih}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .header {{
            background-color: #2196F3;
            color: white;
            padding: 20px;
            text-align: center;
            border-radius: 5px;
            margin-bottom: 20px;
        }}
        .content {{
            background-color: white;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        table {{
            margin: 20px 0;
        }}
        th {{
            font-weight: bold;
        }}
        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        .chart {{
            text-align: center;
            margin: 20px 0;
        }}
        .footer {{
            text-align: center;
            margin-top: 20px;
            color: #666;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>DSİ 11. Bölge - Nehir Debi Takip Sistemi</h1>
        <p>Güncellenme: {tarih}</p>
    </div>
    
    <div class="content">
        <h2>Güncel Debi Verileri</h2>
        {table_html}
        
        <div class="chart">
            <h2>Debi Grafiği</h2>
            <img src="debi_grafik.png" alt="Debi Grafiği" style="max-width: 100%; height: auto;">
        </div>
    </div>
    
    <div class="footer">
        <p>Bu rapor otomatik olarak oluşturulmuştur. | GitHub Actions tarafından her gün 08:00'da güncellenir.</p>
    </div>
</body>
</html>"""
    
    # HTML dosyasını kaydet
    os.makedirs('output', exist_ok=True)
    with open('output/index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    return html

def send_email(html_content, chart_path):
    """E-posta gönderir (Gmail SMTP)"""
    gmail_user = os.environ.get('GMAIL_USER')
    gmail_pass = os.environ.get('GMAIL_PASS')
    
    if not gmail_user or not gmail_pass:
        print("Gmail bilgileri bulunamadı!")
        return False
    
    try:
        msg = MIMEMultipart('related')
        msg['From'] = gmail_user
        msg['To'] = 'serdarerman@gmail.com'
        msg['Subject'] = f"DSİ Nehir Debi Raporu - {datetime.now().strftime('%d.%m.%Y')}"
        
        # HTML içeriği ekle
        msg.attach(MIMEText(html_content, 'html', 'utf-8'))
        
        # Grafiği ekle
        if chart_path and os.path.exists(chart_path):
            with open(chart_path, 'rb') as f:
                img = MIMEImage(f.read())
                img.add_header('Content-ID', '<debi_grafik>')
                img.add_header('Content-Disposition', 'inline', filename='debi_grafik.png')
                msg.attach(img)
        
        # SMTP ile gönder
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(gmail_user, gmail_pass)
        server.send_message(msg)
        server.quit()
        
        print("E-posta başarıyla gönderildi!")
        return True
    
    except Exception as e:
        print(f"E-posta gönderme hatası: {e}")
        return False

def main():
    """Ana fonksiyon"""
    print("DSİ Nehir Debi Scraper başlatıldı...")
    
    # 1. Veri çek
    print("Veri çekiliyor...")
    data = scrape_dsi_data()
    
    if not data:
        print("Veri çekilemedi!")
        return
    
    print(f"{len(data['data'])} satır veri çekildi.")
    
    # 2. Grafik oluştur
    print("Grafik oluşturuluyor...")
    chart_path = create_chart(data)
    
    # 3. HTML raporu oluştur
    print("HTML raporu oluşturuluyor...")
    html = create_html_report(data, chart_path)
    
    # 4. E-posta gönder
    print("E-posta gönderiliyor...")
    send_email(html, chart_path)
    
    print("İşlem tamamlandı!")

if __name__ == '__main__':
    main()