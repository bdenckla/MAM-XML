# MAM-XML
This repo has MAM in an XML format that is simple but not complete. See out/xml.

This format was originally intended for use by STEPBible. But now, for STEPBible, I will try to directly generate OSIS-compliant XML. (This repository used to be called MAM-for-STEPBible.)

In addition to the XML in out/xml, this repo has a program, main_mam_xml_test.py, that is an example of how the XML can be used. In this example program, the XML is used to create a Sefaria-style CSV/HTML version of MAM. The example program's output differs only from the real "MAM for Sefaria" with respect to its versification (verse numbering). The example program's output, like its XML input, has BHS versification, whereas "MAM for Sefaria" has Sefaria versification.
