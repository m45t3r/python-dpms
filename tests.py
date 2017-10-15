import dpms
import os
import unittest


class TestDpms(unittest.TestCase):
    def setUp(self):
        self.d = dpms.DPMS()

    def test_init(self):
        with self.assertRaisesRegexp(
            Exception,
            "Optional display keyword must be a string. e.g. ':0'"
        ):
            dpms.DPMS(display=1)

        with self.assertRaisesRegexp(
            Exception,
            "Cannot open display"
        ):
            dpms.DPMS(display="invalid")

    def test_Display(self):
        self.assertEqual(
            self.d.Display(),
            os.environ["DISPLAY"]
        )

    def test_QueryExtension(self):
        extension = self.d.QueryExtension()
        self.assertTrue(type(extension) is tuple)

        self.assertTrue(type(extension[0]) is bool)
        self.assertTrue(type(extension[1]) is int)
        self.assertTrue(type(extension[2]) is int)

    def test_Capable(self):
        self.assertTrue(type(self.d.Capable()) is bool)

    def test_GetTimeouts(self):
        timeouts = self.d.GetTimeouts()
        self.assertTrue(type(timeouts) is tuple)

        for timeout in timeouts:
            self.assertTrue(type(timeout) is int)

    def test_SetTimeouts(self):
        current_timeouts = self.d.GetTimeouts()

        with self.assertRaisesRegexp(
            Exception,
            "Bad arguments. Should be \(int standby, int suspend, int off\)."
        ):
            self.d.SetTimeouts(standby="600", suspend="600", off="600")

        self.d.SetTimeouts(standby=100, suspend=100, off=100)
        self.assertEqual(
            self.d.GetTimeouts(),
            (100, 100, 100)
        )

        # Restore original timeouts
        self.d.SetTimeouts(*current_timeouts),

    def test_EnableDisable(self):
        _, current_state = self.d.Info()

        self.d.Disable()
        self.assertFalse(self.d.Info()[1])

        self.d.Enable()
        self.assertTrue(self.d.Info()[1])

        # Restore original state
        if current_state:
            self.d.Enable()
        else:
            self.d.Disable()

    def test_ForceLevel(self):
        current_level, _ = self.d.Info()

        with self.assertRaisesRegexp(
            Exception,
            "Bad arguments. Should be \(int level\)."
        ):
            self.d.ForceLevel(level="0")

        with self.assertRaisesRegexp(
            Exception,
            "Bad level."
        ):
            self.d.ForceLevel(level=1000)

        # Your screen may flicker during this test
        self.d.ForceLevel(level=dpms.DPMSModeOn)
        self.d.ForceLevel(level=dpms.DPMSModeStandby)
        self.d.ForceLevel(level=dpms.DPMSModeSuspend)
        self.d.ForceLevel(level=dpms.DPMSModeOff)
        # Restore original level
        self.d.ForceLevel(level=current_level)

    def test_Info(self):
        info = self.d.Info()
        self.assertTrue(type(info) is tuple)

        level, state = info
        self.assertTrue(type(level) is int)
        self.assertTrue(type(state) is bool)


if __name__ == "__main__":
    unittest.main()