import ezdxf
import re

FILE_PATH = r"C:\Users\ali.nasser\Desktop\Masry_AI_ENG-Agent\python\sample 03.dxf"

def clean_mtext(text):
    """
    دالة محترفة لتنظيف نصوص الـ MTEXT من أكواد التنسيق المخفية للأوتوكاد.
    تطير أي رموز تبدأ بـ \ وأقواس مجعدة عشان تصفي النص الإنشائي فقط.
    """
    # 1. إزالة أكواد التنسيق المخفية التي تبدأ بـ \ وتنتهي بـ ;
    text = re.sub(r'\\[Mm]\+?[^\s;]*;', '', text)
    text = re.sub(r'\\^[^\s;]*;', '', text)
    text = re.sub(r'\\\w[^\s;]*;', '', text)
    # 2. إزالة الأقواس المجعدة الخاصة بالمجموعات التنسيقية جوه الكاد {}
    text = re.sub(r'[{}]', '', text)
    # 3. تنظيف أي مسافات زائدة قد تنتج عن الحذف
    return text.strip()

def get_engineering_data():
    try:
        doc = ezdxf.readfile(FILE_PATH)
        msp = doc.modelspace()
    except Exception as e:
        print(f"❌ Error loading DXF file: {e}")
        return None

    beams_data = []
    columns_data = [] 
    texts_data = []

    for entity in msp:
        layer = entity.dxf.layer.lower()
        etype = entity.dxftype()

        # 1. قراءة بيانات الكامرات
        if "beams" in layer and etype == 'LWPOLYLINE':
            pts = list(entity.get_points())
            if len(pts) >= 2:
                pts.sort(key=lambda p: p[0])
                beams_data.append({
                    'start_x': pts[0][0],
                    'end_x': pts[-1][0],
                    'length': ((pts[-1][0]-pts[0][0])**2 + (pts[-1][1]-pts[0][1])**2)**0.5,
                    'center': (sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts))
                })
        
        # 2. قراءة بيانات الأعمدة
        elif "col" in layer and etype == 'LWPOLYLINE':
            pts = list(entity.get_points())
            if len(pts) >= 2:
                x_coords = [p[0] for p in pts]
                columns_data.append({
                    'min_x': min(x_coords),
                    'max_x': max(x_coords),
                    'width': max(x_coords) - min(x_coords)
                })

        # 3. قراءة وتنظيف النصوص (سواء TEXT عادي أو MTEXT معقد)
        elif etype in ('TEXT', 'MTEXT'):
            txt = entity.dxf.text if etype == 'TEXT' else entity.text
            
            # 🔥 السحر هنا: تنظيف النص فوراً قبل الـ Regex للتخلص من شخابيط التنسيق
            txt = clean_mtext(txt)
            
            dims = re.findall(r'\d{2,}', txt)
            if dims:
                texts_data.append({"text": txt, "pos": entity.dxf.insert, "dims": dims})

    # ربط النصوص والقطاعات بالسبانات الخاصة بها
    unique_beams = []
    for b in beams_data:
        current_beam_label = "B" 
        w = 300
        h = 600
        if texts_data:
            closest_t = min(texts_data, key=lambda t: ((b['center'][0]-t['pos'][0])**2 + (b['center'][1]-t['pos'][1])**2)**0.5)
            if ((b['center'][0]-closest_t['pos'][0])**2 + (b['center'][1]-closest_t['pos'][1])**2)**0.5 < 2000:
                current_beam_label = closest_t['text']
                nums = [int(d) for d in closest_t['dims']]
                valid_nums = [n for n in nums if n >= 100]
                h = max(valid_nums) if valid_nums else 600
                w = min(valid_nums) if valid_nums else 300
        
        b['beam_tag'] = current_beam_label 
        b['height'] = h
        b['width'] = w
        
        if not any(((b['center'][0]-saved['center'][0])**2 + (b['center'][1]-saved['center'][1])**2)**0.5 < 400 for saved in unique_beams):
            unique_beams.append(b)
    
    unique_beams.sort(key=lambda b: b['start_x'])

    if not unique_beams: 
        print("⚠️ No beams found in the file.")
        return None

    # تجميع وتصنيف القطاعات الفريدة (Optimization) لمنع تكرار رسم السيكشنز
    unique_sections = []  
    beam_section_tags = []  
    
    for b in unique_beams:
        sec_key = (b['width'], b['height'])
        if sec_key not in unique_sections:
            unique_sections.append(sec_key)
        
        sec_name = f"SEC_{b['width']}x{b['height']}"
        beam_section_tags.append(sec_name)

    first_beam = unique_beams[0]
    last_beam = unique_beams[-1]

    # حساب أبعاد أعمدة الطرف والأعمدة الوسطية
    c_side_start = 300 
    if columns_data:
        matching_cols = [c for c in columns_data if abs(c['max_x'] - first_beam['start_x']) < 100]
        if matching_cols:
            c_side_start = round(matching_cols[0]['width'], 0)

    c_side_end = 300 
    if columns_data:
        matching_cols = [c for c in columns_data if abs(c['min_x'] - last_beam['end_x']) < 100]
        if matching_cols:
            c_side_end = round(matching_cols[0]['width'], 0)

    mid_columns = []
    if len(unique_beams) > 1:
        for i in range(len(unique_beams) - 1):
            gap = unique_beams[i+1]['start_x'] - unique_beams[i]['end_x']
            mid_columns.append(round(gap, 0))

    # بناء قاموس المخرجات النهائي
    results = {
        "beam_texts": [b['beam_tag'] for b in unique_beams], 
        "num_beams": len(unique_beams),
        "clear_spans": [round(float(b['length']), 2) for b in unique_beams],
        "h_beams": [b['height'] for b in unique_beams],  
        "w_beams": [b['width'] for b in unique_beams],   
        "beam_section_tags": beam_section_tags, 
        "unique_sections_to_draw": [{"w": sec[0], "h": sec[1], "name": f"SEC_{sec[0]}x{sec[1]}"} for sec in unique_sections],
        "c_side_start": c_side_start,
        "mid_columns": mid_columns,
        "c_side_end": c_side_end,
        "h_up": 1000,
        "h_down": 700
    }
    
    return results

if __name__ == "__main__":
    results = get_engineering_data()
    if results:
        print("\n" + "="*55)
        print("🚀 INTELLIGENT OPTIMIZED ENGINEERING REPORT")
        print("="*55)
        print(f" Number of Beams:     {results['num_beams']}")
        print(f" Beam Tags:           {', '.join(results['beam_texts'])}") 
        print(f" Clear Spans:        {results['clear_spans']} mm")
        print(f" Section per Span:    {results['beam_section_tags']}")
        print("-"*55)
        print(f" 🎯 Unique Sections to Draw Underneath (No Duplicates):")
        for sec in results['unique_sections_to_draw']:
            print(f"   - Name: {sec['name']} -> Width: {sec['w']}mm, Height: {sec['h']}mm")
        print("="*55 + "\n")