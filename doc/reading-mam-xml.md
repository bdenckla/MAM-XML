# Reading MAM-XML

This document describes the XML format used in MAM-XML and how to extract text from it.

## File Layout

```
out/
  xml-vtrad-bhs/    # BHS versification
  xml-vtrad-sef/    # Sefaria versification
  xml-vtrad-mam/    # MAM native versification
```

Each folder contains one XML file per book group (e.g., `Job.xml`, `Gen.xml`, `1Sam2Sam.xml`).
The three folders differ only in versification — the text content is the same.

## XML Element Hierarchy

```
<book24 versification-tradition="...">       ← root element
  <book39 osisID="Job">                      ← one per biblical book in the group
    <chapter osisID="Job.1">                 ← one per chapter
      <verse osisID="Job.1.1" .../>          ← one per verse
      <verse osisID="Job.1.2" .../>
      ...
    </chapter>
    <spi-pe2/>                               ← parashah marker between chapters
    <chapter osisID="Job.2">
      ...
    </chapter>
  </book39>
</book24>
```

Parashah elements (`spi-pe2`, `spi-pe3`, `spi-samekh2`, `spi-samekh3`)
can appear both between chapters (as children of `book39`)
and within verses (as children of `verse`).

## How Verse Text Is Stored

### Simple verses: `text` attribute

Most verses store their full text in a `text` attribute on the `<verse>` element:

```xml
<verse osisID="Job.34.2" yeivinID="Job 34:2"
       text="שִׁמְע֣וּ חֲכָמִ֣ים מִלָּ֑י וְ֝יֹדְעִ֗ים הַאֲזִ֥ינוּ לִֽי׃"/>
```

### Complex verses: child elements

Verses with special features (legarmeih, paseq, ketiv/qere, etc.)
have **no** `text` attribute.
Instead, the text is distributed across `<text>` child elements,
interspersed with markup elements:

```xml
<verse osisID="Job.1.1" yeivinID="Job 1:1">
  <text text="אִ֛ישׁ הָיָ֥ה בְאֶֽרֶץ־ע֖וּץ אִיּ֣וֹב שְׁמ֑וֹ וְהָיָ֣ה"/>
  <lp-legarmeih/>
  <text text=" הָאִ֣ישׁ הַה֗וּא תָּ֧ם וְיָשָׁ֛ר וִירֵ֥א אֱלֹהִ֖ים וְסָ֥ר מֵרָֽע׃"/>
</verse>
```

### Rule for extracting plain text

1. If the verse has a `text` attribute → use it directly.
2. Otherwise → concatenate the `text` attributes of all `<text>` child elements, in order.

## Child Element Types

| Element | Meaning |
|---------|---------|
| `<text text="..."/>` | A run of Hebrew text |
| `<lp-legarmeih/>` | Legarmeih punctuation (legacy paseq) |
| `<lp-paseq/>` | Paseq punctuation |
| `<implicit-maqaf/>` | Maqaf that is implicit in the manuscript |
| `<letter-small>` | Small letter (contains `<text>` children) |
| `<letter-large>` | Large letter (contains `<text>` children) |
| `<letter-hung>` | Hung/suspended letter (contains `<text>` children) |
| `<kq>` | Ketiv/Qere pair |
| `<kq-k>` | Ketiv portion |
| `<kq-q>` | Qere portion |
| `<kq-trivial>` | Trivial Ketiv/Qere |
| `<kq-k-velo-q>` | Ketiv with no Qere |
| `<kq-q-velo-k>` | Qere with no Ketiv |
| `<cant-combined>` | Combined cantillation |
| `<cant-all-three>` | All three cantillation systems |
| `<cant-alef>`, `<cant-bet>` | Individual cantillation systems |
| `<shirah-space/>` | Shirah (song) spacing |
| `<good-ending>` | Alternative ending |
| `<scrdfftar>` | Scroll-difference-from-target (contains `<sdt-target>` and `<sdt-note>`) |
| `<spi-samekh2>`, `<spi-samekh3>` | Samekh parashah markers |
| `<spi-pe2>`, `<spi-pe3>` | Pe parashah markers |
| `<spi-invnun>` | Inverted nun |

## Verse Attributes

| Attribute | Meaning |
|-----------|---------|
| `osisID` | OSIS-format reference (e.g., `Job.34.24`) |
| `yeivinID` | Yeivin-format reference (e.g., `Job 34:24`) |
| `text` | Full verse text (only present for simple verses) |
| `starts-with-sampe` | Verse starts after a parashah marker (`pe2`, `samekh2`, etc.) |
| `ends-with-sampe` | Verse ends with a parashah marker |
| `contents-corresponds-to` | Versification note (see README) |
| `osisID-of-MAM-src` | Source verse in MAM versification (see README) |

## Example: Extracting Plain Text in Python

```python
import xml.etree.ElementTree as ET

def get_verse_text(verse_el):
    """Extract plain text from a <verse> element."""
    if 'text' in verse_el.attrib:
        return verse_el.attrib['text']
    return ''.join(
        c.attrib['text'] for c in verse_el if c.tag == 'text'
    )

tree = ET.parse('out/xml-vtrad-mam/Job.xml')
book39 = tree.getroot()[0]  # <book39 osisID="Job">

for child in book39:
    if child.tag != 'chapter':
        continue
    for verse in child:
        if verse.tag != 'verse':
            continue
        text = get_verse_text(verse)
        print(f"{verse.attrib['osisID']}: {text}")
```

**Note:** The above `get_verse_text` is a simplification suitable for
extracting the basic consonantal text with vowels and accents.
For handling ketiv/qere, special letters, legarmeih rendering, etc.,
see the handler-based approach in `py-example/pysefaria/mam4sef_handlers.py`.

## The `py-example/` Program

The `py-example/` directory contains a complete working example
of reading MAM-XML and producing the MAM-for-Sefaria CSV/HTML output.
It uses a recursive handler pattern where each element type
has a registered handler function:

- **`mam4sef_or_ajf.py`** — reads XML, walks the tree with `_handle()`
- **`mam4sef_handlers.py`** — handler functions for every element type, keyed by `(tag, class)` tuple

This is the canonical reference for how to process the full range of MAM-XML element types.
