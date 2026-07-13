import streamlit as st
import urllib.parse
from PIL import Image

# 1. واجهة تصميم فائقة العصرية ومخصصة للغة العربية والألوان الدافئة
aesthetic_store_css = """
<style>
/* خلفية الموقع ناعمة ومريحة للعين */
[data-testid="stAppViewContainer"] {
    background-color: #faf7f2 !important;
}

/* قائمة جانبية بيضاء نظيفة ومحددة بخط ناعم */
[data-testid="stSidebar"] {
    background-color: #ffffff !important;
    border-right: 1px solid #efeae4;
}

/* خطوط متناسقة وألوان نصوص خشبية داكنة راقية */
h1, h2, h3, p, label, span {
    color: #4a3f35 !important;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
    text-align: right;
}

/* بطاقات عرض المنتجات بتصميم انسيابي مذهل وبسيط في المعرض */
.product-card {
    background-color: #ffffff;
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0 4px 20px rgba(74,63,53,0.02);
    margin-bottom: 25px;
    border: 1px solid #f4eee6;
    text-align: center;
}

.product-title {
    font-size: 1.3em;
    font-weight: bold;
    color: #4a3f35;
    margin-top: 10px;
    text-align: center;
}

.product-price {
    color: #b58d63;
    font-weight: 700;
    font-size: 1.25em;
    margin-top: 10px;
    text-align: center;
}

/* تنسيق زر الواتساب الأخضر الخاص بالشراء */
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
    box-shadow: 0 4px 10px rgba(18,140,126,0.15);
}
</style>
"""
st.markdown(aesthetic_store_css, unsafe_allow_html=True)

# 2. إدارة ذاكرة المنتجات وسلة التسوق والمنتج المختار الحالي
if 'cart_items' not in st.session_state:
    st.session_state.cart_items = []

if 'selected_product' not in st.session_state:
    st.session_state.selected_product = None  # لمعرفة هل العميل داخل صفحة منتج أم في المعرض الرئيسي

if 'custom_products' not in st.session_state:
    # إعداد المنتجات الافتراضية مع إضافة ميزة الألوان المتعددة لكل منتج
    st.session_state.custom_products = [
        {
            "id": 0,
            "name": "مشبك شعر أنيق 🏷️", 
            "price": 20, 
            "cat": "💍 إكسسوارات", 
            "desc": "أضيفي لمسة من الأناقة لإطلالتك مع مشبك الشعر العصري بتصميم رخامي راقٍ. يتميز بثبات قوي، وخفة وزن، وراحة كاملة في الاستخدام اليومي أو المناسبات.",
            "colors": ["رخامي بيج", "أخضر زيتوني", "أبيض صدف", "وردي ناعم"],
            "image": "https://picsum.photos"
        },
        {
            "id": 1,
            "name": "كوب فخار مصقول 🏺", 
            "price": 150, 
            "cat": "🏺 فخار", 
            "desc": "طين طبيعي مصقول ومُشكل يدوياً بعناية فائقة. رفيق مثالي لمشروباتك الساخنة اليومية ويتحمل الحرارة العالية.",
            "colors": ["بني ترابي", "رمادي مطفي", "أسود ملكي"],
            "image": "https://picsum.photos"
        },
        {
            "name": "حقيبة كتف قطنية 🧵", 
            "id": 2,
            "price": 350, 
            "cat": "🧵 منسوجات", 
            "desc": "حقيبة يدوية منسوجة من خيوط القطن الطبيعي 100% بتصميم بوهيمي واسع وعصري يناسب جميع الطلعات.",
            "colors": ["أوف وايت", "خردلي دافئ", "رمادي فاتح"],
            "image": "https://picsum.photos"
        }
    ]

# 3. القائمة الجانبية (عربة التسوق والتحكم)
st.sidebar.title("متجر الأناقة البسيطة")
st.sidebar.caption("قطع فريدة صُنعت بكل حب وبساطة")
st.sidebar.write("---")

# زر العودة للمعرض الرئيسي يظهر دائماً في العربة إذا كان المستخدم يتصفح منتجاً
if st.session_state.selected_product is not None:
    if st.sidebar.button("⬅️ العودة للمعرض الرئيسي", use_container_width=True):
        st.session_state.selected_product = None
        st.rerun()

category = st.sidebar.selectbox("تصفح الفئات", ["✨ الكل", "🏺 فخار", "🧵 منسوجات", "💍 إكسسوارات"])

st.sidebar.write("---")
st.sidebar.subheader("عربة التسوق 🛒")

total_price = 0

if len(st.session_state.cart_items) == 0:
    st.sidebar.caption("العربة فارغة حالياً.")
else:
    for item in st.session_state.cart_items:
        st.sidebar.write(f"• {item['name']} ({item['color']}) - {item['price']} ج.م")
        total_price += item['price']
    
    st.sidebar.write(f"### الإجمالي: {total_price} ج.م")
    
    # ضع رقم الواتساب الخاص بك هنا (مفتاح الدولة بدون أصفار بالبداية أو علامة +)
    my_whatsapp_number = "201234567890" 
    
    order_text = "مرحباً، أود طلب المنتجات التالية من المتجر:\n"
    for item in st.session_state.cart_items:
        order_text += f"- {item['name']} (اللون: {item['color']}) بسعر {item['price']} ج.م\n"
    order_text += f"\nإجمالي الحساب بالكامل: {total_price} ج.م"
    
    encoded_text = urllib.parse.quote(order_text)
    whatsapp_url = f"https://wa.me{my_whatsapp_number}?text={encoded_text}"
    
    st.sidebar.markdown(f'<a href="{whatsapp_url}" target="_blank" class="whatsapp-btn">إتمام الطلب عبر واتساب 💬</a>', unsafe_allow_html=True)
    st.sidebar.write("")
    
    if st.sidebar.button("إفراغ السلة", use_container_width=True):
        st.session_state.cart_items = []
        st.rerun()

# 4. إدارة طريقة العرض: إما صفحة تفاصيل المنتج أو المعرض العام
if st.session_state.selected_product is not None:
    # ---- صفحة تفاصيل المنتج المستقلة ----
    prod = st.session_state.selected_product
    
    st.title(prod['name'])
    st.write("---")
    
    # تقسيم الصفحة إلى جزأين: اليمين للصورة واليسار للتفاصيل والألوان
    col1, col2 = st.columns([1.2, 1])
    
    with col1:
        st.image(prod['image'], use_container_width=True)
        
    with col2:
        st.subheader("تفاصيل القطعة:")
        st.write(prod['desc'])
        st.write(f"### السعر: {prod['price']} ج.م")
        
        st.write("---")
        # ميزة اختيار اللون المطلب للعميل
        chosen_color = st.radio("الخيارات والألوان المتوفرة:", prod['colors'])
        
        st.write("")
        # زر الإضافة الفوري داخل صفحة المنتج
        if st.button("إضافة هذه القطعة إلى السلة 🛒", use_container_width=True):
            st.session_state.cart_items.append({"name": prod['name'], "price": prod['price'], "color": chosen_color})
            st.toast(f"تمت إضافة {prod['name']} باللون ({chosen_color}) إلى السلة! ✨")
            st.rerun()
            
        if st.button("🚫 إلغاء والعودة للمعرض", use_container_width=True):
            st.session_state.selected_product = None
            st.rerun()

else:
    # ---- المعرض الرئيسي للمتجر ----
    st.title("The Handmade Studio .")
    st.caption("قطع فريدة صُنعت يدوياً بكل حب وبساطة وبمظهر عصري متكامل.")
    st.write("---")
    
    filtered_products = [p for p in st.session_state.custom_products if category == "✨ الكل" or p["cat"] == category]
    
    if len(filtered_products) == 0:
        st.info("لا توجد منتجات معروضة في هذا القسم حالياً.")
    else:
        cols = st.columns(2)
        for index, prod in enumerate(filtered_products):
            with cols[index % 2]:
                # عرض الصورة
                st.image(prod['image'], use_container_width=True)
                
                # بطاقة المنتج البسيطة بدون تكرار
                st.markdown(f"""
                <div class="product-card">
                    <div class="product-title">{prod['name']}</div>
                    <div class="product-price">{prod['price']} ج.م</div>
                </div>
                """, unsafe_allow_html=True)
                
                # زر الدخول والتفاصيل الذي ينقل العميل لصفحة الألوان
                if st.button("عرض التفاصيل والألوان 🔍", key=f"view_{index}", use_container_width=True):
                    st.session_state.selected_product = prod
                    st.rerun()

st.write("---")
st.caption("© 2026 Modern Minimal Handmade Store. All rights reserved.")
