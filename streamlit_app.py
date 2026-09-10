import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image

# ---------- PAGE CONFIGURATION ----------
st.set_page_config(
    page_title="AquaScope AI",
    page_icon="🔬",
    layout="wide"
)

# ---------- LOAD TRAINED MODEL ----------
@st.cache_resource
def load_model():
   return tf.keras.models.load_model("aquascope_model.h5", compile=False) 

model = load_model()

# ---------- HEADER ----------
st.title("🔬 AquaScope AI")
st.subheader("AI-Powered Aquatic Microorganism Screening")

st.write(
    "A low-cost intelligent microscopy platform for rapid "
    "screening and identification of aquatic microorganisms."
)

st.divider()

# ---------- SIDEBAR ----------
st.sidebar.header("AquaScope AI")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "🔬 Microorganism Screening",
        "📊 Analysis",
        "ℹ️ About"
    ]
)

# ---------- HOME ----------
if page == "🏠 Home":

    st.header("Welcome to AquaScope AI")

    st.write(
        "AquaScope AI combines microscopy and artificial intelligence "
        "to support rapid aquatic microorganism screening."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Technology", "AI + Microscopy")

    with col2:
        st.metric("Application", "Aquatic Screening")

    with col3:
        st.metric("Analysis", "Image Based")

    st.divider()

    st.info(
        "Upload aquatic microorganism images to begin the screening process."
    )


# ---------- MICROORGANISM SCREENING ----------
elif page == "🔬 Microorganism Screening":

    st.header("🔬 Microorganism Screening")

    st.write("Upload a microscopic image for AI-based screening.")

    uploaded_file = st.file_uploader(
        "Upload microscope image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file:

        image = Image.open(uploaded_file).convert("RGB")

        st.image(
            image,
            caption="Uploaded Microscopic Image",
            use_container_width=True
        )

        if st.button("🔍 Analyze Image"):

            st.info("AI analysis is being performed...")

            # Resize image
            img = image.resize((224, 224))

            # Convert image to array
            img_array = np.array(img) / 255.0

            # Add batch dimension
            img_array = np.expand_dims(img_array, axis=0)

            # Prediction
            prediction = model.predict(img_array)

            predicted_class = np.argmax(prediction[0])
            confidence = np.max(prediction[0]) * 100

            st.subheader("🧬 Screening Result")

            st.success(
                f"Predicted Class: {predicted_class}"
            )

            st.write(
                f"Confidence: {confidence:.2f}%"
            )

    else:

        st.warning(
            "Please upload a microscope image to start screening."
        )


# ---------- ANALYSIS ----------
elif page == "📊 Analysis":

    st.header("📊 Analysis Dashboard")

    st.write(
        "AI-based classification results generated from "
        "microscopic images."
    )

    st.info(
        "Upload and analyze an image from the Microorganism Screening section."
    )


# ---------- ABOUT ----------
elif page == "ℹ️ About":

    st.header("ℹ️ About AquaScope AI")

    st.write(
        "AquaScope AI is designed as a low-cost intelligent microscopy "
        "platform for rapid aquatic microorganism screening."
    )

    st.write("### Key Features")

    st.write("• AI-based image classification")
    st.write("• Microscopic image upload")
    st.write("• Rapid screening")
    st.write("• Simple user interface")
    st.write("• Trained deep learning model")

    st.divider()

    st.caption(
        "AquaScope AI — AI + Microscopy for Aquatic Microorganism Screening"
    )
