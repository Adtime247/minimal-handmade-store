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
    if os.path.exists(PRODUCTS_FILE):
        try:
            with open(PRODUCTS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def save_products(products):
    with open(PRODUCTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(products, f, ensure_ascii=False, indent=2)

# ==================== HELPER FUNCTION FOR IMAGE ====================
def process_image(uploaded_file):
    """Convert uploaded image to base64 JPEG"""
    if uploaded_file is None:
        return None
    
    try:
        # Open image
        img = Image.open(uploaded_file)
        
        # Convert to RGB if necessary (for PNG with alpha)
        if img.mode in ('RGBA', 'LA', 'P'):
            # Create white background
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize if too large (max 800x800)
        max_size = 800
        if img.width > max_size or img.height > max_size:
            img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
        
        # Save as JPEG with compression
        buffered = BytesIO()
        img.save(buffered, format="JPEG", quality=85, optimize=True)
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return f"data:image/jpeg;base64,{img_str}"
    
    except Exception as e:
        st.error(f"خطأ في معالجة الصورة: {e}")
        return None

# ==================== INITIALIZE SESSION STATE ====================
if 'cart_items' not in st.session_state:
    st.session_state.cart_items = []

if 'selected_product' not in st.session_state:
    st.session_state.selected_product = None

if 'selected_color_index' not in st.session_state:
    st.session_state.selected_color_index = 0

if 'products' not in st.session_state:
    st.session_state.products = load_products()

if 'temp_colors' not in st.session_state:
    st.session_state.temp_colors = []

# ==================== CSS STYLES ====================
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background-color: #faf7f2 !important;
}
[data-testid="stSidebar"] {
    background-color: #ffffff !important;
    border-right: 1px solid #efeae4;
}
h1, h2, h3, p, label, span, div {
    color: #2d2a24 !important;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
}
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
.stButton > button {
    width: 100% !important;
    border-radius: 12px !important;
    font-weight: 500 !important;
    padding: 12px !important;
}
</style>
""", unsafe_allow_html=True)

# ==================== SIDEBAR ====================
st.sidebar.markdown("""
<div style="padding: 10px 0;">
    <h2 style="font-weight: 300; letter-spacing: 6px; color: #2d2a24; margin: 0; font-size: 1.8em;">VITTA</h2>
    <p style="color: #b5a89a; font-size: 0.65em; letter-spacing: 2px; margin: 4px 0 0 0;">CURATED ACCESSORIES</p>
</div>
""", unsafe_allow_html=True)
st.sidebar.write("---")

# Navigation
page = st.sidebar.radio("Navigate", ["🏠 Shop", "📖 About"], index=0)

st.sidebar.write("---")

# Cart
st.sidebar.subheader("Your Cart")
total_price = 0
if len(st.session_state.cart_items) == 0:
    st.sidebar.caption("Your cart is empty")
else:
    for item in st.session_state.cart_items:
        st.sidebar.write(f"• {item['name']} ({item['color']}) - {item['price']} EGP")
        total_price += item['price']
    st.sidebar.write(f"### Total: {total_price} EGP")
    
    my_whatsapp_number = "201234567890"
    order_text = "Hello Vitta Team,\n\nI would like to order:\n"
    for item in st.session_state.cart_items:
        order_text += f"• {item['name']} ({item['color']}) - {item['price']} EGP\n"
    order_text += f"\nTotal: {total_price} EGP"
    encoded_text = urllib.parse.quote(order_text)
    whatsapp_url = f"https://wa.me/{my_whatsapp_number}?text={encoded_text}"
    
    st.sidebar.markdown(f'<a href="{whatsapp_url}" target="_blank" class="whatsapp-btn">Checkout on WhatsApp</a>', unsafe_allow_html=True)
    if st.sidebar.button("Clear Cart", use_container_width=True):
        st.session_state.cart_items = []
        st.rerun()

# ==================== ADMIN PANEL ====================
st.sidebar.write("---")
with st.sidebar.expander("⚙️ إدارة المنتجات", expanded=False):
    admin_mode = st.radio("اختر الإجراء:", ["➕ منتج جديد", "🎨 إضافة لون", "✏️ تعديل منتج"])
    
    # ====== ADD NEW PRODUCT ======
    if admin_mode == "➕ منتج جديد":
        st.markdown("### معلومات المنتج")
        new_name = st.text_input("اسم المنتج")
        new_price = st.number_input("السعر (EGP)", min_value=1, value=50)
        new_cat = st.selectbox("التصنيف", ["مشابك شعر", "ربطات شعر", "إكسسوارات"])
        new_desc = st.text_area("وصف المنتج")
        
        st.markdown("### 🎨 إضافة الألوان والصور")
        col1, col2 = st.columns([1, 1])
        with col1:
            color_name = st.text_input("اسم اللون", value="أحمر", key="color_name_new")
        with col2:
            uploaded_file = st.file_uploader("صورة المنتج بهذا اللون", type=["jpg", "png", "jpeg", "webp"], key="color_img_new")
        
        if st.button("➕ إضافة هذا اللون للقائمة", use_container_width=True):
            if color_name and uploaded_file:
                img_data = process_image(uploaded_file)
                if img_data:
                    st.session_state.temp_colors.append({
                        "name": color_name,
                        "image": img_data
                    })
                    st.success(f"✅ تم إضافة لون {color_name}")
                    st.rerun()
                else:
                    st.error("❌ فشل في معالجة الصورة")
            else:
                st.error("❌ يرجى إدخال اسم اللون ورفع صورة")
        
        if st.session_state.temp_colors:
            st.markdown("**الألوان المضافة:**")
            for idx, color in enumerate(st.session_state.temp_colors):
                col1, col2, col3 = st.columns([1, 4, 1])
                with col1:
                    st.image(color['image'], width=40)
                with col2:
                    st.write(color['name'])
                with col3:
                    if st.button("🗑️", key=f"remove_{idx}"):
                        st.session_state.temp_colors.pop(idx)
                        st.rerun()
        
        if st.button("📦 نشر المنتج", use_container_width=True, type="primary"):
            if new_name and st.session_state.temp_colors:
                new_product = {
                    "id": len(st.session_state.products),
                    "name": new_name,
                    "price": int(new_price),
                    "cat": new_cat,
                    "desc": new_desc,
                    "colors": st.session_state.temp_colors.copy()
                }
                st.session_state.products.append(new_product)
                save_products(st.session_state.products)
                st.session_state.temp_colors = []
                st.success(f"✅ تم إضافة {new_name}!")
                st.rerun()
            else:
                if not new_name:
                    st.error("❌ يرجى إدخال اسم المنتج")
                if not st.session_state.temp_colors:
                    st.error("❌ يرجى إضافة لون واحد على الأقل")
    
    # ====== ADD COLOR TO EXISTING ======
    elif admin_mode == "🎨 إضافة لون":
        existing_names = [p['name'] for p in st.session_state.products]
        if existing_names:
            selected = st.selectbox("اختر المنتج", existing_names)
            new_color_name = st.text_input("اسم اللون الجديد", value="ذهبي")
            uploaded_file = st.file_uploader("صورة المنتج بهذا اللون", type=["jpg", "png", "jpeg", "webp"])
            
            if st.button("إضافة اللون", use_container_width=True):
                if selected and new_color_name and uploaded_file:
                    img_data = process_image(uploaded_file)
                    if img_data:
                        for p in st.session_state.products:
                            if p['name'] == selected:
                                p['colors'].append({
                                    "name": new_color_name,
                                    "image": img_data
                                })
                                break
                        save_products(st.session_state.products)
                        st.success(f"✅ تم إضافة لون {new_color_name}!")
                        st.rerun()
                    else:
                        st.error("❌ فشل في معالجة الصورة")
                else:
                    st.error("❌ يرجى إدخال اسم اللون ورفع صورة")
        else:
            st.info("لا يوجد منتجات بعد")
    
    # ====== EDIT PRODUCT ======
    elif admin_mode == "✏️ تعديل منتج":
        existing_names = [p['name'] for p in st.session_state.products]
        if existing_names:
            selected = st.selectbox("اختر المنتج للتعديل", existing_names)
            
            # Find product
            product_to_edit = None
            product_index = -1
            for idx, p in enumerate(st.session_state.products):
                if p['name'] == selected:
                    product_to_edit = p
                    product_index = idx
                    break
            
            if product_to_edit:
                st.markdown("### معلومات المنتج")
                new_name = st.text_input("اسم المنتج", value=product_to_edit['name'])
                new_price = st.number_input("السعر (EGP)", value=product_to_edit['price'])
                new_cat = st.text_input("التصنيف", value=product_to_edit['cat'])
                new_desc = st.text_area("الوصف", value=product_to_edit['desc'])
                
                st.markdown("### 🎨 تعديل الألوان والصور")
                
                # Edit each color
                updated_colors = []
                for idx, color in enumerate(product_to_edit['colors']):
                    st.markdown(f"**اللون {idx + 1}:** {color['name']}")
                    
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        if color.get('image'):
                            st.image(color['image'], width=80)
                        else:
                            st.markdown("لا توجد صورة")
                    
                    with col2:
                        new_color_name = st.text_input(
                            f"اسم اللون",
                            value=color['name'],
                            key=f"edit_name_{idx}"
                        )
                        new_image = st.file_uploader(
                            f"رفع صورة جديدة (اختياري)",
                            type=["jpg", "png", "jpeg", "webp"],
                            key=f"edit_img_{idx}"
                        )
                        delete_color = st.checkbox(
                            f"🗑️ حذف هذا اللون",
                            key=f"delete_{idx}"
                        )
                    
                    if not delete_color:
                        updated_color = color.copy()
                        updated_color['name'] = new_color_name
                        if new_image is not None:
                            img_data = process_image(new_image)
                            if img_data:
                                updated_color['image'] = img_data
                        updated_colors.append(updated_color)
                    
                    st.markdown("---")
                
                # Update button
                if st.button("💾 حفظ التغييرات", use_container_width=True, type="primary"):
                    product_to_edit['name'] = new_name
                    product_to_edit['price'] = int(new_price)
                    product_to_edit['cat'] = new_cat
                    product_to_edit['desc'] = new_desc
                    product_to_edit['colors'] = updated_colors
                    
                    save_products(st.session_state.products)
                    st.success(f"✅ تم تحديث {new_name}!")
                    st.rerun()
                
                # Delete product
                st.markdown("---")
                if st.button("🗑️ حذف المنتج بالكامل", use_container_width=True):
                    confirm = st.checkbox("تأكيد الحذف", key="confirm_delete")
                    if confirm:
                        st.session_state.products.pop(product_index)
                        save_products(st.session_state.products)
                        st.success("✅ تم حذف المنتج!")
                        st.rerun()
                    else:
                        st.warning("⚠️ يرجى تأكيد الحذف")
        else:
            st.info("لا يوجد منتجات بعد")

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
    st.markdown("""
    <div class="store-header">
        <h1 class="store-title">VITTA</h1>
        <p class="store-subtitle">CURATED ACCESSORIES</p>
        <p class="store-tagline">Crafted with care for everyday elegance</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Product Detail View
    if st.session_state.selected_product is not None:
        product = st.session_state.selected_product
        colors = product.get('colors', [])
        
        if colors:
            current_idx = st.session_state.selected_color_index
            if current_idx >= len(colors):
                current_idx = 0
                st.session_state.selected_color_index = 0
            
            current_color = colors[current_idx]
            
            st.markdown("---")
            st.markdown(f'<div class="detail-title">{product["name"]}</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns([1.2, 1])
            
            with col1:
                img_src = current_color.get('image', '')
                if img_src:
                    st.markdown(f'<div class="detail-main-image"><img src="{img_src}"></div>', unsafe_allow_html=True)
                
                if len(colors) > 1:
                    st.markdown("**الألوان المتاحة:**")
                    color_cols = st.columns(min(len(colors), 4))
                    for idx, color in enumerate(colors):
                        with color_cols[idx % len(color_cols)]:
                            is_selected = idx == current_idx
                            border_class = "selected" if is_selected else ""
                            img = color.get('image', '')
                            st.markdown(f"""
                            <div class="color-option-card {border_class}">
                                <div class="color-option-swatch"><img src="{img}"></div>
                                <div style="font-size: 0.8em;">{color['name']}</div>
                            </div>
                            """, unsafe_allow_html=True)
                            if st.button(f"اختر", key=f"detail_color_{idx}"):
                                st.session_state.selected_color_index = idx
                                st.rerun()
            
            with col2:
                st.markdown(f'<div class="detail-price">{product["price"]} EGP</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="detail-description">{product["desc"]}</div>', unsafe_allow_html=True)
                st.markdown(f"**اللون المختار:** {current_color['name']}")
                
                if st.button("🛒 أضف إلى السلة", use_container_width=True):
                    st.session_state.cart_items.append({
                        "name": product['name'],
                        "price": product['price'],
                        "color": current_color['name']
                    })
                    st.toast(f"✨ تم إضافة {product['name']}!")
                    st.rerun()
                
                if st.button("↩️ العودة للمتجر", use_container_width=True):
                    st.session_state.selected_product = None
                    st.rerun()
    
    # Product Grid
    else:
        if len(st.session_state.products) == 0:
            st.info("🛍️ لا توجد منتجات. استخدم لوحة الإدارة لإضافة منتجات!")
        else:
            cols = st.columns(2)
            for index, product in enumerate(st.session_state.products):
                with cols[index % 2]:
                    first_color = product['colors'][0] if product['colors'] else None
                    img_src = first_color.get('image', '') if first_color else ''
                    
                    color_thumbs = ""
                    for color in product['colors'][:4]:
                        img = color.get('image', '')
                        if img:
                            color_thumbs += f'<div class="color-thumb"><img src="{img}"></div>'
                    
                    st.markdown(f"""
                    <div class="product-card">
                        <div class="product-image-wrapper">
                            {f'<img src="{img_src}">' if img_src else 'لا توجد صورة'}
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
