###############################################################
# Copyright (C) 2014 Fedor Cherepanov

# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
###############################################################

import os, sublime, sublime_plugin

if sublime.platform()=='windows' and os.name=='nt':
	from ctypes import wintypes
	from ctypes import windll
	SetLayeredWindowAttributes = windll.user32.SetLayeredWindowAttributes
	SetLayeredWindowAttributes.restype = wintypes.BOOL
	SetLayeredWindowAttributes.argtypes = [
		wintypes.HWND,
		wintypes.COLORREF,
		wintypes.BYTE,
		wintypes.DWORD
	]

	GetWindowLong = windll.user32.GetWindowLongA
	GetWindowLong.restype = wintypes.LONG
	GetWindowLong.argtypes = [
		wintypes.HWND,
		wintypes.DWORD
	]

	SetWindowLong = windll.user32.SetWindowLongA
	SetWindowLong.restype = wintypes.LONG
	SetWindowLong.argtypes = [
		wintypes.HWND,
		wintypes.INT,
		wintypes.DWORD
	]

	GWL_EXSTYLE = -20
	LWA_ALPHA = 0x00000002
	WS_EX_LAYERED = 0x00080000

	handle = 0

	def set_handle():
		global handle
		handle = sublime.active_window().hwnd()
		windowLong_Layered = GetWindowLong(handle, GWL_EXSTYLE) | WS_EX_LAYERED
		SetWindowLong(handle, GWL_EXSTYLE, windowLong_Layered)
		set_alpha_level(alpha_level)

	alpha_level = 255

	def set_alpha_level(opacity):
		if (handle):
			SetLayeredWindowAttributes(handle, 0, opacity, LWA_ALPHA)

	def plugin_loaded():
		settings = sublime.load_settings('Preferences.sublime-settings')
		global alpha_level
		alpha_level = settings.get('alpha_level', 234)
		sublime.set_timeout_async(lambda: set_handle(), 0) #Executing this function from same thread caused freezing

	class AlphaOff(sublime_plugin.WindowCommand):
		def run(self):
			set_alpha_level(255)

	class AlphaOn(sublime_plugin.WindowCommand):
		def run(self):
			global alpha_level
			set_alpha_level(alpha_level)

	class AlphaInc(sublime_plugin.WindowCommand):
		def run(self):
			global alpha_level
			alpha_level = alpha_level+10
			if alpha_level>255: alpha_level = 255
			set_alpha_level(alpha_level)

	class AlphaDec(sublime_plugin.WindowCommand):
		def run(self):
			global alpha_level
			alpha_level = alpha_level-10
			if alpha_level<126: alpha_level = 126
			set_alpha_level(alpha_level)
