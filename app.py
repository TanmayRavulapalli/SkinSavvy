import streamlit as st
from streamlit_option_menu import option_menu
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from PIL import Image
import pandas as pd
import json
import os

# Set page configuration
st.set_page_config(page_title="SkinSavvy", page_icon=":rose:", layout="wide")

# Function to read credentials from external file
def load_credentials():
    try:
        with open("credentials.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Function to save credentials to external file
def save_credentials(credentials):
    with open("credentials.json", "w") as file:
        json.dump(credentials, file)

# Initialize session state variables
def initialize_session_state():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'email' not in st.session_state:
        st.session_state.email = None
    if 'selected_page' not in st.session_state:
        st.session_state.selected_page = "Login"

# Login function
def login(credentials):
    initialize_session_state()
    if not st.session_state.logged_in:
        st.subheader("Login")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        st.write("Please click twice 🔽")
        if st.button("Login", key="login_button"):
            if email in credentials and credentials[email]["password"] == password:
                st.session_state.logged_in = True
                st.session_state.email = email
                st.session_state.selected_page = "Profile"
            else:
                st.error("Incorrect email or password")


# Signup function
def signup(credentials):
    st.subheader("Sign Up")
    name = st.text_input("Name", key="signup_name")
    email = st.text_input("Email", key="signup_email")
    phone_number = st.text_input("Phone Number", key="signup_phone")
    new_password = st.text_input("Password", type="password", key="signup_password")
    confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm_password")
    uploaded_file = st.file_uploader("Choose a profile picture", type=["jpg", "jpeg", "png"], key="signup_profile_pic")

    if st.button("Sign Up", key="signup_button"):
        if new_password != confirm_password:
            st.error("Passwords do not match")
        elif email in credentials:
            st.error("Email already registered")
        else:
            st.success("Sign up successful! You can now log in.")
            credentials[email] = {
                "password": new_password,
                "name": name,
                "phone_number": phone_number,
                "profile_picture": save_profile_picture(uploaded_file, email) if uploaded_file else None
            }
            save_credentials(credentials)


# Function to save profile picture
def save_profile_picture(uploaded_file, email):
    if not os.path.exists("profile_pictures"):
        os.makedirs("profile_pictures")
    file_path = f"profile_pictures/{email}_profile_picture.jpg"
    with open(file_path, "wb") as file:
        file.write(uploaded_file.read())
    return file_path

# Sidebar with user info
def profile(credentials):
    st.title("Account Info")
    st.write("Email:", st.session_state.email)
    if st.session_state.email in credentials:
        user_info = credentials[st.session_state.email]
        st.write("Name:", user_info["name"])
        st.write("Phone Number:", user_info["phone_number"])
        profile_picture_path = user_info.get("profile_picture")
        
        if profile_picture_path and os.path.exists(profile_picture_path):
            st.image(profile_picture_path, caption="Profile Picture", width=150)  # Set a fixed width for the image
        
        st.write("---")
        st.write("Please click Twice to logout")
        if st.button("Log out"):
            st.session_state.logged_in = False
            st.session_state.email = None
            st.session_state.selected_page = "Login"


#Dataset
skincare = pd.read_csv("export_skincare.csv", encoding='ISO-8859-1', index_col=None)

# Main menu function
def streamlit_menu():
    with st.sidebar:
        selected = option_menu(
            menu_title="  ",
            options=["Profile", "SkinSavvy", "Get Recommendation", "Skin Care 101"],
            icons=["stars", "house", "book", "person"],
            menu_icon="cast",
            default_index=1,
            orientation="Vertical"
        )
    return selected

# Main function
def main():
    credentials = load_credentials()
    initialize_session_state()

    selected = streamlit_menu()

    if selected == "Profile":
        st.title("Profile")

        if not st.session_state.logged_in:
            st.info("🔐 Please log in or sign up to access your profile.")

            tab1, tab2 = st.tabs(["Login", "Sign Up"])

            with tab1:
                login(credentials)
                if st.session_state.logged_in:
                    st.success("✅ Successfully Logged In!")
                    st.experimental_rerun()

            with tab2:
                signup(credentials)
                # After signup, user can go to login manually

        else:
            profile(credentials)

    elif selected == "SkinSavvy":
        Skin_care()

    elif selected == "Get Recommendation":
        skincare_recommendation_page()

    elif selected == "Skin Care 101":
        skin_care_101_page()

    # Optional sidebar hint if not logged in
    if not st.session_state.logged_in:
        st.sidebar.markdown("👤 Not Logged In")
        st.sidebar.markdown("Access your profile by logging in from the **Profile** tab.")




def Skin_care():
    st.title("SkinSavvy")
    st.write('---') 

    st.write(
        """
        ##### **Welcome to the SkinSavvy! We're here to help you find the perfect skincare products to your skin type and concerns. Rest assured, your skincare journey is in good hands with our personalized recommendations!**
        """)
    
    # displaying a local video file
    video_file = open("skincare.mp4", "rb").read()
    st.video(video_file, start_time=1)  # displaying the video 
    
    st.write(' ') 
    st.write(' ')
    st.write(
        """
        ##### You will receive skincare product recommendations from over 300+ products, curated from India’s top 9 affordable skincare brands, tailored to your specific skin needs. The system considers 5 skincare categories, 5 different skin types, and various skin concerns to offer you the best personalized suggestions. While the system provides recommendations based on the data you enter, it is not a substitute for scientific consultation.
        """
    )
    
    # Brand-related information with increased text size and underlined headings
    st.markdown("<p style='font-size:22px; text-decoration: underline;'><b>The Derma Co:</b></p>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:18px;'>Known for its dermatologist-formulated products that focus on solving specific skin concerns, from acne to pigmentation, with a blend of science and natural ingredients.</p>", unsafe_allow_html=True)

    st.markdown("<p style='font-size:22px; text-decoration: underline;'><b>Dot & Key:</b></p>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:18px;'>This brand specializes in products that address skin concerns like dullness, dryness, and dark circles, with a focus on hydration and a gentle skincare routine.</p>", unsafe_allow_html=True)

    st.markdown("<p style='font-size:22px; text-decoration: underline;'><b>Plum:</b></p>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:18px;'>A vegan, cruelty-free brand offering a variety of skincare products that cater to different skin types, emphasizing clean beauty and nourishment.</p>", unsafe_allow_html=True)

    st.markdown("<p style='font-size:22px; text-decoration: underline;'><b>Minimalist:</b></p>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:18px;'>Offering simple, effective, and non-complicated skincare solutions, Minimalist focuses on key ingredients to target specific skin concerns without unnecessary fillers.</p>", unsafe_allow_html=True)

    st.markdown("<p style='font-size:22px; text-decoration: underline;'><b>The Ordinary:</b></p>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:18px;'>Known for its clinically effective formulations that focus on active ingredients, The Ordinary delivers high-performance skincare that is both affordable and results-driven.</p>", unsafe_allow_html=True)

    st.markdown("<p style='font-size:22px; text-decoration: underline;'><b>Cetaphil:</b></p>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:18px;'>A trusted, dermatologist-recommended brand for sensitive skin, Cetaphil provides gentle, non-irritating skincare solutions that focus on hydration and skin barrier repair.</p>", unsafe_allow_html=True)

    st.markdown("<p style='font-size:22px; text-decoration: underline;'><b>Pilgrim:</b></p>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:18px;'>A clean beauty brand inspired by global ingredients, Pilgrim offers solutions based on natural, potent actives to tackle issues like pigmentation, acne, and dullness.</p>", unsafe_allow_html=True)

    st.markdown("<p style='font-size:22px; text-decoration: underline;'><b>Mama Earth:</b></p>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:18px;'>A popular brand that focuses on eco-friendly, toxin-free products, Mama Earth offers skincare solutions for a variety of skin concerns, using natural ingredients for gentle care.</p>", unsafe_allow_html=True)

    st.markdown("<p style='font-size:22px; text-decoration: underline;'><b>Aqualogica:</b></p>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:18px;'>Specializing in water-based hydration, Aqualogica provides products that focus on moisture balance and skin health, making it ideal for dry and dehydrated skin.</p>", unsafe_allow_html=True)
        
    st.write(
        """
        **Have a great day ahead :)**
        """)
    
    st.info('Credit: Created by Bharath Chandra Kollapu')

def skincare_recommendation_page():
    st.title("Get Recommendation")
    st.write(
        """
        ##### **To get recommendations, please enter your skin type, concerns, and desired benefits to get the right skincare product recommendations**
        """
    )
    st.write('---')

    # Predefined visible effects per product type
    visible_effects_by_type = {
        "Face Wash": [
            "Brightens Skin", "Cleanses Skin", "Controls Acne", "Hydrates Skin",
            "Reduces Acne", "Removes Tan", "Reduces Acne Marks", "Smooth Skin",
            "Even Tone Skin", "Minimizes Pores", "Controls Oil", "Glow Natural Pink"
        ],
        "Serum": [
            "Brightens Skin", "Reduces Dark Spots", "Hydrates Skin", "Minimizes Pores",
            "Reduces Wrinkles", "Even Tone Skin", "Glowing Skin", "Reduces Acne",
            "Reduces Acne Marks", "Controls Oil", "Smooth Skin"
        ],
        "Moisturizer": [
            "Hydrates Skin", "Smooth Skin", "Reduces Acne Marks", "Non-Sticky",
            "Reduces Wrinkles", "Brightens Skin", "Even Tone Skin", "Glowing Skin"
        ],
        "Sunscreen": [
            "SPF 50 PA++++", "Brightens Skin", "Hydrates Skin", "Removes Tan",
            "Glowing Skin", "Non-Sticky", "SPF 60 PA+++", "SPF 50+ PA++++",
            "Smooth Skin", "SPF 30", "SPF 45 PA+++", "SPF 40 PA++", "SPF 35 PA+++"
        ],
        "Toner": [
            "Hydrates Skin", "Minimizes Pores", "Brightens Skin", "Even Tone Skin",
            "Reduces Dark Spots", "Cleanses Skin", "Controls Oil", "Smooth Skin"
        ]
    }

    first, last = st.columns(2)

    # Product Type selection
    category = first.selectbox(label='Product Category:', options=visible_effects_by_type.keys())
    category_df = skincare[skincare['product_type'] == category]

    # Skin Type selection
    skin_type = last.selectbox(label='Your Skin Type:', options=['Normal', 'Dry', 'Oily', 'Combination', 'Sensitive'])
    category_skin_df = category_df[category_df[skin_type] == 1]

    # Dynamically show visible effects
    visible_effects = visible_effects_by_type[category]
    selected_effects = st.multiselect("Visible Effects:", options=visible_effects)

    # Final filtered results
    final_df = category_skin_df[
        category_skin_df['notable_effects'].apply(
            lambda x: any(effect in x for effect in selected_effects)
        )
    ]

    # Recommendations
    if st.button("Find Recommendations"):
        recommendations = final_df[['product_name', 'brand', 'price', 'product_link']].drop_duplicates().head(5)

        if not recommendations.empty:
            st.write("### Recommended Products For You")
            for _, row in recommendations.iterrows():
                st.markdown(
                    f"""
                    <span style='font-size: 18px;'>**{row['product_name']}**  <br>
                    Brand: {row['brand']}  <br>
                    Price: {row['price']}  <br>
                    <a href='{row['product_link']}' target='_blank'>View Product</a>  
                    <br>---</span>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.warning("No products found matching your criteria.")

# Skin Care 101 page

def skin_care_101_page():
    st.title("Skin Care 101")
    st.write('---') 

    # Intro text with increased font size
    st.markdown("<p style='font-size:20px;'>Here are tips and tricks that you can follow to maximize the use of skincare products</p>", unsafe_allow_html=True)

    # Facial Wash
    with st.expander(" **Facial Wash**"):
        st.markdown("<p style='font-size:22px;'><b>🌊 Facial Wash</b></p>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:18px;'>- Use the recommended facial wash product or one that is suitable for you</p>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:18px;'>- Wash your face a maximum of 2 times a day, in the morning and at night before bed. Washing your face too often will strip away the skin's natural oils...</p>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:18px;'>- Avoid scrubbing your face harshly as it can remove the skin's natural protective barrier...</p>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:18px;'>- The best way to clean your skin is to use your fingertips for 30-60 seconds with circular and massaging motions...</p>", unsafe_allow_html=True)

    # Toner
    with st.expander(" **Toner**"):
        st.markdown("<p style='font-size:22px;'><b>💧 Toner</b></p>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:18px;'>- Use the recommended toner or one that is suitable for you</p>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:18px;'>- Pour the toner onto a cotton pad and gently wipe your face. For better results...</p>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:18px;'>- Use toner after washing your face...</p>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:18px;'>- For those with sensitive skin, avoid skincare products that contain fragrance as much as possible...</p>", unsafe_allow_html=True)

    # Serum
    with st.expander(" **Serum**"):
        st.markdown("<p style='font-size:22px;'><b>💧 Serum</b></p>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:18px;'>- Use the recommended serum or one that is suitable for you for better results</p>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:18px;'>- Serum should be applied after the face is completely clean to ensure it absorbs properly...</p>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:18px;'>- Apply serum in the morning and at night before bed...</p>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:18px;'>- Choose a serum that suits your needs, such as removing acne scars, dark spots, anti-aging, or other benefits...</p>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:18px;'>- To apply serum for better absorption, pour it into the palm of your hand, gently pat it onto your face...</p>", unsafe_allow_html=True)

    # Moisturizer
    with st.expander(" **Moisturizer**"):
        st.markdown("<p style='font-size:22px;'><b>🧴 Moisturizer</b></p>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:18px;'>- Use the recommended moisturizer or one that is suitable for you for better results</p>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:18px;'>- Moisturizer is essential as it locks in moisture and various nutrients from the serum...</p>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:18px;'>- For better results, use different moisturizers in the morning and at night...</p>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:18px;'>- Allow a gap of 2-3 minutes between applying serum and moisturizer...</p>", unsafe_allow_html=True)

    # Sunscreen
    with st.expander(" **Sunscreen**"):
        st.markdown("<p style='font-size:22px;'><b>☀️ Sunscreen</b></p>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:18px;'>- Use the recommended sunscreen or one that is suitable for you for better results</p>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:18px;'>- Sunscreen is the key to all skincare products as it protects the skin from harmful rays...</p>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:18px;'>- Apply sunscreen approximately along the length of your index and middle fingers...</p>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:18px;'>- Reapply sunscreen every 2-3 hours or as needed...</p>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:18px;'>- Continue to use sunscreen even indoors...</p>", unsafe_allow_html=True)

    # Don't Switch Skincare Products Frequently
    with st.expander(" **Don't Switch Skincare Products Frequently**"):
        st.markdown("<p style='font-size:22px;'><b>🚫 Don't Switch Skincare Products Frequently</b></p>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:18px;'>Frequently switching skincare products can cause facial skin to become stressed as it has to adapt to the ingredients...</p>", unsafe_allow_html=True)

    # Be Consistent
    with st.expander(" **Be Consistent**"):
        st.markdown("<p style='font-size:22px;'><b>🔄 Be Consistent</b></p>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:18px;'>The key to skincare is consistency. Be diligent and persistent in using skincare products because the results are not instant...</p>", unsafe_allow_html=True)

    # Your Face is an Asset
    with st.expander(" **Your Face is an Asset**"):
        st.markdown("<p style='font-size:22px;'><b>💖 Your Face is an Asset</b></p>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:18px;'>The diverse appearances of people are a gift from the Creator. Take good care of that gift as an expression of gratitude...</p>", unsafe_allow_html=True)


main()

# {"Bharath": {"password": "Bharath@sr7", "name": "Bharath", "email": "bharath.leo307@gmail.com", "phone_number": "7386985947", "profile_picture": null}, "bharath.leo307@gmail.com": {"password": "Bharath@sr7", "name": "Bharath", "phone_number": "07386985947", "profile_picture": null}, "bharath.kollapu7@gmail.com": {"password": "Ck@7", "name": "ck", "phone_number": "7386985947", "profile_picture": "profile_pictures/bharath.kollapu7@gmail.com_profile_picture.jpg"}, "1234@gmail.com": {"password": "123", "name": "xyz", "phone_number": "123456789", "profile_picture": null}, "jamilanister7@gmail.com": {"password": "Varun@7", "name": "Varun", "phone_number": "9398015991", "profile_picture": null}, "myneninagakalyan286@gmail.com": {"password": "M.22bce7660@123", "name": "myneni naga kalyan", "phone_number": "9182727018", "profile_picture": null}, "pravallikatapa01@gmail.com": {"password": "Pravali@787", "name": "Tapa pravallika", "phone_number": "9182359787", "profile_picture": null}}