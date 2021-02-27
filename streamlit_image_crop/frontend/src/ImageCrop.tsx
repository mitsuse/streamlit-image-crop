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
        src={buildMediaUri(src)}
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

// ---- Copied from the streamlit ----
const WWW_PORT_DEV = 3000
const WEBSOCKET_PORT_DEV = 8501
const IS_DEV_ENV = +window.location.port === WWW_PORT_DEV

const FINAL_SLASH_RE = /\/+$/
const INITIAL_SLASH_RE = /^\/+/

interface BaseUriParts {
  host: string
  port: number
  basePath: string
}

function isHttps(): boolean {
  return window.location.href.startsWith("https://")
}

function getWindowBaseUriParts(): BaseUriParts {
  const host = window.location.hostname

  let port
  if (IS_DEV_ENV) {
    port = WEBSOCKET_PORT_DEV
  } else if (window.location.port) {
    port = Number(window.location.port)
  } else {
    port = isHttps() ? 443 : 80
  }

  const basePath = window.location.pathname
    .replace(FINAL_SLASH_RE, "")
    .replace(INITIAL_SLASH_RE, "")

  return { host, port, basePath }
}

function makePath(basePath: string, subPath: string): string {
  basePath = basePath.replace(FINAL_SLASH_RE, "").replace(INITIAL_SLASH_RE, "")
  subPath = subPath.replace(FINAL_SLASH_RE, "").replace(INITIAL_SLASH_RE, "")

  if (basePath.length === 0) {
    return subPath
  }

  return `${basePath}/${subPath}`
}

function buildHttpUri(
  { host, port, basePath }: BaseUriParts,
  path: string
): string {
  const protocol = isHttps() ? "https" : "http"
  const fullPath = makePath(basePath, path)
  return `${protocol}://${host}:${port}/${fullPath}`
}

function buildMediaUri(uri: string): string {
  return uri.startsWith("/media")
    ? buildHttpUri(getWindowBaseUriParts(), uri)
    : uri
}
// ----

export default withStreamlitConnection(ImageCrop)
