from __future__ import annotations

from typing import Callable
from typing import Optional
from typing import Tuple
from typing import Union

from dataclasses import dataclass

from PIL.Image import Image


_DEBUG = False
_impl: Optional[Tuple[Callable, Callable[[str], str]]] = None


@dataclass(frozen=True)
class Crop:
    aspect: Optional[float] = None
    x: Optional[float] = None
    y: Optional[float] = None
    width: Optional[float] = None
    height: Optional[float] = None


def image_crop(
    image: Union[bytes, Image],
    crop: Optional[Crop] = None,
    width_preview: Optional[int] = None,
    image_alt: Optional[str] = None,
    min_width: Optional[int] = None,
    min_height: Optional[int] = None,
    max_width: Optional[int] = None,
    max_height: Optional[int] = None,
    # FIXME: Changing these properties, the component is rerendered unfortunately.
    # ----
    # keep_selection: Optional[bool] = None,
    # disabled: Optional[bool] = None,
    # locked: Optional[bool] = None,
    rule_of_thirds: Optional[bool] = None,
    circular_crop: Optional[bool] = None,
    # ----
    key: Optional[str] = None,
) -> Optional[Image]:
    import dataclasses
    from io import BytesIO
    from os import path

    import streamlit as st
    from PIL.Image import composite as composite_image
    from PIL.Image import new as new_image
    from PIL.Image import open as open_image
    from PIL.ImageDraw import Draw
    from streamlit.components import v1 as components
    from streamlit.elements.image import image_to_url

    global _impl

    if _impl is None:
        if _DEBUG:
            option_address = st.get_option("browser.serverAddress")
            option_port = st.get_option("browser.serverPort")
            _impl = (
                components.declare_component(
                    "image_crop",
                    url="http://localhost:3001",
                ),
                lambda s: f"http://{option_address}:{option_port}" + s,
            )
        else:
            _impl = (
                components.declare_component(
                    "image_crop",
                    path=path.join(
                        path.dirname(path.abspath(__file__)), "frontend/build"
                    ),
                ),
                lambda s: s,
            )

    if isinstance(image, Image):
        image_ = image
    else:
        image_ = open_image(BytesIO(image))

    width, _ = image_.size

    src = image_to_url(
        image_,
        width=min(width, width_preview) if width_preview else width,
        clamp=False,
        channels="RGB",
        output_format="auto",
        image_id="foo",
    )

    crop_ = None if crop is None else dataclasses.asdict(crop)

    default = {
        "width": 0.0,
        "height": 0.0,
        "x": 0.0,
        "y": 0.0,
    }

    component, build_url = _impl

    result = component(
        src=build_url(src),
        image_alt=image_alt,
        minWidth=min_width,
        minHeight=min_height,
        maxWidth=max_width,
        maxHeight=max_height,
        # FIXME: Changing these properties, the component is rerendered unfortunately.
        # ----
        keepSelection=None,
        disabled=None,
        locked=None,
        ruleOfThirds=rule_of_thirds,
        circularCrop=circular_crop,
        # ----
        crop=crop_,
        key=key,
        default=default,
    )

    w, h = image_.size

    w_crop = int(w * float(result["width"]) / 100)
    h_crop = int(h * float(result["height"]) / 100)
    x0 = int(w * float(result["x"]) / 100)
    y0 = int(h * float(result["y"]) / 100)
    x1 = x0 + w_crop
    y1 = y0 + h_crop

    if w_crop <= 0 or h_crop <= 0:
        return None
    else:
        image_crop = image_.crop((x0, y0, x1, y1))
        if circular_crop:
            background = new_image("RGBA", (w_crop, h_crop), (0, 0, 0, 0))
            mask = new_image("L", (w_crop, h_crop), 0)
            draw = Draw(mask)
            draw.ellipse((0, 0, w_crop, h_crop), fill="white")
            image_crop = composite_image(image_crop, background, mask)

        return image_crop
