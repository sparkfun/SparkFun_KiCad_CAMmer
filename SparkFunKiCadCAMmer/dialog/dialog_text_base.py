# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.10.1-0-g8feb16b3)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

from .compat import DialogShim
import wx
import wx.xrc
import wx.grid

import gettext
_ = gettext.gettext

###########################################################################
## Class DIALOG_TEXT_BASE
###########################################################################

class DIALOG_TEXT_BASE ( DialogShim ):

    def __init__( self, parent ):
        DialogShim.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"SparkFun KiCad CAMmer"), pos = wx.DefaultPosition, size = wx.Size( 400,500 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER|wx.SYSTEM_MENU )

        self.SetSizeHints( wx.Size( -1,-1 ), wx.DefaultSize )

        MainSizer = wx.BoxSizer( wx.VERTICAL )

        LayerEdgeSizer = wx.FlexGridSizer( 1, 2, 0, 0 )
        LayerEdgeSizer.AddGrowableCol( 0 )
        LayerEdgeSizer.AddGrowableCol( 1 )
        LayerEdgeSizer.AddGrowableRow( 0 )
        LayerEdgeSizer.SetFlexibleDirection( wx.BOTH )
        LayerEdgeSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        LayerSizer = wx.FlexGridSizer( 2, 1, 0, 0 )
        LayerSizer.AddGrowableCol( 0 )
        LayerSizer.AddGrowableRow( 1 )
        LayerSizer.SetFlexibleDirection( wx.BOTH )
        LayerSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.LayersTitle = wx.StaticText( self, wx.ID_ANY, _(u"Layers:"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.LayersTitle.Wrap( -1 )

        self.LayersTitle.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

        LayerSizer.Add( self.LayersTitle, 0, wx.ALL|wx.EXPAND, 5 )

        self.LayersGrid = wx.grid.Grid( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )

        # Grid
        self.LayersGrid.CreateGrid( 1, 2 )
        self.LayersGrid.EnableEditing( True )
        self.LayersGrid.EnableGridLines( True )
        self.LayersGrid.EnableDragGridSize( False )
        self.LayersGrid.SetMargins( 0, 0 )

        # Columns
        self.LayersGrid.AutoSizeColumns()
        self.LayersGrid.EnableDragColMove( False )
        self.LayersGrid.EnableDragColSize( True )
        self.LayersGrid.SetColLabelValue( 0, _(u"Include") )
        self.LayersGrid.SetColLabelValue( 1, _(u"Name") )
        self.LayersGrid.SetColLabelSize( 30 )
        self.LayersGrid.SetColLabelAlignment( wx.ALIGN_LEFT, wx.ALIGN_CENTER )

        # Rows
        self.LayersGrid.AutoSizeRows()
        self.LayersGrid.EnableDragRowSize( False )
        self.LayersGrid.SetRowLabelSize( 1 )
        self.LayersGrid.SetRowLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

        # Label Appearance

        # Cell Defaults
        self.LayersGrid.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
        LayerSizer.Add( self.LayersGrid, 0, wx.ALL|wx.EXPAND, 5 )


        LayerEdgeSizer.Add( LayerSizer, 1, wx.EXPAND, 5 )

        EdgeSizer = wx.FlexGridSizer( 2, 1, 0, 0 )
        EdgeSizer.AddGrowableCol( 0 )
        EdgeSizer.AddGrowableRow( 1 )
        EdgeSizer.SetFlexibleDirection( wx.BOTH )
        EdgeSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.EdgeTitle = wx.StaticText( self, wx.ID_ANY, _(u"Edges:"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.EdgeTitle.Wrap( -1 )

        self.EdgeTitle.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

        EdgeSizer.Add( self.EdgeTitle, 0, wx.ALL|wx.EXPAND, 5 )

        self.EdgesGrid = wx.grid.Grid( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )

        # Grid
        self.EdgesGrid.CreateGrid( 1, 2 )
        self.EdgesGrid.EnableEditing( True )
        self.EdgesGrid.EnableGridLines( True )
        self.EdgesGrid.EnableDragGridSize( False )
        self.EdgesGrid.SetMargins( 0, 0 )

        # Columns
        self.EdgesGrid.AutoSizeColumns()
        self.EdgesGrid.EnableDragColMove( False )
        self.EdgesGrid.EnableDragColSize( True )
        self.EdgesGrid.SetColLabelValue( 0, _(u"Include") )
        self.EdgesGrid.SetColLabelValue( 1, _(u"Name") )
        self.EdgesGrid.SetColLabelSize( 30 )
        self.EdgesGrid.SetColLabelAlignment( wx.ALIGN_LEFT, wx.ALIGN_CENTER )

        # Rows
        self.EdgesGrid.AutoSizeRows()
        self.EdgesGrid.EnableDragRowSize( False )
        self.EdgesGrid.SetRowLabelSize( 1 )
        self.EdgesGrid.SetRowLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

        # Label Appearance

        # Cell Defaults
        self.EdgesGrid.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
        EdgeSizer.Add( self.EdgesGrid, 0, wx.ALL|wx.EXPAND, 5 )


        LayerEdgeSizer.Add( EdgeSizer, 1, wx.EXPAND, 5 )


        MainSizer.Add( LayerEdgeSizer, 1, wx.EXPAND, 5 )

        self.m_staticline2 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        MainSizer.Add( self.m_staticline2, 0, wx.EXPAND |wx.ALL, 5 )

        lowerSizer = wx.BoxSizer( wx.HORIZONTAL )


        lowerSizer.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        self.m_buttonRunCAMmer = wx.Button( self, wx.ID_ANY, _(u"Run CAMmer"), wx.DefaultPosition, wx.DefaultSize, 0 )

        self.m_buttonRunCAMmer.SetDefault()
        lowerSizer.Add( self.m_buttonRunCAMmer, 0, wx.ALL, 5 )

        self.m_buttonCancel = wx.Button( self, wx.ID_ANY, _(u"Cancel"), wx.DefaultPosition, wx.DefaultSize, 0 )
        lowerSizer.Add( self.m_buttonCancel, 0, wx.ALL, 5 )


        MainSizer.Add( lowerSizer, 0, wx.ALL|wx.EXPAND|wx.FIXED_MINSIZE, 5 )


        self.SetSizer( MainSizer )
        self.Layout()

        self.Centre( wx.BOTH )

        # Connect Events
        self.Bind( wx.EVT_INIT_DIALOG, self.OnInitDlg )
        self.m_buttonRunCAMmer.Bind( wx.EVT_BUTTON, self.OnRunCAMmerClick )
        self.m_buttonCancel.Bind( wx.EVT_BUTTON, self.OnCancelClick )

    def __del__( self ):
        pass


    # Virtual event handlers, override them in your derived class
    def OnInitDlg( self, event ):
        pass

    def OnRunCAMmerClick( self, event ):
        pass

    def OnCancelClick( self, event ):
        pass


