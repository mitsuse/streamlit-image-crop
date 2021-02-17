import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib"
import React, { ReactNode } from "react"
import ReactCrop from "react-image-crop"
import "react-image-crop/dist/ReactCrop.css"

class ImageCrop extends StreamlitComponentBase<ReactCrop.Crop> {
  public state: ReactCrop.Crop = {}

  public render = (): ReactNode => {
    const src = this.props.args["src"]
    const crop = { ...this.props.args["crop"], ...this.state }
    const imageAlt = this.props.args["imageAlt"]
    const minWidth = this.props.args["minWidth"]
    const minHeight = this.props.args["minHeight"]
    const maxWidth = this.props.args["maxWidth"]
    const maxHeight = this.props.args["maxHeight"]
    const keepSelection = this.props.args["keepSelection"]
    const disabled = this.props.args["disabled"]
    const locked = this.props.args["locked"]
    const ruleOfThirds = this.props.args["ruleOfThirds"]
    const circularCrop = this.props.args["circularCrop"]

    return (
      <ReactCrop
        src={src}
        crop={crop}
        imageAlt={imageAlt}
        minWidth={minWidth}
        minHeight={minHeight}
        maxWidth={maxWidth}
        maxHeight={maxHeight}
        keepSelection={keepSelection}
        disabled={disabled}
        locked={locked}
        ruleOfThirds={ruleOfThirds}
        circularCrop={circularCrop}
        onChange={(newCrop) => this.setState(newCrop)}
        onComplete={this.onComplete}
      />
    )
  }

  private onComplete = (
    _: ReactCrop.Crop,
    crop: ReactCrop.PercentCrop
  ): void => {
    Streamlit.setComponentValue(crop)
  }
}

export default withStreamlitConnection(ImageCrop)
