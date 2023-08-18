"""Subclass of dialog_text_base, which is generated by wxFormBuilder."""
from logging import exception
import os
import wx
import json
import sys

from . import dialog_text_base

_APP_NAME = "SparkFun KiCad CAMmer"

# sub folder for our resource files
_RESOURCE_DIRECTORY = os.path.join("..", "resource")

#https://stackoverflow.com/a/50914550
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, _RESOURCE_DIRECTORY, relative_path)

def get_version(rel_path: str) -> str:
    try: 
        with open(resource_path(rel_path), encoding='utf-8') as fp:
            for line in fp.read().splitlines():
                if line.startswith("__version__"):
                    delim = '"' if '"' in line else "'"
                    return line.split(delim)[1]
            raise RuntimeError("Unable to find version string.")
    except:
        raise RuntimeError("Unable to find _version.py.")

_APP_VERSION = get_version("_version.py")

class Dialog(dialog_text_base.DIALOG_TEXT_BASE):

    config_defaults = {
        'Layers':
        {
            'F.Cu': 'true',
            'In1.Cu': 'true',
            'In2.Cu': 'true',
            'In3.Cu': 'true',
            'In4.Cu': 'true',
            'B.Cu': 'true',
            'F.Paste': 'true',
            'B.Paste': 'true',
            'F.Silkscreen': 'true',
            'B.Silkscreen': 'true',
            'F.Mask': 'true',
            'B.Mask': 'true'
        },
        'Edges':
        {
            'Edge.Cuts': 'true',
            'User.Comments': 'true'
        }
    }

    def __init__(self, parent, config, layertable, cammer, func):
        dialog_text_base.DIALOG_TEXT_BASE.__init__(self, parent)
        
        # hack for some gtk themes that incorrectly calculate best size
        #best_size = self.BestSize
        #best_size.IncBy(dx=0, dy=30)
        #self.SetClientSize(best_size)

        self.config_file = config

        self.layertable = layertable

        self.cammer = cammer

        self.func = func

        self.error = None

        self.SetTitle(_APP_NAME + " - " + _APP_VERSION)


        # Get config with defaults based on layertable
        self.config = self.config_defaults
        # Delete and defaults not present in layertable
        for key in self.config.keys():
            for layer in self.config[key].keys():
                if layer not in layertable.keys():
                    self.config[key].pop(layer, None)

        self.loadConfig()
        self.LoadSettings()

        # Autosize now grid is populated
        self.LayersGrid.AutoSizeColumns()
        self.EdgesGrid.AutoSizeColumns()

    def loadConfig(self):
        # Load up last sessions config
        try:
            with open(self.config_file, 'r') as cf:
                json_params = json.load(cf)
            self.config.update(json_params)
        except Exception as e:
            # Don't throw exception if we can't load previous config
            pass

    def saveConfig(self):
        try:
            with open(self.config_file, 'w') as cf:
                json.dump(self.CurrentSettings(), cf, indent=2)
        except Exception as e:
            # Don't throw exception if we can't save config
            pass
            
    def LoadSettings(self):
        # Delete any existing rows in LayersGrid
        if self.LayersGrid.NumberRows:
            self.LayersGrid.DeleteRows(0, self.LayersGrid.NumberRows)
        # Append empty rows based on layertable
        self.LayersGrid.AppendRows(len(self.layertable))
        # Initialize them
        row = 0
        for layer in self.layertable.keys():
            enabled = "1" if (layer in self.config['Layers'].keys()) else "0"
            self.LayersGrid.SetCellValue(row, 0, enabled)
            self.LayersGrid.SetCellRenderer(row, 0, wx.grid.GridCellBoolRenderer())
            self.LayersGrid.SetCellValue(row, 1, layer)
            self.LayersGrid.SetReadOnly(row, 1)
            row += 1
            
        # Delete any existing rows in EdgesGrid
        if self.EdgesGrid.NumberRows:
            self.EdgesGrid.DeleteRows(0, self.EdgesGrid.NumberRows)
        # Append empty rows based on layertable
        self.EdgesGrid.AppendRows(len(self.layertable))
        # Initialize them
        row = 0
        for layer in self.layertable.keys():
            enabled = "1" if (layer in self.config['Edges'].keys()) else "0"
            self.EdgesGrid.SetCellValue(row, 0, enabled)
            self.EdgesGrid.SetCellRenderer(row, 0, wx.grid.GridCellBoolRenderer())
            self.EdgesGrid.SetCellValue(row, 1, layer)
            self.EdgesGrid.SetReadOnly(row, 1)
            row += 1

    def CurrentSettings(self):
        params = {}

        for row in range(self.LayersGrid.GetNumberRows()):
            enabled = True if (self.LayersGrid.GetCellValue(row, 0) == "1") else False
            layer = self.LayersGrid.GetCellValue(row, 1)
            params['Layers'][layer] = enabled

        for row in range(self.EdgesGrid.GetNumberRows()):
            enabled = True if (self.EdgesGrid.GetCellValue(row, 0) == "1") else False
            layer = self.EdgesGrid.GetCellValue(row, 1)
            params['Edges'][layer] = enabled

        return params

    def OnRunCAMmerClick(self, e):
        self.saveConfig()
        self.func(self, self.cammer)

    def OnCancelClick(self, e):
        self.EndModal(wx.ID_CANCEL)     
