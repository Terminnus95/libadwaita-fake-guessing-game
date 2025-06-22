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
import time, random, threading

@Gtk.Template(resource_path='/demo/terminnus/fakeguessinggame/window.ui')
class FakeGuessingGameWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'FakeGuessingGameWindow'

    ###########
    # WIDGETS #
    ###########

	# Universal widgets
    master = Gtk.Template.Child()
    toast_overlay = Gtk.Template.Child()

    # Widgets from «input_page»
    input_page = Gtk.Template.Child()
    number_entry = Gtk.Template.Child()

    # Widgets from «loading_page»
    loading_page = Gtk.Template.Child()
    loading_message = Gtk.Template.Child()

    # Widgets from «finish_page»
    finish_page = Gtk.Template.Child()
    number_label = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        ###########
        # THREADS #
		###########

        #Inicialize «modify_loading_message()» on a separate thread
        modify_loading_message_thread = threading.Thread(target=self.modify_loading_message, daemon=True)
        modify_loading_message_thread.start()
        #Inicialize «change_loading_page_to_finish_page()» on a separate thread
        change_loading_page_thread = threading.Thread(target=self.change_loading_page_to_finish_page, daemon=True)
        change_loading_page_thread.start()

        ###########
        # ACTIONS #
        ###########

        self.create_action("guess", self.on_guess)

    ######################
    # LOADING PAGE LOGIC #
    ######################

    def modify_loading_message(self, *kwargs):
        """
        This piece of code will modify loading_message's label every 1-2 seconds
        to a string on «messages»
        """

        # This list contains all of the messages that the label could possibly get
        messages = ["Initiating Mind Reading Algorithm", "Analyzing Neural Patterns",
        "Decoding Cerebral Signals", "Identifying Neural Pathways",
        "Initiating Deep Scan", "Initiating Quantum Neural Inference",
        "Extracting Numeric Imprint", "Establishing a Secure Brainwave Connection",
        "Parsing Synaptic Data", "Tapping Into Short-term Memory", "Filtering Thoughts"]

        while True:
            #Just change the message if the current page is the «loading_page»
            if self.master.get_visible_page().get_tag() == "loading_page":
                print("changed!")
                self.loading_message.set_label(random.choice(messages))
                time.sleep(random.randint(2, 5)) #Wait some time before changing it again
            #Break the loop when the page becomes «finish_page»
            elif self.master.get_visible_page().get_tag() == "finish_page":
                break

    def change_loading_page_to_finish_page(self, *kwargs):
        """
        This function will change the page from «loading_page» to «finish_page»
        after 10-25 seconds after the page becomes «loading_page»
        """
        while True:
            if self.master.get_visible_page().get_tag() == "loading_page":
                time.sleep(random.randint(10, 25)) # Wait before changing
                print("change page!")
                self.master.push(self.finish_page) # Changing the page
                break

    ###################
    # ACTION FUNCIONS #
    ###################

    def on_guess(self, *args):
        """
        This funcion is the effect of presing the «guess» button on the
        first page, this will do the following:
            *Check if the string inputted only contains numbers
            if not, show a toast teling the user to ajust their input.
            *if the string just contains numbers, go over to the next page
        """

        guess = self.number_entry.get_text()

        try:
        	#Try to convert the guess into a int to check if the guess only contains numbers
            int(guess)

            print("valid string")

			#If it is an int, move over to the next page and make the text in «number_label» into «guess»
            self.master.push(self.loading_page)
            self.number_label.set_label(guess)

        except ValueError:
        	print("invalid sring")

        #If not, show a toast
        	toast = Adw.Toast(title="Only Numbers are Accepted", timeout=2)
        	self.toast_overlay.add_toast(toast)

        print(guess)

	########
	# MISC #
	########

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

