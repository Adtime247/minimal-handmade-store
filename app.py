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
                # Ensure each product has the required fields
                for p in data:
                    if 'colors' not in p:
                        p['colors'] = [{"name": "Default", "image": "https://picsum.photos/seed/default/400/400"}]
                return data
        except:
            return get_default_products()
    return get_default_products()

def save_products(products):
    """Save products to JSON file"""
    # Create a clean version without large image data
    products_to_save = []
    for p in products:
        p_copy = p.copy()
        # Keep only the image URLs or small data
        if 'colors' in p_copy:
            for color in p_copy['colors']:
                if 'image' in color and isinstance(color['image'], str) and len(color['image']) > 1000:
                    # If it's a large base64 string, keep it but it's already in the data
                    pass
        products_to_save.append(p_copy)
    
    with open(PRODUCTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(products_to_save, f, ensure_ascii=False, indent=2)

def get_default_products():
    """Default product catalog with multiple color images"""
    return [
        {
            "id": 0,
            "name": "Elegant Hair Claw",
            "price": 20,
            "cat": "Headbands",
            "desc": "A sophisticated hair accessory crafted from premium materials. Features a secure grip mechanism and lightweight design for all-day comfort.",
            "colors": [
                {"name": "Marble Beige", "image": "https://picsum.photos/seed/claw_beige/400/400"},
                {"name": "Olive Green", "image": "https://picsum.photos/seed/claw_green/400/400"},
                {"name": "Pearl White", "image": "https://picsum.photos/seed/claw_white/400/400"},
                {"name": "Soft Pink", "image": "https://picsum.photos/seed/claw_pink/400/400"}
            ]
        },
        {
            "id": 1,
            "name": "Luxury Hair Bow",
            "price": 150,
            "cat": "Hair Bows",
            "desc": "Handcrafted from natural clay with a polished finish. Each piece is uniquely shaped and fired for durability and heat resistance.",
            "colors": [
                {"name": "Earthy Brown", "image": "https://picsum.photos/seed/bow_brown/400/400"},
                {"name": "Matte Grey", "image": "https://picsum.photos/seed/bow_grey/400/400"},
                {"name": "Royal Black", "image": "https://picsum.photos/seed/bow_black/400/400"},
                {"name": "Terracotta", "image": "https://picsum.photos/seed/bow_terra/400/400"}
            ]
        },
        {
            "id": 2,
            "name": "Artisan Hair Band",
            "price": 350,
            "cat": "Hair Bands",
            "desc": "Bohemian-inspired accessory woven from natural cotton threads. Versatile design suitable for casual and formal occasions.",
            "colors": [
                {"name": "Off-White", "image": "https://picsum.photos/seed/band_white/400/400"},
                {"name": "Warm Mustard", "image": "https://picsum.photos/seed/band_mustard/400/400"},
                {"name": "Light Grey", "image": "https://picsum.photos/seed/band_grey/400/400"},
                {"name": "Sage Green", "image": "https://picsum.photos/seed/band_sage/400/400"}
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
}
.product-image-wrapper img {
    width: 100%;
    height: 100%;
    object-fit: cover;
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

/* Product Detail */
.detail-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}
.detail-main-image {
    border-radius: 20px;
    overflow: hidden;
    background: #f8f5f0;
    aspect-ratio: 1/1;
    margin-bottom: 15px;
}
.detail-main-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
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

/* About Page */
.about-section {
    background: #ffffff;
    padding: 40px;
    border-radius: 20px;
    border: 1px solid #f0ebe5;
    margin: 20px 0;
}
.about-title {
    font-size: 1.8em;
    font-weight: 300;
    letter-spacing: 2px;
    margin-bottom: 20px;
}
.about-text {
    color: #6a5f55;
    line-height: 2;
    font-size: 1em;
}

/* Streamlit Overrides */
.stButton > button {
    width: 100% !important;
    border-radius: 12px !important;
    font-weight: 500 !important;
    padding: 12px !important;
}
.stRadio > div {
    gap: 10px !important;
}
</style>
""", unsafe_allow_html=True)

# ==================== HELPER FUNCTIONS ====================
def get_color_image(product, color_index):
    """Get image URL for a specific color"""
    colors = product.get('colors', [])
    if colors and color_index < len(colors):
        return colors[color_index].get('image', 'https://picsum.photos/seed/default/400/400')
    return 'https://picsum.photos/seed/default/400/400'

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
    ["🏠 Shop", "📖 About", "✨ Collections"],
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

# Admin Panel
st.sidebar.write("---")
with st.sidebar.expander("⚙️ Studio Management"):
    admin_mode = st.radio("Action", ["New Product", "Add Color Variant"])
    
    if admin_mode == "New Product":
        new_name = st.text_input("Product Name")
        new_price = st.number_input("Price (EGP)", min_value=1, value=50)
        new_cat = st.selectbox("Category", ["Headbands", "Hair Bows", "Hair Bands"])
        new_desc = st.text_area("Description")
        
        st.markdown("**Color Variants**")
        color_name = st.text_input("Color Name", value="Black")
        uploaded_file = st.file_uploader("Upload Image for this color", type=["jpg", "png", "jpeg"])
        
        if st.button("Add Product", use_container_width=True):
            if new_name:
                img_url = "https://picsum.photos/seed/" + new_name.replace(" ", "") + "/400/400"
                if uploaded_file is not None:
                    # Save as base64
                    img = Image.open(uploaded_file)
                    buffered = BytesIO()
                    img.save(buffered, format="JPEG", quality=70)
                    img_str = base64.b64encode(buffered.getvalue()).decode()
                    img_url = f"data:image/jpeg;base64,{img_str}"
                
                new_product = {
                    "id": len(st.session_state.products),
                    "name": new_name,
                    "price": int(new_price),
                    "cat": new_cat,
                    "desc": new_desc,
                    "colors": [{"name": color_name, "image": img_url}]
                }
                st.session_state.products.append(new_product)
                save_products(st.session_state.products)
                st.success("✨ Product added!")
                st.rerun()
    
    elif admin_mode == "Add Color Variant":
        existing_names = [p['name'] for p in st.session_state.products]
        if existing_names:
            selected = st.selectbox("Select Product", existing_names)
            new_color_name = st.text_input("Color Name", value="Gold")
            uploaded_file = st.file_uploader("Upload Image for this color", type=["jpg", "png", "jpeg"])
            
            if st.button("Add Color Variant", use_container_width=True):
                if selected and new_color_name:
                    img_url = "https://picsum.photos/seed/" + new_color_name.replace(" ", "") + "/400/400"
                    if uploaded_file is not None:
                        img = Image.open(uploaded_file)
                        buffered = BytesIO()
                        img.save(buffered, format="JPEG", quality=70)
                        img_str = base64.b64encode(buffered.getvalue()).decode()
                        img_url = f"data:image/jpeg;base64,{img_str}"
                    
                    for p in st.session_state.products:
                        if p['name'] == selected:
                            p['colors'].append({
                                "name": new_color_name,
                                "image": img_url
                            })
                            break
                    save_products(st.session_state.products)
                    st.success("🎨 Color variant added!")
                    st.rerun()
        else:
            st.info("No products yet. Create one first!")

# ==================== MAIN CONTENT ====================
if page == "📖 About":
    st.markdown("""
    <div class="about-section">
        <div class="about-title">About VITTA</div>
        <div class="about-text">
            <p><strong>VITTA</strong> is a curated accessories brand born from a passion for timeless design and exceptional craftsmanship.</p>
            <p>We believe that everyday accessories should be both beautiful and functional. Each piece in our collection is thoughtfully designed to elevate your daily style while providing lasting quality.</p>
            <p style="margin-top: 20px;">Our philosophy is simple:</p>
            <ul style="color: #6a5f55; line-height: 2; padding-left: 20px;">
                <li><strong>Quality over quantity</strong> — We focus on creating pieces that stand the test of time</li>
                <li><strong>Thoughtful design</strong> — Every detail is considered, from materials to functionality</li>
                <li><strong>Sustainable practice</strong> — We work with responsible suppliers and minimize waste</li>
                <li><strong>Customer experience</strong> — Your satisfaction is our priority, from browsing to delivery</li>
            </ul>
            <p style="margin-top: 20px;">Join us in celebrating the beauty of everyday elegance.</p>
            <p style="font-weight: 300; letter-spacing: 1px; margin-top: 10px; color: #b58d63;">— The VITTA Team</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Mission Section
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div style="text-align: center; padding: 20px; background: #ffffff; border-radius: 16px; border: 1px solid #f0ebe5;">
            <div style="font-size: 2.5em;">🎯</div>
            <h3>Our Mission</h3>
            <p style="color: #6a5f55; font-size: 0.9em; line-height: 1.6;">To create accessories that enhance your personal style while maintaining exceptional quality and comfort.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 20px; background: #ffffff; border-radius: 16px; border: 1px solid #f0ebe5;">
            <div style="font-size: 2.5em;">✨</div>
            <h3>Our Values</h3>
            <p style="color: #6a5f55; font-size: 0.9em; line-height: 1.6;">Craftsmanship, sustainability, and thoughtful design are at the heart of everything we create.</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div style="text-align: center; padding: 20px; background: #ffffff; border-radius: 16px; border: 1px solid #f0ebe5;">
            <div style="font-size: 2.5em;">🌿</div>
            <h3>Our Promise</h3>
            <p style="color: #6a5f55; font-size: 0.9em; line-height: 1.6;">Every piece is made with care, using sustainable materials and ethical production practices.</p>
        </div>
        """, unsafe_allow_html=True)

elif page == "✨ Collections":
    st.markdown("""
    <div style="text-align: center; padding: 30px 0;">
        <h2 style="font-weight: 300; letter-spacing: 3px;">Our Collections</h2>
        <p style="color: #b5a89a; font-weight: 300; letter-spacing: 1px;">Curated with care for everyday elegance</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display categories as collection cards
    categories = list(set([p['cat'] for p in st.session_state.products]))
    icons = ["👑", "🎀", "📎", "✨", "💫", "🌟"]
    
    cols = st.columns(min(len(categories), 3))
    for idx, cat in enumerate(categories):
        with cols[idx % len(cols)]:
            count = len([p for p in st.session_state.products if p['cat'] == cat])
            icon = icons[idx % len(icons)]
            st.markdown(f"""
            <div style="background: #ffffff; padding: 30px; border-radius: 20px; border: 1px solid #f0ebe5; text-align: center; margin-bottom: 15px;">
                <div style="font-size: 3em;">{icon}</div>
                <h3 style="margin: 10px 0 5px 0;">{cat}</h3>
                <p style="color: #b5a89a; font-size: 0.9em;">{count} items</p>
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
    
    # Category Filter
    categories = ["All"] + sorted(list(set([p['cat'] for p in st.session_state.products])))
    selected_category = st.selectbox("Filter by Collection", categories, index=0)
    
    st.write("")
    
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
                st.markdown(f'<div class="detail-main-image"><img src="{current_color["image"]}" alt="{product["name"]}"></div>', unsafe_allow_html=True)
                
                # Color thumbnails
                if len(colors) > 1:
                    st.write("")
                    st.markdown("**Available Colors:**")
                    thumb_cols = st.columns(min(len(colors), 4))
                    for idx, color in enumerate(colors):
                        with thumb_cols[idx % len(thumb_cols)]:
                            active_class = "active" if idx == current_color_idx else ""
                            st.markdown(f'<div class="detail-thumb {active_class}" onclick="location.reload()"><img src="{color["image"]}" alt="{color["name"]}"></div>', unsafe_allow_html=True)
                            if st.button(color['name'], key=f"color_btn_{idx}"):
                                st.session_state.selected_color_index = idx
                                st.rerun()
            
            with col2:
                st.markdown(f'<div class="detail-price">{product["price"]} EGP</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="detail-description">{product["desc"]}</div>', unsafe_allow_html=True)
                
                st.write("")
                selected_color_name = current_color["name"]
                st.markdown(f"**Selected Color:** {selected_color_name}")
                
                if st.button("Add to Cart", use_container_width=True):
                    st.session_state.cart_items.append({
                        "name": product['name'],
                        "price": product['price'],
                        "color": selected_color_name
                    })
                    st.toast(f"✨ Added {product['name']} in {selected_color_name}!")
                    st.rerun()
                
                if st.button("Continue Shopping", use_container_width=True):
                    st.session_state.selected_product = None
                    st.session_state.selected_color_index = 0
                    st.rerun()
    else:
        # Product Grid
        filtered_products = [p for p in st.session_state.products if selected_category == "All" or p['cat'] == selected_category]
        
        if len(filtered_products) == 0:
            st.info("No items in this collection")
        else:
            cols = st.columns(2)
            for index, product in enumerate(filtered_products):
                with cols[index % 2]:
                    # Get first color image for card
                    first_color = product['colors'][0] if product['colors'] else {"name": "Default", "image": "https://picsum.photos/seed/default/400/400"}
                    
                    # Create color thumbnails
                    color_thumbs = ""
                    for color in product['colors'][:4]:
                        color_thumbs += f'<div class="color-thumb"><img src="{color["image"]}" alt="{color["name"]}"></div>'
                    
                    st.markdown(f"""
                    <div class="product-card">
                        <div class="product-image-wrapper">
                            <img src="{first_color['image']}" alt="{product['name']}">
                        </div>
                        <div class="product-info">
                            <div class="product-category">{product['cat']}</div>
                            <div class="product-name">{product['name']}</div>
                            <div class="color-thumbnails">{color_thumbs}</div>
                            <div class="product-price">{product['price']} EGP</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button("View Details →", key=f"view_{product['id']}", use_container_width=True):
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
