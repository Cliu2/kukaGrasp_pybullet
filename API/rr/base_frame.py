# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Apr 24 2017)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

from wx.lib.masked.ipaddrctrl import IpAddrCtrl
import wx
import wx.xrc

###########################################################################
## Class BaseFrame
###########################################################################

class BaseFrame ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 1164,559 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

		bSizer19 = wx.BoxSizer( wx.HORIZONTAL )

		bSizer20 = wx.BoxSizer( wx.VERTICAL )

		sbSizer8 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"robot" ), wx.HORIZONTAL )

		gSizer7 = wx.GridSizer( 0, 2, 0, 0 )

		self.m_staticText13 = wx.StaticText(self, wx.ID_ANY, u"cur_x:", wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
		self.m_staticText13.Wrap( -1 )
		gSizer7.Add( self.m_staticText13, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )

		self.m_robot_cur_x = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer7.Add( self.m_robot_cur_x, 0, wx.ALL, 5 )

		self.m_staticText14 = wx.StaticText(self, wx.ID_ANY, u"cur_y:", wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
		self.m_staticText14.Wrap( -1 )
		gSizer7.Add( self.m_staticText14, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )

		self.m_robot_cur_y = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer7.Add( self.m_robot_cur_y, 0, wx.ALL, 5 )

		self.m_staticText15 = wx.StaticText(self, wx.ID_ANY, u"cur_z:", wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
		self.m_staticText15.Wrap( -1 )
		gSizer7.Add( self.m_staticText15, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )

		self.m_robot_cur_z = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer7.Add( self.m_robot_cur_z, 0, wx.ALL, 5 )

		self.m_staticText16 = wx.StaticText(self, wx.ID_ANY, u"cur_u:", wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
		self.m_staticText16.Wrap( -1 )
		gSizer7.Add( self.m_staticText16, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )

		self.m_robot_cur_u = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer7.Add( self.m_robot_cur_u, 0, wx.ALL, 5 )

		self.m_staticText162 = wx.StaticText(self, wx.ID_ANY, u"cur_v:", wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
		self.m_staticText162.Wrap( -1 )
		gSizer7.Add( self.m_staticText162, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )

		self.m_robot_cur_v = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer7.Add( self.m_robot_cur_v, 0, wx.ALL, 5 )

		self.m_staticText161 = wx.StaticText(self, wx.ID_ANY, u"cur_w:", wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
		self.m_staticText161.Wrap( -1 )
		gSizer7.Add( self.m_staticText161, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )

		self.m_robot_cur_w = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer7.Add( self.m_robot_cur_w, 0, wx.ALL, 5 )


		sbSizer8.Add( gSizer7, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		gSizer4 = wx.GridSizer( 0, 2, 0, 0 )

		self.m_staticText3 = wx.StaticText(self, wx.ID_ANY, u"x:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )
		gSizer4.Add( self.m_staticText3, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		self.m_robot_x_text = wx.TextCtrl(self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer4.Add( self.m_robot_x_text, 0, wx.ALL, 5 )

		self.m_staticText4 = wx.StaticText(self, wx.ID_ANY, u"y:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )
		gSizer4.Add( self.m_staticText4, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		self.m_robot_y_text = wx.TextCtrl(self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer4.Add( self.m_robot_y_text, 0, wx.ALL, 5 )

		self.m_staticText5 = wx.StaticText(self, wx.ID_ANY, u"z:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )
		gSizer4.Add( self.m_staticText5, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		self.m_robot_z_text = wx.TextCtrl(self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer4.Add( self.m_robot_z_text, 0, wx.ALL, 5 )

		self.m_staticText62 = wx.StaticText(self, wx.ID_ANY, u"u:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText62.Wrap( -1 )
		gSizer4.Add( self.m_staticText62, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		self.m_robot_u_text = wx.TextCtrl(self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer4.Add( self.m_robot_u_text, 0, wx.ALL, 5 )

		self.m_staticText6211 = wx.StaticText(self, wx.ID_ANY, u"v:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6211.Wrap( -1 )
		gSizer4.Add( self.m_staticText6211, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		self.m_robot_v_text = wx.TextCtrl(self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer4.Add( self.m_robot_v_text, 0, wx.ALL, 5 )

		self.m_staticText621 = wx.StaticText(self, wx.ID_ANY, u"w:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText621.Wrap( -1 )
		gSizer4.Add( self.m_staticText621, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		self.m_robot_w_text = wx.TextCtrl(self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer4.Add( self.m_robot_w_text, 0, wx.ALL, 5 )

		self.m_staticText7 = wx.StaticText(self, wx.ID_ANY, u"hand mode:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )
		gSizer4.Add( self.m_staticText7, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		m_robot_hand_mode_choiceChoices = [ u"left", u"right", u"auto" ]
		self.m_robot_hand_mode_choice = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_robot_hand_mode_choiceChoices, 0 )
		self.m_robot_hand_mode_choice.SetSelection( 0 )
		gSizer4.Add( self.m_robot_hand_mode_choice, 0, wx.ALL, 5 )

		self.m_staticText8 = wx.StaticText(self, wx.ID_ANY, u"run type:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText8.Wrap( -1 )
		gSizer4.Add( self.m_staticText8, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		m_robot_run_type_choiceChoices = [ u"go", u"move" ]
		self.m_robot_run_type_choice = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_robot_run_type_choiceChoices, 0 )
		self.m_robot_run_type_choice.SetSelection( 0 )
		gSizer4.Add( self.m_robot_run_type_choice, 0, wx.ALL, 5 )

		self.m_button30 = wx.Button(self, wx.ID_ANY, u"run", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer4.Add( self.m_button30, 0, wx.ALL, 5 )

		self.m_button31 = wx.Button(self, wx.ID_ANY, u"stop", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer4.Add( self.m_button31, 0, wx.ALL, 5 )


		sbSizer8.Add( gSizer4, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		gSizer6 = wx.GridSizer( 0, 2, 0, 0 )

		self.m_button47 = wx.Button(self, wx.ID_ANY, u"-x", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer6.Add( self.m_button47, 0, wx.ALL, 5 )

		self.m_button48 = wx.Button(self, wx.ID_ANY, u"+x", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer6.Add( self.m_button48, 0, wx.ALL, 5 )

		self.m_button49 = wx.Button(self, wx.ID_ANY, u"-y", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer6.Add( self.m_button49, 0, wx.ALL, 5 )

		self.m_button50 = wx.Button(self, wx.ID_ANY, u"+y", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer6.Add( self.m_button50, 0, wx.ALL, 5 )

		self.m_button51 = wx.Button(self, wx.ID_ANY, u"-z", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer6.Add( self.m_button51, 0, wx.ALL, 5 )

		self.m_button52 = wx.Button(self, wx.ID_ANY, u"+z", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer6.Add( self.m_button52, 0, wx.ALL, 5 )

		self.m_button53 = wx.Button(self, wx.ID_ANY, u"-u", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer6.Add( self.m_button53, 0, wx.ALL, 5 )

		self.m_button54 = wx.Button(self, wx.ID_ANY, u"+u", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer6.Add( self.m_button54, 0, wx.ALL, 5 )

		self.m_button5445 = wx.Button(self, wx.ID_ANY, u"-v", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer6.Add( self.m_button5445, 0, wx.ALL, 5 )

		self.m_button544 = wx.Button(self, wx.ID_ANY, u"+v", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer6.Add( self.m_button544, 0, wx.ALL, 5 )

		self.m_button543 = wx.Button(self, wx.ID_ANY, u"-w", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer6.Add( self.m_button543, 0, wx.ALL, 5 )

		self.m_button542 = wx.Button(self, wx.ID_ANY, u"+w", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer6.Add( self.m_button542, 0, wx.ALL, 5 )


		sbSizer8.Add( gSizer6, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		bSizer30 = wx.BoxSizer( wx.VERTICAL )

		bSizer18 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText29 = wx.StaticText(self, wx.ID_ANY, u"speed:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText29.Wrap( -1 )
		bSizer18.Add( self.m_staticText29, 0, wx.ALL, 5 )

		m_robot_speed_choiceChoices = [ u"low", u"high" ]
		self.m_robot_speed_choice = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_robot_speed_choiceChoices, 0 )
		self.m_robot_speed_choice.SetSelection( 0 )
		bSizer18.Add( self.m_robot_speed_choice, 0, wx.ALL, 5 )


		bSizer30.Add( bSizer18, 1, wx.EXPAND, 5 )

		self.m_robot_continue_movement_check = wx.CheckBox(self, wx.ID_ANY, u"连续运动", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_robot_continue_movement_check.SetValue(True)
		bSizer30.Add( self.m_robot_continue_movement_check, 0, wx.ALL, 5 )

		bSizer31 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText6 = wx.StaticText(self, wx.ID_ANY, u"步距(mm, deg):", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )
		bSizer31.Add( self.m_staticText6, 1, wx.ALL, 5 )

		self.m_robot_step_text = wx.TextCtrl(self, wx.ID_ANY, u"1", wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
		bSizer31.Add( self.m_robot_step_text, 0, wx.ALL, 5 )


		bSizer30.Add( bSizer31, 0, wx.EXPAND, 5 )


		sbSizer8.Add( bSizer30, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )


		bSizer20.Add( sbSizer8, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )

		sbSizer81 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"xy" ), wx.HORIZONTAL )

		gSizer71 = wx.GridSizer( 0, 2, 0, 0 )

		self.m_staticText131 = wx.StaticText(self, wx.ID_ANY, u"cur_x:", wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
		self.m_staticText131.Wrap( -1 )
		gSizer71.Add( self.m_staticText131, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )

		self.m_xy_cur_x = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer71.Add( self.m_xy_cur_x, 0, wx.ALL, 5 )

		self.m_staticText141 = wx.StaticText(self, wx.ID_ANY, u"cur_y:", wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
		self.m_staticText141.Wrap( -1 )
		gSizer71.Add( self.m_staticText141, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )

		self.m_xy_cur_y = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer71.Add( self.m_xy_cur_y, 0, wx.ALL, 5 )


		sbSizer81.Add( gSizer71, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		gSizer41 = wx.GridSizer( 0, 2, 0, 0 )

		self.m_staticText31 = wx.StaticText(self, wx.ID_ANY, u"x:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText31.Wrap( -1 )
		gSizer41.Add( self.m_staticText31, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		self.m_xy_x_text = wx.TextCtrl(self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer41.Add( self.m_xy_x_text, 0, wx.ALL, 5 )

		self.m_staticText41 = wx.StaticText(self, wx.ID_ANY, u"y:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText41.Wrap( -1 )
		gSizer41.Add( self.m_staticText41, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		self.m_xy_y_text = wx.TextCtrl(self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer41.Add( self.m_xy_y_text, 0, wx.ALL, 5 )

		self.m_button301 = wx.Button(self, wx.ID_ANY, u"run", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer41.Add( self.m_button301, 0, wx.ALL, 5 )

		self.m_button311 = wx.Button(self, wx.ID_ANY, u"stop", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer41.Add( self.m_button311, 0, wx.ALL, 5 )


		sbSizer81.Add( gSizer41, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		gSizer61 = wx.GridSizer( 0, 2, 0, 0 )

		self.m_button511 = wx.Button(self, wx.ID_ANY, u"-x", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer61.Add( self.m_button511, 0, wx.ALL, 5 )

		self.m_button521 = wx.Button(self, wx.ID_ANY, u"+x", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer61.Add( self.m_button521, 0, wx.ALL, 5 )

		self.m_button531 = wx.Button(self, wx.ID_ANY, u"-y", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer61.Add( self.m_button531, 0, wx.ALL, 5 )

		self.m_button541 = wx.Button(self, wx.ID_ANY, u"+y", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer61.Add( self.m_button541, 0, wx.ALL, 5 )


		sbSizer81.Add( gSizer61, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		bSizer301 = wx.BoxSizer( wx.VERTICAL )

		bSizer181 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText291 = wx.StaticText(self, wx.ID_ANY, u"speed:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText291.Wrap( -1 )
		bSizer181.Add( self.m_staticText291, 0, wx.ALL, 5 )

		m_xy_speed_choiceChoices = [ u"low", u"high" ]
		self.m_xy_speed_choice = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_xy_speed_choiceChoices, 0 )
		self.m_xy_speed_choice.SetSelection( 0 )
		bSizer181.Add( self.m_xy_speed_choice, 0, wx.ALL, 5 )


		bSizer301.Add( bSizer181, 1, wx.EXPAND, 5 )

		self.m_xy_continue_movement_check = wx.CheckBox(self, wx.ID_ANY, u"连续运动", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_xy_continue_movement_check.SetValue(True)
		bSizer301.Add( self.m_xy_continue_movement_check, 0, wx.ALL, 5 )

		bSizer311 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText61 = wx.StaticText(self, wx.ID_ANY, u"步距(mm, deg):", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText61.Wrap( -1 )
		bSizer311.Add( self.m_staticText61, 1, wx.ALL, 5 )

		self.m_xy_step_text = wx.TextCtrl(self, wx.ID_ANY, u"1", wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
		bSizer311.Add( self.m_xy_step_text, 0, wx.ALL, 5 )


		bSizer301.Add( bSizer311, 0, wx.EXPAND, 5 )


		sbSizer81.Add( bSizer301, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )


		bSizer20.Add( sbSizer81, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )


		bSizer19.Add( bSizer20, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )

		bSizer10 = wx.BoxSizer( wx.VERTICAL )

		bSizer22 = wx.BoxSizer( wx.HORIZONTAL )

		sbSizer3 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"input IO" ), wx.VERTICAL )

		self.m_scrolledWindow1 = wx.ScrolledWindow(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
		self.m_scrolledWindow1.SetScrollRate( 5, 5 )
		gSizer1011 = wx.GridSizer( 0, 2, 0, 0 )

		self.m_io_input_check_0 = wx.CheckBox( self.m_scrolledWindow1, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1011.Add( self.m_io_input_check_0, 0, wx.ALL, 5 )

		self.m_io_input_check_1 = wx.CheckBox( self.m_scrolledWindow1, wx.ID_ANY, u"1", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1011.Add( self.m_io_input_check_1, 0, wx.ALL, 5 )

		self.m_io_input_check_2 = wx.CheckBox( self.m_scrolledWindow1, wx.ID_ANY, u"2", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1011.Add( self.m_io_input_check_2, 0, wx.ALL, 5 )

		self.m_io_input_check_3 = wx.CheckBox( self.m_scrolledWindow1, wx.ID_ANY, u"3", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1011.Add( self.m_io_input_check_3, 0, wx.ALL, 5 )

		self.m_io_input_check_4 = wx.CheckBox( self.m_scrolledWindow1, wx.ID_ANY, u"4", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1011.Add( self.m_io_input_check_4, 0, wx.ALL, 5 )

		self.m_io_input_check_5 = wx.CheckBox( self.m_scrolledWindow1, wx.ID_ANY, u"5", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1011.Add( self.m_io_input_check_5, 0, wx.ALL, 5 )

		self.m_io_input_check_6 = wx.CheckBox( self.m_scrolledWindow1, wx.ID_ANY, u"6", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1011.Add( self.m_io_input_check_6, 0, wx.ALL, 5 )

		self.m_io_input_check_7 = wx.CheckBox( self.m_scrolledWindow1, wx.ID_ANY, u"7", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1011.Add( self.m_io_input_check_7, 0, wx.ALL, 5 )

		self.m_io_input_check_8 = wx.CheckBox( self.m_scrolledWindow1, wx.ID_ANY, u"8", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1011.Add( self.m_io_input_check_8, 0, wx.ALL, 5 )

		self.m_io_input_check_9 = wx.CheckBox( self.m_scrolledWindow1, wx.ID_ANY, u"9", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1011.Add( self.m_io_input_check_9, 0, wx.ALL, 5 )

		self.m_io_input_check_10 = wx.CheckBox( self.m_scrolledWindow1, wx.ID_ANY, u"10", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1011.Add( self.m_io_input_check_10, 0, wx.ALL, 5 )

		self.m_io_input_check_11 = wx.CheckBox( self.m_scrolledWindow1, wx.ID_ANY, u"11", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1011.Add( self.m_io_input_check_11, 0, wx.ALL, 5 )

		self.m_io_input_check_12 = wx.CheckBox( self.m_scrolledWindow1, wx.ID_ANY, u"12", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1011.Add( self.m_io_input_check_12, 0, wx.ALL, 5 )

		self.m_io_input_check_13 = wx.CheckBox( self.m_scrolledWindow1, wx.ID_ANY, u"13", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1011.Add( self.m_io_input_check_13, 0, wx.ALL, 5 )

		self.m_io_input_check_14 = wx.CheckBox( self.m_scrolledWindow1, wx.ID_ANY, u"14", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1011.Add( self.m_io_input_check_14, 0, wx.ALL, 5 )

		self.m_io_input_check_15 = wx.CheckBox( self.m_scrolledWindow1, wx.ID_ANY, u"15", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1011.Add( self.m_io_input_check_15, 0, wx.ALL, 5 )

		self.m_io_input_check_16 = wx.CheckBox( self.m_scrolledWindow1, wx.ID_ANY, u"16", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1011.Add( self.m_io_input_check_16, 0, wx.ALL, 5 )

		self.m_io_input_check_17 = wx.CheckBox( self.m_scrolledWindow1, wx.ID_ANY, u"17", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1011.Add( self.m_io_input_check_17, 0, wx.ALL, 5 )

		self.m_io_input_check_18 = wx.CheckBox( self.m_scrolledWindow1, wx.ID_ANY, u"18", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1011.Add( self.m_io_input_check_18, 0, wx.ALL, 5 )

		self.m_io_input_check_19 = wx.CheckBox( self.m_scrolledWindow1, wx.ID_ANY, u"19", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1011.Add( self.m_io_input_check_19, 0, wx.ALL, 5 )

		self.m_io_input_check_20 = wx.CheckBox( self.m_scrolledWindow1, wx.ID_ANY, u"20", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1011.Add( self.m_io_input_check_20, 0, wx.ALL, 5 )

		self.m_io_input_check_21 = wx.CheckBox( self.m_scrolledWindow1, wx.ID_ANY, u"21", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1011.Add( self.m_io_input_check_21, 0, wx.ALL, 5 )

		self.m_io_input_check_22 = wx.CheckBox( self.m_scrolledWindow1, wx.ID_ANY, u"22", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1011.Add( self.m_io_input_check_22, 0, wx.ALL, 5 )

		self.m_io_input_check_23 = wx.CheckBox( self.m_scrolledWindow1, wx.ID_ANY, u"23", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1011.Add( self.m_io_input_check_23, 0, wx.ALL, 5 )

		self.m_io_input_check_24 = wx.CheckBox( self.m_scrolledWindow1, wx.ID_ANY, u"24", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1011.Add( self.m_io_input_check_24, 0, wx.ALL, 5 )

		self.m_io_input_check_25 = wx.CheckBox( self.m_scrolledWindow1, wx.ID_ANY, u"25", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1011.Add( self.m_io_input_check_25, 0, wx.ALL, 5 )

		self.m_io_input_check_26 = wx.CheckBox( self.m_scrolledWindow1, wx.ID_ANY, u"26", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1011.Add( self.m_io_input_check_26, 0, wx.ALL, 5 )

		self.m_io_input_check_27 = wx.CheckBox( self.m_scrolledWindow1, wx.ID_ANY, u"27", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1011.Add( self.m_io_input_check_27, 0, wx.ALL, 5 )

		self.m_io_input_check_28 = wx.CheckBox( self.m_scrolledWindow1, wx.ID_ANY, u"28", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1011.Add( self.m_io_input_check_28, 0, wx.ALL, 5 )

		self.m_io_input_check_29 = wx.CheckBox( self.m_scrolledWindow1, wx.ID_ANY, u"29", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1011.Add( self.m_io_input_check_29, 0, wx.ALL, 5 )

		self.m_io_input_check_30 = wx.CheckBox( self.m_scrolledWindow1, wx.ID_ANY, u"30", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1011.Add( self.m_io_input_check_30, 0, wx.ALL, 5 )

		self.m_io_input_check_31 = wx.CheckBox( self.m_scrolledWindow1, wx.ID_ANY, u"31", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1011.Add( self.m_io_input_check_31, 0, wx.ALL, 5 )


		self.m_scrolledWindow1.SetSizer( gSizer1011 )
		self.m_scrolledWindow1.Layout()
		gSizer1011.Fit( self.m_scrolledWindow1 )
		sbSizer3.Add( self.m_scrolledWindow1, 1, wx.EXPAND |wx.ALL, 5 )


		bSizer22.Add( sbSizer3, 1, wx.EXPAND, 5 )

		sbSizer4 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"output IO" ), wx.VERTICAL )

		self.m_scrolledWindow11 = wx.ScrolledWindow(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
		self.m_scrolledWindow11.SetScrollRate( 5, 5 )
		gSizer101 = wx.GridSizer( 0, 2, 0, 0 )

		self.m_io_output_check_0 = wx.CheckBox( self.m_scrolledWindow11, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer101.Add( self.m_io_output_check_0, 0, wx.ALL, 5 )

		self.m_io_output_check_1 = wx.CheckBox( self.m_scrolledWindow11, wx.ID_ANY, u"1", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer101.Add( self.m_io_output_check_1, 0, wx.ALL, 5 )

		self.m_io_output_check_2 = wx.CheckBox( self.m_scrolledWindow11, wx.ID_ANY, u"2", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer101.Add( self.m_io_output_check_2, 0, wx.ALL, 5 )

		self.m_io_output_check_3 = wx.CheckBox( self.m_scrolledWindow11, wx.ID_ANY, u"3", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer101.Add( self.m_io_output_check_3, 0, wx.ALL, 5 )

		self.m_io_output_check_4 = wx.CheckBox( self.m_scrolledWindow11, wx.ID_ANY, u"4", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer101.Add( self.m_io_output_check_4, 0, wx.ALL, 5 )

		self.m_io_output_check_5 = wx.CheckBox( self.m_scrolledWindow11, wx.ID_ANY, u"5", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer101.Add( self.m_io_output_check_5, 0, wx.ALL, 5 )

		self.m_io_output_check_6 = wx.CheckBox( self.m_scrolledWindow11, wx.ID_ANY, u"6", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer101.Add( self.m_io_output_check_6, 0, wx.ALL, 5 )

		self.m_io_output_check_7 = wx.CheckBox( self.m_scrolledWindow11, wx.ID_ANY, u"7", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer101.Add( self.m_io_output_check_7, 0, wx.ALL, 5 )

		self.m_io_output_check_8 = wx.CheckBox( self.m_scrolledWindow11, wx.ID_ANY, u"8", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer101.Add( self.m_io_output_check_8, 0, wx.ALL, 5 )

		self.m_io_output_check_9 = wx.CheckBox( self.m_scrolledWindow11, wx.ID_ANY, u"9", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer101.Add( self.m_io_output_check_9, 0, wx.ALL, 5 )

		self.m_io_output_check_10 = wx.CheckBox( self.m_scrolledWindow11, wx.ID_ANY, u"10", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer101.Add( self.m_io_output_check_10, 0, wx.ALL, 5 )

		self.m_io_output_check_11 = wx.CheckBox( self.m_scrolledWindow11, wx.ID_ANY, u"11", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer101.Add( self.m_io_output_check_11, 0, wx.ALL, 5 )

		self.m_io_output_check_12 = wx.CheckBox( self.m_scrolledWindow11, wx.ID_ANY, u"12", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer101.Add( self.m_io_output_check_12, 0, wx.ALL, 5 )

		self.m_io_output_check_13 = wx.CheckBox( self.m_scrolledWindow11, wx.ID_ANY, u"13", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer101.Add( self.m_io_output_check_13, 0, wx.ALL, 5 )

		self.m_io_output_check_14 = wx.CheckBox( self.m_scrolledWindow11, wx.ID_ANY, u"14", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer101.Add( self.m_io_output_check_14, 0, wx.ALL, 5 )

		self.m_io_output_check_15 = wx.CheckBox( self.m_scrolledWindow11, wx.ID_ANY, u"15", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer101.Add( self.m_io_output_check_15, 0, wx.ALL, 5 )

		self.m_io_output_check_16 = wx.CheckBox( self.m_scrolledWindow11, wx.ID_ANY, u"16", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer101.Add( self.m_io_output_check_16, 0, wx.ALL, 5 )

		self.m_io_output_check_17 = wx.CheckBox( self.m_scrolledWindow11, wx.ID_ANY, u"17", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer101.Add( self.m_io_output_check_17, 0, wx.ALL, 5 )

		self.m_io_output_check_18 = wx.CheckBox( self.m_scrolledWindow11, wx.ID_ANY, u"18", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer101.Add( self.m_io_output_check_18, 0, wx.ALL, 5 )

		self.m_io_output_check_19 = wx.CheckBox( self.m_scrolledWindow11, wx.ID_ANY, u"19", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer101.Add( self.m_io_output_check_19, 0, wx.ALL, 5 )

		self.m_io_output_check_20 = wx.CheckBox( self.m_scrolledWindow11, wx.ID_ANY, u"20", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer101.Add( self.m_io_output_check_20, 0, wx.ALL, 5 )

		self.m_io_output_check_21 = wx.CheckBox( self.m_scrolledWindow11, wx.ID_ANY, u"21", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer101.Add( self.m_io_output_check_21, 0, wx.ALL, 5 )

		self.m_io_output_check_22 = wx.CheckBox( self.m_scrolledWindow11, wx.ID_ANY, u"22", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer101.Add( self.m_io_output_check_22, 0, wx.ALL, 5 )

		self.m_io_output_check_23 = wx.CheckBox( self.m_scrolledWindow11, wx.ID_ANY, u"23", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer101.Add( self.m_io_output_check_23, 0, wx.ALL, 5 )

		self.m_io_output_check_24 = wx.CheckBox( self.m_scrolledWindow11, wx.ID_ANY, u"24", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer101.Add( self.m_io_output_check_24, 0, wx.ALL, 5 )

		self.m_io_output_check_25 = wx.CheckBox( self.m_scrolledWindow11, wx.ID_ANY, u"25", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer101.Add( self.m_io_output_check_25, 0, wx.ALL, 5 )

		self.m_io_output_check_26 = wx.CheckBox( self.m_scrolledWindow11, wx.ID_ANY, u"26", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer101.Add( self.m_io_output_check_26, 0, wx.ALL, 5 )

		self.m_io_output_check_27 = wx.CheckBox( self.m_scrolledWindow11, wx.ID_ANY, u"27", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer101.Add( self.m_io_output_check_27, 0, wx.ALL, 5 )

		self.m_io_output_check_28 = wx.CheckBox( self.m_scrolledWindow11, wx.ID_ANY, u"28", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer101.Add( self.m_io_output_check_28, 0, wx.ALL, 5 )

		self.m_io_output_check_29 = wx.CheckBox( self.m_scrolledWindow11, wx.ID_ANY, u"29", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer101.Add( self.m_io_output_check_29, 0, wx.ALL, 5 )

		self.m_io_output_check_30 = wx.CheckBox( self.m_scrolledWindow11, wx.ID_ANY, u"30", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer101.Add( self.m_io_output_check_30, 0, wx.ALL, 5 )

		self.m_io_output_check_31 = wx.CheckBox( self.m_scrolledWindow11, wx.ID_ANY, u"31", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer101.Add( self.m_io_output_check_31, 0, wx.ALL, 5 )


		self.m_scrolledWindow11.SetSizer( gSizer101 )
		self.m_scrolledWindow11.Layout()
		gSizer101.Fit( self.m_scrolledWindow11 )
		sbSizer4.Add( self.m_scrolledWindow11, 1, wx.EXPAND |wx.ALL, 5 )


		bSizer22.Add( sbSizer4, 1, wx.EXPAND, 5 )


		bSizer10.Add( bSizer22, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )

		gSizer9 = wx.GridSizer( 0, 2, 0, 0 )

		self.m_staticText19 = wx.StaticText( self, wx.ID_ANY, u"ip:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText19.Wrap( -1 )
		gSizer9.Add( self.m_staticText19, 0, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_text_ctrl_ip = IpAddrCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer9.Add( self.m_text_ctrl_ip, 1, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText20 = wx.StaticText( self, wx.ID_ANY, u"port:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText20.Wrap( -1 )
		gSizer9.Add( self.m_staticText20, 0, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_text_ctrl_port = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer9.Add( self.m_text_ctrl_port, 0, wx.ALL, 5 )

		self.m_staticText21 = wx.StaticText( self, wx.ID_ANY, u"机械手类型：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText21.Wrap( -1 )
		gSizer9.Add( self.m_staticText21, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 5 )

		m_choice_robot_typeChoices = [ u"4轴-RR", u"6轴-RR", u"4轴-KEN", u"6轴-KEN" ]
		self.m_choice_robot_type = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_robot_typeChoices, 0 )
		self.m_choice_robot_type.SetSelection( 0 )
		gSizer9.Add( self.m_choice_robot_type, 0, wx.ALL, 5 )


		bSizer10.Add( gSizer9, 0, 0, 5 )

		self.m_button_connect = wx.Button( self, wx.ID_ANY, u"connect", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer10.Add( self.m_button_connect, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )

		self.m_button17 = wx.Button( self, wx.ID_ANY, u"Exit", wx.DefaultPosition, wx.Size( -1,50 ), 0 )
		bSizer10.Add( self.m_button17, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )


		bSizer19.Add( bSizer10, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer19 )
		self.Layout()
		self.m_timer4 = wx.Timer()
		self.m_timer4.SetOwner( self, wx.ID_ANY )
		self.m_timer4.Start( 300 )


		self.Centre( wx.BOTH )

		# Connect Events
		self.m_button30.Bind( wx.EVT_LEFT_DOWN, self.onRobotRun )
		self.m_button31.Bind( wx.EVT_LEFT_DOWN, self.onRobotStop )
		self.m_button47.Bind( wx.EVT_LEFT_DOWN, self.onRobotSubX )
		self.m_button47.Bind( wx.EVT_LEFT_UP, self.onRobotButtonUp )
		self.m_button48.Bind( wx.EVT_LEFT_DOWN, self.onRobotAddX )
		self.m_button48.Bind( wx.EVT_LEFT_UP, self.onRobotButtonUp )
		self.m_button49.Bind( wx.EVT_LEFT_DOWN, self.onRobotSubY )
		self.m_button49.Bind( wx.EVT_LEFT_UP, self.onRobotButtonUp )
		self.m_button50.Bind( wx.EVT_LEFT_DOWN, self.onRobotAddY )
		self.m_button50.Bind( wx.EVT_LEFT_UP, self.onRobotButtonUp )
		self.m_button51.Bind( wx.EVT_LEFT_DOWN, self.onRobotSubZ )
		self.m_button51.Bind( wx.EVT_LEFT_UP, self.onRobotButtonUp )
		self.m_button52.Bind( wx.EVT_LEFT_DOWN, self.onRobotAddZ )
		self.m_button52.Bind( wx.EVT_LEFT_UP, self.onRobotButtonUp )
		self.m_button53.Bind( wx.EVT_LEFT_DOWN, self.onRobotSubU )
		self.m_button53.Bind( wx.EVT_LEFT_UP, self.onRobotButtonUp )
		self.m_button54.Bind( wx.EVT_LEFT_DOWN, self.onRobotAddU )
		self.m_button54.Bind( wx.EVT_LEFT_UP, self.onRobotButtonUp )
		self.m_button5445.Bind( wx.EVT_LEFT_DOWN, self.onRobotSubV )
		self.m_button5445.Bind( wx.EVT_LEFT_UP, self.onRobotButtonUp )
		self.m_button544.Bind( wx.EVT_LEFT_DOWN, self.onRobotAddV )
		self.m_button544.Bind( wx.EVT_LEFT_UP, self.onRobotButtonUp )
		self.m_button543.Bind( wx.EVT_LEFT_DOWN, self.onRobotSubW )
		self.m_button543.Bind( wx.EVT_LEFT_UP, self.onRobotButtonUp )
		self.m_button542.Bind( wx.EVT_LEFT_DOWN, self.onRobotAddW )
		self.m_button542.Bind( wx.EVT_LEFT_UP, self.onRobotButtonUp )
		self.m_button301.Bind( wx.EVT_LEFT_DOWN, self.onXYRun )
		self.m_button311.Bind( wx.EVT_LEFT_DOWN, self.onXYStop )
		self.m_button511.Bind( wx.EVT_LEFT_DOWN, self.onXYSubX )
		self.m_button511.Bind( wx.EVT_LEFT_UP, self.onXYButtonUp )
		self.m_button521.Bind( wx.EVT_LEFT_DOWN, self.onXYAddX )
		self.m_button521.Bind( wx.EVT_LEFT_UP, self.onXYButtonUp )
		self.m_button531.Bind( wx.EVT_LEFT_DOWN, self.onXYSubY )
		self.m_button531.Bind( wx.EVT_LEFT_UP, self.onXYButtonUp )
		self.m_button541.Bind( wx.EVT_LEFT_DOWN, self.onXYAddY )
		self.m_button541.Bind( wx.EVT_LEFT_UP, self.onXYButtonUp )
		self.m_io_output_check_0.Bind( wx.EVT_CHECKBOX, self.onSetOutputIO )
		self.m_io_output_check_1.Bind( wx.EVT_CHECKBOX, self.onSetOutputIO )
		self.m_io_output_check_2.Bind( wx.EVT_CHECKBOX, self.onSetOutputIO )
		self.m_io_output_check_3.Bind( wx.EVT_CHECKBOX, self.onSetOutputIO )
		self.m_io_output_check_4.Bind( wx.EVT_CHECKBOX, self.onSetOutputIO )
		self.m_io_output_check_5.Bind( wx.EVT_CHECKBOX, self.onSetOutputIO )
		self.m_io_output_check_6.Bind( wx.EVT_CHECKBOX, self.onSetOutputIO )
		self.m_io_output_check_7.Bind( wx.EVT_CHECKBOX, self.onSetOutputIO )
		self.m_io_output_check_8.Bind( wx.EVT_CHECKBOX, self.onSetOutputIO )
		self.m_io_output_check_9.Bind( wx.EVT_CHECKBOX, self.onSetOutputIO )
		self.m_io_output_check_10.Bind( wx.EVT_CHECKBOX, self.onSetOutputIO )
		self.m_io_output_check_11.Bind( wx.EVT_CHECKBOX, self.onSetOutputIO )
		self.m_io_output_check_12.Bind( wx.EVT_CHECKBOX, self.onSetOutputIO )
		self.m_io_output_check_13.Bind( wx.EVT_CHECKBOX, self.onSetOutputIO )
		self.m_io_output_check_14.Bind( wx.EVT_CHECKBOX, self.onSetOutputIO )
		self.m_io_output_check_15.Bind( wx.EVT_CHECKBOX, self.onSetOutputIO )
		self.m_io_output_check_16.Bind( wx.EVT_CHECKBOX, self.onSetOutputIO )
		self.m_io_output_check_17.Bind( wx.EVT_CHECKBOX, self.onSetOutputIO )
		self.m_io_output_check_18.Bind( wx.EVT_CHECKBOX, self.onSetOutputIO )
		self.m_io_output_check_19.Bind( wx.EVT_CHECKBOX, self.onSetOutputIO )
		self.m_io_output_check_20.Bind( wx.EVT_CHECKBOX, self.onSetOutputIO )
		self.m_io_output_check_21.Bind( wx.EVT_CHECKBOX, self.onSetOutputIO )
		self.m_io_output_check_22.Bind( wx.EVT_CHECKBOX, self.onSetOutputIO )
		self.m_io_output_check_23.Bind( wx.EVT_CHECKBOX, self.onSetOutputIO )
		self.m_io_output_check_24.Bind( wx.EVT_CHECKBOX, self.onSetOutputIO )
		self.m_io_output_check_25.Bind( wx.EVT_CHECKBOX, self.onSetOutputIO )
		self.m_io_output_check_26.Bind( wx.EVT_CHECKBOX, self.onSetOutputIO )
		self.m_io_output_check_27.Bind( wx.EVT_CHECKBOX, self.onSetOutputIO )
		self.m_io_output_check_28.Bind( wx.EVT_CHECKBOX, self.onSetOutputIO )
		self.m_io_output_check_29.Bind( wx.EVT_CHECKBOX, self.onSetOutputIO )
		self.m_io_output_check_30.Bind( wx.EVT_CHECKBOX, self.onSetOutputIO )
		self.m_io_output_check_31.Bind( wx.EVT_CHECKBOX, self.onSetOutputIO )
		self.m_button_connect.Bind( wx.EVT_BUTTON, self._onConnect )
		self.m_button17.Bind( wx.EVT_BUTTON, self.onExit )
		self.Bind( wx.EVT_TIMER, self.onUpdate, id=wx.ID_ANY )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def onRobotRun( self, event ):
		event.Skip()

	def onRobotStop( self, event ):
		event.Skip()

	def onRobotSubX( self, event ):
		event.Skip()

	def onRobotButtonUp( self, event ):
		event.Skip()

	def onRobotAddX( self, event ):
		event.Skip()


	def onRobotSubY( self, event ):
		event.Skip()


	def onRobotAddY( self, event ):
		event.Skip()


	def onRobotSubZ( self, event ):
		event.Skip()


	def onRobotAddZ( self, event ):
		event.Skip()


	def onRobotSubU( self, event ):
		event.Skip()


	def onRobotAddU( self, event ):
		event.Skip()


	def onRobotSubV( self, event ):
		event.Skip()


	def onRobotAddV( self, event ):
		event.Skip()


	def onRobotSubW( self, event ):
		event.Skip()


	def onRobotAddW( self, event ):
		event.Skip()


	def onXYRun( self, event ):
		event.Skip()

	def onXYStop( self, event ):
		event.Skip()

	def onXYSubX( self, event ):
		event.Skip()

	def onXYButtonUp( self, event ):
		event.Skip()

	def onXYAddX( self, event ):
		event.Skip()


	def onXYSubY( self, event ):
		event.Skip()


	def onXYAddY( self, event ):
		event.Skip()


	def onSetOutputIO( self, event ):
		event.Skip()
































	def _onConnect( self, event ):
		event.Skip()
	
	def onExit( self, event ):
		event.Skip()
	
	def onUpdate( self, event ):
		event.Skip()
	

