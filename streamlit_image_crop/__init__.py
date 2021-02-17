from __future__ import annotations

from typing import Any
from typing import Optional
from typing import Union

from dataclasses import dataclass

from PIL.Image import Image


_DEBUG = False
_component_func: Any = None


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
    image_alt: Optional[str] = None,
    min_width: Optional[int] = None,
    min_height: Optional[int] = None,
    max_width: Optional[int] = None,
    max_height: Optional[int] = None,
    keep_selection: Optional[bool] = None,
    disabled: Optional[bool] = None,
    locked: Optional[bool] = None,
    rule_of_thirds: Optional[bool] = None,
    circular_crop: Optional[bool] = None,
    key: Optional[str] = None,
) -> Optional[Image]:
    import dataclasses
    from io import BytesIO
    from os import path

    from PIL.Image import open as open_image
    from streamlit.components import v1 as components
    from streamlit.elements.image import image_to_url

    global _component_func

    if _component_func is None:
        if _DEBUG:
            _component_func = components.declare_component(
                "image_crop",
                url="http://localhost:3001",
            )
        else:
            _component_func = components.declare_component(
                "image_crop",
                path=path.join(path.dirname(path.abspath(__file__)), "frontend/build"),
            )

    if isinstance(image, Image):
        image_ = image
    else:
        image_ = open_image(BytesIO(image))

    src = image_to_url(
        image_,
        width=500,
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

    result = _component_func(
        src=src,
        image_alt=image_alt,
        minWidth=min_width,
        minHeight=min_height,
        maxWidth=max_width,
        maxHeight=max_height,
        keepSelection=keep_selection,
        disabled=disabled,
        locked=locked,
        ruleOfThirds=rule_of_thirds,
        circularCrop=circular_crop,
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
        return image_.crop((x0, y0, x1, y1))
