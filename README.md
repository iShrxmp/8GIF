<div align="center">
  <img src="assets/icon.png" alt="8GIF Logo" width="120" />
  <h1>8GIF</h1>
  <p><strong>Professional GIF & Image Optimizer</strong></p>
  <p>
    <img src="https://img.shields.io/badge/platform-Windows-blue?style=flat-square" />
    <img src="https://img.shields.io/badge/python-3.10%2B-blue?style=flat-square&logo=python" />
    <img src="https://img.shields.io/badge/UI-CustomTkinter-informational?style=flat-square" />
    <img src="https://img.shields.io/github/v/release/iShrxmp/8GIF?style=flat-square&color=brightgreen" />
  </p>
</div>

---

## What is 8GIF?

**8GIF** is a lightweight, feature-rich desktop application for optimizing GIFs and images. Built with a modern dark UI, it gives you full control over compression, cropping, resizing, and exporting — all without needing command-line tools or online services.

---

## Features

### GIF Optimizer
- **Live Before / After Preview** — Animate both the original and processed GIF side by side in real time
- **Compression Slider** — Manually control quality from 0% to 100%
- **Discord Mode** — Automatically compresses to under 10 MB for Discord uploads
- **Resize** — Pixel-based or percentage-based rescaling with Adaptive or Stretch behavior
- **Visual Crop** — Draw a selection rectangle, ellipse, star, or freehand lasso directly on the canvas
- **Shape Masking** — Crop with transparency using Circle, Star, or Lasso masks
- **Finalize & Save** — Review the result before committing to a file

### Image Tools
- **Background Eraser** — Remove solid backgrounds using color sampling or auto corner detection, with adjustable tolerance
- **PNG → ICO Converter** — Convert any image to a multi-size `.ico` file (16 / 32 / 48 / 64 / 128 / 256 px)
- **Save PNG** — Export the result with full transparency preserved

### Multilingual UI
Switch the interface language instantly between **English**, **Turkish (Türkçe)** and **German (Deutsch)**.

---

## Screenshots

> _Coming soon_

---

## Download

Head to the [**Releases**](../../releases/latest) page and download **8GIF.exe** — no installation required, just run it.

| Platform | Status |
|---|---|
| Windows 10 / 11 | Fully supported |
| macOS / Linux | Not tested |

---

## How to Use

### GIF Optimizer
1. Click **Load New GIF** (or any supported image format)
2. Draw a crop selection on the left canvas (optional)
3. Adjust resize, compression, and shape settings in the panel
4. Click **Update Preview** to see the result on the right
5. Click **Finalize & Save** to export

### Image Tools
1. Click **Image Tools** in the top bar
2. Open any PNG / JPEG / WebP image
3. Use **Background Eraser** to remove the background (auto corner detection or manual colour pick)
4. Export as **PNG** (with transparency) or convert to **ICO**

---

## Supported Formats

| Input | Output |
|---|---|
| GIF, PNG, WebP, JPG, BMP, TIFF | GIF, PNG, ICO |

---

## Built With

| Library | Purpose |
|---|---|
| [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) | Modern dark UI |
| [Pillow](https://python-pillow.org/) | Image processing |
| [PyInstaller](https://pyinstaller.org/) | Standalone executable |

---

## License

Copyright (c) 2026 iShrxmp. All Rights Reserved.

This software is proprietary. Redistribution, modification, or commercial use is not permitted without explicit written permission from the author.
