import streamlit as st

# ---------- PAGE CONFIGURATION ----------
st.set_page_config(
    page_title="AquaScope AI",
    page_icon="🔬",
    layout="wide"
)

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

    st.write(
        "Upload one or more microscopic images for screening."
    )

    uploaded_files = st.file_uploader(
        "Upload microscope images",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True
    )

    if uploaded_files:

        st.success(
            f"{len(uploaded_files)} image(s) uploaded successfully!"
        )

        st.subheader("Uploaded Images")

        for uploaded_file in uploaded_files:

            st.image(
                uploaded_file,
                caption=uploaded_file.name,
                use_container_width=True
            )

        st.divider()

        if st.button("🔍 Analyze Images"):

            st.info("AI analysis is being performed...")

            st.subheader("Screening Results")

            for uploaded_file in uploaded_files:

                st.write(
                    f"### 📷 {uploaded_file.name}"
                )

                col1, col2 = st.columns(2)

                with col1:
                    st.write("**Detected Category**")
                    st.write("Aquatic Microorganism")

                with col2:
                    st.write("**Confidence**")
                    st.write("Demo Result")

                st.success(
                    "Screening completed successfully."
                )

                st.divider()

    else:

        st.warning(
            "Please upload microscope images to start screening."
        )


# ---------- ANALYSIS ----------
elif page == "📊 Analysis":

    st.header("📊 Analysis Dashboard")

    st.write(
        "This section displays analysis information generated "
        "from uploaded microscopic images."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Images Analyzed", "0")

    with col2:
        st.metric("Detected Samples", "0")

    with col3:
        st.metric("Status", "Ready")

    st.info(
        "AI-based classification results will be displayed here "
        "when the trained model is connected."
    )


# ---------- ABOUT ----------
elif page == "ℹ️ About":

    st.header("ℹ️ About AquaScope AI")

    st.write(
        "AquaScope AI is designed as a low-cost intelligent microscopy "
        "platform for rapid aquatic microorganism screening."
    )

    st.write("### Key Features")

    st.write("• Multiple microscopic image upload")
    st.write("• AI-assisted screening")
    st.write("• Rapid analysis")
    st.write("• Simple user interface")
    st.write("• Future integration with trained AI models")

    st.divider()

    st.caption(
        "AquaScope AI — AI + Microscopy for Aquatic Microorganism Screening"
    )
