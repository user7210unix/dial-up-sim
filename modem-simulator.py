#!/usr/bin/env python3
import gi
import time
import subprocess
import random
from playsound import playsound

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, GdkPixbuf

class ModemSimulator(Gtk.Window):
    def __init__(self):
        super().__init__(title="IBM Internet Dial-Up")
        self.set_border_width(10)
        self.set_default_size(400, 300)

        vbox = Gtk.VBox(spacing=6)
        self.add(vbox)

        # Load IBM logo
        logo = GdkPixbuf.Pixbuf.new_from_file_at_scale("assets/logo.png", 50, 50, True)
        image = Gtk.Image.new_from_pixbuf(logo)
        vbox.pack_start(image, False, False, 0)

        self.label = Gtk.Label(label="IBM Internet Dial-Up")
        self.label.set_markup("<b>IBM Internet Dial-Up</b>")
        vbox.pack_start(self.label, False, False, 0)

        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        vbox.pack_start(grid, True, True, 0)

        phone_label = Gtk.Label(label="Dial-up Number:")
        phone_label.set_xalign(0)
        grid.attach(phone_label, 0, 0, 1, 1)

        self.phone_entry = Gtk.Entry()
        self.phone_entry.set_placeholder_text("e.g., 555-1234")
        grid.attach(self.phone_entry, 1, 0, 1, 1)

        user_label = Gtk.Label(label="Username:")
        user_label.set_xalign(0)
        grid.attach(user_label, 0, 1, 1, 1)

        self.user_entry = Gtk.Entry()
        self.user_entry.set_placeholder_text("e.g., johndoe")
        grid.attach(self.user_entry, 1, 1, 1, 1)

        pass_label = Gtk.Label(label="Password:")
        pass_label.set_xalign(0)
        grid.attach(pass_label, 0, 2, 1, 1)

        self.pass_entry = Gtk.Entry()
        self.pass_entry.set_visibility(False)
        self.pass_entry.set_placeholder_text("********")
        grid.attach(self.pass_entry, 1, 2, 1, 1)

        url_label = Gtk.Label(label="Website URL:")
        url_label.set_xalign(0)
        grid.attach(url_label, 0, 3, 1, 1)

        self.url_entry = Gtk.Entry()
        self.url_entry.set_placeholder_text("e.g., http://www.altavista.com")
        grid.attach(self.url_entry, 1, 3, 1, 1)

        self.button = Gtk.Button(label="Connect")
        self.button.set_sensitive(False)
        self.button.connect("clicked", self.on_connect_clicked)
        vbox.pack_start(self.button, False, False, 0)

        self.status_label = Gtk.Label(label="")
        vbox.pack_start(self.status_label, False, False, 0)

        self.phone_entry.connect("changed", self.on_entry_changed)
        self.user_entry.connect("changed", self.on_entry_changed)
        self.pass_entry.connect("changed", self.on_entry_changed)
        self.url_entry.connect("changed", self.on_entry_changed)

    def on_entry_changed(self, widget):
        phone_number = self.phone_entry.get_text().strip()
        username = self.user_entry.get_text().strip()
        password = self.pass_entry.get_text().strip()
        url = self.url_entry.get_text().strip()
        self.button.set_sensitive(bool(phone_number and username and password and url))

    def on_connect_clicked(self, widget):
        self.status_label.set_text("Dialing...")
        self.button.set_sensitive(False)
        GLib.timeout_add(1000, self.play_modem_sound)

    def play_modem_sound(self):
        playsound("assets/modem_sound.mp3")
        if random.random() < 0.2:  # 20% chance of failure
            self.status_label.set_text("Connection Failed. Redialing...")
            GLib.timeout_add(5000, self.on_connect_clicked, None)
        else:
            GLib.timeout_add(5000, self.authenticate)
        return False

    def authenticate(self):
        self.status_label.set_text("Authenticating...")
        GLib.timeout_add(random.randint(2000, 4000), self.establish_connection)
        return False

    def establish_connection(self):
        self.status_label.set_text("Establishing Connection...")
        GLib.timeout_add(random.randint(2000, 4000), self.finalize_connection)
        return False

    def finalize_connection(self):
        speed = random.choice(["14.4kbps", "28.8kbps", "33.6kbps", "56kbps"])
        self.status_label.set_text(f"Connection Speed: {speed}")
        GLib.timeout_add(2000, self.launch_browser)
        return False

    def launch_browser(self):
        url = self.url_entry.get_text().strip()
        self.status_label.set_text("Connected! Launching Dillo...")
        GLib.timeout_add(1000, self.show_welcome_message)
        subprocess.Popen(["dillo", url])
        return False

    def show_welcome_message(self):
        messages = [
            "Welcome to the Information Superhighway!",
            "Please be patient... This is dial-up!",
            "Now entering Cyberspace!",
            "Enjoy your slow browsing experience!"
        ]
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text=random.choice(messages)
        )
        dialog.run()
        dialog.destroy()
        return False

if __name__ == "__main__":
    win = ModemSimulator()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()

