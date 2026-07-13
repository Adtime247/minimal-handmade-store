import streamlit as st
import urllib.parse
from PIL import Image

# 1. واجهة تصميم عصرية وفائقة البساطة (Modern Minimal UI)
modern_style_css = """
<style>
/* خلفية الموقع حديثة وخفيفة جداً */
[data-testid="stAppViewContainer"] {
    background-color: #fcfbfa !important;
}

/* قائمة جانبية بلون أبيض صافي وفاخر */
[data-testid="stSidebar"] {
    background-color: #ffffff !important;
    border-right: 1px solid #f2eee9;
}

/* خطوط عصرية داكنة وراقية */
h1, h2, h3, p, label {
    color: #3d3535 !important;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}

/* بطاقات المنتجات بنمط عصري عائم وهادئ */
.product-card {
    background-color: #ffffff;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(61,53,53,0.03);
    margin-bottom: 20px;
    border: 1px solid #f7f5f2;
    text-align: center;
    transition: transform 0.2s ease;
}

.product-price {
    color: #9c8470;
    font-weight: 600;
    margin-top: 10px;
    font-size: 1.15em;
}

/* زر إتمام الشراء عبر الواتساب */
.whatsapp-btn {
    display: block;
    width: 100%;
    padding: 12px;
    background-color: #128C7E;
    color: white !important;
    text-align: center;
    text-decoration: none;
    font-weight: bold;
    border-radius: 8px;
    border: none;
    box-shadow: 0 2px 6px rgba(18,140,126,0.2);
}
</style>
"""
st.markdown(modern_style_css, unsafe_allow_html=True)

# 2. تهيئة مخزن الذاكرة الذكي للمتجر والمنتجات
if 'cart_items' not in st.session_state:
    st.session_state.cart_items = []

if 'custom_products' not in st.session_state:
    # منتجات افتراضية ذكية ومستقرة لبدء المتجر
    st.session_state.custom_products = [
        {
            "name": "كوب فخار رمادي ناعم", 
            "price": 25, 
            "cat": "🏺 فخار", 
            "desc": "طين طبيعي مصقول ومُشكل يدوياً بعناية.",
            "image": "https://picsum.photos"
        },
        {
            "name": "حقيبة كتف قطنية منسوجة", 
            "price": 45, 
            "cat": "🧵 منسوجات", 
            "desc": "خيوط قطن طبيعية ومغزولة 100%.",
            "image": "https://picsum.photos"
        },
        {
            "name": "سوار من الفضة المطفي", 
            "price": 30, 
            "cat": "💍 إكسسوارات", 
            "desc": "تصميم هندسي بسيط ومصنوع من الفضة النقية.",
            "image": "https://picsum.photos"
        }
    ]

# 3. بناء القائمة الجانبية (الفلترة، عربة التسوق، لوحة التحكم)
st.sidebar.title("M i n i m a l  S h o p")
st.sidebar.caption("البرمجة تلتقي بالفن اليدوي")
st.sidebar.write("---")

category = st.sidebar.selectbox("الفئة / Category", ["✨ الكل", "🏺 فخار", "🧵 منسوجات", "💍 إكسسوارات"])

st.sidebar.write("---")
st.sidebar.subheader("عربة التسوق 🛒")

total_price = 0

if len(st.session_state.cart_items) == 0:
    st.sidebar.caption("العربة فارغة حالياً.")
else:
    for item in st.session_state.cart_items:
        st.sidebar.write(f"- {item['name']} ({item['price']}£)")
        total_price += item['price']
    
    st.sidebar.write(f"### الإجمالي: {total_price}£")
    
    # ضع رقمك هنا مباشرة (رمز الدولة بدون أصفار أو علامة +)
    my_whatsapp_number = "201234567890" 
    
    order_text = "مرحباً، أود طلب المنتجات التالية من المتجر:\n"
    for item in st.session_state.cart_items:
        order_text += f"- {item['name']} ({item['price']}£)\n"
    order_text += f"\nإجمالي الحساب: {total_price}£"
    
    encoded_text = urllib.parse.quote(order_text)
    whatsapp_url = f"https://wa.me{my_whatsapp_number}?text={encoded_text}"
    
    st.sidebar.markdown(f'<a href="{whatsapp_url}" target="_blank" class="whatsapp-btn">إتمام الطلب عبر واتساب 💬</a>', unsafe_allow_html=True)
    st.sidebar.write("")
    
    if st.sidebar.button("إفراغ السلة", use_container_width=True):
        st.session_state.cart_items = []
        st.rerun()

# تحديث لوحة التحكم لتدعم رفع ملفات الصور مباشرة من جهازك
st.sidebar.write("---")
with st.sidebar.expander("➕ إضافة منتج جديد (لوحة المدير)"):
    new_name = st.text_input("اسم المنتج الجديد:")
    new_price = st.number_input("السعر بالجنيه المصري (£):", min_value=1, value=15)
    new_cat = st.selectbox("اختر الفئة التابع لها:", ["🏺 فخار", "🧵 منسوجات", "💍 إكسسوارات"])
    new_desc = st.text_input("اكتب وصفاً مختصراً:")
    
    # ميزة رفع الملفات الجديدة
    uploaded_file = st.file_uploader("ارفع صورة المنتج من حاسوبك:", type=["jpg", "png", "jpeg"])
    
    if st.button("نشر وعرض المنتج بالمتجر ✨", use_container_width=True):
        if new_name:
            # التحقق من أن المستخدم رفع صورة، وإلا نضع صورة افتراضية مؤقتة
            img_to_save = "https://picsum.photos"
            if uploaded_file is not None:
                img_to_save = Image.open(uploaded_file)
                
            new_prod = {
                "name": new_name,
                "price": int(new_price),
                "cat": new_cat,
                "desc": new_desc,
                "image": img_to_save
            }
            st.session_state.custom_products.append(new_prod)
            st.success("تم رفع الصورة وإضافة المنتج بنجاح!")
            st.rerun()
        else:
            st.warning("يرجى كتابة اسم المنتج على الأقل لتتم الإضافة.")

# 4. بناء الواجهة والمعرض الرئيسي للموقع حياً
st.title("The Handmade Studio .")
st.caption("قطع فريدة صُنعت يدوياً بكل حب وبساطة وبمظهر عصري متكامل.")
st.write("---")

filtered_products = [p for p in st.session_state.custom_products if category == "✨ الكل" or p["cat"] == category]

if len(filtered_products) == 0:
    st.info("لا توجد معروضات متوفرة في هذا القسم حالياً.")
else:
    cols = st.columns(2)
    for index, prod in enumerate(filtered_products):
        with cols[index % 2]:
            # عرض الصورة سواء كانت رابط إنترنت أو ملف تم رفعه من الجهاز
            if isinstance(prod['image'], str):
                st.image(prod['image'], use_container_width=True)
            else:
                st.image(prod['image'], use_container_width=True)
            
            # عرض بطاقة السعر والوصف العصرية
            st.markdown(f"""
            <div class="product-card">
                <h3>{prod['name']}</h3>
                <p>{prod['desc']}</p>
                <div class="product-price">{prod['price']}£</div>
            </div>
            """, unsafe_allow_html=True)
            
            # زر الإضافة الفوري للسلة لشراء المنتج
            if st.button(f"إضافة للسلة", key=f"btn_{index}", use_container_width=True):
                st.session_state.cart_items.append({"name": prod['name'], "price": prod['price']})
                st.toast(f"تمت إضافة {prod['name']} إلى السلة! 🌾")
                st.rerun()

st.write("---")
st.caption("© 2026 Modern Minimal Handmade Store. All rights reserved.")
