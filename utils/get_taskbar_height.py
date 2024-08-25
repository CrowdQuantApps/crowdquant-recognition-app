import ctypes
from ctypes import wintypes


def get_taskbar_height():
    taskbar = ctypes.windll.user32.FindWindowW(u'Shell_traywnd', None)
    rect = ctypes.wintypes.RECT()
    ctypes.windll.user32.GetWindowRect(taskbar, ctypes.byref(rect))
    return rect.bottom - rect.top
