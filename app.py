import streamlit as st
import urllib.parse
from PIL import Image
import base64
from io import BytesIO

# 1. Professional Store CSS with Modern Minimal Aesthetic (Beige & White)
aesthetic_store_css = """
<style>
/* Global Styles */
[data-testid="stAppViewContainer"] {
    background-color: #faf7f2 !important;
}
[data-testid="stSidebar"] {
    background-color: #ffffff !important;
    border-right: 1px solid #efeae4;
}
h1, h2, h3, p, label, span {
    color: #2d2a24 !important;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
}

/* Header */
.store-header {
    text-align: center;
    padding: 40px 0 20px 0;
}
.store-title {
    font-size: 2.8em;
    font-weight: 300;
    letter-spacing: 6px;
    color: #2d2a24;
    margin: 0;
}
.store-subtitle {
    font-size: 1em;
    color: #8a7a6a;
    letter-spacing: 3px;
    font-weight: 300;
    margin-top: 8px;
}

/* Product Grid Layout */
.product-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 30px;
    padding: 20px 0;
}

/* Product Card - Premium Design */
.product-card {
    background: #ffffff;
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0 2px 20px rgba(0,0,0,0.04);
    transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    border: 1px solid #f0ebe5;
    position: relative;
}
.product-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 12px 40px rgba(45,42,36,0.08);
    border-color: #e0d6cc;
}

.product-image-wrapper {
    position: relative;
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
    padding: 20px 24px 24px;
}
.product-name {
    font-size: 1.1em;
    font-weight: 600;
    color: #2d2a24;
    margin: 0 0 6px 0;
    letter-spacing: -0.3px;
}
.product-category {
    font-size: 0.75em;
    color: #b5a89a;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    font-weight: 500;
    margin-bottom: 10px;
}
.product-price {
    font-size: 1.4em;
    font-weight: 600;
    color: #b58d63;
    margin: 8px 0 12px 0;
}
.product-colors {
    display: flex;
    gap: 6px;
    margin: 12px 0;
    flex-wrap: wrap;
}
.color-swatch {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    border: 2px solid #f0ebe5;
    cursor: pointer;
    transition: border-color 0.2s ease;
}
.color-swatch:hover {
    border-color: #b58d63;
}
.color-swatch.selected {
    border-color: #b58d63;
    border-width: 2.5px;
}

/* Buttons */
.btn-primary {
    width: 100%;
    padding: 14px;
    background: #2d2a24;
    color: white !important;
    border: none;
    border-radius: 12px;
    font-weight: 500;
    font-size: 0.95em;
    letter-spacing: 0.5px;
    transition: all 0.2s ease;
    cursor: pointer;
}
.btn-primary:hover {
    background: #4a3f35;
    transform: scale(1.01);
}
.btn-outline {
    width: 100%;
    padding: 14px;
    background: transparent;
    color: #2d2a24 !important;
    border: 1.5px solid #e0d6cc;
    border-radius: 12px;
    font-weight: 500;
    font-size: 0.95em;
    transition: all 0.2s ease;
    cursor: pointer;
}
.btn-outline:hover {
    border-color: #b58d63;
    background: #f8f5f0;
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

/* Cart Sidebar */
.cart-item {
    padding: 10px 0;
    border-bottom: 1px solid #f5f0eb;
}
.cart-item-name {
    font-weight: 500;
    color: #2d2a24;
}
.cart-item-detail {
    font-size: 0.85em;
    color: #b5a89a;
}

/* Color Picker in Detail View */
.color-options-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
    gap: 10px;
    margin: 15px 0;
}
.color-option-card {
    padding: 10px;
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
}
.color-option-swatch {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    margin: 0 auto 6px;
    border: 1px solid #e0d6cc;
}

/* Product Detail */
.product-detail-container {
    max-width: 1100px;
    margin: 0 auto;
    padding: 20px;
}
.detail-image {
    border-radius: 20px;
    overflow: hidden;
    background: #f8f5f0;
}
.detail-title {
    font-size: 2.2em;
    font-weight: 300;
    letter-spacing: 1px;
    color: #2d2a24;
    margin-bottom: 10px;
}
.detail-price {
    font-size: 1.8em;
    font-weight: 600;
    color: #b58d63;
}
.detail-description {
    color: #6a5f55;
    line-height: 1.8;
    font-size: 1em;
}

/* Whatsapp Button */
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
    box-shadow: 0 4px 15px rgba(37,211,102,0.2);
    transition: all 0.2s ease;
}
.whatsapp-btn:hover {
    background: #20b85a;
    transform: scale(1.01);
}

/* Streamlit Overrides */
.stButton > button {
    width: 100% !important;
    border-radius: 12px !important;
    font-weight: 500 !important;
    padding: 12px !important;
    transition: all 0.2s ease !important;
}
.stSelectbox > div {
    border-radius: 12px !important;
}
.stRadio > div {
    gap: 12px !important;
}
</style>
"""
st.markdown(aesthetic_store_css, unsafe_allow_html=True)

# 2. Initialize State
if 'cart_items' not in st.session_state:
    st.session_state.cart_items = []

if 'selected_product' not in st.session_state:
    st.session_state.selected_product = None  

if 'custom_products' not in st.session_state:
    # Professional product database with multiple color options
    st.session_state.custom_products = [
        {
            "id": 0,
            "name": "Elegant Hair Claw",
            "price": 20,
            "cat": "👑 Headbands",
            "desc": "A sophisticated hair accessory crafted from premium materials. Features a secure grip mechanism and lightweight design for all-day comfort.",
            "colors": ["Marble Beige", "Olive Green", "Pearl White", "Soft Pink"],
            "image": "https://picsum.photos/seed/hairclaw1/400/400"
        },
        {
            "id": 1,
            "name": "Luxury Hair Bow",
            "price": 150,
            "cat": "🎀 Hair Bows",
            "desc": "Handcrafted from natural clay with a polished finish. Each piece is uniquely shaped and fired for durability and heat resistance.",
            "colors": ["Earthy Brown", "Matte Grey", "Royal Black", "Terracotta"],
            "image": "https://picsum.photos/seed/hairbow1/400/400"
        },
        {
            "id": 2,
            "name": "Artisan Hair Band",
            "price": 350,
            "cat": "Hair Bands & Pins📎",
            "desc": "Bohemian-inspired accessory woven from natural cotton threads. Versatile design suitable for casual and formal occasions.",
            "colors": ["Off-White", "Warm Mustard", "Light Grey", "Sage Green"],
            "image": "https://picsum.photos/seed/hairband1/400/400"
        },
        {
            "id": 3,
            "name": "Classic Headband",
            "price": 95,
            "cat": "👑 Headbands",
            "desc": "Timeless design with a modern twist. Made from sustainable materials with a comfortable fit for extended wear.",
            "colors": ["Black", "Ivory", "Navy", "Burgundy"],
            "image": "https://picsum.photos/seed/headband2/400/400"
        },
        {
            "id": 4,
            "name": "Silk Hair Scrunchie",
            "price": 45,
            "cat": "🎀 Hair Bows",
            "desc": "Luxurious silk scrunchie that protects your hair from breakage. Available in a curated selection of sophisticated colors.",
            "colors": ["Champagne", "Rose Gold", "Deep Burgundy", "Midnight Blue"],
            "image": "https://picsum.photos/seed/scrunchie1/400/400"
        },
        {
            "id": 5,
            "name": "Minimalist Hair Pin",
            "price": 65,
            "cat": "Hair Bands & Pins📎",
            "desc": "Sleek and minimal design that complements any outfit. Perfect for creating effortless, elegant hairstyles.",
            "colors": ["Gold", "Silver", "Rose Gold", "Brass"],
            "image": "https://picsum.photos/seed/hairpin1/400/400"
        }
    ]

# 3. Sidebar
st.sidebar.markdown("""
<div style="padding: 10px 0;">
    <h2 style="font-weight: 300; letter-spacing: 4px; color: #2d2a24; margin: 0;">VITTA</h2>
    <p style="color: #b5a89a; font-size: 0.7em; letter-spacing: 2px; margin: 4px 0 0 0;">CURATED ACCESSORIES</p>
</div>
""", unsafe_allow_html=True)
st.sidebar.write("---")

if st.session_state.selected_product is not None:
    if st.sidebar.button("← Back to Shop", use_container_width=True):
        st.session_state.selected_product = None
        st.rerun()

category = st.sidebar.selectbox(
    "Collection",
    ["✨ All", "👑 Headbands", "🎀 Hair Bows", "Hair Bands & Pins📎"]
)

st.sidebar.write("---")
st.sidebar.subheader("Your Cart")
st.sidebar.write("")

total_price = 0

if len(st.session_state.cart_items) == 0:
    st.sidebar.caption("Your cart is empty")
else:
    for item in st.session_state.cart_items:
        st.sidebar.markdown(f"""
        <div class="cart-item">
            <div class="cart-item-name">{item['name']}</div>
            <div class="cart-item-detail">{item['color']} · {item['price']} EGP</div>
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

# --- Admin Panel ---
st.sidebar.write("---")
with st.sidebar.expander("⚙️ Studio Management"):
    admin_mode = st.radio("Action", ["New Product", "Add Colors"])
    
    if admin_mode == "New Product":
        new_name = st.text_input("Product Name")
        new_price = st.number_input("Price (EGP)", min_value=1, value=50)
        new_cat = st.selectbox("Category", ["👑 Headbands", "🎀 Hair Bows", "Hair Bands & Pins📎"])
        new_desc = st.text_area("Description")
        new_colors_input = st.text_input("Colors (comma separated)", value="Black, White")
        uploaded_file = st.file_uploader("Product Image", type=["jpg", "png", "jpeg"])
        
        if st.button("Publish Product", use_container_width=True):
            if new_name:
                colors_list = [c.strip() for c in new_colors_input.split(",") if c.strip()]
                if not colors_list: colors_list = ["Default"]
                    
                img_to_save = f"https://picsum.photos/seed/{new_name.replace(' ', '')}/400/400"
                if uploaded_file is not None:
                    img_to_save = Image.open(uploaded_file)
                    
                new_id = len(st.session_state.custom_products)
                st.session_state.custom_products.append({
                    "id": new_id, "name": new_name, "price": int(new_price),
                    "cat": new_cat, "desc": new_desc, "colors": colors_list, "image": img_to_save
                })
                st.success("✨ Product published!")
                st.rerun()
                
    elif admin_mode == "Add Colors":
        existing_names = [p['name'] for p in st.session_state.custom_products]
        selected = st.selectbox("Select Product", existing_names)
        additional_colors = st.text_input("New Colors", value="Gold, Silver")
        
        if st.button("Update Colors", use_container_width=True):
            if additional_colors:
                new_colors = [c.strip() for c in additional_colors.split(",") if c.strip()]
                for p in st.session_state.custom_products:
                    if p['name'] == selected:
                        for color in new_colors:
                            if color not in p['colors']:
                                p['colors'].append(color)
                st.success("🎨 Colors updated!")
                st.rerun()

# 4. Main Content
if st.session_state.selected_product is not None:
    prod_id = st.session_state.selected_product['id']
    prod = next((p for p in st.session_state.custom_products if p['id'] == prod_id), st.session_state.selected_product)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown('<div class="detail-image">', unsafe_allow_html=True)
        st.image(prod['image'], use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'<div class="detail-title">{prod["name"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="detail-price">{prod["price"]} EGP</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="detail-description">{prod["desc"]}</div>', unsafe_allow_html=True)
        st.write("")
        
        st.markdown("**Choose your color**")
        chosen_color = st.radio("", prod['colors'], key="color_radio")
        
        # Show color swatches
        color_map = {
            "Marble Beige": "#f5e6d3", "Olive Green": "#6b8e23", "Pearl White": "#f8f4f0",
            "Soft Pink": "#f4c2c2", "Earthy Brown": "#8b7355", "Matte Grey": "#808080",
            "Royal Black": "#1a1a1a", "Off-White": "#f5f0eb", "Warm Mustard": "#e5b85c",
            "Light Grey": "#d3d3d3", "Black": "#000000", "White": "#ffffff",
            "Gold": "#ffd700", "Silver": "#c0c0c0", "Terracotta": "#e2725b",
            "Sage Green": "#9caf88", "Navy": "#1a2a3a", "Burgundy": "#722f37",
            "Champagne": "#f7e7ce", "Rose Gold": "#b76e79", "Midnight Blue": "#191970",
            "Brass": "#b5a642"
        }
        
        cols = st.columns(len(prod['colors']))
        for idx, color in enumerate(prod['colors']):
            with cols[idx]:
                bg = color_map.get(color, "#cccccc")
                selected = "selected" if color == chosen_color else ""
                st.markdown(f"""
                <div class="color-option-card {selected}" style="cursor: default;">
                    <div class="color-option-swatch" style="background: {bg};"></div>
                    <div style="font-size: 0.75em; color: #6a5f55; margin-top: 4px;">{color}</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.write("")
        if st.button("Add to Cart", use_container_width=True):
            st.session_state.cart_items.append({"name": prod['name'], "price": prod['price'], "color": chosen_color})
            st.toast(f"✨ Added {prod['name']} in {chosen_color}!")
            st.rerun()
        
        st.write("")
        if st.button("Continue Shopping", use_container_width=True):
            st.session_state.selected_product = None
            st.rerun()

else:
    # Store Header
    st.markdown("""
    <div class="store-header">
        <h1 class="store-title">VITTA</h1>
        <p class="store-subtitle">CURATED ACCESSORIES</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    
    # Product Grid
    filtered_products = [p for p in st.session_state.custom_products if category == "✨ All" or p["cat"] == category]
    
    if len(filtered_products) == 0:
        st.info("No items in this collection")
    else:
        # Display products in a 2-column grid
        cols = st.columns(2)
        for index, prod in enumerate(filtered_products):
            with cols[index % 2]:
                # Color swatches for display
                color_map = {
                    "Marble Beige": "#f5e6d3", "Olive Green": "#6b8e23", "Pearl White": "#f8f4f0",
                    "Soft Pink": "#f4c2c2", "Earthy Brown": "#8b7355", "Matte Grey": "#808080",
                    "Royal Black": "#1a1a1a", "Off-White": "#f5f0eb", "Warm Mustard": "#e5b85c",
                    "Light Grey": "#d3d3d3", "Black": "#000000", "White": "#ffffff",
                    "Gold": "#ffd700", "Silver": "#c0c0c0", "Terracotta": "#e2725b",
                    "Sage Green": "#9caf88", "Navy": "#1a2a3a", "Burgundy": "#722f37",
                    "Champagne": "#f7e7ce", "Rose Gold": "#b76e79", "Midnight Blue": "#191970",
                    "Brass": "#b5a642"
                }
                
                # Create color swatches HTML
                color_swatches = ""
                for color in prod['colors'][:4]:  # Show max 4 colors
                    bg = color_map.get(color, "#cccccc")
                    color_swatches += f'<span class="color-swatch" style="background: {bg};" title="{color}"></span>'
                if len(prod['colors']) > 4:
                    color_swatches += f'<span style="font-size: 0.7em; color: #b5a89a; margin-left: 4px;">+{len(prod["colors"])-4}</span>'
                
                st.markdown(f"""
                <div class="product-card">
                    <div class="product-image-wrapper">
                        <img src="{prod['image']}" alt="{prod['name']}">
                    </div>
                    <div class="product-info">
                        <div class="product-category">{prod['cat']}</div>
                        <div class="product-name">{prod['name']}</div>
                        <div class="product-colors">{color_swatches}</div>
                        <div class="product-price">{prod['price']} EGP</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("View Details →", key=f"view_{prod['id']}", use_container_width=True):
                    st.session_state.selected_product = prod
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
