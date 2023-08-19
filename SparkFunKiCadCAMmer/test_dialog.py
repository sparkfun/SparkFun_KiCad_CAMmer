#!/usr/bin/env python
from dialog.dialog import *

import sys
import subprocess

from cammer.cammer import CAMmer

class MyApp(wx.App):
    def OnInit(self):

        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cammer_config.json')

        layertable = {
                'F.Cu': 0,
                'In1.Cu': 1,
                'In2.Cu': 2,
                'B.Cu': 5,
                'F.Paste': 6,
                'B.Paste': 7,
                'F.Silkscreen': 8,
                'B.Silkscreen': 9,
                'F.Mask': 10,
                'B.Mask': 11,
                'Edge.Cuts': 12,
                'User.Comments': 13,
                'Fake.Fake': 20
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