import os
import logging
import wx
import wx.aui

import pcbnew

from .dialog import Dialog

from .cammer.cammer import CAMmer

class CAMmerPlugin(pcbnew.ActionPlugin, object):

    def __init__(self):
        super(CAMmerPlugin, self).__init__()

        self.logger = None
        self.config_file = None

        self.name = "CAMmer"
        self.category = "Read PCB"
        self.pcbnew_icon_support = hasattr(self, "show_toolbar_button")
        self.show_toolbar_button = True
        icon_dir = os.path.dirname(__file__)
        self.icon_file_name = os.path.join(icon_dir, 'icon.png')
        self.description = "Generate PCB Gerber and drill files"
        
        self._pcbnew_frame = None

        self.supportedVersions = ['7.','8.','9.']

        self.kicad_build_version = pcbnew.GetBuildVersion()

    def IsSupported(self):
        for v in self.supportedVersions:
            if self.kicad_build_version.startswith(v):
                return True
        return False
    
    def Run(self):
        if self._pcbnew_frame is None:
            try:
                self._pcbnew_frame = [x for x in wx.GetTopLevelWindows() if ('pcbnew' in x.GetTitle().lower() and not 'python' in x.GetTitle().lower()) or ('pcb editor' in x.GetTitle().lower())]
                if len(self._pcbnew_frame) == 1:
                    self._pcbnew_frame = self._pcbnew_frame[0]
                else:
                    self._pcbnew_frame = None
            except:
                pass

        # Construct the config_file path from the board name
        board = pcbnew.GetBoard()
        outputPath = os.path.split(board.GetFileName())[0] # Get the file path head
        self.config_file = os.path.join(outputPath, 'cammer_config.json')
        self.ordering_instructions = os.path.join(outputPath, 'ordering_instructions.txt')

        logFile = os.path.join(outputPath, 'cammer.log')
        try:
            os.remove(logFile)
        except FileNotFoundError:
            pass

        self.logger = logging.getLogger('cammer_logger')
        f_handler = logging.FileHandler(logFile)
        f_handler.setLevel(logging.DEBUG) # Log everything
        f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        f_handler.setFormatter(f_format)
        self.logger.addHandler(f_handler)

        # Build layer table
        layertable = {}
        numlayers = pcbnew.PCB_LAYER_ID_COUNT
        for i in range(numlayers):
            layertable[i] = {'standardName': board.GetStandardLayerName(i), 'actualName': board.GetLayerName(i)}

        # Check the number of copper layers. Delete unwanted layers from the table.
        wantedCopper = []
        wantedCopper.append("F.Cu")
        wantedCopper.append("B.Cu")
        if (board.GetCopperLayerCount() > 2):
            for i in range(1, board.GetCopperLayerCount() - 1):
                wantedCopper.append("In{}.Cu".format(i))
        deleteLayers = []
        for layer, names in layertable.items():
            if names['standardName'][-3:] == ".Cu":
                if names['standardName'] not in wantedCopper:
                    deleteLayers.append(layer)
        for layer in deleteLayers:
            layertable.pop(layer, None)

        def run_cammer(dlg, p_cammer):
            self.logger.log(logging.INFO, "Running CAMmer")

            if not self.IsSupported():
                # Log a warning if this version of KiCad has not been tested
                self.logger.log(logging.WARNING, "Version check failed. \"{}\" may not be supported. CAMming may fail".format(self.kicad_build_version))

            command = []

            layers = dlg.CurrentSettings()["Layers"]
            layersCommand = ""
            for layer,include in layers.items():
                if include == 'true': # JSON format
                    if layersCommand == "":
                        layersCommand = layer
                    else:
                        layersCommand = layersCommand + "," + layer

            if layersCommand != "":
                command.extend(['-l', layersCommand])

            edges = dlg.CurrentSettings()["Edges"]
            edgesCommand = ""
            for edge,include in edges.items():
                if include == 'true': # JSON format
                    if edgesCommand == "":
                        edgesCommand = edge
                    else:
                        edgesCommand = edgesCommand + "," + edge

            if edgesCommand != "":
                command.extend(['-e', edgesCommand])

            self.logger.log(logging.INFO, command)

            board = pcbnew.GetBoard()

            if board is not None:
                sysExit, report = p_cammer.startCAMmerCommand(command, board, self.logger)
                logWarn = logging.INFO
                if sysExit >= 1:
                    logWarn = logging.WARNING
                if sysExit >= 2:
                    logWarn = logging.ERROR
                self.logger.log(logWarn, report)
                if sysExit > 0:
                    wx.MessageBox("CAMmer " + ("warning" if (sysExit == 1) else "error") + ".\nPlease check cammer.log for details.",
                        ("Warning" if (sysExit == 1) else "Error"), wx.OK | (wx.ICON_WARNING if (sysExit == 1) else wx.ICON_ERROR))
                else:
                    wx.MessageBox("CAMmer complete.\nPlease check cammer.log for details.",
                        "Info", wx.OK | wx.ICON_INFORMATION)
            else:
                self.logger.log(logging.ERROR, "Could not get the board")

            dlg.EndModal(wx.ID_OK)

        dlg = Dialog(self._pcbnew_frame, self.config_file, layertable, CAMmer(), run_cammer)
    
        try:
            result = dlg.ShowModal()
            if result == wx.ID_OK:
                self.logger.log(logging.INFO, "CAMmer complete")
            elif result == wx.ID_CANCEL:
                self.logger.log(logging.INFO, "CAMmer cancelled")
            else:
                self.logger.log(logging.INFO, "CAMmer finished - " + str(result))

        finally:
            self.logger.removeHandler(f_handler)
            dlg.Destroy()
                        

    