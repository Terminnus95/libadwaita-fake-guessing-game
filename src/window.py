# window.py
#
# Copyright 2025 Terminnus
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk, Gio, Adw

@Gtk.Template(resource_path='/demo/terminnus/fakeguessinggame/window.ui')
class FakeGuessingGameWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'FakeGuessingGameWindow'

    number_entry = Gtk.Template.Child()
    master = Gtk.Template.Child()
    loading_page = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        ###########
        # ACTIONS #
        ###########
        self.create_action("guess", self.on_guess)

    ###################
    # ACTION FUNCIONS #
    ###################
    def on_guess(self, *args):
        """
        This funcion is the effect of presing the «guess» button on the
        first page, this will do the following:
        *Check if the string inputted only contains numbers
        if not, show a banner teling the user to ajust their input.
        *if the string just contains numbers, go over to the second page
        """

        guess = self.number_entry.get_text()

        #Try to convert the guess into a int to check if the guess is a pure integer
        try:
            int(guess)
            print("valid string")

            #If all is correct, move over to the next page
            self.master.push(self.loading_page)

        except Exception:
        #If not, show a banner warning the user [NOT CURRENTLY WORKING]
            print("invalid sring")
            banner = Adw.Banner(title="Invalid value",
            button_label="ok")
            banner.set_revealed(True)


        print(guess)

    def create_action(self, name, callback, shortcuts=None):
        """Add an application action.

        Args:
            name: the name of the action
            callback: the function to be called when the action is
            activated
            shortcuts: an optional list of accelerators
        """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)
