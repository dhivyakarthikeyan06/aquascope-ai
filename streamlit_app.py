import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="AquaScope AI",
    page_icon="🔬",
    layout="wide"
)

# ---------- LOAD MODEL ----------
@st.cache_resource
def load_model():
    return tf.keras.models.load_model(
        "aquascope_model.keras",
        compile=False
    )

model = load_model()

# ---------- LOAD SIMILARITY REFERENCE ----------
similarity_data = np.load(
    "aquascope_similarity_reference.npz"
)

all_embeddings = similarity_data["all_embeddings"]
all_labels = similarity_data["all_labels"]
SIMILARITY_THRESHOLD = float(
    similarity_data["similarity_threshold"]
)

# ---------- EMBEDDING MODEL ----------
embedding_model = tf.keras.Model(
    inputs=model.input,
    outputs=model.get_layer(
        "global_average_pooling2d"
    ).output
)
# ---------- CLASSES ----------
class_names = ["Ciliates", "Diatoms"]

# ---------- CHARACTERISTICS ----------
characteristics = {
    "Ciliates": [
        "Single-celled microorganisms",
        "Covered with hair-like cilia",
        "Cilia help in movement and feeding",
        "Commonly found in aquatic environments"
    ],
    "Diatoms": [
        "Microscopic photosynthetic algae",
        "Have a silica-based cell wall",
        "Can have round, elongated or symmetrical shapes",
        "Important primary producers in aquatic ecosystems"
    ]
}

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
        st.metric("Classes", "2")

    st.divider()

    st.info(
        "Upload a microscopic image to screen for Ciliates or Diatoms."
    )

# ---------- MICROORGANISM SCREENING ----------
elif page == "🔬 Microorganism Screening":

    st.header("🔬 Microorganism Screening")

    st.write(
        "Upload a microscopic image for AI-based screening."
    )

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

            with st.spinner("AI is analyzing the image..."):

                # Resize image
                img = image.resize((224, 224))

                # Convert image to array
                img_array = np.array(
                    img,
                    dtype=np.float32
                )

                # Add batch dimension
                img_array = np.expand_dims(
                    img_array,
                    axis=0
                )

                # ---------- CLASS PREDICTION ----------
                prediction = model(
                    img_array,
                    training=False
                ).numpy()

                predicted_index = np.argmax(
                    prediction[0]
                )

                confidence = float(
                    np.max(prediction[0]) * 100
                )

                predicted_class = class_names[
                    predicted_index
                ]

               # ---------- SIMILARITY-BASED OOD CHECK ----------
embedding = embedding_model(
    img_array,
    training=False
).numpy()[0]

embedding = embedding / (
    np.linalg.norm(embedding) + 1e-8
)

# Compare with all known training embeddings
similarities = np.dot(
    all_embeddings,
    embedding
)

best_similarity = float(
    np.max(similarities)
)

best_index = int(
    np.argmax(similarities)
)

closest_class = class_names[
    int(all_labels[best_index])
]

# ---------- UNKNOWN CHECK ----------
is_unknown = (
    best_similarity < SIMILARITY_THRESHOLD
) 
            st.divider()
            st.subheader("🧬 Screening Result")

            if is_unknown:

                st.error(
                    "⚠️ Unrecognized Microorganism"
                )

                st.write(
                    f"Model confidence: {confidence:.2f}%"
                )

                st.warning(
                    "The image does not sufficiently match "
                    "the trained Ciliates or Diatoms classes. "
                    "Manual verification is recommended."
                )
            
            else:

                st.success(
                    f"Predicted Class: {predicted_class}"
                )

                st.metric(
                    "Confidence",
                    f"{confidence:.2f}%"
                )

                st.subheader(
                    f"🔬 Characteristics of {predicted_class}"
                )

                for item in characteristics[
                    predicted_class
                ]:
                    st.write(f"• {item}")

            # ---------- PROBABILITIES ----------
            st.subheader("📊 Class Probabilities")

            for i, class_name in enumerate(class_names):

                probability = float(
                    prediction[0][i] * 100
                )

                st.write(
                    f"{class_name}: {probability:.2f}%"
                )

                st.progress(
                    float(prediction[0][i])
                )

    else:

        st.warning(
            "Please upload a microscope image "
            "to start screening."
        )

# ---------- ANALYSIS ----------
elif page == "📊 Analysis":

    st.header("📊 Analysis Dashboard")

    st.write(
        "AI-based classification results generated "
        "from microscopic images."
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Supported Classes", "2")

    with col2:
        st.metric("Input Type", "Microscopic Image")

    st.divider()

    st.write("### Supported Microorganisms")

    st.write("🔵 Ciliates")
    st.write("🟢 Diatoms")

    st.info(
        "Images that do not sufficiently match the trained "
        "classes are displayed as Unrecognized for manual verification."
    )

# ---------- ABOUT ----------
elif page == "ℹ️ About":

    st.header("ℹ️ About AquaScope AI")

    st.write(
        "AquaScope AI is designed as a low-cost intelligent "
        "microscopy platform for rapid aquatic microorganism screening."
    )

    st.write("### Key Features")

    st.write("• AI-based image classification")
    st.write("• Microscopic image upload")
    st.write("• Rapid screening")
    st.write("• Ciliates and Diatoms classification")
    st.write("• OOD-based unrecognized screening")
    st.write("• Confidence score")
    st.write("• Microorganism characteristics")
    st.write("• Simple user interface")

    st.divider()

    st.write("### AI Model")

    st.write(
        "The system uses a MobileNetV2-based transfer learning "
        "model for aquatic microorganism image classification "
        "with an additional embedding-based OOD screening layer."
    )

    st.caption(
        "AquaScope AI — AI + Microscopy for Aquatic Microorganism Screening"
    )
