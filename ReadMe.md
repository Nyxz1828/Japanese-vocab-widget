# JP Vocab Widget

## Quick Start

Download the project and press the `.exe` file to start the widget.

You can also download it from Google Drive:

https://drive.google.com/drive/folders/1g9RX1_DDhRdSSDXLTqaIw8R1R-2Ve9E1

This widget is designed to run while you are working, so you can keep seeing Japanese vocabulary and slowly remember new words during daily use.

---

## Description

JP Vocab Widget is a small desktop vocabulary widget for learning Japanese while working. The widget stays always on top of all windows and pages, so the vocabulary remains visible while using other apps, browsers, or documents.

The window is half-transparent, making it less distracting while still allowing users to review Japanese words, furigana, and meanings during daily work or study.



---


## How to Change Code

The main program is inside:

```text
app/main.py
```

To edit the widget:

1. Open the project folder.
2. Go to the `app` folder.
3. Edit `main.py`.
4. Run the program again.

If you are using the launcher:

```text
JPWidgetLauncher.exe
```

The launcher will open:

```text
app/main.py
```

If you change `main.py`, you usually do not need to rebuild the `.exe` unless you changed the launcher script.

---

## Future Changes

Possible future improvements:

- Add auto-change vocabulary every few seconds or minutes.
- Add setting for font size.
- Add setting for window transparency.
- Add option to choose JLPT level: N5, N4, N3, N2, N1, or ALL.
- Add favorite/saved words.
- Add word history.
- Add dark/light theme.
- Add local JSON cache so the app can run without internet.
- Add keyboard shortcuts for next and previous vocabulary.
- Add pronunciation/audio support.

---

## JSON Source and Credits To

Vocabulary data is loaded from:

```text
https://github.com/wkei/jlpt-vocab-api
```

Raw JSON source:

```text
https://raw.githubusercontent.com/wkei/jlpt-vocab-api/main/data-source/db/
```

Credits to the original JLPT vocabulary API/data source creator:

```text
wkei/jlpt-vocab-api
```

This project uses the JSON data only for vocabulary learning and display purposes.
