# Android-to-iOS Plist Converter

A Python script for converting Android XML save-game files (structured as `<map>`, `<list>`, `<int>`, `<float>`, `<bool>`, etc.) into an iOS-compatible XML Property List (`.plist`). This ensures correct key names, value types, nested structures, and insertion order for use in your iOS app.

---

## Features

- **Automatic percent-unescaping** of `name` attributes (e.g., `ui%3Acompass` → `ui:compass`).
- **Type conversion** for `<int>`, `<float>`, `<bool>`, `<map>`, `<list>`, and fallback to strings.
- **Nested dictionaries and arrays** supported via recursive parsing.
- **Ordered keys** preserved (requires Python 3.7+; for older versions, install `ordereddict`).
- **Easy customization** for additional tags (e.g., `<long>`, `<date>`, custom array tags).

---

## Prerequisites

- Python **3.7+** (dict insertion order guaranteed) or Python **3.4+** with `pip install ordereddict`.
- No external dependencies beyond the standard library.

---

## Installation

1. Clone this repository or copy the script into your project directory:
   ```bash
   git clone https://github.com/yourusername/android-to-ios-plist.git
   cd android-to-ios-plist
   ```
2. (Optional) Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate     # Windows
   ```

---

## Usage

```bash
python android_to_ios_plist.py <input_android.xml> <output_ios.plist>
```

Example:

```bash
python android_to_ios_plist.py save_android.xml save_ios.plist
```

- `<input_android.xml>`: Path to your Android-style XML file with a top-level `<map>` element.
- `<output_ios.plist>`: Desired output path for the generated XML `.plist`.

After running, you can verify the plist structure with:

```bash
plutil -p save_ios.plist
```

Or open it in Xcode.

---

## Customisation

### Additional Tags

To support new tags like `<long>` or `<date>`, add cases in `convert_element`:

```python
if tag == "long":
    return int(elem.get("value", elem.text or 0))
if tag == "date":
    from datetime import datetime
    return datetime.fromisoformat(elem.text)
```

### Custom Array Tags

If your XML uses `<array>` instead of `<list>`, add:

```python
if tag == "array":
    return [convert_element(c) for c in elem]
```

### Nested Maps

The script already handles `<map>` inside `<map>` recursively, producing nested `<dict>` blocks in the output plist.

---

## How It Works

1. **Parse** the Android XML via `xml.etree.ElementTree`.
2. **Walk** the `<map>` elements to build an `OrderedDict` of key-value pairs:
   - Decode per cent escapes in attribute `name`.
   - Convert each element to its Python equivalent (`int`, `float`, `bool`, `str`, `list`, `dict`).
3. **Dump** to an XML plist using `plistlib.dump(..., fmt=plistlib.FMT_XML, sort_keys=False)`.

