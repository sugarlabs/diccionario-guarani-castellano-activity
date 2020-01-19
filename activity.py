# Copyright 2014 Richar Nunez - rnezferreira9@gmail.com
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf

from sugar3.activity import activity
from sugar3.graphics.toolbarbox import ToolbarBox
from sugar3.activity.widgets import ActivityButton
from sugar3.activity.widgets import TitleEntry
from sugar3.activity.widgets import StopButton
from sugar3.activity.widgets import ShareButton
from configparser import ConfigParser


class Hablando_Guarani(activity.Activity):

    def __init__(self, handle):
        activity.Activity.__init__(self, handle)

        # we do not have collaboration features
        # make the share option insensitive
        self.max_participants = 1

        # toolbar with the new toolbar redesign
        toolbar_box = ToolbarBox()

        activity_button = ActivityButton(self)
        toolbar_box.toolbar.insert(activity_button, 0)
        activity_button.show()

        title_entry = TitleEntry(self)
        toolbar_box.toolbar.insert(title_entry, -1)
        title_entry.show()

        share_button = ShareButton(self)
        toolbar_box.toolbar.insert(share_button, -1)
        share_button.show()

        separator = Gtk.SeparatorToolItem()
        separator.props.draw = False
        separator.set_expand(True)
        toolbar_box.toolbar.insert(separator, -1)
        separator.show()

        stop_button = StopButton(self)
        toolbar_box.toolbar.insert(stop_button, -1)
        stop_button.show()

        self.set_toolbar_box(toolbar_box)
        toolbar_box.show()

        # label with the text, make the string translatable
        win = Gtk.VBox()
        eb = Gtk.EventBox()
        eb.add(win)
        eb.modify_bg(Gtk.StateType.NORMAL, Gdk.Color.parse('White')[1])
        title = Gtk.Image()
        achehety = Gtk.Image()
        texto = Gtk.Entry()
        traducido = Gtk.TextView()
        traducido.set_editable(False)
        traducido.set_wrap_mode(Gtk.WrapMode.WORD)
        dic = Gtk.TextView()
        textbuffer = dic.get_buffer()
        dic.set_wrap_mode(Gtk.WrapMode.WORD)
        dic.set_editable(False)

        hbox3 = Gtk.HButtonBox()
        hbox3.set_layout(Gtk.ButtonBoxStyle.CENTER)

        parser = ConfigParser()
        parser.read('config.ini')
        bo1 = Gtk.Button(parser.get('dic', 'A'))
        bo1.modify_bg(Gtk.StateType.NORMAL, Gdk.Color.parse('#FCB947')[1])
        bo2 = Gtk.Button(parser.get('dic', 'E'))
        bo3 = Gtk.Button(parser.get('dic', 'I'))
        bo3.modify_bg(Gtk.StateType.NORMAL, Gdk.Color.parse('#FCB947')[1])
        bo4 = Gtk.Button(parser.get('dic', 'O'))
        bo5 = Gtk.Button(parser.get('dic', 'U'))
        bo5.modify_bg(Gtk.StateType.NORMAL, Gdk.Color.parse('#FCB947')[1])
        bo6 = Gtk.Button(parser.get('dic', 'Y'))
        bo7 = Gtk.Button(parser.get('dic', 'G'))
        bo7.modify_bg(Gtk.StateType.NORMAL, Gdk.Color.parse('#FCB947')[1])
        # connect
        pixbuf = GdkPixbuf.Pixbuf.new_from_file('images/logo.jpg')
        scaled_pixbuf = pixbuf.scale_simple(400, 100, GdkPixbuf.InterpType.BILINEAR)
        title.set_from_pixbuf(scaled_pixbuf)
        pixbuf = GdkPixbuf.Pixbuf.new_from_file('images/achegety.jpg')
        scaled_pixbuf = pixbuf.scale_simple(600, 200, GdkPixbuf.InterpType.BILINEAR)
        achehety.set_from_pixbuf(scaled_pixbuf)
        bo1.connect('clicked', self.__agregar__, texto, 'A')
        bo2.connect('clicked', self.__agregar__, texto, 'E')
        bo3.connect('clicked', self.__agregar__, texto, 'I')
        bo4.connect('clicked', self.__agregar__, texto, 'O')
        bo5.connect('clicked', self.__agregar__, texto, 'U')
        bo6.connect('clicked', self.__agregar__, texto, 'Y')
        bo7.connect('clicked', self.__agregar__, texto, 'G')
        # Cargando archivo .txt
        infile = open("lang/guarani/dic.txt", "r")
        if infile:
            string = infile.read()
            infile.close()
            textbuffer.set_text(string)

        hbox2 = Gtk.HBox()

        # Conexion de botones
        texto.connect("activate", self.traducir_cb, traducido)
        texto.connect("backspace", self.__backspace_cb, traducido)

        # creando scrolled
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_border_width(10)
        scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.ALWAYS)

        scrolled_window.add_with_viewport(dic)
        # Disenho de ventana
        self.set_canvas(eb)
        win.add(title)
        win.add(hbox3)
        hbox3.add(bo1)
        hbox3.add(bo2)
        hbox3.add(bo3)
        hbox3.add(bo4)
        hbox3.add(bo5)
        hbox3.add(bo6)
        hbox3.add(bo7)
        win.add(texto)
        win.add(traducido)
        win.add(hbox2)
        win.add(achehety)
        win.add(scrolled_window)

        eb.show_all()

    def __agregar__(self, bo1, texto=None, Data=None):
        parser = ConfigParser()
        parser.read('config.ini')
        texto.set_text(texto.get_text()+parser.get('dic', Data))

    def traducir_cb(self, texto, traducido=None):
        entry = texto.get_text()+' = '
        cargar = traducido.get_buffer()
        infile = "lang/guarani/dic.txt"
        with open(infile, 'r') as f:
            for line in f:
                if line.lstrip().startswith(entry.capitalize()):
                    line = line.lstrip(entry.capitalize())
                    line = line.rstrip()
                    cargar.set_text(line)
                    break

                if entry != line:
                    cargar.set_text('No se ha encontrado coincidencia')

    def __backspace_cb(self, texto, traducido=None):
        cargar = traducido.get_buffer()
        cargar.set_text('')
