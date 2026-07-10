import streamlit as st

# 1. كود CSS لتطبيق تصميم الـ Minimal (البسيط والأنيق)
minimal_css = """
<style>
/* ضبط الخلفية العامة للموقع باللون الأبيض الهادئ */
[data-testid="stAppViewContainer"] {
    background-color: #faf9f6 !important; /* لون أوف وايت ناعم */
}

/* ضبط القائمة الجانبية بلون رمادي فاتح جداً */
[data-testid="stSidebar"] {
    background-color: #f4f4f2 !important;
    border-right: 1px solid #e4e4e2;
}

/* تنسيق النصوص بألوان داكنة مريحة للعين */
h1, h2, h3, p, label {
    color: #2b2b2a !important;
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
}

/* مظهر مخصص لبطاقات المنتجات */
.product-card {
    background-color: #ffffff;
    padding: 20px;
    border-radius: 4px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    margin-bottom: 20px;
    border: 1px solid #eee;
    text-align: center;
}

.product-price {
    color: #8c8c88;
    font-weight: bold;
    margin-bottom: 10px;
}
</style>
"""

# حقن تصميم الـ Minimal في الموقع
st.markdown(minimal_css, unsafe_allow_html=True)

# 2. القائمة الجانبية (عربة التسوق والفلترة)
st.sidebar.title("M i n i m a l  S h o p")
st.sidebar.write("---")
category = st.sidebar.selectbox("الفئة / Category", ["الكل", "فخار", "منسوجات", "إكسسوارات"])

st.sidebar.write("---")
st.sidebar.subheader("عربة التسوق 🛒")
# إنشاء سلة تسوق وهمية بسيطة في الذاكرة
if 'cart' not in st.session_state:
    st.session_state.cart = []

if len(st.session_state.cart) == 0:
    st.sidebar.caption("العربة فارغة حالياً.")
else:
    for item in st.session_state.cart:
        st.sidebar.write(f"- {item}")
    if st.sidebar.button("إفراغ السلة"):
        st.session_state.cart = []
        st.rerun()

# 3. المحتوى الرئيسي للمتجر
st.title("The Handmade Studio .")
st.caption("قطع فريدة صُنعت يدوياً بكل حب وبساطة.")
st.write("---")

# بيانات المنتجات (بشكل مبسط كأمثلة)
products = [
    {"name": "كوب فخار رمادي ناعم", "price": "25$", "cat": "فخار", "desc": "طين طبيعي مشكل يدوياً."},
    {"name": "حقيبة كتف قطنية منسوجة", "price": "45$", "cat": "منسوجات", "desc": "خيوط قطن طبيعية 100%."},
    {"name": "سوار من الفضة المطفي", "price": "30$", "cat": "إكسسوارات", "desc": "تصميم هندسي بسيط وعصري."},
    {"name": "وعاء نباتات طيني كبير", "price": "35$", "cat": "فخار", "desc": "مناسب للنباتات الداخلية الحية."}
]

# تصفية المنتجات بناءً على خيار المستخدم من القائمة الجانبية
filtered_products = [p for p in products if category == "الكل" or p["cat"] == category]

# عرض المنتجات في شبكة (Columns) نظيفة
cols = st.columns(2)  # تقسيم الشاشة إلى عمودين متساويين

for index, prod in enumerate(filtered_products):
    # التبديل بين العمود الأول والثاني تلقائياً
    with cols[index % 2]:
        # إنشاء حاوية مخصصة للمنتج باستخدام HTML
        st.markdown(f"""
        <div class="product-card">
            <h3>{prod['name']}</h3>
            <p>{prod['desc']}</p>
            <div class="product-price">{prod['price']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # زر إضافة المنتج للسلة (تحت البطاقة)
        if st.button(f"إضافة للسلة", key=f"btn_{index}"):
            st.session_state.cart.append(prod['name'])
            st.toast(f"تمت إضافة {prod['name']} إلى السلة! 🌾")
            st.rerun()

st.write("---")
st.caption("© 2026 Minimal Handmade Store. All rights reserved.")
