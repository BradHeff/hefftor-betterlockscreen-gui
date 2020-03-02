#!/usr/bin/env python3

# =================================================================
# =                  Author: Brad Heffernan                       =
# =================================================================

import gi
import Functions as fn
import GUI
import threading as th
import webbrowser
import Splash
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, Gdk, GLib # noqa


class Main(Gtk.Window):
    def __init__(self):
        super(Main, self).__init__(title="Betterlockscreen GUI")
        self.set_border_width(10)
        self.set_default_size(700, 460)
        self.set_icon_from_file(fn.os.path.join(
            GUI.base_dir, 'images/hefftorlinux.svg'))
        self.set_position(Gtk.WindowPosition.CENTER)

        self.timeout_id = None
        self.image_path = None

        self.loc = Gtk.Entry()
        self.hbox3 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,
                             spacing=10)
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        self.fb = Gtk.FlowBox()
        self.fb.set_valign(Gtk.Align.START)
        self.fb.set_max_children_per_line(6)
        self.fb.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.fb.connect("child-activated", self.on_item_clicked)
        # self.create_flowbox(fb)

        scrolled.add(self.fb)

        self.hbox3.pack_start(scrolled, True, True, 0)

        splScr = Splash.splashScreen()

        while Gtk.events_pending():
            Gtk.main_iteration()
        # self.create_flowbox(self.loc.get_text())
        t = th.Thread(target=self.create_flowbox,
                      args=(self.loc.get_text(),))
        t.daemon = True
        t.start()
        t.join()

        splScr.destroy()

        GUI.GUI(self, Gtk, GdkPixbuf, Gdk, th)

    def on_apply_clicked(self, widget):

        if self.image_path is None:
            fn.show_in_app_notification(self,
                                        "You need to select an image first")
        else:
            self.btnset.set_sensitive(False)
            self.status.set_text("applying lockscreen....")
            t = th.Thread(target=self.set_lockscreen, args=())
            t.daemon = True
            t.start()

    def set_lockscreen(self):
        if len(self.res.get_text()) < 1:
            command = ["betterlockscreens", "-u", self.image_path]
        else:
            command = ["betterlockscreens", "-u", self.image_path,
                       "-r", self.res.get_text()]
        try:
            with fn.subprocess.Popen(command, bufsize=1, stdout=fn.subprocess.PIPE, universal_newlines=True) as p:
                for line in p.stdout:
                    GLib.idle_add(self.status.set_text, line.strip())
            # fn.subprocess.call(command, shell=False)
            fn.show_in_app_notification(self, "Lockscreen set successfully")
            GLib.idle_add(self.btnset.set_sensitive, True)
            GLib.idle_add(self.status.set_text, "")
        except:  # noqa
            GLib.idle_add(self.status.set_text, "ERROR: is betterlockscreen installed?")
            GLib.idle_add(self.btnset.set_sensitive, True)

    def on_item_clicked(self, widget, data):
        for x in data:
            self.image_path = x.get_name()
        # print(widget.get_selected_children())

    def on_load_clicked(self, widget, fb):
        # self.fb.select_all()

        # for x in self.fb.get_selected_children():
        #     print(x)
        #     self.fb.remove(x)
        self.create_flowbox(self.loc.get_text())
        # t = th.Thread(target=self.create_flowbox,
        #               args=(self.fb, self.loc.get_text(),))
        # t.daemon = True
        # t.start()
        # t.join()

    def create_flowbox(self, text):
        if len(text) < 1:
            paths = "/usr/share/backgrounds/hefftorlinux/"
            if not fn.os.path.isdir(paths):
                paths = "/usr/share/backgrounds/arcolinux/"
            if not fn.os.path.isdir(paths):
                return 0
        else:
            paths = text

        # try:
        images = [x for x in fn.os.listdir(paths)] # noqa

        for image in images:
            # fbchild = Gtk.FlowBoxChild()
            pb = GdkPixbuf.Pixbuf().new_from_file_at_size(paths + image, 128, 128) # noqa
            pimage = Gtk.Image()
            pimage.set_name(paths + image)
            pimage.set_from_pixbuf(pb)
            # print(image)
            # fbchild.add(pimage)
            self.fb.add(pimage)
        # except Exception as e:
        #     print(e)
            # print(image)

    def on_social_clicked(self, widget, event, link):
        t = th.Thread(target=self.weblink, args=(link,))
        t.daemon = True
        t.start()

    def weblink(self, link):
        webbrowser.open_new_tab(link)

    def tooltip_callback(self, widget, x, y, keyboard_mode, tooltip, text):
        tooltip.set_text(text)
        return True

    def MessageBox(self, title, message):
        md = Gtk.MessageDialog(parent=self, flags=0,
                               message_type=Gtk.MessageType.INFO,
                               buttons=Gtk.ButtonsType.OK, text=title)
        md.format_secondary_markup(message)
        md.run()
        md.destroy()


if __name__ == "__main__":
    w = Main()
    w.connect("delete-event", Gtk.main_quit)
    w.show_all()
    Gtk.main()
