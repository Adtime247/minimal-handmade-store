import streamlit as st
import urllib.parse
from PIL import Image

# 1. UI Customization with Modern Minimal Aesthetic (Beige & White)
aesthetic_store_css = """
<style>
[data-testid="stAppViewContainer"] {
    background-color: #faf7f2 !important;
}
[data-testid="stSidebar"] {
    background-color: #ffffff !important;
    border-right: 1px solid #efeae4;
}
h1, h2, h3, p, label, span {
    color: #4a3f35 !important;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
    text-align: left;
}
.product-card {
    background-color: #ffffff;
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0 4px 20px rgba(74,63,53,0.02);
    margin-bottom: 25px;
    border: 1px solid #f4eee6;
    text-align: center;
    transition: transform 0.2s ease;
}
.product-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 30px rgba(74,63,53,0.05);
}
.product-title {
    font-size: 1.2em;
    font-weight: 600;
    color: #4a3f35;
    margin-top: 10px;
    text-align: center;
    letter-spacing: -0.3px;
}
.product-price {
    color: #b58d63;
    font-weight: 700;
    font-size: 1.2em;
    margin-top: 8px;
    text-align: center;
}
.product-color-options {
    display: flex;
    gap: 6px;
    justify-content: center;
    margin: 10px 0;
    flex-wrap: wrap;
}
.color-dot {
    display: inline-block;
    width: 24px;
    height: 24px;
    border-radius: 50%;
    border: 2px solid #efeae4;
    margin: 2px;
}
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
    transition: background-color 0.2s ease;
}
.whatsapp-btn:hover {
    background-color: #0d6e62;
}
.stButton > button {
    background-color: #ffffff !important;
    color: #4a3f35 !important;
    border: 1px solid #e0d6cc !important;
    border-radius: 8px !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    background-color: #f5f0eb !important;
    border-color: #c8bdb0 !important;
}
</style>
"""
st.markdown(aesthetic_store_css, unsafe_allow_html=True)

# 2. Initialize State for Session Cart and Selected View
if 'cart_items' not in st.session_state:
    st.session_state.cart_items = []

if 'selected_product' not in st.session_state:
    st.session_state.selected_product = None  

if 'custom_products' not in st.session_state:
    # Fully English default database with multi-color setup
    st.session_state.custom_products = [
        {
            "id": 0,
            "name": "Elegant Hair Claw", 
            "price": 20, 
            "cat": "👑 Headbands", 
            "desc": "Add a touch of elegance to your look with this modern marble design hair claw. Features a strong grip, light weight, and complete comfort for daily wear or special occasions.",
            "colors": ["Marble Beige", "Olive Green", "Pearl White", "Soft Pink"],
            "image": "https://picsum.photos/seed/hairclaw/300/300"
        },
        {
            "id": 1,
            "name": "Hair Bows", 
            "price": 150, 
            "cat": "🎀 Hair Bows", 
            "desc": "Natural polished clay, beautifully shaped by hand with ultimate care. A perfect companion for your daily hot beverages, durable and heat-resistant.",
            "colors": ["Earthy Brown", "Matte Grey", "Royal Black"],
            "image": "https://picsum.photos/seed/hairbow/300/300"
        },
        {
            "id": 2,
            "name": "Hair Bands & Pins", 
            "price": 350, 
            "cat": "Hair Bands & Pins📎", 
            "desc": "Handcrafted shoulder bag made from 100% natural cotton threads. Features a spacious, modern bohemian design suitable for all your outings.",
            "colors": ["Off-White", "Warm Mustard", "Light Grey"],
            "image": "https://picsum.photos/seed/hairband/300/300"
        }
    ]

# 3. Sidebar (Cart, Filter, and Manager Panel)
st.sidebar.title("M i n i m a l  S h o p")
st.sidebar.caption("Where Coding Meets Handmade Art")
st.sidebar.write("---")

if st.session_state.selected_product is not None:
    if st.sidebar.button("⬅️ Back to Shop Gallery", use_container_width=True):
        st.session_state.selected_product = None
        st.rerun()

category = st.sidebar.selectbox("Filter Categories", ["✨ All", "👑 Headbands", "🎀 Hair Bows", "Hair Bands & Pins📎"])

st.sidebar.write("---")
st.sidebar.subheader("Shopping Cart 🛒")

total_price = 0

if len(st.session_state.cart_items) == 0:
    st.sidebar.caption("Your cart is currently empty.")
else:
    for item in st.session_state.cart_items:
        st.sidebar.write(f"• {item['name']} ({item['color']}) - {item['price']} EGP")
        total_price += item['price']
    
    st.sidebar.write(f"### Total: {total_price} EGP")
    
    my_whatsapp_number = "201234567890" 
    
    order_text = "Hello, I would like to order the following items from the store:\n"
    for item in st.session_state.cart_items:
        order_text += f"- {item['name']} (Color: {item['color']}) - {item['price']} EGP\n"
    order_text += f"\nTotal Amount: {total_price} EGP"
    
    encoded_text = urllib.parse.quote(order_text)
    whatsapp_url = f"https://wa.me/{my_whatsapp_number}?text={encoded_text}"
    
    st.sidebar.markdown(f'<a href="{whatsapp_url}" target="_blank" class="whatsapp-btn">Checkout via WhatsApp 💬</a>', unsafe_allow_html=True)
    st.sidebar.write("")
    
    if st.sidebar.button("Clear Cart", use_container_width=True):
        st.session_state.cart_items = []
        st.rerun()

# --- Manager Panel (INTELLIGENT UPDATE TO PREVENT DUPLICATES) ---
st.sidebar.write("---")
with st.sidebar.expander("➕ Admin Panel (Add/Update Products)"):
    admin_mode = st.radio("Choose Action:", ["Create New Product", "Add Colors to Existing Product"])
    
    if admin_mode == "Create New Product":
        new_name = st.text_input("Product Title:")
        new_price = st.number_input("Price (EGP):", min_value=1, value=50)
        new_cat = st.selectbox("Category:", ["👑 Headbands", "🎀 Hair Bows", "Hair Bands & Pins📎"])
        new_desc = st.text_area("Short Description:")
        new_colors_input = st.text_input("Available Colors (separate with comma ,):", value="Black, White")
        uploaded_file = st.file_uploader("Upload Product Image:", type=["jpg", "png", "jpeg"])
        
        if st.button("Publish New Product ✨", use_container_width=True):
            if new_name:
                colors_list = [c.strip() for c in new_colors_input.split(",") if c.strip()]
                if not colors_list: 
                    colors_list = ["Default"]
                    
                img_to_save = "https://picsum.photos/seed/" + new_name.replace(" ", "") + "/300/300"
                if uploaded_file is not None: 
                    img_to_save = Image.open(uploaded_file)
                    
                new_id = len(st.session_state.custom_products)
                st.session_state.custom_products.append({
                    "id": new_id, 
                    "name": new_name, 
                    "price": int(new_price),
                    "cat": new_cat, 
                    "desc": new_desc, 
                    "colors": colors_list, 
                    "image": img_to_save
                })
                st.success("New product published successfully!")
                st.rerun()
                
    elif admin_mode == "Add Colors to Existing Product":
        existing_product_names = [p['name'] for p in st.session_state.custom_products]
        selected_existing = st.selectbox("Select Product to Update:", existing_product_names)
        additional_colors = st.text_input("Type new colors to add (separate with comma ,):", value="Gold, Silver")
        
        if st.button("Update Product Colors 🔄", use_container_width=True):
            if additional_colors:
                new_colors = [c.strip() for c in additional_colors.split(",") if c.strip()]
                for p in st.session_state.custom_products:
                    if p['name'] == selected_existing:
                        for color in new_colors:
                            if color not in p['colors']:
                                p['colors'].append(color)
                st.success(f"Updated colors for {selected_existing} successfully!")
                st.rerun()

# 4. View Controller: Product Details Page OR Main Gallery Catalog
if st.session_state.selected_product is not None:
    prod_id = st.session_state.selected_product['id']
    prod = next((p for p in st.session_state.custom_products if p['id'] == prod_id), st.session_state.selected_product)
    
    st.title(prod['name'])
    st.write("---")
    col1, col2 = st.columns([1.2, 1])
    with col1:
        st.image(prod['image'], use_container_width=True)
    with col2:
        st.subheader("Product Description:")
        st.write(prod['desc'])
        st.write(f"### Price: {prod['price']} EGP")
        st.write("---")
        st.subheader("Choose Your Color:")
        chosen_color = st.radio("Available Colors/Options for this item:", prod['colors'])
        st.write("")
        
        # Display color dots for visual reference
        st.write("Color preview:")
        color_html = '<div class="product-color-options">'
        for color in prod['colors']:
            # Simple color mapping for preview (you can expand this)
            color_map = {
                "Marble Beige": "#f5e6d3",
                "Olive Green": "#6b8e23",
                "Pearl White": "#f8f4f0",
                "Soft Pink": "#f4c2c2",
                "Earthy Brown": "#8b7355",
                "Matte Grey": "#808080",
                "Royal Black": "#1a1a1a",
                "Off-White": "#f5f0eb",
                "Warm Mustard": "#e5b85c",
                "Light Grey": "#d3d3d3",
                "Black": "#000000",
                "White": "#ffffff",
                "Gold": "#ffd700",
                "Silver": "#c0c0c0"
            }
            bg_color = color_map.get(color, "#cccccc")
            color_html += f'<span class="color-dot" style="background-color: {bg_color};" title="{color}"></span>'
        color_html += '</div>'
        st.markdown(color_html, unsafe_allow_html=True)
        
        if st.button("Add to Cart 🛒", use_container_width=True):
            st.session_state.cart_items.append({"name": prod['name'], "price": prod['price'], "color": chosen_color})
            st.toast(f"Added {prod['name']} ({chosen_color}) to cart! ✨")
            st.rerun()
        if st.button("Cancel & Return to Shop", use_container_width=True):
            st.session_state.selected_product = None
            st.rerun()
else:
    st.title("The Handmade Studio ✨")
    st.caption("Unique handmade pieces, crafted with love, simplicity, and natural warm colors.")
    st.write("---")
    
    filtered_products = [p for p in st.session_state.custom_products if category == "✨ All" or p["cat"] == category]
    
    if len(filtered_products) == 0:
        st.info("No items available in this category at the moment.")
    else:
        cols = st.columns(2)
        for index, prod in enumerate(filtered_products):
            with cols[index % 2]:
                st.image(prod['image'], use_container_width=True)
                st.markdown(f"""
                <div class="product-card">
                    <div class="product-title">{prod['name']}</div>
                    <div class="product-price">{prod['price']} EGP</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("View Options & Details 🔍", key=f"view_{prod['id']}", use_container_width=True):
                    st.session_state.selected_product = prod
                    st.rerun()

st.write("---")
