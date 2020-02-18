# =================================================================
# =                  Author: Brad Heffernan                       =
# =================================================================

from Functions import base_dir, os


def GUI(self, Gtk, GdkPixbuf, Gdk, th):

    self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
    self.add(self.vbox)

    hbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox3 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

    # =======================================================
    #                       App Notifications
    # =======================================================

    self.notification_revealer = Gtk.Revealer()
    self.notification_revealer.set_reveal_child(False)

    self.notification_label = Gtk.Label()

    pb_panel = GdkPixbuf.Pixbuf().new_from_file(base_dir + '/images/panel.png')
    panel = Gtk.Image().new_from_pixbuf(pb_panel)

    overlayFrame = Gtk.Overlay()
    overlayFrame.add(panel)
    overlayFrame.add_overlay(self.notification_label)

    self.notification_revealer.add(overlayFrame)

    hbox1.pack_start(self.notification_revealer, True, False, 0)

    # ==========================================================
    #                       PATREON
    # ==========================================================
    self.fb = Gtk.FlowBox()
    scrolled = Gtk.ScrolledWindow()
    scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

    self.fb.set_valign(Gtk.Align.START)
    self.fb.set_max_children_per_line(6)
    self.fb.set_selection_mode(Gtk.SelectionMode.SINGLE)
    self.fb.connect("child-activated", self.on_item_clicked)
    # self.create_flowbox(fb)

    scrolled.add(self.fb)

    hbox3.pack_start(scrolled, True, True, 0)

    # ==========================================================
    #                       PATREON
    # ==========================================================

    pE2 = Gtk.EventBox()

    pbp2 = GdkPixbuf.Pixbuf().new_from_file_at_size(
        os.path.join(base_dir, 'images/patreon.png'), 28, 28)
    pimage2 = Gtk.Image().new_from_pixbuf(pbp2)

    pE2.add(pimage2)

    pE2.connect("button_press_event", self.on_social_clicked,
                "https://t.me/arcolinux_d_b")

    pE2.set_property("has-tooltip", True)

    pE2.connect("query-tooltip", self.tooltip_callback,
                "Support Brad on Patreon")

    hbox2.pack_start(pE2, False, False, 0)  # Patreon

    # ==========================================================
    #                       PACK TO WINDOW
    # ==========================================================

    self.vbox.pack_start(hbox1, False, False, 0)
    self.vbox.pack_start(hbox3, True, True, 0)
    self.vbox.pack_end(hbox2, False, False, 0)  # Patreon
