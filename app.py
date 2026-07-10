import streamlit as st
import urllib.parse

# 1. تخصيص التصميم بالألوان المطلوبة (بيج دافئ وأبيض فاتح)
minimal_beige_css = """
<style>
/* الخلفية الرئيسية للموقع باللون البيج الفاتح الناعم */
[data-testid="stAppViewContainer"] {
    background-color: #f7f4eb !important; /* لون بيج ناعم جداً */
}

/* القائمة الجانبية بلون أبيض ناصع ونظيف */
[data-testid="stSidebar"] {
    background-color: #ffffff !important;
    border-right: 1px solid #eadecc;
}

/* تنسيق النصوص بألوان خشبية/بنية دافئة متناسقة مع البيج */
h1, h2, h3, p, label {
    color: #4a3e3d !important;
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
}

/* مظهر بطاقات المنتجات باللون الأبيض مع زوايا ناعمة وظل خفيف */
.product-card {
    background-color: #ffffff;
    padding: 15px;
    border-radius: 8px;
    box-shadow: 0 2px 5px rgba(74,62,61,0.05);
    margin-bottom: 15px;
    border: 1px solid #f1eae0;
    text-align: center;
}

.product-price {
    color: #8c7a6b;
    font-weight: bold;
    margin-top: 8px;
    margin-bottom: 8px;
    font-size: 1.1em;
}
</style>
"""
st.markdown(minimal_beige_css, unsafe_allow_html=True)

# 2. إعداد الذاكرة لحفظ المنتجات والسلة
if 'cart_items' not in st.session_state:
    st.session_state.cart_items = []

# المنتجات الافتراضية للمتجر
if 'custom_products' not in st.session_state:
    st.session_state.custom_products = [
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
        }
    ]

# 3. القائمة الجانبية (عربة التسوق والفلترة ولوحة التحكم)
st.sidebar.title("M i n i m a l  S h o p")
st.sidebar.write("---")

# تصفية الفئات
category = st.sidebar.selectbox("الفئة / Category", ["الكل", "فخار", "منسوجات", "إكسسوارات"])

st.sidebar.write("---")
st.sidebar.subheader("عربة التسوق 🛒")

total_price = 0

if len(st.session_state.cart_items) == 0:
    st.sidebar.caption("العربة فارغة حالياً.")
else:
    for item in st.session_state.cart_items:
        st.sidebar.write(f"- {item['name']} ({item['price']}$)")
        total_price += item['price']
    
    st.sidebar.write(f"### الإجمالي: {total_price}$")
    
    # رقم الهاتف الخاص بك (بدون أصفار بالبداية أو علامة +)
    my_whatsapp_number = "201234567890" 
    
    order_text = "مرحباً، أود طلب المنتجات التالية من المتجر:\n"
    for item in st.session_state.cart_items:
        order_text += f"- {item['name']} ({item['price']}$)\n"
    order_text += f"\nإجمالي الحساب: {total_price}$"
    
    encoded_text = urllib.parse.quote(order_text)
    whatsapp_url = f"https://wa.me{my_whatsapp_number}?text={encoded_text}"
    
    st.sidebar.markdown(f'<a href="{whatsapp_url}" target="_blank"><button style="width:100%; padding:10px; background-color:#25D366; color:white; border:none; border-radius:4px; font-weight:bold; cursor:pointer;">إتمام الطلب عبر واتساب 💬</button></a>', unsafe_allow_html=True)
    
    if st.sidebar.button("إفراغ السلة", use_container_width=True):
        st.session_state.cart_items = []
        st.rerun()

# ميزة إضافة المنتجات يدويًا للمدير داخل القائمة الجانبية
st.sidebar.write("---")
with st.sidebar.expander("➕ إضافة منتج جديد (لوحة المدير)"):
    new_name = st.text_input("اسم المنتج:")
    new_price = st.number_input("السعر ($):", min_value=1, value=10)
    new_cat = st.selectbox("الفئة:", ["فخار", "منسوجات", "إكسسوارات"])
    new_desc = st.text_input("وصف قصير:")
    new_img = st.text_input("رابط الصورة المباشر:", value="https://unsplash.com")
    
    if st.button("نشر المنتج بالمتجر ✨", use_container_width=True):
        if new_name and new_img:
            new_prod = {
                "name": new_name,
                "price": int(new_price),
                "cat": new_cat,
                "desc": new_desc,
                "image": new_img
            }
            st.session_state.custom_products.append(new_prod)
            st.success("تمت إضافة المنتج بنجاح!")
            st.rerun()

# 4. المحتوى الرئيسي للمتجر
st.title("The Handmade Studio .")
st.caption("قطع فريدة صُنعت يدوياً بكل حب وبساطة وبألوان طبيعية دافئة.")
st.write("---")

# تصفية المعروضات بناءً على الفئة المختارة
filtered_products = [p for p in st.session_state.custom_products if category == "الكل" or p["cat"] == category]

# عرض المنتجات في عمودين بنمط Minimal البيج والأبيض
if len(filtered_products) == 0:
    st.info("لا توجد منتجات متوفرة في هذه الفئة حالياً.")
else:
    cols = st.columns(2)
    for index, prod in enumerate(filtered_products):
        with cols[index % 2]:
            # عرض صورة المنتج
            st.image(prod['image'], use_container_width=True)
            
            # تفاصيل المنتج وتصميمه البيج والأبيض
            st.markdown(f"""
            <div class="product-card">
                <h3>{prod['name']}</h3>
                <p>{prod['desc']}</p>
                <div class="product-price">{prod['price']}$</div>
            </div>
            """, unsafe_allow_html=True)
            
            # زر الإضافة للسلة
            if st.button(f"إضافة للسلة", key=f"btn_{index}", use_container_width=True):
                st.session_state.cart_items.append({"name": prod['name'], "price": prod['price']})
                st.toast(f"تمت إضافة {prod['name']} إلى السلة! 🌾")
                st.rerun()

st.write("---")
st.caption("© 2026 Minimal Handmade Store. All rights reserved.")

