import streamlit as st
import urllib.parse
from PIL import Image
import json
import os
import base64
from io import BytesIO

# ==================== CONFIGURATION ====================
PRODUCTS_FILE = "products_data.json"

# ==================== DATA PERSISTENCE ====================
def load_products():
    """Load products from JSON file"""
    if os.path.exists(PRODUCTS_FILE):
        try:
            with open(PRODUCTS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data
        except:
            return get_default_products()
    return get_default_products()

def save_products(products):
    """Save products to JSON file"""
    with open(PRODUCTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(products, f, ensure_ascii=False, indent=2)

def get_default_products():
    """Default product catalog with placeholder images"""
    return [
        {
            "id": 0,
            "name": "مشبك شعر أنيق",
            "price": 20,
            "cat": "مشابك شعر",
            "desc": "مشبك شعر أنيق مصنوع من مواد عالية الجودة. تصميم عصري يناسب جميع المناسبات.",
            "colors": [
                {"name": "أحمر", "image": ""},
                {"name": "أخضر", "image": ""},
                {"name": "أسود", "image": ""},
                {"name": "أبيض", "image": ""}
            ]
        },
        {
            "id": 1,
            "name": "ربطة شعر فاخرة",
            "price": 150,
            "cat": "ربطات شعر",
            "desc": "ربطة شعر مصنوعة يدوياً من خامات طبيعية. تصميم فريد وأنيق.",
            "colors": [
                {"name": "ذهبي", "image": ""},
                {"name": "فضي", "image": ""},
                {"name": "وردي", "image": ""}
            ]
        }
    ]

# ==================== INITIALIZE SESSION STATE ====================
if 'cart_items' not in st.session_state:
    st.session_state.cart_items = []

if 'selected_product' not in st.session_state:
    st.session_state.selected_product = None

if 'selected_color_index' not in st.session_state:
    st.session_state.selected_color_index = 0

if 'products' not in st.session_state:
    st.session_state.products = load_products()

# ==================== CSS STYLES ====================
st.markdown("""
<style>
/* Reset and Base */
[data-testid="stAppViewContainer"] {
    background-color: #faf7f2 !important;
}
[data-testid="stSidebar"] {
    background-color: #ffffff !important;
    border-right: 1px solid #efeae4;
}

/* Typography */
h1, h2, h3, p, label, span, div {
    color: #2d2a24 !important;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
}

/* Header */
.store-header {
    text-align: center;
    padding: 30px 0 15px 0;
}
.store-title {
    font-size: 2.8em;
    font-weight: 300;
    letter-spacing: 8px;
    color: #2d2a24;
    margin: 0;
}
.store-subtitle {
    font-size: 0.85em;
    color: #b5a89a;
    letter-spacing: 4px;
    font-weight: 300;
    margin-top: 5px;
}
.store-tagline {
    font-size: 0.9em;
    color: #8a7a6a;
    font-weight: 300;
    letter-spacing: 2px;
    margin-top: 8px;
}

/* Product Card */
.product-card {
    background: #ffffff;
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0 2px 20px rgba(0,0,0,0.04);
    transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    border: 1px solid #f0ebe5;
    margin-bottom: 20px;
}
.product-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 40px rgba(45,42,36,0.08);
}

.product-image-wrapper {
    overflow: hidden;
    background: #f8f5f0;
    aspect-ratio: 1/1;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 10px;
}
.product-image-wrapper img {
    width: 100%;
    height: 100%;
    object-fit: contain;
    transition: transform 0.4s ease;
}
.product-card:hover .product-image-wrapper img {
    transform: scale(1.03);
}

.product-info {
    padding: 18px 20px 20px;
}
.product-category {
    font-size: 0.7em;
    color: #b5a89a;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    font-weight: 500;
}
.product-name {
    font-size: 1.1em;
    font-weight: 600;
    color: #2d2a24;
    margin: 4px 0 6px 0;
}
.product-price {
    font-size: 1.3em;
    font-weight: 600;
    color: #b58d63;
    margin: 6px 0 10px 0;
}
.color-thumbnails {
    display: flex;
    gap: 6px;
    margin: 8px 0;
    flex-wrap: wrap;
}
.color-thumb {
    width: 30px;
    height: 30px;
    border-radius: 50%;
    border: 2px solid #f0ebe5;
    overflow: hidden;
}
.color-thumb img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}
.no-image-placeholder {
    width: 30px;
    height: 30px;
    border-radius: 50%;
    border: 2px solid #f0ebe5;
    background: #e8e0d8;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 10px;
    color: #999;
}

/* Product Detail */
.detail-main-image {
    border-radius: 20px;
    overflow: hidden;
    background: #f8f5f0;
    aspect-ratio: 1/1;
    margin-bottom: 15px;
    padding: 20px;
}
.detail-main-image img {
    width: 100%;
    height: 100%;
    object-fit: contain;
}
.detail-thumbnails {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
}
.detail-thumb {
    width: 70px;
    height: 70px;
    border-radius: 12px;
    overflow: hidden;
    border: 2px solid #f0ebe5;
    cursor: pointer;
    transition: all 0.2s ease;
}
.detail-thumb:hover {
    border-color: #b58d63;
}
.detail-thumb.active {
    border-color: #b58d63;
    border-width: 2.5px;
}
.detail-thumb img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}
.detail-title {
    font-size: 2em;
    font-weight: 300;
    letter-spacing: 1px;
    color: #2d2a24;
}
.detail-price {
    font-size: 1.8em;
    font-weight: 600;
    color: #b58d63;
}
.detail-description {
    color: #6a5f55;
    line-height: 1.8;
    font-size: 0.95em;
}

/* Color option cards in detail */
.color-option-card {
    padding: 12px;
    border: 2px solid #f0ebe5;
    border-radius: 12px;
    text-align: center;
    cursor: pointer;
    transition: all 0.2s ease;
    background: #faf8f5;
}
.color-option-card:hover {
    border-color: #b58d63;
    background: #ffffff;
}
.color-option-card.selected {
    border-color: #b58d63;
    background: #ffffff;
    box-shadow: 0 2px 10px rgba(181, 141, 99, 0.1);
}
.color-option-swatch {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    margin: 0 auto 8px;
    border: 1px solid #e0d6cc;
    overflow: hidden;
}
.color-option-swatch img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

/* Buttons */
.whatsapp-btn {
    display: block;
    width: 100%;
    padding: 14px;
    background: #25D366;
    color: white !important;
    text-align: center;
    text-decoration: none;
    font-weight: 600;
    border-radius: 12px;
    transition: all 0.2s ease;
}
.whatsapp-btn:hover {
    background: #20b85a;
}

/* Footer */
.footer {
    text-align: center;
    padding: 40px 0 20px 0;
    border-top: 1px solid #efeae4;
    margin-top: 40px;
}
.footer-text {
    font-size: 0.85em;
    color: #b5a89a;
    letter-spacing: 1.5px;
    font-weight: 300;
}
.footer-divider {
    width: 40px;
    height: 1px;
    background: #e0d6cc;
    margin: 16px auto;
}

/* Streamlit Overrides */
.stButton > button {
    width: 100% !important;
    border-radius: 12px !important;
    font-weight: 500 !important;
    padding: 12px !important;
}
</style>
""", unsafe_allow_html=True)

# ==================== HELPER FUNCTIONS ====================
def display_image(image_data, width=200, height=200):
    """Display image from base64 or URL"""
    if not image_data:
        return None
    if image_data.startswith('data:image'):
        return image_data
    return image_data

def get_color_image(product, color_index):
    """Get image for a specific color"""
    colors = product.get('colors', [])
    if colors and color_index < len(colors):
        img = colors[color_index].get('image', '')
        if img:
            return img
    return None

# ==================== SIDEBAR ====================
st.sidebar.markdown("""
<div style="padding: 10px 0;">
    <h2 style="font-weight: 300; letter-spacing: 6px; color: #2d2a24; margin: 0; font-size: 1.8em;">VITTA</h2>
    <p style="color: #b5a89a; font-size: 0.65em; letter-spacing: 2px; margin: 4px 0 0 0;">CURATED ACCESSORIES</p>
</div>
""", unsafe_allow_html=True)
st.sidebar.write("---")

# Navigation
page = st.sidebar.radio(
    "Navigate",
    ["🏠 Shop", "📖 About"],
    index=0
)

st.sidebar.write("---")

# Cart
st.sidebar.subheader("Your Cart")
st.sidebar.write("")

total_price = 0
if len(st.session_state.cart_items) == 0:
    st.sidebar.caption("Your cart is empty")
else:
    for item in st.session_state.cart_items:
        st.sidebar.markdown(f"""
        <div style="padding: 8px 0; border-bottom: 1px solid #f5f0eb;">
            <div style="font-weight: 500; font-size: 0.9em;">{item['name']}</div>
            <div style="font-size: 0.8em; color: #b5a89a;">{item['color']} · {item['price']} EGP</div>
        </div>
        """, unsafe_allow_html=True)
        total_price += item['price']
    
    st.sidebar.markdown(f"### Total: {total_price} EGP")
    
    my_whatsapp_number = "201234567890"
    order_text = "Hello Vitta Team,\n\nI would like to order:\n"
    for item in st.session_state.cart_items:
        order_text += f"• {item['name']} ({item['color']}) - {item['price']} EGP\n"
    order_text += f"\nTotal: {total_price} EGP"
    
    encoded_text = urllib.parse.quote(order_text)
    whatsapp_url = f"https://wa.me/{my_whatsapp_number}?text={encoded_text}"
    
    st.sidebar.markdown(f'<a href="{whatsapp_url}" target="_blank" class="whatsapp-btn">Checkout on WhatsApp</a>', unsafe_allow_html=True)
    st.sidebar.write("")
    
    if st.sidebar.button("Clear Cart", use_container_width=True):
        st.session_state.cart_items = []
        st.rerun()

# Admin Panel - IMPROVED
st.sidebar.write("---")
with st.sidebar.expander("⚙️ إدارة المنتجات", expanded=False):
    admin_mode = st.radio("اختر الإجراء:", ["➕ منتج جديد", "🎨 إضافة لون", "✏️ تعديل منتج"])
    
    if admin_mode == "➕ منتج جديد":
        st.markdown("### معلومات المنتج")
        new_name = st.text_input("اسم المنتج")
        new_price = st.number_input("السعر (EGP)", min_value=1, value=50)
        new_cat = st.selectbox("التصنيف", ["مشابك شعر", "ربطات شعر", "إكسسوارات"])
        new_desc = st.text_area("وصف المنتج")
        
        st.markdown("### إضافة لون وصورة")
        color_name = st.text_input("اسم اللون", value="أحمر")
        uploaded_file = st.file_uploader("صورة المنتج بهذا اللون", type=["jpg", "png", "jpeg"])
        
        if st.button("إضافة المنتج", use_container_width=True):
            if new_name and uploaded_file:
                # Convert image to base64
                img = Image.open(uploaded_file)
                buffered = BytesIO()
                img.save(buffered, format="JPEG", quality=80)
                img_str = base64.b64encode(buffered.getvalue()).decode()
                
                new_product = {
                    "id": len(st.session_state.products),
                    "name": new_name,
                    "price": int(new_price),
                    "cat": new_cat,
                    "desc": new_desc,
                    "colors": [{"name": color_name, "image": f"data:image/jpeg;base64,{img_str}"}]
                }
                st.session_state.products.append(new_product)
                save_products(st.session_state.products)
                st.success(f"✅ تم إضافة {new_name} بنجاح!")
                st.rerun()
            else:
                st.error("❌ يرجى إدخال اسم المنتج ورفع صورة")
    
    elif admin_mode == "🎨 إضافة لون":
        existing_names = [p['name'] for p in st.session_state.products]
        if existing_names:
            selected = st.selectbox("اختر المنتج", existing_names)
            new_color_name = st.text_input("اسم اللون الجديد", value="ذهبي")
            uploaded_file = st.file_uploader("صورة المنتج بهذا اللون", type=["jpg", "png", "jpeg"])
            
            if st.button("إضافة اللون", use_container_width=True):
                if selected and new_color_name and uploaded_file:
                    img = Image.open(uploaded_file)
                    buffered = BytesIO()
                    img.save(buffered, format="JPEG", quality=80)
                    img_str = base64.b64encode(buffered.getvalue()).decode()
                    
                    for p in st.session_state.products:
                        if p['name'] == selected:
                            p['colors'].append({
                                "name": new_color_name,
                                "image": f"data:image/jpeg;base64,{img_str}"
                            })
                            break
                    save_products(st.session_state.products)
                    st.success(f"✅ تم إضافة لون {new_color_name} بنجاح!")
                    st.rerun()
                else:
                    st.error("❌ يرجى إدخال اسم اللون ورفع صورة")
        else:
            st.info("لا يوجد منتجات بعد. أضف منتجاً أولاً!")
    
    elif admin_mode == "✏️ تعديل منتج":
        existing_names = [p['name'] for p in st.session_state.products]
        if existing_names:
            selected = st.selectbox("اختر المنتج للتعديل", existing_names)
            
            # Find product
            product_to_edit = None
            for p in st.session_state.products:
                if p['name'] == selected:
                    product_to_edit = p
                    break
            
            if product_to_edit:
                new_name = st.text_input("اسم المنتج", value=product_to_edit['name'])
                new_price = st.number_input("السعر", value=product_to_edit['price'])
                new_cat = st.text_input("التصنيف", value=product_to_edit['cat'])
                new_desc = st.text_area("الوصف", value=product_to_edit['desc'])
                
                if st.button("تحديث المنتج", use_container_width=True):
                    product_to_edit['name'] = new_name
                    product_to_edit['price'] = int(new_price)
                    product_to_edit['cat'] = new_cat
                    product_to_edit['desc'] = new_desc
                    save_products(st.session_state.products)
                    st.success("✅ تم تحديث المنتج!")
                    st.rerun()
        else:
            st.info("لا يوجد منتجات بعد. أضف منتجاً أولاً!")

# ==================== MAIN CONTENT ====================
if page == "📖 About":
    st.markdown("""
    <div style="background: #ffffff; padding: 40px; border-radius: 20px; border: 1px solid #f0ebe5; margin: 20px 0;">
        <h2 style="font-weight: 300; letter-spacing: 2px;">About VITTA</h2>
        <p style="color: #6a5f55; line-height: 2; font-size: 1em;">
            <strong>VITTA</strong> is a curated accessories brand born from a passion for timeless design and exceptional craftsmanship.
        </p>
        <p style="color: #6a5f55; line-height: 2; font-size: 1em;">
            We believe that everyday accessories should be both beautiful and functional. Each piece in our collection is thoughtfully designed to elevate your daily style while providing lasting quality.
        </p>
        <p style="font-weight: 300; letter-spacing: 1px; margin-top: 10px; color: #b58d63;">— The VITTA Team</p>
    </div>
    """, unsafe_allow_html=True)

else:  # Shop Page
    # Store Header
    st.markdown("""
    <div class="store-header">
        <h1 class="store-title">VITTA</h1>
        <p class="store-subtitle">CURATED ACCESSORIES</p>
        <p class="store-tagline">Crafted with care for everyday elegance</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if we're viewing a product detail
    if st.session_state.selected_product is not None:
        product = st.session_state.selected_product
        colors = product.get('colors', [])
        
        if colors:
            current_color_idx = st.session_state.selected_color_index
            if current_color_idx >= len(colors):
                current_color_idx = 0
                st.session_state.selected_color_index = 0
            
            current_color = colors[current_color_idx]
            
            st.markdown("---")
            st.markdown(f'<div class="detail-title">{product["name"]}</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns([1.2, 1])
            
            with col1:
                # Main image
                img_src = current_color.get('image', '')
                if img_src:
                    st.markdown(f'<div class="detail-main-image"><img src="{img_src}" alt="{product["name"]}"></div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="detail-main-image" style="display:flex;align-items:center;justify-content:center;color:#999;">لا توجد صورة</div>', unsafe_allow_html=True)
                
                # Color options
                if len(colors) > 1:
                    st.write("")
                    st.markdown("**الألوان المتاحة:**")
                    
                    # Display color options as cards
                    color_cols = st.columns(min(len(colors), 4))
                    for idx, color in enumerate(colors):
                        with color_cols[idx % len(color_cols)]:
                            is_selected = idx == current_color_idx
                            border_class = "selected" if is_selected else ""
                            img = color.get('image', '')
                            
                            if img:
                                st.markdown(f"""
                                <div class="color-option-card {border_class}" style="cursor: pointer;">
                                    <div class="color-option-swatch"><img src="{img}" alt="{color['name']}"></div>
                                    <div style="font-size: 0.8em; color: #6a5f55;">{color['name']}</div>
                                </div>
                                """, unsafe_allow_html=True)
                            else:
                                st.markdown(f"""
                                <div class="color-option-card {border_class}" style="cursor: pointer;">
                                    <div class="color-option-swatch" style="background: #e8e0d8;"></div>
                                    <div style="font-size: 0.8em; color: #6a5f55;">{color['name']}</div>
                                </div>
                                """, unsafe_allow_html=True)
                            
                            if st.button(f"اختر", key=f"color_btn_{idx}"):
                                st.session_state.selected_color_index = idx
                                st.rerun()
            
            with col2:
                st.markdown(f'<div class="detail-price">{product["price"]} EGP</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="detail-description">{product["desc"]}</div>', unsafe_allow_html=True)
                
                st.write("")
                selected_color_name = current_color["name"]
                st.markdown(f"**اللون المختار:** {selected_color_name}")
                
                if st.button("🛒 أضف إلى السلة", use_container_width=True):
                    st.session_state.cart_items.append({
                        "name": product['name'],
                        "price": product['price'],
                        "color": selected_color_name
                    })
                    st.toast(f"✨ تم إضافة {product['name']} - {selected_color_name} إلى السلة!")
                    st.rerun()
                
                if st.button("↩️ العودة للمتجر", use_container_width=True):
                    st.session_state.selected_product = None
                    st.session_state.selected_color_index = 0
                    st.rerun()
    else:
        # Product Grid
        filtered_products = st.session_state.products
        
        if len(filtered_products) == 0:
            st.info("لا توجد منتجات. استخدم لوحة الإدارة لإضافة منتجات!")
        else:
            cols = st.columns(2)
            for index, product in enumerate(filtered_products):
                with cols[index % 2]:
                    # Get first color image for card
                    first_color = product['colors'][0] if product['colors'] else None
                    img_src = first_color.get('image', '') if first_color else ''
                    
                    # Create color thumbnails
                    color_thumbs = ""
                    for color in product['colors'][:4]:
                        img = color.get('image', '')
                        if img:
                            color_thumbs += f'<div class="color-thumb"><img src="{img}" alt="{color["name"]}"></div>'
                        else:
                            color_thumbs += f'<div class="no-image-placeholder">?</div>'
                    
                    st.markdown(f"""
                    <div class="product-card">
                        <div class="product-image-wrapper">
                            {f'<img src="{img_src}" alt="{product["name"]}">' if img_src else '<span style="color:#999;">لا توجد صورة</span>'}
                        </div>
                        <div class="product-info">
                            <div class="product-category">{product['cat']}</div>
                            <div class="product-name">{product['name']}</div>
                            <div class="color-thumbnails">{color_thumbs}</div>
                            <div class="product-price">{product['price']} EGP</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button("🔍 عرض التفاصيل", key=f"view_{product['id']}", use_container_width=True):
                        st.session_state.selected_product = product
                        st.session_state.selected_color_index = 0
                        st.rerun()
    
    # Footer
    st.markdown("""
    <div class="footer">
        <div class="footer-divider"></div>
        <div class="footer-text">Crafted with care for everyday elegance.</div>
        <div style="margin-top: 10px;">
            <span style="color: #d4c9bf; font-size: 0.7em; letter-spacing: 1px;">VITTA — EST. 2024</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
