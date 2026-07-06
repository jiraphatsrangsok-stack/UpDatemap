import os  # 1. เพิ่มการนำเข้า os เพื่อใช้ดึง Port สำหรับ Deploy ขึ้น Render
from flask import Flask, render_template
import folium

app = Flask(__name__)

# ข้อมูลสถานที่ท่องเที่ยว แหล่งประวัติศาสตร์ และธรรมชาติในกำแพงเพชร
LOCATIONS = [
    {
        "id": 1,
        "name": "อุทยานประวัติศาสตร์กำแพงเพชร",
        "lat": 16.5015,
        "lng": 99.5218,
        "description": "มรดกโลกทางวัฒนธรรม โดดเด่นด้วยโบราณสถานขนาดใหญ่ที่สร้างด้วยศิลาแลง เช่น วัดช้างรอบ และวัดพระสี่อิริยาบถ",
        "image": "https://images.unsplash.com/photo-1627589901931-15570fe3d441?auto=format&fit=crop&w=600&q=80",
        "type": "ประวัติศาสตร์"
    },
    {
        "id": 2,
        "name": "วัดพระแก้ว (ในกำแพงเมือง)",
        "lat": 16.4886,
        "lng": 99.5230,
        "description": "วัดสำคัญที่ตั้งอยู่ใจกลางเมืองโบราณ ประดิษฐานพระพุทธรูปปูนปั้นปางมารวิชัยและปางไสยาสน์ขนาดใหญ่",
        "image": "https://images.unsplash.com/photo-1608958416715-bc440994f31c?auto=format&fit=crop&w=600&q=80",
        "type": "ประวัติศาสตร์"
    },
    {
        "id": 3,
        "name": "บ่อน้ำพุร้อนพระร่วง",
        "lat": 16.6439,
        "lng": 99.4182,
        "description": "แหล่งท่องเที่ยวเพื่อสุขภาพ แช่น้ำแร่ธรรมชาติผ่อนคลายกล้ามเนื้อ ท่ามกลางบรรยากาศร่มรื่น",
        "image": "https://images.unsplash.com/photo-1540555700478-4be289fbecef?auto=format&fit=crop&w=600&q=80",
        "type": "ธรรมชาติ"
    },
    {
        "id": 4,
        "name": "ตลาดโบราณนครชุม",
        "lat": 16.4815,
        "lng": 99.5112,
        "description": "ย่านค้าขายเก่าแก่ริมฝั่งแม่น้ำปิง สัมผัสวิถีชีวิตดั้งเดิม ชิมอาหารท้องถิ่นขึ้นชื่อ เช่น หมี่ซั่ว และขนมจีบโบราณ",
        "image": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?auto=format&fit=crop&w=600&q=80",
        "type": "วัฒนธรรม/ของกิน"
    }
]

@app.route('/')
def index():
    # สร้างแผนที่ Folium โดยตั้ง Center ไว้ที่ตัวเมืองกำแพงเพชร
    m = folium.Map(location=[16.5200, 99.4800], zoom_start=11, tiles="OpenStreetMap")
    
    # เพิ่ม Marker สำหรับแต่ละสถานที่
    for loc in LOCATIONS:
        # ออกแบบ Pop-up ของแผนที่โดยใช้ HTML/CSS สไตล์มินิมอล
        popup_html = f"""
        <div style="font-family: 'Helvetica Neue', Arial, sans-serif; width: 220px; font-size: 14px; color: #333;">
            <img src="{loc['image']}" style="width:100%; height:110px; object-fit:cover; border-radius:6px; margin-bottom:8px;">
            <strong style="font-size:15px; color:#1a365d;">{loc['name']}</strong>
            <p style="margin: 4px 0 8px 0; color:#555; font-size:12px; line-height:1.4;">{loc['description'][:60]}...</p>
            <a href="https://www.google.com/maps/search/?api=1&query={loc['lat']},{loc['lng']}" 
               target="_blank" 
               style="display:inline-block; background-color:#3182ce; color:white; padding:5px 10px; text-decoration:none; border-radius:4px; font-size:11px; font-weight:bold;">
               🗺️ นำทางด้วย Google Maps
            </a>
        </div>
        """
        
        # เลือกสีหมุดตามประเภทสถานที่
        icon_color = "red" if loc['type'] == "ประวัติศาสตร์" else "green" if loc['type'] == "ธรรมชาติ" else "orange"
        
        folium.Marker(
            location=[loc['lat'], loc['lng']],
            popup=folium.Popup(popup_html, max_width=250),
            tooltip=loc['name'],
            icon=folium.Icon(color=icon_color, icon="info-sign")
        ).add_to(m)
    
    # แปลงแผนที่ Folium ให้เป็น HTML String เพื่อไปฝังในหน้าเว็บ
    map_html = m._repr_html_()
    
    return render_template('index.html', map_html=map_html, locations=LOCATIONS)

if __name__ == '__main__':
    
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)