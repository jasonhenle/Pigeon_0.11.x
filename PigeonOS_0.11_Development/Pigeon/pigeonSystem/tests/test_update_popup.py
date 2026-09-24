"""Update popup: no OK button while a GitHub check is in flight."""

from __future__ import annotations

import os
import sys
import unittest
import xml.etree.ElementTree as ET

_SYS_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _SYS_ROOT not in sys.path:
    sys.path.insert(0, _SYS_ROOT)

from pigeon.widgets.main_settings import (  # noqa: E402
    MainSettingsState,
    _find_by_logical_id,
)
from pigeon.widgets.update_popup import (  # noqa: E402
    ID_NOW_GROUP,
    ID_NOW_TEXT,
    apply_update_popup_svg_state,
    default_update_popup_svg_path,
    update_popup_focus_ring,
)


def _hidden(el: ET.Element | None) -> bool:
    return el is not None and el.get("display") == "none"


class UpdatePopupCheckingTests(unittest.TestCase):
    def test_focus_ring_empty_while_checking(self) -> None:
        self.assertEqual(
            update_popup_focus_ring(update_available=False, checking=True),
            (),
        )
        self.assertEqual(
            update_popup_focus_ring(update_available=True, checking=True),
            (),
        )
        self.assertEqual(
            update_popup_focus_ring(update_available=False),
            ("now",),
        )

    def test_checking_hides_ok_button(self) -> None:
        path = default_update_popup_svg_path()
        self.assertTrue(path.is_file(), msg=str(path))
        root = ET.parse(path).getroot()
        st = MainSettingsState()
        st.update_checking = True
        st.update_local_version = "0.11.17"
        st.update_changelog = "Checking GitHub for updates…"
        apply_update_popup_svg_state(root, st)
        self.assertTrue(_hidden(_find_by_logical_id(root, ID_NOW_GROUP)))

    def test_up_to_date_keeps_ok(self) -> None:
        path = default_update_popup_svg_path()
        root = ET.parse(path).getroot()
        st = MainSettingsState()
        st.update_checking = False
        st.update_available = False
        st.update_local_version = "0.11.17"
        apply_update_popup_svg_state(root, st)
        now = _find_by_logical_id(root, ID_NOW_GROUP)
        self.assertFalse(_hidden(now))
        text = _find_by_logical_id(root, ID_NOW_TEXT)
        self.assertIsNotNone(text)
        body = "".join(text.itertext()) if text is not None else ""
        self.assertIn("OK", body)


if __name__ == "__main__":
    unittest.main()
