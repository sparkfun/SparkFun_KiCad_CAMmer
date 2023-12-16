import os
import sys
from argparse import ArgumentParser
import logging
from datetime import datetime
import wx
import zipfile

from pcbnew import *

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
            logger.setLevel(logging.DEBUG)

        logger.info('CAMMER START: ' + datetime.now().isoformat())

        # Read the args
        sourceBoardFile = args.path
        layers = args.layers
        edges = args.edges

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
                board = LoadBoard(sourceBoardFile)
                outputPath = os.path.split(sourceBoardFile)[0] # Get the file path head
                zipFilename = os.path.split(sourceBoardFile)[1] # Get the file path tail
                zipFilename = os.path.join(outputPath, os.path.splitext(zipFilename)[0] + ".zip")
        else: # Running in a plugin
            sourceBoardFile = board.GetFileName()
            outputPath = os.path.split(sourceBoardFile)[0] # Get the file path head
            zipFilename = os.path.split(sourceBoardFile)[1] # Get the file path tail
            zipFilename = os.path.join(outputPath, os.path.splitext(zipFilename)[0] + ".zip")

        if board is None:
            report += "Could not load board. Quitting.\n"
            sysExit = 2
            return sysExit, report    

        if (not layers) and (not edges):
            report += "No layers and edges defined. Quitting.\n"
            sysExit = 2
            return sysExit, report

        # Check if about to overwrite a zip file
        if os.path.isfile(zipFilename):
            if wx.GetApp() is not None:
                resp = wx.MessageBox("You are about to overwrite existing files.\nAre you sure?",
                            'Warning', wx.OK | wx.CANCEL | wx.ICON_WARNING)
                if resp != wx.OK:
                    report += "User does not want to overwrite the files. Quitting.\n"
                    sysExit = 1
                    return sysExit, report

        # Build layer table
        layertable = {}
        numlayers = PCB_LAYER_ID_COUNT
        for i in range(numlayers):
            layertable[i] = {'standardName': board.GetStandardLayerName(i), 'actualName': board.GetLayerName(i)}

        # Protel file extensions
        file_ext = {
            "F.Cu": "GTL",
            "B.Cu": "GBL",
            "F.Mask": "GTS",
            "B.Mask": "GBS",
            "F.Paste": "GTP",
            "B.Paste": "GBP",
            "F.Silkscreen": "GTO",
            "B.Silkscreen": "GBO",
            "Edge.Cuts": "GKO"
        }
        for i in range(1,31): # Add 30 internal copper layers
            file_ext["In{}.Cu".format(i)] = "GL{}".format(i)

        # Start plotting: https://gitlab.com/kicad/code/kicad/-/blob/master/demos/python_scripts_examples/plot_board.py

        pctl = PLOT_CONTROLLER(board)

        popt = pctl.GetPlotOptions()

        # Set some important plot options:
        # One cannot plot the frame references, because the board does not know
        # the frame references.
        popt.SetPlotFrameRef(False)
        popt.SetSketchPadLineWidth(FromMM(0.1))

        popt.SetAutoScale(False)
        popt.SetScale(1)
        popt.SetMirror(False)
        popt.SetUseGerberAttributes(True)
        popt.SetUseAuxOrigin(True)

        # This by gerbers only (also the name is truly horrid!)
        popt.SetSubtractMaskFromSilk(False) #remove solder mask from silk to be sure there is no silk on pads
        popt.SetDrillMarksType(DRILL_MARKS_NO_DRILL_SHAPE)
        popt.SetSkipPlotNPTH_Pads(False)

        filesToZip = []


        # Copper, Silk, Mask

        for layer in layers.split(","):
            if layer not in file_ext.keys():
                report += "Unknown layer " + layer + "!\n"
                sysExit= 2
            else:
                layername = layer.replace(".", "_")
                layerNumber = None
                for id, names in layertable.items():
                    if layer in names['standardName']:
                        layerNumber = id
                        break
                pctl.SetLayer(layerNumber)
                pctl.OpenPlotfile(layername, PLOT_FORMAT_GERBER)
                pctl.PlotLayer()
                pctl.ClosePlot() # Release the file - or we can't rename it

                plotfile = os.path.splitext(sourceBoardFile)[0] + "-" + layername + ".gbr"
                newname = os.path.splitext(sourceBoardFile)[0] + "." + file_ext[layer]

                if not os.path.isfile(plotfile):
                    report += "Could not plot " + plotfile + "\n"
                    sysExit = 2
                else:
                    if os.path.isfile(newname):
                        report += "Deleting existing " + newname + "\n"
                        os.remove(newname)
                    report += "Renaming " + plotfile + " to " + newname + "\n"
                    os.rename(plotfile, newname)
                    if not os.path.isfile(newname):
                        report += "Could not rename " + newname + "\n"
                        sysExit = 2
                    else:
                        filesToZip.append(newname)


        # Edge cuts (dimensions) and V_SCORE (from User.Comments)
        # See: https://gitlab.com/kicad/code/kicad/-/issues/13841

        allEdges = LSEQ()
        edge_ext = ""
        for e in edges.split(","):
            if e in file_ext.keys():
                edge_ext = file_ext[e]
                layername = e.replace(".", "_")
            for id, names in layertable.items():
                if e in names['standardName']:
                    allEdges.push_back(id)
                    break

        if edge_ext == "":
            report += "Unknown edge(s): " + str(edges) + "\n"
            sysExit= 2
        else:
            pctl.OpenPlotfile(layername, PLOT_FORMAT_GERBER)
            pctl.PlotLayers(allEdges)
            pctl.ClosePlot() # Release the file - or we can't rename it

            plotfile = os.path.splitext(sourceBoardFile)[0] + "-" + layername + ".gbr"
            newname = os.path.splitext(sourceBoardFile)[0] + "." + edge_ext

            if not os.path.isfile(plotfile):
                report += "Could not plot " + plotfile + "\n"
                sysExit = 2
            else:
                if os.path.isfile(newname):
                    report += "Deleting existing " + newname + "\n"
                    os.remove(newname)
                report += "Renaming " + plotfile + " to " + newname + "\n"
                os.rename(plotfile, newname)
                if not os.path.isfile(newname):
                    report += "Could not rename " + newname + "\n"
                    sysExit = 2
                else:
                    filesToZip.append(newname)


        # Excellon drill file
        # https://gitlab.com/kicad/code/kicad/-/blob/master/demos/python_scripts_examples/gen_gerber_and_drill_files_board.py

        # Fabricators need drill files.
        # sometimes a drill map file is asked (for verification purpose)
        drlwriter = EXCELLON_WRITER( board )
        #drlwriter.SetMapFileFormat( PLOT_FORMAT_PDF )

        mirror = False
        minimalHeader = False
        offset = board.GetDesignSettings().GetAuxOrigin() # Was: offset = VECTOR2I(0,0)
        # False to generate 2 separate drill files (one for plated holes, one for non plated holes)
        # True to generate only one drill file
        mergeNPTH = True
        drlwriter.SetOptions( mirror, minimalHeader, offset, mergeNPTH )

        metricFmt = True
        drlwriter.SetFormat( metricFmt )

        genDrl = True
        genMap = False
        drlwriter.CreateDrillandMapFilesSet( pctl.GetPlotDirName(), genDrl, genMap )
        
        if mergeNPTH:
            holes = os.path.splitext(sourceBoardFile)[0] + ".drl"
            if os.path.isfile(holes):
                filesToZip.append(holes)
            else:
                report += "No drill file created\n"
        else:
            npth = os.path.splitext(sourceBoardFile)[0] + "-NPTH.drl"
            if os.path.isfile(npth):
                filesToZip.append(npth)
            else:
                report += "No NPTH drill file created\n"

            pth = os.path.splitext(sourceBoardFile)[0] + "-PTH.drl"
            if os.path.isfile(pth):
                filesToZip.append(pth)
            else:
                report += "No PTH drill file created\n"

        # One can create a text file to report drill statistics
        rptfn = pctl.GetPlotDirName() + 'drill_report.rpt'
        report += "Drill report: {}\n".format( rptfn )
        drlwriter.GenDrillReportFile( rptfn )


        # Zip the files

        zf = zipfile.ZipFile(zipFilename, "w")
        for filename in filesToZip:
            zf.write(filename, os.path.basename(filename), compress_type=zipfile.ZIP_DEFLATED)
        # Include the ordering_instructions - if present
        oi = os.path.join(outputPath, "ordering_instructions.txt")
        if os.path.isfile(oi):
            zf.write(oi, os.path.basename(oi), compress_type=zipfile.ZIP_DEFLATED)
        zf.close()


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
