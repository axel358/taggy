#!/usr/bin/python3
import gi
import os

import taglib
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, Gdk


class Taggy():
    TAGS = ['TITLE', 'ARTIST', 'ALBUM', 'GENRE', 'TRACKNUMBER']
    MULTAGS = ['ARTIST', 'ALBUM', 'GENRE']

    def __init__(self):

        icon_theme = Gtk.IconTheme.get_default()
        icon_theme.append_search_path('./icons')

        css_provider = Gtk.CssProvider()
        css_provider.load_from_path('style.css')
        Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), css_provider,
                                                 Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        self.builder = Gtk.Builder()
        self.builder.add_from_file('window.ui')

        self.window = self.builder.get_object('main_window')
        self.window.set_icon_name("usub")
        self.window.set_position(Gtk.WindowPosition.CENTER)
        self.window.connect("destroy", Gtk.main_quit)

        self.song_listbox = self.builder.get_object('song_listbox')
        self.tags_listbox = self.builder.get_object('tags_listbox')

        self.builder.connect_signals(self)
        self.window.show_all()

    def open(self, button):
        dialog = Gtk.FileChooserDialog(title='Select songs', parent=self.window, action=Gtk.FileChooserAction.OPEN)
        dialog.set_select_multiple(True)
        f_filter = Gtk.FileFilter()
        f_filter.add_mime_type('audio/*')
        dialog.add_filter(f_filter)
        dialog.add_buttons("_Cancel", Gtk.ResponseType.CANCEL, "_Open", Gtk.ResponseType.ACCEPT)
        response = dialog.run()

        if response == Gtk.ResponseType.ACCEPT:
            self.songs = dialog.get_filenames()

            for child in self.song_listbox.get_children():
                self.song_listbox.remove(child)

            for song in self.songs:
                row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
                icon = Gtk.Image().new_from_icon_name('audio-x-generic-symbolic', Gtk.IconSize.BUTTON)
                icon.set_valign(Gtk.Align.CENTER)
                row.pack_start(icon, False, False, 0)
                row.set_spacing(6)
                row.set_margin_top(3)
                row.set_margin_bottom(3)
                row.set_margin_start(6)
                row.set_margin_end(6)
                row.pack_start(Gtk.Label(label=os.path.basename(song)), False, False, 0)
                self.song_listbox.add(row)
                self.song_listbox.show_all()

        dialog.destroy()
        self.builder.get_object('main_stack').set_visible_child_name('page1')

    def load_tags(self, box, row):

        if len(self.song_listbox.get_selected_rows()) < 2:

            song = taglib.File(self.songs[row.get_index()])

            for tag in self.TAGS:
                entry = self.builder.get_object(tag.lower() + '_entry')
                if tag in song.tags and len(song.tags[tag]) > 0:
                    entry.set_text(song.tags[tag][0])
                else:
                    entry.set_text('')
        else:
            rows = self.song_listbox.get_selected_rows()
            artist = ''

            for row in rows:
                song = taglib.File(self.songs[row.get_index()])

                for tag in self.MULTAGS:
                    entry = self.builder.get_object(tag.lower() + '_entry')
                    if tag in song.tags and len(song.tags[tag]) > 0:
                        entry.set_text(song.tags[tag][0])
                    else:
                        entry.set_text('')

    def save_tags(self, button):
        if len(self.song_listbox.get_selected_rows()) < 2:
            row = self.song_listbox.get_selected_row()
            song = taglib.File(self.songs[row.get_index()])

            for tag in self.TAGS:
                entry = self.builder.get_object(tag.lower() + '_entry')
                tag_value = entry.get_text()
                song.tags[tag] = tag_value

            song.save()
        else:
            rows = self.song_listbox.get_selected_rows()

            for row in rows:
                song = taglib.File(self.songs[row.get_index()])

                for tag in self.MULTAGS:
                    entry = self.builder.get_object(tag.lower() + '_entry')
                    tag_value = entry.get_text()
                    song.tags[tag] = tag_value

                song.save()


if __name__ == "__main__":
    Taggy()
    Gtk.main()
