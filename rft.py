import pyautogui
import ctypes
import time
import sys
from read_cad import get_engineering_data 

# --- 1. SETTINGS & SAFETY ---
pyautogui.PAUSE = 0.15
pyautogui.FAILSAFE = True
time.sleep(3)
w_beam=300
h_beam=700
def find_and_dont_click_check_icon(search_region, image_path, timeout=5):

    start_time = time.time() # تسجيل وقت البداية
    
    print(f"🔍 جاري البحث عن الأيقونة... (المدة المتاحة: {timeout} ثانية)")
    
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
                return True # نجحنا، اخرج من الدالة
            
        except Exception as e:
            # بنتجاهل الأخطاء العادية أثناء البحث عشان ميتوقفش الكود
            pass

        # التحقق من الوقت: لو عدينا الـ Timeout نوقف بحث
        if time.time() - start_time > timeout:
            return False
            
        time.sleep(0.2) # استراحة بسيطة عشان المعالج (CPU) ميرفعش حرارة

def find_and_click_check_icon(search_region, image_path, timeout=5):

    start_time = time.time() # تسجيل وقت البداية
    
    print(f"🔍 جاري البحث عن الأيقونة... (المدة المتاحة: {timeout} ثانية)")
    
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
                return True # نجحنا، اخرج من الدالة
            
        except Exception as e:
            # بنتجاهل الأخطاء العادية أثناء البحث عشان ميتوقفش الكود
            pass

        # التحقق من الوقت: لو عدينا الـ Timeout نوقف بحث
        if time.time() - start_time > timeout:
            print("⚠️ انتهى الوقت ولم يتم العثور على الأيقونة.")
            return False
            
        time.sleep(0.2) # استراحة بسيطة عشان المعالج (CPU) ميرفعش حرارة
time.sleep(0.2)
#stirrups_rft()
def stirrups_rft_description():
    data = get_engineering_data()
    w_beam = data["w_beam"] 
    search_region_3 = (318, 34, 90, 36) # أرقام مثال: ابدأ من 100,200 وابحث في مساحة 500x600
    image_path_3 = r'C:\Users\CompuMarts\OneDrive\Desktop\Masry_AI_ENG-Agent\screenshots\stirrup disciption style.jpg'
    search_region_2 = (268, 158, 90, 36) # أرقام مثال: ابدأ من 100,200 وابحث في مساحة 500x600
    image_path_2 = r'C:\Users\CompuMarts\OneDrive\Desktop\Masry_AI_ENG-Agent\screenshots\stirrup distripution rft.jpg'
    p_des = f"{int(w_beam + 1800)},-8800"
    p1 = 300,0
    captured_points2 = 1633.33,0
    p3= 2966.66,0
    find_and_dont_click_check_icon(search_region_2,image_path_2)
    time.sleep(0.4)
    pyautogui.mouseDown(x=512, y=68)
    pyautogui.mouseDown(x=512, y=68)
    pyautogui.mouseUp()
    time.sleep(0.3)
    pyautogui.write('150')
    time.sleep(0.2) # انتظار ظهور النافذة
    #pyautogui.mouseDown(x=512, y=104)
    #time.sleep(0.2) # انتظار ظهور النافذة
    #pyautogui.press('enter')
    




stirrups_rft_description()