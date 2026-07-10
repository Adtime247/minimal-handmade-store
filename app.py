import streamlit as st
import urllib.parse

# 1. كود CSS لتطبيق تصميم الـ Minimal (البسيط والأنيق) وتحسين مظهر الصور
minimal_css = """
<style>
[data-testid="stAppViewContainer"] {
    background-color: #faf9f6 !important;
}
[data-testid="stSidebar"] {
    background-color: #f4f4f2 !important;
    border-right: 1px solid #e4e4e2;
}
h1, h2, h3, p, label {
    color: #2b2b2a !important;
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
}
.product-card {
    background-color: #ffffff;
    padding: 15px;
    border-radius: 4px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    margin-bottom: 15px;
    border: 1px solid #eee;
    text-align: center;
}
.product-price {
    color: #8c8c88;
    font-weight: bold;
    margin-top: 8px;
    margin-bottom: 8px;
}
</style>
"""
st.markdown(minimal_css, unsafe_allow_html=True)

# 2. إعدادات سلة التسوق في الذاكرة (Session State)
if 'cart_items' not in st.session_state:
    st.session_state.cart_items = []

# 3. القائمة الجانبية (عربة التسوق والفلترة)
st.sidebar.title("M i n i m a l  S h o p")
st.sidebar.write("---")
category = st.sidebar.selectbox("الفئة / Category", ["الكل", "فخار", "منسوجات", "إكسسوارات"])

st.sidebar.write("---")
st.sidebar.subheader("عربة التسوق 🛒")

total_price = 0

if len(st.session_state.cart_items) == 0:
    st.sidebar.caption("العربة فارغة حالياً.")
else:
    # عرض المنتجات وحساب الإجمالي
    for item in st.session_state.cart_items:
        st.sidebar.write(f"- {item['name']} ({item['price']}$)")
        total_price += item['price']
    
    st.sidebar.write("---")
    st.sidebar.write(f"### الإجمالي: {total_price}$")
    
    # ضع رقم هاتفك هنا بدلاً من الرقم الافتراضي (تأكد من كتابة رمز الدولة بدون أصفار أو علامة +)
    my_whatsapp_number = "201234567890" 
    
    # تجهيز رسالة الواتساب تلقائياً
    order_text = "مرحباً، أود طلب المنتجات التالية من المتجر:\n"
    for item in st.session_state.cart_items:
        order_text += f"- {item['name']} ({item['price']}$)\n"
    order_text += f"\nإجمالي الحساب: {total_price}$"
    
    # تحويل النص ليكون صالحاً للروابط
    encoded_text = urllib.parse.quote(order_text)
    whatsapp_url = f"https://wa.me{my_whatsapp_number}?text={encoded_text}"
    
    # أزرار السلة
    st.sidebar.markdown(f'<a href="{whatsapp_url}" target="_blank"><button style="width:100%; padding:10px; background-color:#25D366; color:white; border:none; border-radius:4px; font-weight:bold; cursor:pointer;">إتمام الطلب عبر واتساب 💬</button></a>', unsafe_allow_html=True)
    
    if st.sidebar.button("إفراغ السلة", use_container_width=True):
        st.session_state.cart_items = []
        st.rerun()

# 4. المحتوى الرئيسي للمتجر
st.title("The Handmade Studio .")
st.caption("قطع فريدة صُنعت يدوياً بكل حب وبساطة.")
st.write("---")

# بيانات المنتجات مع صور حقيقية مجانية ومباشرة من موقع Unsplash
products = [
    {
        "name": "كوب فخار رمادي ناعم", 
        "price": 25, 
        "cat": "فخار", 
        "desc": "طين طبيعي مشكل يدوياً.",
        "image": "https://unsplash.com"
    },
    {
        "name": "حقيبة كتف قطنية منسوجة", 
        "price": 45, 
        "cat": "منسوجات", 
        "desc": "خيوط قطن طبيعية 100%.",
        "image": "https://unsplash.com"
    },
    {
        "name": "سوار من الفضة المطفي", 
        "price": 30, 
        "cat": "إكسسوارات", 
        "desc": "تصميم هندسي بسيط وعصري.",
        "image": "https://unsplash.com"
    },
    {
        "name": "وعاء نباتات طيني كبير", 
        "price": 35, 
        "cat": "فخار", 
        "desc": "مناسب للنباتات الداخلية الحية.",
        "image": "https://unsplash.com"
    }
]

# تصفية المنتجات بناءً على التصنيف
filtered_products = [p for p in products if category == "الكل" or p["cat"] == category]

# عرض المنتجات في عمودين نظيفين
cols = st.columns(2)

for index, prod in enumerate(filtered_products):
    with cols[index % 2]:
        # عرض صورة المنتج أولاً بدقة عالية وتنسيق Minimal
        st.image(prod['image'], use_container_width=True)
        
        # معلومات المنتج أسفل الصورة
        st.markdown(f"""
        <div class="product-card">
            <h3>{prod['name']}</h3>
            <p>{prod['desc']}</p>
            <div class="product-price">{prod['price']}$</div>
        </div>
        """, unsafe_allow_html=True)
        
        # زر الإضافة
        if st.button(f"إضافة للسلة", key=f"btn_{index}", use_container_width=True):
            st.session_state.cart_items.append({"name": prod['name'], "price": prod['price']})
            st.toast(f"تمت إضافة {prod['name']} إلى السلة! 🌾")
            st.rerun()

st.write("---")
st.caption("© 2026 Minimal Handmade Store. All rights reserved.")
