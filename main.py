import pyautogui
import pywintypes
import win32com.client
import winsound
import ctypes
import time
import sys
from read_cad import get_engineering_data 

# --- 1. SETTINGS & SAFETY ---
pyautogui.PAUSE = 0.2
pyautogui.FAILSAFE = True

#### مرحلة التعريفات فقط

#التأكد من ان اللغة انجليزي
def ensure_english_keyboard():
    lib = ctypes.windll.User32
    
    current_layout = lib.GetKeyboardLayout(0) & 0xFFFF
    
    # لو اللغة مش إنجليزية (1033)
    if current_layout != 1033:
        print("❌ language not english.")
        sys.exit() # إيقاف الكود بالكامل فوراً

#تعريف أمر run cmd
def run_cmd(cmd_string):
        
    # لو الأوتوكاد مهنج، هيحاول كذا مرة بفواصل زمنية صغيرة جداً
    for attempt in range(20): 
        try:
            doc.SendCommand(f"{cmd_string}\n")
            break # لو الأمر عدا بسلام، اخرج من اللوب كمل السكربت علطول
        except pywintypes.com_error as e:
            # الكود -2147418111 معناه الأوتوكاد مشغول وبيرفض الإدخال حالياً
            if e.hresult == -2147418111:
                # استراحة قصيرة جداً (0.05 ثانية) عشان الكاد يتنفس ويخلص المعالجة
                time.sleep(0.05) 
            else:
                 # لو فيه خطأ حقيقي تاني في صياغة الأمر نفسه، يطبع ويقفل للأمان
                print(f"❌ Error in command '{cmd_string}': {e}")
                sys.exit()
        else:
            # لو حاول 20 مرة (يعني فضل مربع ثانية كاملة رافض) كدة الكاد قفل خالص
            print(f"❌ Critical: AutoCAD frozen on command: {cmd_string}")
            sys.exit()

#تعريف البحث عن صورة مع عدم الضغط عليها والتوقف في حالة عدم العثور عليها 
def find_and_dont_click_check_icon(search_region, image_path, timeout=2):

    start_time = time.time() # تسجيل وقت البداية
    
    print(f"🔍 searching for pic")
    
    while True:
        try:
            # محاولة تحديد مكان الصورة
            location = pyautogui.locateCenterOnScreen(
                image_path, 
                confidence=0.8, 
                grayscale=True, 
                region=search_region
            )
            
            if location:
                print("pic was found.")
                return True # نجحنا، اخرج من الدالة
            
        except Exception as e:
            # بنتجاهل الأخطاء العادية أثناء البحث عشان ميتوقفش الكود
            pass

        # التحقق من الوقت: لو عدينا الـ Timeout نوقف بحث
        if time.time() - start_time > timeout:
            print("⚠️  time's up    .")
            sys.exit() # إيقاف الكود بالكامل فوراً
            return False
            
        time.sleep(0.1) # استراحة بسيطة عشان المعالج (CPU) ميرفعش حرارة

#تعريف البحث عن صورة مع عدم الضغط عليها وعدم التوقف في حالة عدم العثور عليها 
def find_and_dont_click_skip_icon(search_region, image_path, timeout=0.5):

    start_time = time.time() # تسجيل وقت البداية
    
    print(f"🔍 searching for pic")
    
    while True:
        try:
            # محاولة تحديد مكان الصورة
            location = pyautogui.locateCenterOnScreen(
                image_path, 
                confidence=0.95, 
                grayscale=True, 
                region=search_region
            )
            
            if location:
                print("pic was found.")
                return True # نجحنا، اخرج من الدالة
            
        except Exception as e:
            # بنتجاهل الأخطاء العادية أثناء البحث عشان ميتوقفش الكود
            pass

        # التحقق من الوقت: لو عدينا الـ Timeout نوقف بحث
        if time.time() - start_time > timeout:
            print("⚠️  time's up    .")
            return False
            
        time.sleep(0.1) # استراحة بسيطة عشان المعالج (CPU) ميرفعش حرارة

#تعريف البحث عن صورة مع الضغط عليها وعدم التوقف في حالة عدم العثور عليها 
def find_and_click_or_skip_icon(search_region, image_path, timeout=1):

    start_time = time.time() # تسجيل وقت البداية
    
    print(f"🔍 searching for pic")
    
    while True:
        try:
            # محاولة تحديد مكان الصورة
            location = pyautogui.locateCenterOnScreen(
                image_path, 
                confidence=0.80, 
                grayscale=True, 
                region=search_region
            )
            
            if location:
                pyautogui.click(location)
                print("pic was found.")
                return True # نجحنا، اخرج من الدالة
            
        except Exception as e:
            # بنتجاهل الأخطاء العادية أثناء البحث عشان ميتوقفش الكود
            pass

        # التحقق من الوقت: لو عدينا الـ Timeout نوقف بحث
        if time.time() - start_time > timeout:
            print("⚠️  time's up    .")
            
            return False
            
        time.sleep(0.1) # استراحة بسيطة عشان المعالج (CPU) ميرفعش حرارة

#تعريف البحث عن صورة مع الضغط عليها والتوقف في حالة عدم العثور عليها 
def find_and_click_check_icon(search_region, image_path, timeout=2):

    start_time = time.time() # تسجيل وقت البداية
    
    print(f"🔍 searching for pic")
    
    while True:
        try:
            # محاولة تحديد مكان الصورة
            location = pyautogui.locateCenterOnScreen(
                image_path, 
                confidence=0.8, 
                grayscale=True, 
                region=search_region
            )
            
            if location:
                pyautogui.click(location)
                print("pic was found.")
                return True # نجحنا، اخرج من الدالة
            
        except Exception as e:
            # بنتجاهل الأخطاء العادية أثناء البحث عشان ميتوقفش الكود
            pass

        # التحقق من الوقت: لو عدينا الـ Timeout نوقف بحث
        if time.time() - start_time > timeout:
            print("⚠️  time's up    .")
            sys.exit() # إيقاف الكود بالكامل فوراً
            
            return False
            
        time.sleep(0.1) # استراحة بسيطة عشان المعالج (CPU) ميرفعش حرارة

#رسم السكاشن والقطاعات
def draw_section_with_approved_breaklines():
    # استدعاء البيانات الديناميكية من الكود السابق
    data = get_engineering_data()
    
    if not data:
        print("❌ data failure.")
        return

    # استخراج القيم (التي أصبحت الآن قوائم أو قيم ديناميكية)
    clear_spans = data["clear_spans"]  # قائمة بالبحور
    h_beams = data["h_beams"]           
    w_beams = data["w_beams"]      
    beam_section_tags = data["beam_section_tags"] 
    unique_sections = data["unique_sections_to_draw"]     
    c_side_start = data["c_side_start"]
    mid_columns = data["mid_columns"]  # قائمة بعروض أعمدة الوسط
    c_side_end = data["c_side_end"]
    h_up = data["h_up"]          
    h_down = data["h_down"]        

    # إعدادات الـ Break Line
    brk_ext, brk_z_width, brk_z_peak = 100, 150, 103
    dim_y = h_up - 350

    print(f"\n🚀 Go 3alawy Go! ")
    print(" 1 sec to open autocad ... run!! ")
    time.sleep(1)
    
    # دالة الرسم المساعدة
    def play_beep():
        sound_path = r'C:\Users\ali.nasser\Desktop\Masry_AI_ENG-Agent\sound effect\myinstants3.wav'
        try:
           # SND_ASYNC بتخلي الصوت يشتغل في الخلفية من غير ما يعطل سرعة الكود
           winsound.PlaySound(sound_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
        except Exception as e:
           # لو المسار فيه غلط أو الملف مش موجود، الكود مش هيقف وهيطلع زنة بسيطة بديلة
           winsound.MessageBeep()

    def draw_approved_breakline(x_left, x_right, y):
        x_center = (x_left + x_right) / 2
        p1 = f"{x_left - brk_ext},{y}"
        p2 = f"{x_center - brk_z_width/2},{y}"
        p3 = f"{x_center},{y + brk_z_peak}"
        p4 = f"{x_center},{y - brk_z_peak}"
        p5 = f"{x_center + brk_z_width/2},{y}"
        p6 = f"{x_right + brk_ext},{y}"
        
        run_cmd(f"PLINE {p1} {p2} {p3} {p4} {p5} {p6} ")
        play_beep()
        

    # --- 2. حساب الإحداثيات التراكمية (X) ---
    # سنقوم ببناء قائمة بكل نقاط الأعمدة (يسار ويمين كل عمود)
    current_x = 0
    column_points = [] # قائمة تحتوي على (x_left, x_right) لكل عمود

    # العمود الأول
    column_points.append((current_x, current_x + c_side_start))
    current_x += c_side_start

    # التكرار لبناء بقية المنشأ (بحر ثم عمود وسط...)
    for i in range(len(clear_spans)):
        # إضافة إحداثيات البحر (تخطي المسافة فقط)
        span_start = current_x
        current_x += clear_spans[i]
        span_end = current_x
        
        # إضافة عمود (إما وسط أو طرف أخير)
        if i < len(mid_columns):
            col_w = mid_columns[i]
        else:
            col_w = c_side_end
            
        column_points.append((current_x, current_x + col_w))
        current_x += col_w

    # --- 3. التنفيذ البرمجي للرسم ---
    upper_intersection_points = []
    y_top = h_up

    # أ. رسم كل الأعمدة وخطوط القطع
    for i, (xl, xr) in enumerate(column_points):
        if i == 0:
            h_local = h_beams[0]
        elif i == len(column_points) - 1:
            h_local = h_beams[-1]
        else:
            # العمود الوسطي بياخد الارتفاع الأكبر بين البحرين اللي شيلهم
            h_local = max(h_beams[i-1], h_beams[i])
        y_bot = -(h_local + h_down)    
        # الخطوط الرأسية للأعمدة
        run_cmd(f"LINE {xl},{y_top} {xl},0 ")
        play_beep()
        run_cmd(f"LINE {xl},{-h_local} {xl},{y_bot} ")
        play_beep()
        run_cmd(f"LINE {xr},{y_top} {xr},0 ")
        play_beep()
        run_cmd(f"LINE {xr},{-h_local} {xr},{y_bot} ")
        play_beep()
        upper_intersection_points.append((xl, 0))
        upper_intersection_points.append((xr, 0))

        # إغلاق الأطراف الخارجية فقط
        if i == 0: 
            run_cmd(f"LINE {xl},0 {xl},{-h_local} ")
        if i == len(column_points) - 1: 
            run_cmd(f"LINE {xr},0 {xr},{-h_local} ")

        draw_approved_breakline(xl, xr, y_top)
        play_beep()
        draw_approved_breakline(xl, xr, y_bot)
        play_beep()

    # ب. رسم خطوط الكمرات الأفقية (الوصلات بين الأعمدة)
    for i in range(len(column_points) - 1):
        x_beam_start = column_points[i][1]
        x_beam_end = column_points[i+1][0]
        h_current_beam = h_beams[i]  # 🔥 سحب الارتفاع الحقيقي للسبان الحالي
        
        run_cmd(f"LINE {x_beam_start},0 {x_beam_end},0 ")
        play_beep()
        run_cmd(f"LINE {x_beam_start},{-h_current_beam} {x_beam_end},{-h_current_beam} ")
        play_beep()
        
        # تقسيم البحر لثلاثة أجزاء (رسم الخطوط الرأسية للتقسيم)
        third = (x_beam_end - x_beam_start) / 3
        pt_third_1 = x_beam_start + third
        pt_third_2 = x_beam_start + 2*third

        if i == 0 and (i + 1) < len(h_beams) and h_beams[i] < h_beams[i+1]:
            run_cmd(f"LINE {x_beam_end},{-h_beams[i+1]} {x_beam_end},{-h_beams[i]} ")

        # المقارنة مع البحر السابق (تحدث فقط لو فيه بحر سابق فعلاً)
        if i > 0 and (i - 1) >= 0 and h_beams[i] < h_beams[i-1]:
            run_cmd(f"LINE {x_beam_start},{-h_beams[i-1]} {x_beam_start},{-h_beams[i]} ")

        run_cmd(f"LINE {pt_third_1},0 {pt_third_1},{y_top} ")
        play_beep()
        run_cmd(f"LINE {pt_third_2},0 {pt_third_2},{y_top} ")
        play_beep()

        # حفظ نقط التقسيم عند (Y=0)
        upper_intersection_points.append((pt_third_1, 0))
        upper_intersection_points.append((pt_third_2, 0))
    upper_intersection_points.sort()
    
    # رسم ال cross section
    start_x_sec = 0  # نقطة البداية الأفقية لأول سيكشن
    spacing_between_sections = 5000  # مسافة أمان أفصل بيها المستطيلات عن بعض
    
    for sec in unique_sections:
        w_sec = sec["w"]
        h_sec = sec["h"]
        tag_name = sec["name"]
        
        # حساب المنسوب السفلي للقطاع بناءً على ارتفاعه المتغير
        Y_Bottom = -8500 - h_sec
        
        p1 = f"{start_x_sec},-8500"
        p2 = f"{start_x_sec + w_sec},-8500"
        p3 = f"{start_x_sec + w_sec},{Y_Bottom}"
        p4 = f"{start_x_sec},{Y_Bottom}"
        
        # رسم مستطيل القطاع
        run_cmd(f"RECTANG {p1} {p3} ")
        time.sleep(0.05)
            
        # رسم أبعاد الـ Cross Section الحالي
        p6_dim = f"{start_x_sec - 200},-8300" # خط البُعد على اليسار
        run_cmd("-DIMSTYLE R ALI_B_25 ")
        time.sleep(0.05)

        run_cmd(f"DIMHORIZONTAL {p1} {p2} {p6_dim} ")
        time.sleep(0.05)
        run_cmd(f"DIMVERTICAL {p1} {p4} {p6_dim} ")
        time.sleep(0.05)
        
        # ترحيل الإحداثي الأفقي للقطاع القادم عشان ميركبوش فوق بعض
        start_x_sec += w_sec + spacing_between_sections
    
    run_cmd("-DIMSTYLE R ALI_B ")
    time.sleep(0.05) # استراحة بسيطة للأوتوكاد

    beam_labels = data["beam_texts"]
    text_height = 190 # ارتفاع الخط في الأوتوكاد
    y_text_pos = 1250   # إزاحة النص للأعلى عن خط الكمرة العلوي
    
    for i in range(len(column_points) - 1):
        x_mid = (column_points[i][1] + column_points[i+1][0]) / 2
        label = beam_labels[i].replace(" ", "_")
        
        run_cmd(f"-TEXT\nJ\nMC\n{x_mid},{y_text_pos}\n0\n{label}\n")
        time.sleep(0.05)
        

    # --- 4. رسم الأبعاد (Dimensions) ---
    
    # السلسلة العلوية (أبعاد تفصيلية)
    # تبدأ من أول نقطة في أول عمود
    start_point = f"{column_points[0][0]},{dim_y}"
    run_cmd(f"DIMHORIZONTAL {start_point} {column_points[0][1]},{dim_y} {start_point} ")
    
    points_to_dim = []
    for i in range(len(column_points)-1):
        xl_next = column_points[i+1][0]
        xr_next = column_points[i+1][1]
        span_w = xl_next - column_points[i][1]
        
        points_to_dim.append(f"{column_points[i][1] + span_w/3},{dim_y}")
        points_to_dim.append(f"{column_points[i][1] + 2*span_w/3},{dim_y}")
        points_to_dim.append(f"{xl_next},{dim_y}")
        points_to_dim.append(f"{xr_next},{dim_y}")

    for p in points_to_dim:
        run_cmd(f"DIMCONTINUE {p} \n")
        
    

    # السلسلة السفلية (أبعاد البحور الصافية Clear Spans)
    for i in range(len(column_points)-1):
        x1 = column_points[i][1]
        x2 = column_points[i+1][0]
        run_cmd(f"DIMHORIZONTAL {x1},{dim_y-2000} {x2},{dim_y-2000} {x1},{dim_y-2000} ")
        time.sleep(0.05)

    print("\n✅ done drawing.")
    return upper_intersection_points

#رسم الكانات
def stirrups_rft():
    data = get_engineering_data()
    beam_section_tags = data["beam_section_tags"]
    unique_sections = data["unique_sections_to_draw"]
    
    if not data:
        print("❌ data failure.")
        return

    unique_sections = data["unique_sections_to_draw"]
    
    # إعدادات الترحيل (نفس المنطق اللي رسمنا بيه المستطيلات فوق)
    start_x_sec = 0
    spacing_between_sections = 5000  # 🔥 المسافة الجديدة اللي أنت عدلتها

    # هنلف على كل سيكشن فريد ونفتح أمر الكانات ونرسم الكانة في مكان السيكشن الصح
    for sec in unique_sections:
        w_sec = sec["w"]
        h_sec = sec["h"]
        
        # حساب نقطة نقرة الكانة جوه السيكشن المترحل (مثلاً مشفتة 100 ملم جوه الـ X الحالية)
        stirrup_x = start_x_sec + 100
        stirrup_y = -8700

        x_offset = get_section_x_offset(sec["name"], unique_sections, 5000)

        stirrup_pick_x = x_offset + 25
        p_des = f"{int(x_offset + w_sec + 800)},-8800"

        print(f"Drawing Stirrup Bar for {sec['name']} at X: {stirrup_x}")
        
        pyautogui.click(x=700, y=10)
        time.sleep(0.1) # انتظار ظهور النافذة
        pyautogui.press('esc')
        time.sleep(0.1)
        pyautogui.typewrite("rbcr_def_bar_bs ", interval=0.005)
        time.sleep(1) # انتظار ظهور النافذة

        search_region_7 = (14, 39, 255, 205) # أرقام مثال: ابدأ من 100,200 وابحث في مساحة 500x600
        image_path_7 = r'C:\Users\ali.nasser\Desktop\Masry_AI_ENG-Agent\screenshots\STEEL GRADE T.PNG'
        if find_and_dont_click_skip_icon(search_region_7,image_path_7):
            pyautogui.click(x=190, y=180)
            time.sleep(0.1) # انتظار ظهور النافذة
            pyautogui.click(x=190, y=200)
            time.sleep(0.1) # انتظار ظهور النافذة
        else:
            print("⏭️steel grade is R")

        search_region_6 = (14, 39, 255, 205) # أرقام مثال: ابدأ من 100,200 وابحث في مساحة 500x600
        image_path_6 = r'C:\Users\ali.nasser\Desktop\Masry_AI_ENG-Agent\screenshots\Dia is 8.PNG'
        if find_and_dont_click_skip_icon(search_region_6,image_path_6):
            print("⏭️steel Dia is 8")    
        else:
        
            pyautogui.click(x=135, y=80)
            time.sleep(0.1) # انتظار ظهور النافذة
            pyautogui.click(x=135, y=110)
            time.sleep(0.1) # انتظار ظهور النافذة
    
        search_region_1 = (132, 0, 247, 186) # أرقام مثال: ابدأ من 100,200 وابحث في مساحة 500x600
        image_path_2 = r'C:\Users\ali.nasser\Desktop\Masry_AI_ENG-Agent\screenshots\stirrups len is locked.PNG'
        find_and_click_or_skip_icon(search_region_1,image_path_2)
        time.sleep(0.1)
        search_region_2 = (383, 0, 250, 224) # أرقام مثال: ابدأ من 100,200 وابحث في مساحة 500x600
        find_and_click_or_skip_icon(search_region_2,image_path_2)
        time.sleep(0.1)
    
        search_region_5 = (219, 70, 128, 45) # أرقام مثال: ابدأ من 100,200 وابحث في مساحة 500x600
        image_path_5 = r'C:\Users\ali.nasser\Desktop\Masry_AI_ENG-Agent\screenshots\hook is 100.PNG'
        if find_and_dont_click_skip_icon(search_region_5,image_path_5):
            print("⏭️steel hook is 100")    
        else:
        
            pyautogui.click(x=298, y=90)
            time.sleep(0.1) # انتظار ظهور النافذة
            pyautogui.keyDown('ctrl')
            time.sleep(0.05) # انتظار ظهور النافذة
            pyautogui.keyDown('a')
            time.sleep(0.05) # انتظار ظهور النافذة
            pyautogui.keyUp('ctrl')
            time.sleep(0.05) # انتظار ظهور النافذة
            pyautogui.keyUp('a')
            time.sleep(0.05) # انتظار ظهور النافذة
            pyautogui.write('100')
    
        search_region_4 = (414, 70, 128, 45) # أرقام مثال: ابدأ من 100,200 وابحث في مساحة 500x600
        image_path_4 = r'C:\Users\ali.nasser\Desktop\Masry_AI_ENG-Agent\screenshots\hook is 100 r.PNG'
        if find_and_dont_click_skip_icon(search_region_4,image_path_4):
            print("⏭️steel hook is 100")    
        else:
        
            pyautogui.click(x=475, y=92)
            time.sleep(0.05) # انتظار ظهور النافذة
            pyautogui.keyDown('ctrl')
            time.sleep(0.05) # انتظار ظهور النافذة
            pyautogui.keyDown('a')
            time.sleep(0.05) # انتظار ظهور النافذة
            pyautogui.keyUp('ctrl')
            time.sleep(0.05) # انتظار ظهور النافذة
            pyautogui.keyUp('a')
            time.sleep(0.05) # انتظار ظهور النافذة
            pyautogui.write('100')
            time.sleep(0.05)
    
    
        image_path_1 = r'C:\Users\ali.nasser\Desktop\Masry_AI_ENG-Agent\screenshots\stirrups len is unlocked.jpg'
        find_and_click_or_skip_icon(search_region_1,image_path_1)
        time.sleep(0.1)
        find_and_click_or_skip_icon(search_region_2,image_path_1)      
        pyautogui.click(x=564, y=126)
        time.sleep(0.5) # انتظار ظهور النافذة
    
        pyautogui.typewrite(f"{stirrup_x},{stirrup_y}\n")
        time.sleep(0.5)
        pyautogui.typewrite(f"{stirrup_x},{stirrup_y}\n")
        time.sleep(0.5)

        search_region_10 = (505, 334, 781, 347) # أرقام مثال: ابدأ من 100,200 وابحث في مساحة 500x600
        image_path_10 = r'C:\Users\ali.nasser\Desktop\Masry_AI_ENG-Agent\screenshots\douplicated stirrups rft yes.png'
        find_and_click_or_skip_icon(search_region_10,image_path_10)
        pyautogui.click(x=527, y=53)
        time.sleep(0.1)
        pyautogui.click(x=527, y=96)
        time.sleep(0.1)

        pyautogui.click(x=406, y=198)
        pyautogui.write('STR')
        time.sleep(0.05)
        pyautogui.mouseDown(x=585, y=54)
        time.sleep(0.1) # خلي الماوس "مضغوط" لمدة 200 مللي ثانية
        pyautogui.mouseUp()
        time.sleep(0.5)
        pyautogui.typewrite(f"{p_des}\n")
        pyautogui.press('enter')
        time.sleep(0.2)

        pyautogui.typewrite("rbcr_def_pull\n", interval=0.005)
        pyautogui.typewrite(f"{stirrup_pick_x},-8800\n")
        pull_dis = f"{int(x_offset + w_sec + 2500)},-8800"
        pyautogui.typewrite(f"{pull_dis}\n")
        pull_des_dis = f"{int(x_offset + w_sec + 2250)},-9300"
        pyautogui.typewrite(f"{pull_des_dis}\n")
        time.sleep(0.2)

        # ترحيل الـ X للسيكشن اللي بعده
        start_x_sec += w_sec + spacing_between_sections

def get_section_x_offset(target_tag, unique_sections, spacing=5000):
    current_offset = 0
    for sec in unique_sections:
        if sec["name"] == target_tag:
            return current_offset
        current_offset += sec["w"] + spacing
    return 0

#توزيع الكانات
def stirrups_rft_description(captured_points):
    data = get_engineering_data()
    w_beams = data["w_beams"] 
    h_beams = data["h_beams"]  
    beam_section_tags = data["beam_section_tags"]
    unique_sections = data["unique_sections_to_draw"]
    w_beam = w_beams[0]
    h_beam = h_beams[0]
    x_offset = get_section_x_offset(beam_section_tags[0], unique_sections, 5000)
    stirrup_pick_x = x_offset + 25

    pyautogui.typewrite("rbcr_distribution\n", interval=0.005)
    pyautogui.typewrite(f"{stirrup_pick_x},-8800\n")
    pyautogui.press('enter')
    time.sleep(0.2)
    search_region_1 = (376, 83, 90, 36) # أرقام مثال: ابدأ من 100,200 وابحث في مساحة 500x600
    image_path_1 = r'C:\Users\ali.nasser\Desktop\Masry_AI_ENG-Agent\screenshots\stirrup dis.jpg'
    find_and_click_check_icon(search_region_1,image_path_1)
    time.sleep(0.2)
    pyautogui.press('enter')
    pyautogui.write(f"{captured_points[1][0]},{captured_points[1][1]}\n")
    pyautogui.write(f"{captured_points[2][0]},{captured_points[2][1]}\n")
    pyautogui.typewrite("n\n")
    pyautogui.press('enter')

    search_region_2 = (268, 158, 90, 36) # أرقام مثال: ابدأ من 100,200 وابحث في مساحة 500x600
    image_path_2 = r'C:\Users\ali.nasser\Desktop\Masry_AI_ENG-Agent\screenshots\stirrup distripution rft.jpg'
    find_and_dont_click_check_icon(search_region_2,image_path_2)
    pyautogui.click(x=370, y=175)
    pyautogui.keyDown('ctrl')
    pyautogui.keyDown('a')
    pyautogui.keyUp('a')
    pyautogui.keyUp('ctrl')
    pyautogui.write('50')
    pyautogui.click(x=404, y=171)
    time.sleep(0.1) # انتظار ظهور النافذة
    pyautogui.click(x=404, y=183)
    time.sleep(0.4) # انتظار ظهور النافذة
    pyautogui.click(x=421, y=174)
    time.sleep(0.1) # انتظار ظهور النافذة
    pyautogui.press('enter')
    time.sleep(0.1) # انتظار ظهور النافذة

    search_region_3 = (318, 34, 90, 36) # أرقام مثال: ابدأ من 100,200 وابحث في مساحة 500x600
    image_path_3 = r'C:\Users\ali.nasser\Desktop\Masry_AI_ENG-Agent\screenshots\stirrup disciption style.jpg'
    find_and_click_check_icon(search_region_3,image_path_3)
    pyautogui.click(x=584, y=208)
    time.sleep(0.1) # انتظار ظهور النافذة
    pyautogui.write('STR')
    time.sleep(0.05) # انتظار ظهور النافذة
    pyautogui.mouseDown(x=716, y=51)
    time.sleep(0.1) # خلي الماوس "مضغوط" لمدة 200 مللي ثانية
    pyautogui.mouseUp()
    time.sleep(0.5)

    pyautogui.write(f"{captured_points[1][0]},{captured_points[1][1]+80}\n", interval=0.005)
    pyautogui.write(f"{captured_points[1][0]+100},{captured_points[1][1]+200}\n", interval=0.005)
    pyautogui.write(f"{captured_points[1][0]+1500},{captured_points[1][1]+200}\n", interval=0.005)
    pyautogui.press('enter')

    pyautogui.typewrite("select\n", interval=0.005)
    pyautogui.write(f"{captured_points[1][0]+100},{captured_points[1][1]+200}\n")
    pyautogui.write(f"{captured_points[1][0]-100},{captured_points[1][1]+100}\n")
    pyautogui.write(f"{captured_points[2][0]+100},{captured_points[2][1]-h_beam-100}\n")
    pyautogui.press('enter')
    pyautogui.typewrite("mirror\n", interval=0.005)
    pyautogui.write(f"{(captured_points[2][0]+captured_points[3][0])/2},{captured_points[2][1]}\n", interval=0.005)
    pyautogui.write(f"{(captured_points[2][0]+captured_points[3][0])/2},{captured_points[2][1]-500}\n", interval=0.005)
    pyautogui.typewrite("n\n")

    pyautogui.typewrite("rbcr_distribution\n", interval=0.005)
    pyautogui.typewrite(f"{stirrup_pick_x},-8800\n", interval=0.005)
    pyautogui.press('enter')
    time.sleep(0.4)
    find_and_click_check_icon(search_region_1, image_path_1)
    time.sleep(0.4)
    pyautogui.press('enter')
    pyautogui.write(f"{captured_points[2][0]},{captured_points[2][1]}\n", interval=0.005)
    pyautogui.write(f"{captured_points[3][0]},{captured_points[3][1]}\n", interval=0.005)
    pyautogui.typewrite("n\n")
    pyautogui.press('enter')
    find_and_dont_click_check_icon(search_region_2, image_path_2)
    time.sleep(0.4)
    pyautogui.mouseDown(x=512, y=68)
    pyautogui.mouseUp()
    pyautogui.keyDown('ctrl')
    pyautogui.keyDown('a')
    pyautogui.keyUp('a')
    pyautogui.keyUp('ctrl')
    pyautogui.write('150')
    time.sleep(0.05)
    pyautogui.mouseDown(x=512, y=104)
    time.sleep(0.2) # انتظار ظهور النافذة
    pyautogui.press('enter')
    find_and_click_check_icon(search_region_3,image_path_3)
    pyautogui.click(x=584, y=208)
    time.sleep(0.1) # انتظار ظهور النافذة
    pyautogui.write('STR')
    time.sleep(0.05) # انتظار ظهور النافذة
    pyautogui.mouseDown(x=716, y=51)
    time.sleep(0.1) # خلي الماوس "مضغوط" لمدة 200 مللي ثانية
    pyautogui.mouseUp()
    time.sleep(1)

    pyautogui.write(f"{captured_points[2][0]},{captured_points[2][1]+80}\n", interval=0.005)
    pyautogui.write(f"{captured_points[2][0]+300},{captured_points[2][1]+400}\n", interval=0.005)
    pyautogui.write(f"{captured_points[2][0]+1700},{captured_points[2][1]+400}\n", interval=0.005)
    pyautogui.press('enter')
    pyautogui.typewrite("select\n", interval=0.005)
    pyautogui.write(f"{captured_points[2][0]},{captured_points[2][1]+990}\n", interval=0.005)
    pyautogui.write(f"{captured_points[3][0]},{captured_points[3][1]+990}\n", interval=0.005)
    pyautogui.press('enter')
    pyautogui.typewrite("e\n")

def handle_continuous_beam(captured_points):
    data = get_engineering_data()
    w_beams = data["w_beams"] 
    h_beams = data["h_beams"]  
    beam_section_tags = data["beam_section_tags"]
    unique_sections = data["unique_sections_to_draw"]

    w_beam = w_beams[1]
    h_beam = h_beams[1]
    x_offset = get_section_x_offset(beam_section_tags[1], unique_sections, 5000)
    stirrup_pick_x = x_offset + 25 # التقاط الكانة المترصّدة للقطاع الثاني
    
    pyautogui.typewrite("rbcr_distribution\n", interval=0.005)
    pyautogui.typewrite(f"{stirrup_pick_x},-8800\n")
    pyautogui.press('enter')
    time.sleep(0.4)
    search_region_1 = (376, 83, 90, 36) # أرقام مثال: ابدأ من 100,200 وابحث في مساحة 500x600
    image_path_1 = r'C:\Users\ali.nasser\Desktop\Masry_AI_ENG-Agent\screenshots\stirrup dis.jpg'
    find_and_click_check_icon(search_region_1,image_path_1)
    time.sleep(0.4)
    pyautogui.press('enter')
    pyautogui.write(f"{captured_points[5][0]},{captured_points[5][1]}\n", interval=0.005)
    pyautogui.write(f"{captured_points[6][0]},{captured_points[6][1]}\n", interval=0.005)
    pyautogui.typewrite("n\n")
    pyautogui.press('enter')

    search_region_2 = (268, 158, 90, 36) # أرقام مثال: ابدأ من 100,200 وابحث في مساحة 500x600
    image_path_2 = r'C:\Users\ali.nasser\Desktop\Masry_AI_ENG-Agent\screenshots\stirrup distripution rft.jpg'
    find_and_dont_click_check_icon(search_region_2,image_path_2)
    pyautogui.click(x=370, y=175)
    pyautogui.keyDown('ctrl')
    pyautogui.keyDown('a')
    pyautogui.keyUp('a')
    pyautogui.keyUp('ctrl')
    pyautogui.write('50')
    time.sleep(0.4)
    pyautogui.click(x=404, y=171)
    time.sleep(0.2)
    pyautogui.click(x=404, y=183)
    time.sleep(0.4)
    pyautogui.click(x=421, y=174)
    time.sleep(0.2)
    pyautogui.press('enter')
    time.sleep(0.1)

    search_region_3 = (318, 34, 90, 36) # أرقام مثال: ابدأ من 100,200 وابحث في مساحة 500x600
    image_path_3 = r'C:\Users\ali.nasser\Desktop\Masry_AI_ENG-Agent\screenshots\stirrup disciption style.jpg'
    find_and_click_check_icon(search_region_3,image_path_3)
    pyautogui.click(x=584, y=208)
    time.sleep(0.1)
    pyautogui.write('STR')
    time.sleep(0.2)
    pyautogui.mouseDown(x=716, y=51)
    pyautogui.mouseUp()
    time.sleep(1)
    pyautogui.write(f"{captured_points[5][0]},{captured_points[5][1]+80}\n", interval=0.005)
    pyautogui.write(f"{captured_points[5][0]+100},{captured_points[5][1]+200}\n", interval=0.005)
    pyautogui.write(f"{captured_points[5][0]+1500},{captured_points[5][1]+200}\n", interval=0.005)
    pyautogui.press('enter')

    pyautogui.typewrite("select\n", interval=0.005)
    pyautogui.write(f"{captured_points[5][0]+100},{captured_points[5][1]+200}\n", interval=0.005)
    pyautogui.write(f"{captured_points[5][0]-100},{captured_points[5][1]+100}\n", interval=0.005)
    pyautogui.write(f"{captured_points[6][0]+100},{captured_points[6][1]-h_beam-100}\n", interval=0.005)
    pyautogui.press('enter')
    pyautogui.typewrite("mirror\n", interval=0.005)
    pyautogui.write(f"{(captured_points[6][0]+captured_points[7][0])/2},{captured_points[6][1]}\n", interval=0.005)
    pyautogui.write(f"{(captured_points[6][0]+captured_points[7][0])/2},{captured_points[6][1]-500}\n", interval=0.005)
    pyautogui.typewrite("n\n")

    pyautogui.typewrite("rbcr_distribution\n", interval=0.005)
    pyautogui.typewrite(f"{stirrup_pick_x},-8800\n", interval=0.005)
    pyautogui.press('enter')
    time.sleep(0.4)
    find_and_click_check_icon(search_region_1,image_path_1)
    time.sleep(0.4)
    pyautogui.press('enter')
    pyautogui.write(f"{captured_points[6][0]},{captured_points[6][1]}\n", interval=0.005)
    pyautogui.write(f"{captured_points[7][0]},{captured_points[7][1]}\n", interval=0.005)
    pyautogui.typewrite("n\n")
    pyautogui.press('enter')

    find_and_dont_click_check_icon(search_region_2,image_path_2)
    time.sleep(0.4)
    pyautogui.mouseDown(x=512, y=68)
    pyautogui.mouseUp()
    pyautogui.keyDown('ctrl')
    pyautogui.keyDown('a')
    pyautogui.keyUp('a')
    pyautogui.keyUp('ctrl')
    pyautogui.write('150')
    time.sleep(0.2)
    pyautogui.mouseDown(x=512, y=104)
    time.sleep(0.2)
    pyautogui.press('enter')

    find_and_click_check_icon(search_region_3,image_path_3)
    pyautogui.click(x=584, y=208)
    time.sleep(0.1)
    pyautogui.write('STR')
    time.sleep(0.2)
    pyautogui.mouseDown(x=716, y=51)
    pyautogui.mouseUp()
    time.sleep(1)
    pyautogui.write(f"{captured_points[6][0]},{captured_points[6][1]+80}\n", interval=0.005)
    pyautogui.write(f"{captured_points[6][0]+300},{captured_points[6][1]+400}\n", interval=0.005)
    pyautogui.write(f"{captured_points[6][0]+1700},{captured_points[6][1]+400}\n", interval=0.005)
    pyautogui.press('enter')
    pyautogui.typewrite("select\n", interval=0.005)
    pyautogui.write(f"{captured_points[6][0]},{captured_points[6][1]+990}\n", interval=0.005)
    pyautogui.write(f"{captured_points[7][0]},{captured_points[7][1]+990}\n", interval=0.005)
    pyautogui.press('enter')
    pyautogui.typewrite("e\n")

def handle_more_continuous_beam(captured_points):
    data = get_engineering_data()
    w_beams = data["w_beams"] 
    h_beams = data["h_beams"]  
    beam_section_tags = data["beam_section_tags"]
    unique_sections = data["unique_sections_to_draw"]
    
    w_beam = w_beams[2]
    h_beam = h_beams[2]
    x_offset = get_section_x_offset(beam_section_tags[2], unique_sections, 5000)
    stirrup_pick_x = x_offset + 25 # التقاط الكانة التابعة لقطاع السبان الثالث

    pyautogui.typewrite("rbcr_distribution\n")
    pyautogui.typewrite(f"{stirrup_pick_x},-8800\n")
    pyautogui.press('enter')
    time.sleep(0.4)

    search_region_1 = (376, 83, 90, 36) # أرقام مثال: ابدأ من 100,200 وابحث في مساحة 500x600
    image_path_1 = r'C:\Users\ali.nasser\Desktop\Masry_AI_ENG-Agent\screenshots\stirrup dis.jpg'
    find_and_click_check_icon(search_region_1,image_path_1)
    time.sleep(0.4)
    pyautogui.press('enter')
    pyautogui.write(f"{captured_points[9][0]},{captured_points[9][1]}\n")
    pyautogui.write(f"{captured_points[10][0]},{captured_points[10][1]}\n")
    pyautogui.typewrite("n\n")
    pyautogui.press('enter')

    search_region_2 = (268, 158, 90, 36) # أرقام مثال: ابدأ من 100,200 وابحث في مساحة 500x600
    image_path_2 = r'C:\Users\ali.nasser\Desktop\Masry_AI_ENG-Agent\screenshots\stirrup distripution rft.jpg'
    find_and_dont_click_check_icon(search_region_2,image_path_2)
    pyautogui.click(x=370, y=175)
    pyautogui.keyDown('ctrl')
    pyautogui.keyDown('a')
    pyautogui.keyUp('a')
    pyautogui.keyUp('ctrl')
    pyautogui.write('50')
    time.sleep(0.05)
    pyautogui.click(x=404, y=171)
    time.sleep(0.2)
    pyautogui.click(x=404, y=183)
    time.sleep(0.2)
    time.sleep(0.4)
    pyautogui.click(x=421, y=174)
    time.sleep(0.2)
    pyautogui.press('enter')
    time.sleep(0.1)

    search_region_3 = (318, 34, 90, 36) # أرقام مثال: ابدأ من 100,200 وابحث في مساحة 500x600
    image_path_3 = r'C:\Users\ali.nasser\Desktop\Masry_AI_ENG-Agent\screenshots\stirrup disciption style.jpg'
    find_and_click_check_icon(search_region_3,image_path_3)
    pyautogui.click(x=584, y=208)
    time.sleep(0.1)
    pyautogui.write('STR')
    time.sleep(0.05)
    pyautogui.mouseDown(x=716, y=51)
    pyautogui.mouseUp()
    time.sleep(1)
    pyautogui.write(f"{captured_points[9][0]},{captured_points[9][1]+80}\n")
    pyautogui.write(f"{captured_points[9][0]+100},{captured_points[9][1]+200}\n")
    pyautogui.write(f"{captured_points[9][0]+1500},{captured_points[9][1]+200}\n")
    pyautogui.press('enter')

    pyautogui.typewrite("select\n", interval=0.005)
    pyautogui.write(f"{captured_points[9][0]+100},{captured_points[9][1]+200}\n")
    pyautogui.write(f"{captured_points[9][0]-100},{captured_points[9][1]+100}\n")
    pyautogui.write(f"{captured_points[10][0]+100},{captured_points[10][1]-h_beam-100}\n")
    pyautogui.press('enter')
    pyautogui.typewrite("mirror\n", interval=0.005)
    pyautogui.write(f"{(captured_points[10][0]+captured_points[11][0])/2},{captured_points[10][1]}\n")
    pyautogui.write(f"{(captured_points[10][0]+captured_points[11][0])/2},{captured_points[10][1]-500}\n")
    pyautogui.typewrite("n\n")

    pyautogui.typewrite("rbcr_distribution\n", interval=0.005)
    pyautogui.typewrite(f"{stirrup_pick_x},-8800\n")
    pyautogui.press('enter')
    time.sleep(0.4)
    
    find_and_click_check_icon(search_region_1,image_path_1)
    time.sleep(0.4)
    pyautogui.press('enter')
    pyautogui.write(f"{captured_points[10][0]},{captured_points[10][1]}\n")
    pyautogui.write(f"{captured_points[11][0]},{captured_points[11][1]}\n")
    pyautogui.typewrite("n\n")
    pyautogui.press('enter')

    find_and_dont_click_check_icon(search_region_2,image_path_2)
    time.sleep(0.4)
    pyautogui.mouseDown(x=512, y=68)
    pyautogui.mouseUp()
    pyautogui.keyDown('ctrl')
    pyautogui.keyDown('a')
    pyautogui.keyUp('a')
    pyautogui.keyUp('ctrl')
    pyautogui.write('150')
    time.sleep(0.05)
    pyautogui.mouseDown(x=512, y=104)
    time.sleep(0.2)
    pyautogui.press('enter')

    find_and_click_check_icon(search_region_3,image_path_3)
    pyautogui.click(x=584, y=208)
    time.sleep(0.1)
    pyautogui.write('STR')
    time.sleep(0.05)
    pyautogui.mouseDown(x=716, y=51)
    pyautogui.mouseUp()
    time.sleep(1)
    pyautogui.write(f"{captured_points[10][0]},{captured_points[10][1]+80}\n")
    pyautogui.write(f"{captured_points[10][0]+300},{captured_points[10][1]+400}\n")
    pyautogui.write(f"{captured_points[10][0]+1700},{captured_points[10][1]+400}\n")
    pyautogui.press('enter')
    pyautogui.typewrite("select\n", interval=0.005)
    pyautogui.write(f"{captured_points[10][0]},{captured_points[10][1]+990}\n")
    pyautogui.write(f"{captured_points[11][0]},{captured_points[11][1]+990}\n")
    pyautogui.press('enter')
    pyautogui.typewrite("e\n")

#التسليح الرئيسي السفلي
def draw_bottom_reinforcement_single_section():
    # 1. Fetch data and check conditions
    data = get_engineering_data()
    if not data:
        print("❌ Data failure.")
        return

    unique_sections = data["unique_sections_to_draw"]
    if len(unique_sections) != 1:
        print("Skipping: Multi-section detected.")
        return

    print("🔥  Enjoy!!")

    # 2. Base structural parameters
    cover = 25
    bar_dia = 16
    ld = 60 * bar_dia
    max_commercial_length = 12000

    h_beam = data["h_beams"][0]
    clear_spans = data["clear_spans"]
    c_side_start = data["c_side_start"]
    mid_columns = data["mid_columns"]
    c_side_end = data["c_side_end"]

    y_top = 0
    y_bottom = -h_beam

    # 3. Build cumulative column X coordinates
    current_x = 0
    column_points = []
    column_points.append((current_x, current_x + c_side_start))
    current_x += c_side_start

    for i in range(len(clear_spans)):
        current_x += clear_spans[i]
        col_w = mid_columns[i] if i < len(mid_columns) else c_side_end
        column_points.append((current_x, current_x + col_w))
        current_x += col_w

    absolute_start_x = column_points[0][0]
    absolute_end_x = column_points[-1][1]
    final_bar_end_x = absolute_end_x - cover

    # ----------------------------------------------------
    # 🔥 GUI Automation Initialization (Runs Once)
    # ----------------------------------------------------

    # 4. Unified Rebar Generation Loop
    current_bar_start_x = absolute_start_x + cover
    bar_index = 1

    last_bar_end_point = None
    

    while current_bar_start_x < final_bar_end_x:
        pyautogui.click(x=700, y=10)
        time.sleep(0.1) 
        pyautogui.press('esc')
        time.sleep(0.1)
        pyautogui.typewrite("rbcr_def_bar_bv ", interval=0.005)
        time.sleep(1) 

        search_region_7 = (0, 0, 277, 169) 
        image_path_7 = r'C:\Users\ali.nasser\Desktop\Masry_AI_ENG-Agent\screenshots\Reinforcment elev.PNG'
        find_and_dont_click_skip_icon(search_region_7, image_path_7)
        pyautogui.click(x=218, y=206)
        time.sleep(0.2) 

        pyautogui.click(x=310, y=60)
        time.sleep(0.1) 
        pyautogui.click(x=310, y=80)
        time.sleep(0.1) 

        pyautogui.click(x=490, y=60)
        time.sleep(0.1) 
        pyautogui.click(x=490, y=80)
        time.sleep(0.1) 

        pyautogui.click(x=550, y=167)
        time.sleep(0.1) # Ready to receive points in AutoCAD command line

        needed_horizontal_for_final = absolute_end_x - current_bar_start_x - cover
        
        is_first = (bar_index == 1)
        left_leg = (h_beam - (2 * cover)) if is_first else 0
        right_leg_check = h_beam - (2 * cover)
        
        can_reach_final = (needed_horizontal_for_final + right_leg_check <= max_commercial_length) if not is_first else False
        
        # Array to hold the points for the current bar execution
        bar_points_sequence = []
        actual_bar_start_x = current_bar_start_x

        # --- CASE A: Final Right L-Bar or single-span U-bar covers the rest ---
        if (is_first and (left_leg + right_leg_check + needed_horizontal_for_final <= max_commercial_length)) or can_reach_final:
            p1 = f"{current_bar_start_x},{y_bottom}" if not is_first else f"{absolute_start_x},{y_top}"
            p2 = f"{absolute_end_x},{y_bottom}" if not is_first else f"{absolute_start_x},{y_bottom}"
            p3 = f"{absolute_end_x},{y_top}" if not is_first else f"{absolute_end_x},{y_bottom}"
            
            if is_first:
                p4 = f"{absolute_end_x},{y_top}"
                bar_points_sequence = [p1, p2, p3, p4]
                total_len = left_leg + needed_horizontal_for_final + right_leg_check
                actual_bar_start_x = absolute_start_x + cover
            else:
                bar_points_sequence = [p1, p2, p3]
                total_len = needed_horizontal_for_final + right_leg_check
                
            
            # Execute drawing automation for Case A
            actual_bar_end_x = absolute_end_x - cover
            pull_p1, pull_p2 = calculate_single_pull_point(actual_bar_start_x, actual_bar_end_x, y_bottom, column_points)
            execute_points_automation(bar_points_sequence, is_first)
            time.sleep(0.4)
            search_region_1 = (634, 342, 684, 353) # أرقام مثال: ابدأ من 100,200 وابحث في مساحة 500x600
            image_path_2 = r'C:\Users\ali.nasser\Desktop\Masry_AI_ENG-Agent\screenshots\yes same.PNG'
            find_and_click_or_skip_icon(search_region_1,image_path_2)
            time.sleep(0.1)


            #خلي بالك الكود بتاع الديسكربشن هنا كوبي
            time.sleep(0.2) 
            pyautogui.click(x=406, y=198)
            pyautogui.write('B1')
            time.sleep(0.05)
            pyautogui.mouseDown(x=585, y=54)
            time.sleep(0.1) # خلي الماوس "مضغوط" لمدة 200 مللي ثانية
            pyautogui.mouseUp()
            time.sleep(0.5)
            pyautogui.typewrite(f"{pull_p1} {pull_p2}  \n", interval=0.005)
            pyautogui.press('esc')
            time.sleep(0.2) 

            mid_p2 = f"{((float(p1.split(',')[0]) + float(p2.split(',')[0])) / 2) - 700},{((float(p1.split(',')[1]) + float(p2.split(',')[1])) / 2) - 3600}"
            m_desc = f"{p1.split(',')[0]},{float(p1.split(',')[1]) - 3400}"
            mid_p = f"{(float(p1.split(',')[0]) + float(p2.split(',')[0])) / 2},{(float(p1.split(',')[1]) + float(p2.split(',')[1])) / 2}"
            pyautogui.typewrite(f'RBCR_DEF_PULL {mid_p} {m_desc} {mid_p2} ', interval=0.005)
            time.sleep(0.1)


            ###############################################################
            pyautogui.press('esc')
            time.sleep(0.2)    

            bar_index += 1
            # --- CASE B: Segmented Bar (Left L-Bar OR Middle Straight Bar) ---
            break
        else:
            max_allowed_horizontal = max_commercial_length - left_leg - (0 if is_first else cover)
            max_allowed_x = current_bar_start_x + max_allowed_horizontal

            chosen_col_index = 0
            for idx, (xl, xr) in enumerate(column_points):
                if xr <= max_allowed_x:
                    chosen_col_index = idx
                else:
                    break

            next_bar_end_x = column_points[chosen_col_index][1] - cover

            # Safety Check
            if next_bar_end_x - ld <= current_bar_start_x and not is_first:
                print("⚠️ Safety Triggered: Forcing bar to next available column face to prevent loop.")
                if chosen_col_index + 1 < len(column_points):
                    chosen_col_index += 1
                    next_bar_end_x = column_points[chosen_col_index][1] - cover

            actual_horizontal = next_bar_end_x - (absolute_start_x + cover if is_first else current_bar_start_x)
            total_len = left_leg + actual_horizontal

            if is_first:
                p1 = f"{absolute_start_x},{y_top}"
                p2 = f"{absolute_start_x},{y_bottom}"
                p3 = f"{column_points[chosen_col_index][1]},{y_bottom}"
                bar_points_sequence = [p1, p2, p3]
                actual_bar_start_x = absolute_start_x + cover
                print(f"📐 Bar {bar_index} (Left L-Shape) -> Total Length: {total_len} mm")
            else:
                p1 = f"{current_bar_start_x},{y_bottom}"
                p2 = f"{column_points[chosen_col_index][1]},{y_bottom}"
                bar_points_sequence = [p1, p2]
                print(f"📐 Bar {bar_index} (Straight Mid Bar) -> Total Length: {total_len} mm")
            actual_bar_end_x = next_bar_end_x
            pull_p1, pull_p2 = calculate_single_pull_point(actual_bar_start_x, actual_bar_end_x, y_bottom, column_points)
            # Execute drawing automation for Case B
            execute_points_automation(bar_points_sequence, is_first)

            # Advance parameters
            previous_start = current_bar_start_x
            current_bar_start_x = next_bar_end_x - ld - 25
            
            if current_bar_start_x <= previous_start:
                print("❌ Loop iteration stalled. Breaking to prevent crash.")
                break
            
            time.sleep(0.4)
            search_region_1 = (634, 342, 684, 353) # أرقام مثال: ابدأ من 100,200 وابحث في مساحة 500x600
            image_path_2 = r'C:\Users\ali.nasser\Desktop\Masry_AI_ENG-Agent\screenshots\yes same.PNG'
            find_and_click_or_skip_icon(search_region_1,image_path_2)
            time.sleep(0.1)

            time.sleep(0.2) 
            #ضيف كود ال ديسكربشن هنا
            pyautogui.click(x=406, y=198)
            pyautogui.write('B1')
            time.sleep(0.05)
            pyautogui.mouseDown(x=585, y=54)
            time.sleep(0.1) # خلي الماوس "مضغوط" لمدة 200 مللي ثانية
            pyautogui.mouseUp()
            time.sleep(0.5)
            pyautogui.typewrite(f"{pull_p1} {pull_p2}  \n", interval=0.005)
            pyautogui.press('esc')
            time.sleep(0.2) 

            mid_p2 = f"{((float(p2.split(',')[0]) + float(p3.split(',')[0])) / 2) - 700},{((float(p2.split(',')[1]) + float(p3.split(',')[1])) / 2) - 3700}"
            m_desc = f"{p1.split(',')[0]},{float(p1.split(',')[1]) - 3500}"
            mid_p = f"{(float(p2.split(',')[0]) + float(p3.split(',')[0])) / 2},{(float(p2.split(',')[1]) + float(p3.split(',')[1])) / 2}"
            pyautogui.typewrite(f'RBCR_DEF_PULL {mid_p} {m_desc} {mid_p2} ', interval=0.005)
            time.sleep(0.1)
            
            ###############################################################
            pyautogui.press('esc')
            time.sleep(0.2)    

            current_bar_start_point = f"{current_bar_start_x + 25},{-h_beam}"
            last_bar_end_point = f"{next_bar_end_x},{-h_beam}"
            if last_bar_end_point is not None:
               dim_text_x = (float(last_bar_end_point.split(',')[0]) + float(current_bar_start_point.split(',')[0])) / 2
               dim_line_position = f"{dim_text_x},{-h_beam - 3700}"
    
               pyautogui.press('esc')
               time.sleep(0.05)
               pyautogui.write('_DIMLINEAR ', interval=0.005)
               time.sleep(0.05)
               pyautogui.typewrite(f"{last_bar_end_point} {current_bar_start_point} {dim_line_position} \n", interval=0.005)
               time.sleep(0.1)
               pyautogui.press('esc')
               time.sleep(0.05)
            
            bar_index += 1

#حساب نقاط ال Description
def calculate_single_pull_point(bar_start_x, bar_end_x, y_bottom, column_points):
    """ Computes 1/3 span description coordinates safely below the rebar """
    bar_center_x = (bar_start_x + bar_end_x) / 2
    span_start_x = bar_start_x
    span_end_x = bar_end_x

    for i in range(len(column_points) - 1):
        if column_points[i][1] <= bar_center_x <= column_points[i+1][0]:
            span_start_x = column_points[i][1]
            span_end_x = column_points[i+1][0]
            break

    current_span_length = span_end_x - span_start_x
    pull_x1 = span_start_x + 600
    pull_y1 = y_bottom - 360
    
    # الـ Pull Points بقوا جاهزين هنا لو حبيت تكتبهم في الكوماند لاين
    return f"{pull_x1},{pull_y1}", f"{pull_x1 + 200},{pull_y1}"

def execute_points_automation(points, is_first_bar):
    """
    Helper function to handle pyautogui input sequence for rebar points.
    Injects "s " between the first and second point of EVERY bar.
    """
    for idx, pt in enumerate(points):
        # Type the point coordinate into AutoCAD
        pyautogui.typewrite(f"{pt} ", interval=0.005)
        time.sleep(0.1)
        
        # 🔥 MODIFIED: Inject "s " after the FIRST point of EVERY single bar
        if idx == 0:
            pyautogui.typewrite("s ", interval=0.005)
            time.sleep(0.1)
            
    # Send Enter to finish the current bar description loop in ASD
    pyautogui.press('enter')
    time.sleep(0.2)

#التسليح الرئيسي العلوي
def draw_top_reinforcement_single_section():
    # 1. Fetch data and check conditions
    data = get_engineering_data()
    if not data:
        print("❌ Data failure.")
        return

    unique_sections = data["unique_sections_to_draw"]
    if len(unique_sections) != 1:
        print("Skipping: Multi-section detected.")
        return

    print("🔥 Intelligent TOP Reinforcement Engine Activated...")

    # 2. Base structural parameters (Top Bar Modifications)
    cover = 25
    bar_dia = 16
    # تعديل الـ ld للتسليح العلوي مضروب في 1.3
    ld = 60 * bar_dia * 1.3  
    
    # قائمة الأطوال التجارية المفروضة بالترتيب المطلوب للبحث عن التوقف المثالي
    commercial_lengths_pool = [12000, 6000, 8000, 9000, 4000, 3000]

    h_beam = data["h_beams"][0]
    clear_spans = data["clear_spans"]
    c_side_start = data["c_side_start"]
    mid_columns = data["mid_columns"]
    c_side_end = data["c_side_end"]

    # قلب الإحداثيات لفوق: الحديد العلوي هيمشي على منسوب y_top
    y_top = 0
    y_bottom = -h_beam

    # 3. Build cumulative column X coordinates & Extract Spans Clear Mid-Thirds
    current_x = 0
    column_points = []
    column_points.append((current_x, current_x + c_side_start))
    current_x += c_side_start

    span_mid_thirds = []  # لتخزين حدود الثلث الأوسط لكل بحر كمرة
    for i in range(len(clear_spans)):
        span_start = current_x
        span_end = current_x + clear_spans[i]
        
        # حساب الثلث الأوسط للبحر الحالي هندسياً
        one_third = clear_spans[i] / 3
        span_mid_thirds.append((span_start + one_third, span_end - one_third))
        
        current_x += clear_spans[i]
        col_w = mid_columns[i] if i < len(mid_columns) else c_side_end
        column_points.append((current_x, current_x + col_w))
        current_x += col_w

    absolute_start_x = column_points[0][0]
    absolute_end_x = column_points[-1][1]
    final_bar_end_x = absolute_end_x - cover

    # 4. Unified Top Rebar Generation Loop
    current_bar_start_x = absolute_start_x + cover
    bar_index = 1
    last_bar_end_point = None

    while current_bar_start_x < final_bar_end_x:
        if last_bar_end_point is not None:
            current_bar_start_point = f"{current_bar_start_x + 25},{y_top - 25}"
            dim_text_x = (float(last_bar_end_point.split(',')[0]) + float(current_bar_start_point.split(',')[0])) / 2
            dim_line_position = f"{dim_text_x},{y_top - 1800}" 
            
            pyautogui.press('esc')
            time.sleep(0.05)
            pyautogui.write('_DIMLINEAR ', interval=0.005)
            time.sleep(0.05)
            pyautogui.typewrite(f"{last_bar_end_point} {current_bar_start_point} {dim_line_position} \n", interval=0.005)
            time.sleep(0.1)
            pyautogui.press('esc')

        needed_horizontal_for_final = absolute_end_x - current_bar_start_x - cover
        
        is_first = (bar_index == 1)
        left_leg = (h_beam - (2 * cover)) if is_first else 0
        right_leg_check = h_beam - (2 * cover)
        
        # --- CASE A: السيخ العلوي الأول (Full U-Shape) أو السيخ الأخير (Final Right L-Shape) ---
        can_reach_final = (needed_horizontal_for_final + right_leg_check <= 12000) if not is_first else False
        
        if (is_first and (left_leg + right_leg_check + needed_horizontal_for_final <= 12000)) or can_reach_final:
            p1 = f"{absolute_start_x},{y_bottom}" if is_first else f"{current_bar_start_x},{y_top}"
            p2 = f"{absolute_start_x},{y_top}" if is_first else f"{absolute_end_x - cover + 25},{y_top}"
            p3 = f"{absolute_end_x - cover + 25},{y_top}" if is_first else f"{absolute_end_x - cover + 25},{y_bottom}"
            
            if is_first:
                p4 = f"{absolute_end_x - cover + 25},{y_bottom}"
                bar_points_sequence = [p1, p2, p3, p4]
                actual_bar_start_x = absolute_start_x + cover
            else:
                bar_points_sequence = [p1, p2, p3]
                actual_bar_start_x = current_bar_start_x
                
            actual_bar_end_x = absolute_end_x - cover
            
            # تشغيل الأوتوماسيون للسيخ النهائي
            execute_top_bar_flow(bar_points_sequence, actual_bar_start_x, actual_bar_end_x, y_top,y_bottom, column_points, is_first, last_bar_end_point)
            break

        # --- CASE B: السيخ مقطوع (Segmented Bar) بناءً على شرط الـ 85% من الـ ld جوة الثلث الأوسط ---
        else:
            chosen_commercial_length = None
            next_bar_end_x = None
            
            # لف على حمام الأطوال التجارية بالترتيب المطلوب
            for length in commercial_lengths_pool:
                theoretical_horizontal = length - left_leg - (0 if is_first else cover)
                theoretical_end_x = current_bar_start_x + theoretical_horizontal
                
                # 🔥 فحص هندسي: حساب مدى احتواء الثلث الأوسط على 85% على الأقل من طول الوصلة ld
                is_valid_stop = False
                for t_start, t_end in span_mid_thirds:
                    # تمديد الوصلة هندسياً: بداية الوصلة ونهايتها
                    ld_start = theoretical_end_x - ld
                    ld_end = theoretical_end_x
                    
                    # إيجاد حدود منطقة التقاطع بين الـ ld والثلث الأوسط للبحر الحالي
                    overlap_start = max(ld_start, t_start)
                    overlap_end = min(ld_end, t_end)
                    overlap_length = max(0, overlap_end - overlap_start)
                    
                    # الشرط الجديد: هل طول التقاطع يغطي على الأقل 85% من الـ ld الكاملة؟
                    if (t_start <= theoretical_end_x <= t_end) or (overlap_length >= (0.50 * ld)):
                        is_valid_stop = True
                        break
                
                # لو الطول ده حقق الشرط الآمن، اعتمده فوراً واقفل البحث
                if is_valid_stop and theoretical_end_x < final_bar_end_x:
                    chosen_commercial_length = length
                    next_bar_end_x = theoretical_end_x
                    print(f"🎯 Perfect Match Found! Bar {bar_index} approved with Commercial Length: {length}mm")
                    break
            
            # Fallback Safety: حماية الطوارئ
            if chosen_commercial_length == None:
                # لو مفيش طول حقق، بنشوف أقرب طول تجاري متاح يوصلنا لأقرب ثلث أوسط متاح بدل الإجبار على 12م
                chosen_commercial_length = 8000 if (current_bar_start_x + 8000 < final_bar_end_x) else 12000
                theoretical_horizontal = chosen_commercial_length - left_leg - (0 if is_first else cover)
                next_bar_end_x = current_bar_start_x + theoretical_horizontal
                print(f"⚠️ Safety Warning: No strict mid-third split found for Bar {bar_index}. Opting for commercial length: {chosen_commercial_length}mm")

            if is_first:
                p1 = f"{absolute_start_x},{y_bottom}"
                p2 = f"{absolute_start_x},{y_top}"
                p3 = f"{next_bar_end_x + 25},{y_top}"  # زيادة الـ 25 مم هنا
                bar_points_sequence = [p1, p2, p3]
                actual_bar_start_x = absolute_start_x + cover
            else:
                p1 = f"{current_bar_start_x},{y_top}"
                p2 = f"{next_bar_end_x + 25},{y_top}"  # زيادة الـ 25 مم هنا
                bar_points_sequence = [p1, p2]
                actual_bar_start_x = current_bar_start_x

            actual_bar_end_x = next_bar_end_x
            
            # تشغيل الأوتوماسيون للسيخ الحالي
            execute_top_bar_flow(bar_points_sequence, actual_bar_start_x, actual_bar_end_x, y_top, y_bottom, column_points, is_first, last_bar_end_point)

            # التجهيز للسيخ القادم: ترحيل وإعداد النقط للدايمنشن التالي
            last_bar_end_point = f"{next_bar_end_x + 25},{y_top - 25}"
            
            previous_start = current_bar_start_x
            current_bar_start_x = next_bar_end_x - ld - 25
            
            if current_bar_start_x <= previous_start:
                print("❌ Loop iteration stalled. Breaking to prevent crash.")
                break
                
            bar_index += 1


def execute_top_bar_flow(points, bar_start_x, bar_end_x, y_top,y_bottom, column_points, is_first_bar, last_bar_end_point):
    """ Standardized Drawing, Dimensioning and Pull Descriptions Flow for Top Rebar """
    # 1. استدعاء وتجهيز نافذة الـ ASD في الأوتوكاد
    pyautogui.click(x=700, y=10)
    time.sleep(0.1) 
    pyautogui.press('esc')
    time.sleep(0.1)
    pyautogui.typewrite("rbcr_def_bar_bv ", interval=0.005)
    time.sleep(1) 
    search_region_7 = (0, 0, 277, 169) 
    image_path_7 = r'C:\Users\ali.nasser\Desktop\Masry_AI_ENG-Agent\screenshots\Reinforcment elev.PNG'
    find_and_dont_click_skip_icon(search_region_7, image_path_7)



    # اختيار الخصائص الثابتة
    pyautogui.click(x=218, y=206)
    time.sleep(0.2) 
    pyautogui.click(x=310, y=60)
    time.sleep(0.1) 
    pyautogui.click(x=310, y=80)
    time.sleep(0.1) 
    pyautogui.click(x=490, y=60)
    time.sleep(0.1) 
    pyautogui.click(x=490, y=80)
    time.sleep(0.1) 
    pyautogui.click(x=550, y=167)
    time.sleep(0.1) 

    # 🔥 2. رسم مسار السيخ صريح ورا بعض بمسافات (تم إلغاء حرف الـ s تماماً بناءً على طلبك)
    for pt in points:
        pyautogui.typewrite(f"{pt} ", interval=0.005)
        time.sleep(0.1)
            
    pyautogui.press('enter')
    time.sleep(0.2)
    # 3. حساب نقط التفريد والـ Description أوتوماتيكياً (مرحل)
    bar_center_x = (bar_start_x + bar_end_x) / 2
    span_start_x = bar_start_x
    span_end_x = bar_end_x

    for i in range(len(column_points) - 1):
        if column_points[i][1] <= bar_center_x <= column_points[i+1][0]:
            span_start_x = column_points[i][1]
            span_end_x = column_points[i+1][0]
            break

    current_span_length = span_end_x - span_start_x
    pull_x1 = span_end_x - 600
    pull_y1 = y_bottom - 180
    
    mid_p = f"{pull_x1},{pull_y1}"
    m_desc = f"{pull_x1 - 200 },{pull_y1}"
    mid_p2 = f"{pull_x1},{pull_y1 + 3700}"

    time.sleep(0.4)
    search_region_1 = (634, 342, 684, 353) # أرقام مثال: ابدأ من 100,200 وابحث في مساحة 500x600
    image_path_2 = r'C:\Users\ali.nasser\Desktop\Masry_AI_ENG-Agent\screenshots\yes same.PNG'
    find_and_click_or_skip_icon(search_region_1,image_path_2)

    time.sleep(0.2) 
    pyautogui.click(x=406, y=198)
    pyautogui.write('T1') 
    time.sleep(0.05)
    pyautogui.mouseDown(x=585, y=54)
    time.sleep(0.1) 
    pyautogui.mouseUp()
    time.sleep(0.5)
    pyautogui.typewrite(f"{mid_p} {m_desc} m \n", interval=0.005)

    pyautogui.press('esc')
    time.sleep(0.2)

    m_desc = f"{bar_start_x},{y_bottom - 1400}"
    mid_p2 = f"{bar_center_x - 600 },{y_bottom - 1600}"

    if is_first_bar:
        m_desc = f"{bar_start_x},{y_bottom - 2000}"
    else:
        pass
    mid_p = f"{bar_center_x + 100},{y_top - 25}"
    # تنفيذ أمر تفريد الكتابة
    pyautogui.press('esc')
    time.sleep(0.1)
    pyautogui.typewrite('RBCR_DEF_PULL ', interval=0.005)
    time.sleep(0.1)
    pyautogui.typewrite(f"{mid_p} {m_desc} {mid_p2} ", interval=0.005) 
    time.sleep(0.1)
    pyautogui.press('esc')
    time.sleep(0.1)

    
#### مرحلة التشغيل فقط

#الاتصال بال ASD
try:
    # الاتصال المباشر بالأوتوكاد عبر الـ COM (أسرع وأنظف بكثير)
    acad = win32com.client.GetActiveObject("AutoCAD.Application.20")
    doc = acad.ActiveDocument
    print(f"Connected to AutoCAD: {doc.Name}")
except Exception as e:
    print("❌ Cannot connect to AutoCAD. Make sure it is open.")
    sys.exit()

#التأكد من ان اللغة انجليزي
ensure_english_keyboard()
time.sleep(1)

#تفعيل نافذة ال asd ووضعها في حالة fullscreen
for attempt in range(10): # هيحاول 10 مرات كحد أقصى
    try:
        acad.Visible = True
        acad.WindowState = 3 # Maximized
        print("✅ AutoCAD window activated and maximized successfully!")
        break # لو نجح، يخرج من اللوب ويكمل رسم فوراً
    except pywintypes.com_error as e:
        # لو الأوتوكاد رفض (Call was rejected)، هينتظر ثانية ويحاول تاني
        if e.hresult == -2147418111:
            print(f"⏳ AutoCAD is busy (Attempt {attempt+1}/10)... Retrying in 1 sec.")
            time.sleep(1)
        else:
            # لو فيه خطأ مفاجئ تاني خالص، يطبع الخطأ ويقفل الكود فوراً للأمان
            print(f"❌ Unexpected COM error: {e}")
            sys.exit()
else:
    # السطر ده مش بيتنفذ إلا لو الـ 10 محاولات خلصوا كلهم وفشلوا
    print("❌ Critical Error: AutoCAD rejected the call 10 times. Script stopped for safety.")
    sys.exit() # إيقاف الكود بالكامل فوراً

#رسم السيكشن
if __name__ == "__main__":
    pts=draw_section_with_approved_breaklines()

#رسم الكانات
time.sleep(0.1)
stirrups_rft()

#توزيع الكانات
if pts:
        stirrups_rft_description(pts)

#    كمرة اكثر من بحر واحد
if len(pts) > 6:
     handle_continuous_beam(pts)
else: 
        print(f"⚠️ Stopped: points count is , which is NOT > 6")
       
#    كمرة اكثر من بحرين 
if len(pts) > 10:
     handle_more_continuous_beam(pts)
else: 
        print(f"⚠️ Stopped: points count is , which is NOT > 6")

#رسم حديد التسليح الرئيسي
data = get_engineering_data()
unique_sections = data["unique_sections_to_draw"]
if len(unique_sections) == 1:
    print("🎯Main rft in progress")
    
    master_sec = unique_sections[0]
    w_sec = master_sec["w"]
    h_sec = master_sec["h"]

    draw_bottom_reinforcement_single_section()
    draw_top_reinforcement_single_section()
    # (هنا هتحط الكود الجديد اللي أنت عاوزه بالكامل)
    pass


