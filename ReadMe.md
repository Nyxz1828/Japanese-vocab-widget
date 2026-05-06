# JP Vocab Widget for Mobile

## Quick Start

This widget is designed to run while you are working, so you can keep seeing Japanese vocabulary and slowly remember new words during daily use.

---

## Description

JP Vocab Widget is a small mobile-friendly vocabulary widget for learning Japanese on the go. It keeps Japanese words, furigana, and meanings easy to check while you use other apps on your phone or tablet.

The interface is designed to stay unobtrusive, making it easy to review vocabulary during commuting, breaks, or daily study sessions.

---
## To Do
- Available on both Android and iOS.
- Create a simple widget that displays one Japanese word with furigana and meaning.
- Use the JLPT vocabulary data from the provided JSON source.
- PiP support
- Widget support
- Favorite words
- Auto-change vocabulary every few seconds or minutes
- Notification to show new vocabulary



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
