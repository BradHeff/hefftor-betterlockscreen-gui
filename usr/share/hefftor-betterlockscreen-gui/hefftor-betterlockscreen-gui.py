#!/usr/bin/env python3

# =================================================================
# =                  Author: Brad Heffernan                       =
# =================================================================

import gi
import Functions as fn
import GUI
import threading as th
import webbrowser

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, Gdk # noqa


class Main(Gtk.Window):
    def __init__(self):
        super(Main, self).__init__(title="TWM Color Changer")
        self.set_border_width(10)
        self.set_default_size(700, 460)
        self.set_icon_from_file(fn.os.path.join(
            GUI.base_dir, 'images/hefftorlinux.svg'))
        self.set_position(Gtk.WindowPosition.CENTER)

        self.timeout_id = None

        GUI.GUI(self, Gtk, GdkPixbuf, Gdk, th)

        self.create_flowbox(self.fb)

        # t = th.Thread(target=self.create_flowbox, args=(self.fb,))
        # t.daemon = True
        # t.start()

    def on_item_clicked(self, widget, data):
        for x in data:
            print(x)
        # print(widget.get_selected_children())

    def create_flowbox(self, fb):
        # fb.clear()
        # for x in fb.get_child_at_index():
        #     print(x)
        images = [x for x in fn.os.listdir("/usr/share/backgrounds/hefftorlinux/")] # noqa

        for image in images:
            pb = GdkPixbuf.Pixbuf().new_from_file_at_size("/usr/share/backgrounds/hefftorlinux/" + image, 128, 128) # noqa
            pimage = Gtk.Image()
            pimage.set_from_pixbuf(pb)

            fb.add(pimage)
            print(image)

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
