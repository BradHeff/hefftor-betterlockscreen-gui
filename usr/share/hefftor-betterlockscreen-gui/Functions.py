# =================================================================
# =                  Author: Brad Heffernan                       =
# =================================================================
import os
import subprocess
from gi.repository import GLib
from os.path import expanduser

home = expanduser("~")
base_dir = os.path.dirname(os.path.realpath(__file__))

# ================================================
#                   GLOBALS
# ================================================

# ================================================
#               NOTIFICATIONS
# ================================================


def show_in_app_notification(self, message):
    if self.timeout_id is not None:
        GLib.source_remove(self.timeout_id)
        self.timeout_id = None

    self.notification_label.set_markup("<span foreground=\"white\">" +
                                       message + "</span>")
    self.notification_revealer.set_reveal_child(True)
    self.timeout_id = GLib.timeout_add(3000, timeOut, self)


def timeOut(self):
    close_in_app_notification(self)


def close_in_app_notification(self):
    self.notification_revealer.set_reveal_child(False)
    GLib.source_remove(self.timeout_id)
    self.timeout_id = None
