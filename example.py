from __future__ import annotations

import streamlit as st
import streamlit_image_crop
from streamlit_image_crop import image_crop
from streamlit_image_crop import Crop

streamlit_image_crop._DEBUG = True


def main() -> None:
    st.title("React Image Crop")

    st.sidebar.header("Parameters")

    fixed_aspect_ratio = st.sidebar.checkbox("Fixed aspect cropping", value=False)

    if fixed_aspect_ratio:
        aspect_ratio = st.sidebar.slider(
            "Aspect ratio",
            value=1.0,
            min_value=0.2,
            max_value=5.0,
            step=0.2,
        )
    else:
        aspect_ratio = None

    min_width = st.sidebar.slider(
        "Minimum width",
        value=0,
        min_value=0,
        max_value=200,
    )
    min_height = st.sidebar.slider(
        "Minimum height",
        value=0,
        min_value=0,
        max_value=200,
    )

    max_width = st.sidebar.slider(
        "Maximum width",
        value=1000,
        min_value=0,
        max_value=1000,
    )
    max_height = st.sidebar.slider(
        "Maximum height",
        value=1000,
        min_value=0,
        max_value=1000,
    )

    keep_selection = st.sidebar.checkbox("Keep selection", value=False)
    disabled = st.sidebar.checkbox("disabled", value=False)
    locked = st.sidebar.checkbox("locked", value=False)
    rule_of_thirds = st.sidebar.checkbox("Rule of Thirds", value=False)
    circular_crop = st.sidebar.checkbox("Circular Crop", value=False)

    f = st.file_uploader("Choose a image")
    if f is None:
        return

    bytes_image = f.getvalue()

    col_left, col_right = st.beta_columns(2)

    with col_left:
        image_cropped = image_crop(
            bytes_image,
            crop=Crop(aspect=aspect_ratio),
            min_width=min_width,
            min_height=min_height,
            max_width=max_width,
            max_height=max_height,
            keep_selection=keep_selection,
            disabled=disabled,
            locked=locked,
            rule_of_thirds=rule_of_thirds,
            circular_crop=circular_crop,
        )

    if image_cropped is None:
        return

    with col_right:
        st.image(image_cropped)


main()
