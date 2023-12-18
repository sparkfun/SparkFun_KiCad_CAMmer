#!/usr/bin/env python
from dialog.dialog import *

import sys
import subprocess

from cammer.cammer import CAMmer

class MyApp(wx.App):
    def OnInit(self):

        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cammer_config.json')

        layertable = {
                0: { 'standardName': 'F.Cu', 'actualName': 'F-Cu-Renamed' },
                1: { 'standardName': 'In1.Cu', 'actualName': 'In1-Cu-Renamed' },
                2: { 'standardName': 'In2.Cu', 'actualName': 'In2.Cu' },
                5: { 'standardName': 'B.Cu', 'actualName': 'B.Cu' },
                6: { 'standardName': 'F.Paste', 'actualName': 'F.Paste' },
                7: { 'standardName': 'B.Paste', 'actualName': 'B.Paste' },
                8: { 'standardName': 'F.Silkscreen', 'actualName': 'F.Silkscreen' },
                9: { 'standardName': 'B.Silkscreen', 'actualName': 'B.Silkscreen' },
                10: { 'standardName': 'F.Mask', 'actualName': 'F.Mask' },
                11: { 'standardName': 'B.Mask', 'actualName': 'B.Mask' },
                12: { 'standardName': 'Edge.Cuts', 'actualName': 'Edge.Cuts' },
                13: { 'standardName': 'User.Comments', 'actualName': 'User.Comments' },
                20: { 'standardName': 'Fake.Fake', 'actualName': 'Fake.Fake' }
        }

        self.frame = frame = Dialog(None, config_file, layertable, CAMmer(), self.run)
        if frame.ShowModal() == wx.ID_OK:
            print("Graceful Exit")
        frame.Destroy()
        return True

    def run(self, dlg, p_cammer):

        self.frame.EndModal(wx.ID_OK)


app = MyApp()
app.MainLoop()

print("Done")