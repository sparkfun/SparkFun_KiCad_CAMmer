import os
import sys
from argparse import ArgumentParser
import pcbnew
import logging
from datetime import datetime
import wx

class CAMmer():
    def __init__(self):
        pass

    def args_parse(self, args):
        # set up command-line arguments parser
        parser = ArgumentParser(description="A script to generate and zip PCB Gerber and drill files.")
        parser.add_argument(
            "-p", "--path", help="Path to the *.kicad_pcb file"
        )
        parser.add_argument(
            "-l", "--layers", help="CSV list of copper, silk and resist layers"
        )
        parser.add_argument(
            "-e", "--edges", help="CSV list of edge (outline / keep out) layers"
        )
        return parser.parse_args(args)

    def startCAMmer(self, args, board=None, logger=None):
        """The main method

        Args:
            args - the command line args [1:] - parsed with args_parse
            board - the KiCad BOARD when running in a plugin
            logger - logging logger from parent

        Returns:
            sysExit - the value for sys.exit (if called from __main__)
            report - a helpful text report
        """

        sysExit = -1 # -1 indicates sysExit has not (yet) been set. The code below will set this to 0, 1, 2.
        report = "\nSTART: " + datetime.now().isoformat() + "\n"

        if logger is None:
            logger = logging.getLogger()
            logger.setLevel([ logging.WARNING, logging.DEBUG ][args.verbose])

        logger.info('CAMMER START: ' + datetime.now().isoformat())

        # Read the args
        sourceBoardFile = args.path
        layers = args.layers
        edges = args.edge

        # Check if this is running in a plugin
        if board is None:
            if sourceBoardFile is None:
                report += "No path to kicad_pcb file. Quitting.\n"
                sysExit = 2
                return sysExit, report
            else:
                # Check that input board is a *.kicad_pcb file
                sourceFileExtension = os.path.splitext(sourceBoardFile)[1]
                if not sourceFileExtension == ".kicad_pcb":
                    report += sourceBoardFile + " is not a *.kicad_pcb file. Quitting.\n"
                    sysExit = 2
                    return sysExit, report

                # Load source board from file
                board = pcbnew.LoadBoard(sourceBoardFile)
                outputPath = os.path.split(sourceBoardFile)[0] # Get the file path head
                zipFile = os.path.split(sourceBoardFile)[1] # Get the file path tail
                zipFile = os.path.join(outputPath, os.path.splitext(zipFile)[0] + ".zip")
        else: # Running in a plugin
            outputPath = os.path.split(board.GetFileName())[0] # Get the file path head
            zipFile = os.path.split(board.GetFileName())[1] # Get the file path tail
            zipFile = os.path.join(outputPath, os.path.splitext(zipFile)[0] + ".zip")

        if board is None:
            report += "Could not load board. Quitting.\n"
            sysExit = 2
            return sysExit, report    

        if (not layers) and (not edges):
            report += "No layers and edges defined. Quitting.\n"
            sysExit = 2
            return sysExit, report

        # Check if about to overwrite a zip file
        if os.path.isfile(zipFile):
            if wx.GetApp() is not None:
                resp = wx.MessageBox("You are about to overwrite existing files.\nAre you sure?",
                            'Warning', wx.OK | wx.CANCEL | wx.ICON_WARNING)
                if resp != wx.OK:
                    report += "User does not want to overwrite the files. Quitting.\n"
                    sysExit = 1
                    return sysExit, report


        # ADD MUCH STUFF HERE


        if sysExit < 0:
            sysExit = 0

        return sysExit, report

    def startCAMmerCommand(self, command, board=None, logger=None):

        parser = self.args_parse(command)

        sysExit, report = self.startCAMmer(parser, board, logger)

        return sysExit, report

if __name__ == '__main__':

    cammer = CAMmer()

    if len(sys.argv) < 2:
        parser = cammer.args_parse(['-h']) # Test args: e.g. ['-p','<path to board>']
    else:
        parser = cammer.args_parse(sys.argv[1:]) #Parse the args

    sysExit, report = cammer.startCAMmer(parser)

    print(report)

    sys.exit(sysExit)
