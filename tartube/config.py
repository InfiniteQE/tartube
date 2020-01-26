#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2019-2020 A S Lewis
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.


"""Configuration window classes."""


# Import Gtk modules
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject, GdkPixbuf


# Import other modules
import os


# Import our modules
import __main__
import formats
import mainapp
import mainwin
import media
import utils


# Classes


class GenericConfigWin(Gtk.Window):

    """Generic Python class for windows in which the user can modify various
    settings.


    Inherited by two types of windows - 'preference windows' (in which changes
    are applied immediately), and 'edit window' (in which changes are stored
    temporarily, and only applied once the user has finished making changes.
    """


    # Standard class methods


#   def __init__():             # Provided by child object


    # Public class methods


    def setup(self):

        """Called by self.__init__().

        Sets up the config window when it opens.
        """

        # Set the default window size
        self.set_default_size(
            self.app_obj.config_win_width,
            self.app_obj.config_win_height,
        )

        # Set the window's Gtk icon list
        self.set_icon_list(self.app_obj.main_win_obj.win_pixbuf_list)

        # Set up main widgets
        self.setup_grid()
        self.setup_notebook()
        self.setup_button_strip()
        self.setup_gap()

        # Set up tabs
        self.setup_tabs()

        # Procedure complete
        self.show_all()

        # Inform the main window of this window's birth (so that Tartube
        #   doesn't allow a download/update/refresh operation to start until
        #   all configuration windows have closed)
        self.app_obj.main_win_obj.add_child_window(self)
        # Add a callback so we can inform the main window of this window's
        #   destruction
        self.connect('destroy', self.close)


    def setup_grid(self):

        """Called by self.setup().

        Sets up a Gtk.Grid, on which a notebook and a button strip will be
        placed. (Each of the notebook's tabs also has its own Gtk.Grid.)
        """

        self.grid = Gtk.Grid()
        self.add(self.grid)


    def setup_notebook(self):

        """Called by self.setup().

        Sets up a Gtk.Notebook, after which self.setup_tabs() is called to fill
        it with tabs.
        """

        self.notebook = Gtk.Notebook()
        self.grid.attach(self.notebook, 0, 1, 1, 1)
        self.notebook.set_border_width(self.spacing_size)


    def add_notebook_tab(self, name):

        """Called by various functions in the child edit/preference window.

        Adds a tab to the main Gtk.Notebook, creating a Gtk.Grid inside it, on
        which the calling function can more widgets.

        Args:

            name (string): The name of the tab

        Returns:

            The tab created (in the form of a Gtk.Box) and its Gtk.Grid.

        """

        tab = Gtk.Box()
        self.notebook.append_page(tab, Gtk.Label.new_with_mnemonic(name))
        tab.set_hexpand(True)
        tab.set_vexpand(True)
        tab.set_border_width(self.spacing_size)

        scrolled = Gtk.ScrolledWindow()
        tab.add(scrolled)
        scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_vexpand(True)

        grid = Gtk.Grid()
        scrolled.add_with_viewport(grid)
        grid.set_border_width(self.spacing_size)
        grid.set_column_spacing(self.spacing_size)
        grid.set_row_spacing(self.spacing_size)

        return tab, grid


#   def setup_button_strip():   # Provided by child object


    def setup_gap(self):

        """Called by self.setup().

        Adds an empty box beneath the button strip for aesthetic purposes.
        """

        hbox = Gtk.HBox()
        self.grid.attach(hbox, 0, 3, 1, 1)
        hbox.set_border_width(self.spacing_size)


    def close(self, also_self):

        """Called from callback in self.setup().

        Inform the main window that this window is closing.

        Args:

            also_self (an object inheriting from config.GenericConfigWin):
                another copy of self

        """

        self.app_obj.main_win_obj.del_child_window(self)


class GenericEditWin(GenericConfigWin):

    """Generic Python class for windows in which the user can modify various
    settings in a class object (such as a media.Video or an
    options.OptionsManager object).

    The modifications are stored temporarily, and only applied once the user
    has finished making changes.
    """


    # Standard class methods


#   def __init__():             # Provided by child object


    # Public class methods


#   def setup():                # Inherited from GenericConfigWin


#   def setup_grid():           # Inherited from GenericConfigWin


#   def setup_notebook():       # Inherited from GenericConfigWin


#   def add_notebook_tab():     # Inherited from GenericConfigWin


    def setup_button_strip(self):

        """Called by self.setup().

        Creates a strip of buttons at the bottom of the window. Any changes the
        user has made are applied by clicking the 'OK' or 'Apply' buttons, and
        cancelled by using the 'Reset' or 'Cancel' buttons.

        The window is closed by using the 'OK' and 'Cancel' buttons.

        If self.multi_button_flag is True, only the 'OK' button is created.
        """

        hbox = Gtk.HBox()
        self.grid.attach(hbox, 0, 2, 1, 1)

        if self.multi_button_flag:

            # 'Reset' button
            self.reset_button = Gtk.Button('Reset')
            hbox.pack_start(self.reset_button, False, False, self.spacing_size)
            self.reset_button.get_child().set_width_chars(10)
            self.reset_button.set_tooltip_text(
                'Reset changes without closing the window',
            );
            self.reset_button.connect('clicked', self.on_button_reset_clicked)

            # 'Apply' button
            self.apply_button = Gtk.Button('Apply')
            hbox.pack_start(self.apply_button, False, False, self.spacing_size)
            self.apply_button.get_child().set_width_chars(10)
            self.apply_button.set_tooltip_text(
                'Apply changes without closing the window',
            );
            self.apply_button.connect('clicked', self.on_button_apply_clicked)

        # 'OK' button
        self.ok_button = Gtk.Button('OK')
        hbox.pack_end(self.ok_button, False, False, self.spacing_size)
        self.ok_button.get_child().set_width_chars(10)
        self.ok_button.set_tooltip_text('Apply changes');
        self.ok_button.connect('clicked', self.on_button_ok_clicked)

        if self.multi_button_flag:

            # 'Cancel' button
            self.cancel_button = Gtk.Button('Cancel')
            hbox.pack_end(self.cancel_button, False, False, self.spacing_size)
            self.cancel_button.get_child().set_width_chars(10)
            self.cancel_button.set_tooltip_text('Cancel changes');
            self.cancel_button.connect(
                'clicked',
                self.on_button_cancel_clicked,
            )


#   def setup_gap():            # Inherited from GenericConfigWin


    # (Non-widget functions)


    def apply_changes(self):

        """Called by self.on_button_ok_clicked() and
        self.on_button_apply_clicked().

        Any changes the user has made are temporarily stored in self.edit_dict.
        Apply to those changes to the object being edited.
        """

        # Apply any changes the user has made
        for key in self.edit_dict.keys():
            setattr(self.edit_obj, self.edit_dict[key])

        # The changes can now be cleared
        self.edit_dict = {}


    def reset_with_new_edit_obj(self, new_edit_obj):

        """At the moment, only called by
        mainapp.TartubeApp.reset_options_manager().

        Resets the object whose values are being edited in this window, i.e.
        self.edit_obj, to the specified object.

        Then redraws the window itself, as if the user had clicked the 'Reset'
        button at the bottom of the window. This makes new_edit_obj's IVs
        visible in the edit window, without the need to destroy the old one and
        replace it with a new one.

        Args:

            new_edit_obj (class): The replacement edit object

        """

        self.edit_obj = new_edit_obj

        # The rest of this function is copied from
        #   self.on_button_reset_clicked()

        # Remove all existing tabs from the notebook
        number = self.notebook.get_n_pages()
        if number:

            for count in range(0, number):
                self.notebook.remove_page(0)

        # Empty self.edit_dict, destroying any changes the user has made
        self.edit_dict = {}

        # Re-draw all the tabs
        self.setup_tabs()

        # Render the changes
        self.show_all()


    def retrieve_val(self, name):

        """Can be called by anything.

        Any changes the user has made are temporarily stored in self.edit_dict.

        Each key corresponds to an attribute in the object being edited,
        self.edit_obj.

        If 'name' exists as a key in that dictionary, retrieve the
        corresponding value and return it. Otherwise, the user hasn't yet
        modified the value, so retrieve directly from the attribute in the
        object being edited.

        Args:

            name (string): The name of the attribute in the object being
                edited

        Returns:

            The original or modified value of that attribute.

        """

        if name in self.edit_dict:
            return self.edit_dict[name]
        else:
            return getattr(self.edit_obj, name)


    # (Add widgets)


    def add_checkbutton(self, grid, text, prop, x, y, wid, hei):

        """Called by various functions in the child edit window.

        Adds a Gtk.CheckButton to the tab's Gtk.Grid.

        Args:

            grid (Gtk.Grid): The grid on which this widget will be placed

            text (string or None): The text to display in the checkbutton's
                label. No label is used if 'text' is an empty string or None

            prop (string or None): The name of the attribute in self.edit_obj
                whose value will be set to the contents of this widget. If
                None, no changes are made to self.edit_dict; it's up to the
                calling function to provide a .connect()

            x, y, wid, hei (int): Position on the grid at which the widget is
                placed

        Returns:

            The checkbutton widget created

        """

        checkbutton = Gtk.CheckButton()
        grid.attach(checkbutton, x, y, wid, hei)
        checkbutton.set_hexpand(True)
        if text is not None and text != '':
            checkbutton.set_label(text)

        if prop is not None:
            checkbutton.set_active(self.retrieve_val(prop))
            checkbutton.connect('toggled', self.on_checkbutton_toggled, prop)

        return checkbutton


    def add_combo(self, grid, combo_list, prop, x, y, wid, hei):

        """Called by various functions in the child edit window.

        Adds a simple Gtk.ComboBox to the tab's Gtk.Grid.

        Args:

            grid (Gtk.Grid): The grid on which this widget will be placed

            combo_list (list): A list of values to display in the combobox.
                This function expects a simple, one-dimensional list. For
                something more complex, see self.add_combo_with_data()

            prop (string or None): The name of the attribute in self.edit_obj
                whose value will be set to the contents of this widget. If
                None, no changes are made to self.edit_dict; it's up to the
                calling function to provide a .connect()

            x, y, wid, hei (int): Position on the grid at which the widget is
                placed

        Returns:

            The combobox widget created

        """

        store = Gtk.ListStore(str)
        for string in combo_list:
            store.append( [string] )

        combo = Gtk.ComboBox.new_with_model(store)
        grid.attach(combo, x, y, wid, hei)
        renderer_text = Gtk.CellRendererText()
        combo.pack_start(renderer_text, True)
        combo.add_attribute(renderer_text, 'text', 0)
        combo.set_entry_text_column(0)

        if prop is not None:
            val = self.retrieve_val(prop)
            index = combo_list.index(val)
            combo.set_active(index)

            combo.connect('changed', self.on_combo_changed, prop)

        return combo


    def add_combo_with_data(self, grid, combo_list, prop, x, y, wid, hei):

        """Called by various functions in the child edit window.

        Adds a more complex Gtk.ComboBox to the tab's Gtk.Grid. This function
        expects a list of values in the form

            [ [val1, val2], [val1, val2], ... ]

        The combobox displays the 'val1' values. If one of them is selected,
        the corresponding 'val2' is used to set the attribute described by
        'prop'.

        Args:

            grid (Gtk.Grid): The grid on which this widget will be placed

            combo_list (list): The list described above. For something more
                simple, see self.add_combo()

            prop (string or None): The name of the attribute in self.edit_obj
                whose value will be set to the contents of this widget. If
                None, no changes are made to self.edit_dict; it's up to the
                calling function to provide a .connect()

            x, y, wid, hei (int): Position on the grid at which the widget is
                placed

        Returns:

            The combobox widget created

        """

        store = Gtk.ListStore(str, str)

        index_list = []
        for mini_list in combo_list:
            store.append( [ mini_list[0], mini_list[1] ] )
            index_list.append(mini_list[1])

        combo = Gtk.ComboBox.new_with_model(store)
        grid.attach(combo, x, y, wid, hei)
        renderer_text = Gtk.CellRendererText()
        combo.pack_start(renderer_text, True)
        combo.add_attribute(renderer_text, 'text', 0)
        combo.set_entry_text_column(0)

        if prop is not None:
            val = self.retrieve_val(prop)
            index = index_list.index(val)
            combo.set_active(index)

            combo.connect('changed', self.on_combo_with_data_changed, prop)

        return combo


    def add_entry(self, grid, prop, x, y, wid, hei):

        """Called by various functions in the child edit window.

        Adds a Gtk.Entry to the tab's Gtk.Grid.

        Args:

            grid (Gtk.Grid): The grid on which this widget will be placed

            prop (string or None): The name of the attribute in self.edit_obj
                whose value will be set to the contents of this widget. If
                None, no changes are made to self.edit_dict; it's up to the
                calling function to provide a .connect()

            x, y, wid, hei (int): Position on the grid at which the widget is
                placed

        Returns:

            The entry widget created

        """

        entry = Gtk.Entry()
        grid.attach(entry, x, y, wid, hei)
        entry.set_hexpand(True)

        if prop is not None:
            value = self.retrieve_val(prop)
            if value is not None:
                entry.set_text(str(value))

            entry.connect('changed', self.on_entry_changed, prop)

        return entry


    def add_image(self, grid, image_path, x, y, wid, hei):

        """Called by various functions in the child edit window.

        Adds a Gtk.Image to the tab's Gtk.Grid.

        Args:

            grid (Gtk.Grid): The grid on which this widget will be placed

            image_path (string): Full path to the image file to load

            x, y, wid, hei (int): Position on the grid at which the widget is
                placed

        Returns:

            The Gtk.Frame containing the image

        """

        frame = Gtk.Frame()
        grid.attach(frame, x, y, wid, hei)

        image = Gtk.Image()
        frame.add(image)
        image.set_from_pixbuf(
            self.app_obj.file_manager_obj.load_to_pixbuf(image_path),
        )

        return frame


    def add_pixbuf(self, grid, pixbuf_name, x, y, wid, hei):

        """Called by various functions in the child edit window.

        Adds a Gtk.Image to the tab's Gtk.Grid. A modified version of
        self.add_image(), which is called with a path to an image file; this
        function is called with one of the pixbuf names specified by
        mainwin.MainWin.pixbuf_dict, e.g. 'video_both_large'.

        Args:

            grid (Gtk.Grid): The grid on which this widget will be placed

            pixbuf_name (string): One of the keys in
                mainwin.MainWin.pixbuf_dict, e.g. 'video_both_large'.

            x, y, wid, hei (int): Position on the grid at which the widget is
                placed

        Returns:

            The Gtk.Frame containing the image

        """

        frame = Gtk.Frame()
        grid.attach(frame, x, y, wid, hei)

        image = Gtk.Image()
        frame.add(image)

        main_win_obj = self.app_obj.main_win_obj
        if pixbuf_name in main_win_obj.pixbuf_dict:
            image.set_from_pixbuf(main_win_obj.pixbuf_dict[pixbuf_name])
        else:
            # Unrecognised pixbuf name
            image.set_from_pixbuf(
                main_win_obj.pixbuf_dict['question_large'],
            )

        return frame


    def add_label(self, grid, text, x, y, wid, hei):

        """Called by various functions in the child edit window.

        Adds a Gtk.Label to the tab's Gtk.Grid.

        Args:

            grid (Gtk.Grid): The grid on which this widget will be placed

            text (string): Pango markup displayed in the label

            x, y, wid, hei (int): Position on the grid at which the widget is
                placed

        Returns:

            The label widget created

        """

        label = Gtk.Label()
        grid.attach(label, x, y, wid, hei)
        label.set_markup(text)
        label.set_hexpand(True)
        label.set_alignment(0, 0.5)

        return label


    def add_radiobutton(self, grid, prev_button, text, prop, value, x, y, \
    wid, hei):

        """Called by various functions in the child edit window.

        Adds a Gtk.RadioButton to the tab's Gtk.Grid.

        Args:

            grid (Gtk.Grid): The grid on which this widget will be placed

            prev_button (Gtk.RadioButton or None): When this is the first
                radio button in the group, None. Otherwise, the previous
                radio button in the group. Use of this IV links the radio
                buttons together, ensuring that only one of them can be active
                at any time

            text (string or None): The text to display in the radiobutton's
                label. No label is used if 'text' is an empty string or None

            prop (string or None): The name of the attribute in self.edit_obj
                whose value will be set to the contents of this widget. If
                None, no changes are made to self.edit_dict; it's up to the
                calling function to provide a .connect()

            value (any): When this radiobutton becomes the active one, and if
                'prop' is not None, then 'prop' and 'value' are added as a new
                key-value pair to self.edit_dict

            x, y, wid, hei (int): Position on the grid at which the widget is
                placed

        Returns:

            The radiobutton widget created

        """

        radiobutton = Gtk.RadioButton.new_from_widget(prev_button)
        grid.attach(radiobutton, x, y, wid, hei)
        radiobutton.set_hexpand(True)
        if text is not None and text != '':
            radiobutton.set_label(text)

        if prop is not None:
            if value is not None and self.retrieve_val(prop) == value:
                radiobutton.set_active(True)

            radiobutton.connect(
                'toggled',
                self.on_radiobutton_toggled, prop, value,
            )

        return radiobutton


    def add_spinbutton(self, grid, min_val, max_val, step, prop, x, y, wid, \
    hei):

        """Called by various functions in the child edit window.

        Adds a Gtk.SpinButton to the tab's Gtk.Grid.

        Args:

            grid (Gtk.Grid): The grid on which this widget will be placed

            min_val (int): The minimum permitted in the spinbutton

            max_val (int or None): The maximum values permitted in the
                spinbutton. If None, this function assigns a very large maximum
                value (a billion)

            step (int): Clicking the up/down arrows in the spin button
                increments/decrements the value by this much

            prop (string or None): The name of the attribute in self.edit_obj
                whose value will be set to the contents of this widget. If
                None, no changes are made to self.edit_dict; it's up to the
                calling function to provide a .connect()

            x, y, wid, hei (int): Position on the grid at which the widget is
                placed

        Returns:

            The spinbutton widget created

        """

        # If the specified value of 'max_valu' was none, just use a very big
        #   number (as Gtk.SpinButton won't accept the None argument)
        if max_val is None:
            max_val = 1000000000

        spinbutton = Gtk.SpinButton.new_with_range(min_val, max_val, step)
        grid.attach(spinbutton, x, y, wid, hei)
        spinbutton.set_hexpand(False)

        if prop is not None:
            spinbutton.set_value(self.retrieve_val(prop))
            spinbutton.connect(
                'value-changed',
                self.on_spinbutton_changed,
                prop,
            )

        return spinbutton


    def add_textview(self, grid, prop, x, y, wid, hei):

        """Called by various functions in the child edit window.

        Adds a Gtk.TextView to the tab's Gtk.Grid. The contents of the textview
        are used as a single string (perhaps including newline characters) to
        set the value of a string attribute.

        Args:

            grid (Gtk.Grid): The grid on which this widget will be placed

            prop (string or None): The name of the attribute in self.edit_obj
                whose value will be set to the contents of this widget. The
                attribute can be an integer, string, list or tuple. If None, no
                changes are made to self.edit_dict; it's up to the calling
                function to provide a .connect()

            x, y, wid, hei (int): Position on the grid at which the widget is
                placed

        Returns:

            The textview and textbuffer widgets created

        """

        scrolled = Gtk.ScrolledWindow()
        grid.attach(scrolled, x, y, wid, hei)
        scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_vexpand(True)

        frame = Gtk.Frame()
        scrolled.add_with_viewport(frame)

        textview = Gtk.TextView()
        frame.add(textview)

        textbuffer = textview.get_buffer()

        if prop is not None:
            value = self.retrieve_val(prop)
            if value is not None:
                if type(value) is list or type(value) is tuple:
                    textbuffer.set_text(str.join('\n', value))
                else:
                    textbuffer.set_text(str(value))

            textbuffer.connect('changed', self.on_textview_changed, prop)

        return textview, textbuffer


    def add_treeview(self, grid, x, y, wid, hei):

        """Called by various functions in the child edit window.

        Adds a Gtk.Treeview to the tab's Gtk.Grid. No callback function is
        created by this function; it's up to the calling code to supply one.

        Args:

            grid (Gtk.Grid): The grid on which this widget will be placed

            x, y, wid, hei (int): Position on the grid at which the widget is
                placed

        Returns:

            The treeview widget created

        """

        scrolled = Gtk.ScrolledWindow()
        grid.attach(scrolled, x, y, wid, hei)
        scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_vexpand(True)

        treeview = Gtk.TreeView()
        scrolled.add(treeview)
        treeview.set_headers_visible(False)

        renderer_text = Gtk.CellRendererText()
        column_text = Gtk.TreeViewColumn(
            '',
            renderer_text,
            text=0,
        )
        treeview.append_column(column_text)

        liststore = Gtk.ListStore(str)
        treeview.set_model(liststore)

        return treeview, liststore


    # Callback class methods


    def on_button_apply_clicked(self, button):

        """Called from a callback in self.setup_button_strip().

        Applies any changes made by the user and re-draws the window's tabs,
        showing their new values.

        Args:

            button (Gtk.Button): The widget clicked

        """

        # Apply any changes the user has made
        self.apply_changes()

        # Remove all existing tabs from the notebook
        number = self.notebook.get_n_pages()
        if number:

            for count in range(0, number):
                self.notebook.remove_page(0)

        # Re-draw all the tabs
        self.setup_tabs()

        # Render the changes
        self.show_all()


    def on_button_cancel_clicked(self, button):

        """Called from a callback in self.setup_button_strip().

        Destroys any changes made by the user and re-draws the window's tabs,
        showing their original values.

        Args:

            button (Gtk.Button): The widget clicked

        """

        # Destroy the window
        self.destroy()


    def on_button_ok_clicked(self, button):

        """Called from a callback in self.setup_button_strip().

        Destroys any changes made by the user and then closes the window.

        Args:

            button (Gtk.Button): The widget clicked

        """

        # Apply any changes the user has made
        self.apply_changes()

        # Destroy the window
        self.destroy()


    def on_button_reset_clicked(self, button):

        """Called from a callback in self.setup_button_strip().

        Destroys any changes made by the user and re-draws the window's tabs,
        showing their original values.

        Args:

            button (Gtk.Button): The widget clicked

        """

        # Remove all existing tabs from the notebook
        number = self.notebook.get_n_pages()
        if number:

            for count in range(0, number):
                self.notebook.remove_page(0)

        # Empty self.edit_dict, destroying any changes the user has made
        self.edit_dict = {}

        # Re-draw all the tabs
        self.setup_tabs()

        # Render the changes
        self.show_all()


    def on_checkbutton_toggled(self, checkbutton, prop):

        """Called from a callback in self.add_checkbutton().

        Adds a key-value pair to self.edit_dict, using True if the button is
        selected, False if not.

        Args:

            checkbutton (Gtk.CheckButton): The widget clicked

            prop (string): The attribute in self.edit_obj to modify

        """

        if not checkbutton.get_active():
            self.edit_dict[prop] = False
        else:
            self.edit_dict[prop] = True


    def on_combo_changed(self, combo, prop):

        """Called from a callback in self.add_combo().

        Temporarily stores the contents of the widget in self.edit_dict.

        Args:

            combo (Gtk.ComboBox): The widget clicked

            prop (string): The attribute in self.edit_obj to modify

        """

        tree_iter = combo.get_active_iter()
        model = combo.get_model()
        self.edit_dict[prop] = model[tree_iter][0]


    def on_combo_with_data_changed(self, combo, prop):

        """Called from a callback in self.add_combo_with-data().

        Extracts the value visible in the widget, converts it into another
        value, and stores the later in self.edit_dict.

        Args:

            combo (Gtk.ComboBox): The widget clicked

            prop (string): The attribute in self.edit_obj to modify

        """

        tree_iter = combo.get_active_iter()
        model = combo.get_model()
        self.edit_dict[prop] = model[tree_iter][1]


    def on_entry_changed(self, entry, prop):

        """Called from a callback in self.add_entry().

        Temporarily stores the contents of the widget in self.edit_dict.

        Args:

            entry (Gtk.Entry): The widget clicked

            prop (string): The attribute in self.edit_obj to modify

        """

        self.edit_dict[prop] = entry.get_text()


    def on_radiobutton_toggled(self, checkbutton, prop, value):

        """Called from a callback in self.add_radiobutton().

        Adds a key-value pair to self.edit_dict, but only if this radiobutton
        (from those in the group) is the selected one.

        Args:

            checkbutton (Gtk.CheckButton): The widget clicked

            prop (string): The attribute in self.edit_obj to modify

            value (-): The attribute's new value

        """

        if radiobutton.get_active():
            self.edit_dict[prop] = value


    def on_spinbutton_changed(self, spinbutton, prop):

        """Called from a callback in self.add_spinbutton().

        Temporarily stores the contents of the widget in self.edit_dict.

        Args:

            spinbutton (Gtk.SpinkButton): The widget clicked

            prop (string): The attribute in self.edit_obj to modify

        """

        self.edit_dict[prop] = int(spinbutton.get_value())


    def on_textview_changed(self, textbuffer, prop):

        """Called from a callback in self.add_textview().

        Temporarily stores the contents of the widget in self.edit_dict.

        Args:

            textbuffer (Gtk.TextBuffer): The widget modified

            prop (string): The attribute in self.edit_obj to modify

        """

        text = textbuffer.get_text(
            textbuffer.get_start_iter(),
            textbuffer.get_end_iter(),
            # Don't include hidden characters
            False,
        )

        old_value = self.retrieve_val(prop)

        if type(old_value) is list:
            self.edit_dict[prop] = text.split()
        elif type(old_value) is tuple:
            self.edit_dict[prop] = text.split()
        else:
             self.edit_dict[prop] = text


    # (Inherited by VideoEditWin, ChannelPlaylistEditWin and FolderEditWin)


    def add_container_properties(self, grid):

        """Called by VideoEditWin.setup_tabs(),
        ChannelPlaylistEditWin.setup_tabs() and FolderEditWin.setup_tabs().

        Adds widgets common to those edit windows.

        Args:

            grid (Gtk.Grid): The grid on which widgets are arranged in their
                tab

        """

        entry = self.add_entry(grid,
            None,
            0, 1, 1, 1,
        )
        entry.set_text('#' + str(self.edit_obj.dbid))
        entry.set_editable(False)
        entry.set_hexpand(False)
        entry.set_width_chars(8)

        main_win_obj = self.app_obj.main_win_obj
        if isinstance(self.edit_obj, media.Channel):
            icon_path = main_win_obj.icon_dict['channel_small']
        elif isinstance(self.edit_obj, media.Playlist):
            icon_path = main_win_obj.icon_dict['playlist_small']
        else:
            icon_path = main_win_obj.icon_dict['folder_small']

        frame = self.add_image(grid,
            icon_path,
            1, 1, 1, 1,
        )
        # (The frame looks cramped without this. The icon itself is 16x16)
        frame.set_size_request(
            16 + (self.spacing_size * 2),
            -1,
        )

        entry2 = self.add_entry(grid,
            'name',
            2, 1, 1, 1,
        )
        entry2.set_editable(False)

        label = self.add_label(grid,
            'Listed as',
            0, 2, 1, 1,
        )
        label.set_hexpand(False)

        entry3 = self.add_entry(grid,
            'nickname',
            2, 2, 1, 1,
        )
        entry3.set_editable(False)

        label2 = self.add_label(grid,
            'Contained in',
            0, 3, 1, 1,
        )
        label2.set_hexpand(False)

        parent_obj = self.edit_obj.parent_obj
        if parent_obj:
            if isinstance(parent_obj, media.Channel):
                icon_path2 = main_win_obj.icon_dict['channel_small']
            elif isinstance(parent_obj, media.Playlist):
                icon_path2 = main_win_obj.icon_dict['playlist_small']
            else:
                icon_path2 = main_win_obj.icon_dict['folder_small']
        else:
            icon_path2 = main_win_obj.icon_dict['folder_black_small']

        frame2 = self.add_image(grid,
            icon_path2,
            1, 3, 1, 1,
        )
        frame2.set_size_request(
            16 + (self.spacing_size * 2),
            -1,
        )

        entry4 = self.add_entry(grid,
            None,
            2, 3, 1, 1,
        )
        entry4.set_editable(False)
        if parent_obj:
            entry4.set_text(parent_obj.name)


    def add_source_properties(self, grid):

        """Called by VideoEditWin.setup_tabs() and
        ChannelPlaylistEditWin.setup_tabs().

        Adds widgets common to those edit windows.

        Args:

            grid (Gtk.Grid): The grid on which widgets are arranged in their
                tab

        """

        label2 = self.add_label(grid,
            utils.upper_case_first(self.media_type) + ' URL',
            0, 4, 1, 1,
        )
        label2.set_hexpand(False)

        entry5 = self.add_entry(grid,
            'source',
            1, 4, 2, 1,
        )
        entry5.set_editable(False)


    def add_destination_properties(self, grid):

        """Called by ChannelPlaylistEditWin.setup_tabs() and
        FolderEditWin.setup_tabs().

        Adds widgets common to those edit windows.

        Args:

            grid (Gtk.Grid): The grid on which widgets are arranged in their
                tab

        """

        # To avoid messing up the neat format of the rows above, add another
        #   grid, and put the next set of widgets inside it
        grid2 = Gtk.Grid()
        grid.attach(grid2, 0, 5, 3, 1)
        grid2.set_vexpand(False)
        grid2.set_column_spacing(self.spacing_size)
        grid2.set_row_spacing(self.spacing_size)

        label3 = self.add_label(grid2,
            'Videos downloaded to',
            0, 0, 1, 1,
        )
        label3.set_hexpand(False)

        main_win_obj = self.app_obj.main_win_obj
        dest_obj = self.app_obj.media_reg_dict[self.edit_obj.master_dbid]
        if isinstance(dest_obj, media.Channel):
            icon_path3 = main_win_obj.icon_dict['channel_small']
        elif isinstance(dest_obj, media.Playlist):
            icon_path3 = main_win_obj.icon_dict['playlist_small']
        else:
            icon_path3 = main_win_obj.icon_dict['folder_small']

        frame3 = self.add_image(grid2,
            icon_path3,
            1, 0, 1, 1,
        )
        frame3.set_size_request(
            16 + (self.spacing_size * 2),
            -1,
        )

        entry6 = self.add_entry(grid2,
            None,
            2, 0, 1, 1,
        )
        entry6.set_editable(False)
        entry6.set_text(dest_obj.name)

        label5 = self.add_label(grid2,
            'Location on filesystem',
            0, 1, 1, 1,
        )
        label5.set_hexpand(False)

        entry7 = self.add_entry(grid2,
            None,
            1, 1, 2, 1,
        )
        entry7.set_editable(False)
        entry7.set_text(self.edit_obj.get_dir(self.app_obj))


    def setup_download_options_tab(self):

        """Called by self.setup_tabs().

        Sets up the 'General' tab.
        """

        tab, grid = self.add_notebook_tab('_Download options')

        # Download options
        self.add_label(grid,
            '<u>Download options</u>',
            0, 0, 2, 1,
        )

        self.apply_options_button = Gtk.Button('Apply download options')
        grid.attach(self.apply_options_button, 0, 1, 1, 1)
        self.apply_options_button.connect(
            'clicked',
            self.on_button_apply_clicked,
        )

        self.edit_button = Gtk.Button('Edit download options')
        grid.attach(self.edit_button, 1, 1, 1, 1)
        self.edit_button.connect('clicked', self.on_button_edit_clicked)

        self.remove_button = Gtk.Button('Remove download options')
        grid.attach(self.remove_button, 1, 2, 1, 1)
        self.remove_button.connect('clicked', self.on_button_remove_clicked)

        if self.edit_obj.options_obj:
            self.apply_options_button.set_sensitive(False)
        else:
            self.edit_button.set_sensitive(False)
            self.remove_button.set_sensitive(False)


    def on_button_apply_clicked(self, button):

        """Called from callback in self.setup_general_tab().

        Apply download options to the media data object.

        Args:

            button (Gtk.Button): The widget clicked

        """

        if self.edit_obj.options_obj:
            return self.app_obj.system_error(
                401,
                'Download options already applied',
            )

        # Apply download options to the media data object
        self.app_obj.apply_download_options(self.edit_obj)
        # (De)sensitise buttons appropriately
        self.apply_options_button.set_sensitive(False)
        self.edit_options_button.set_sensitive(True)
        self.remove_options_button.set_sensitive(True)


    def on_button_edit_clicked(self, button):

        """Called from callback in self.setup_general_tab().

        Edit download options for the media data object.

        Args:

            button (Gtk.Button): The widget clicked

        """

        if not self.edit_obj.options_obj:
            return self.app_obj.system_error(
                402,
                'Download options not already applied',
            )

        # Open an edit window to show the options immediately
        OptionsEditWin(
            self.app_obj,
            self.edit_obj.options_obj,
            self.edit_obj,
        )


    def on_button_remove_clicked(self, button):

        """Called from callback in self.setup_general_tab().

        Remove download options from the media data object.

        Args:

            button (Gtk.Button): The widget clicked

        """

        if not self.edit_obj.options_obj:
            return self.app_obj.system_error(
                403,
                'Download options not already applied',
            )

        # Remove download options from the media data object
        self.app_obj.remove_download_options(self.edit_obj)
        # (De)sensitise buttons appropriately
        self.apply_options_button.set_sensitive(True)
        self.edit_options_button.set_sensitive(False)
        self.remove_options_button.set_sensitive(False)


class GenericPrefWin(GenericConfigWin):

    """Generic Python class for windows in which the user can modify various
    system settings.

    Any modifications are applied immediately (unlike in an 'edit window', in
    which the modifications are stored temporarily, and only applied once the
    user has finished making changes).
    """


    # Standard class methods


#   def __init__():             # Provided by child object


    # Public class methods


#   def setup():                # Inherited from GenericConfigWin


#   def setup_grid():           # Inherited from GenericConfigWin


#   def setup_notebook():       # Inherited from GenericConfigWin


#   def add_notebook_tab():     # Inherited from GenericConfigWin


    def setup_button_strip(self):

        """Called by self.setup().

        Creates a strip of buttons at the bottom of the window. For preference
        windows, there is only a single 'OK' button, which closes the window.
        """

        hbox = Gtk.HBox()
        self.grid.attach(hbox, 0, 2, 1, 1)

        # 'OK' button
        self.ok_button = Gtk.Button('OK')
        hbox.pack_end(self.ok_button, False, False, self.spacing_size)
        self.ok_button.get_child().set_width_chars(10)
        self.ok_button.set_tooltip_text('Close this window');
        self.ok_button.connect('clicked', self.on_button_ok_clicked)


#   def setup_gap():            # Inherited from GenericConfigWin


    # (Non-widget functions)


    def reset_window(self):

        """At the moment, only called by mainapp.TartubeApp.switch_db().

        Redraws the window, without the need to destroy the old one and replace
        it with a new one.
        """

        # This code is copied from
        #   config.GenericEditWin.on_button_reset_clicked()

        # Remove all existing tabs from the notebook
        number = self.notebook.get_n_pages()
        if number:

            for count in range(0, number):
                self.notebook.remove_page(0)

        # Re-draw all the tabs
        self.setup_tabs()

        # Render the changes
        self.show_all()


    # (Add widgets)


    def add_checkbutton(self, grid, text, set_flag, mod_flag, x, y, wid, hei):

        """Called by various functions in the child edit window.

        Adds a Gtk.CheckButton to the tab's Gtk.Grid.

        Args:

            grid (Gtk.Grid): The grid on which this widget will be placed

            text (string or None): The text to display in the checkbutton's
                label. No label is used if 'text' is an empty string or None

            set_flag (True or False): True if the checkbutton is selected

            mod_flag (True of False): True if the checkbutton can be toggled
                by the user

            x, y, wid, hei (int): Position on the grid at which the widget is
                placed

        Returns:

            The checkbutton widget created

        """

        checkbutton = Gtk.CheckButton()
        grid.attach(checkbutton, x, y, wid, hei)
        checkbutton.set_active(set_flag)
        checkbutton.set_sensitive(mod_flag)
        checkbutton.set_hexpand(True)
        if text is not None and text != '':
            checkbutton.set_label(text)

        return checkbutton


    def add_combo(self, grid, combo_list, active_val, x, y, wid, hei):

        """Called by various functions in the child edit window.

        Adds a simple Gtk.ComboBox to the tab's Gtk.Grid.

        Args:

            grid (Gtk.Grid): The grid on which this widget will be placed

            combo_list (list): A list of values to display in the combobox.
                This function expects a simple, one-dimensional list. There is
                not generic self.add_combo_with_data() function for preference
                windows.

            active_val (string or None): If not None, a value matching one of
                the items in combo_list, that should be the active row in the
                combobox

            x, y, wid, hei (int): Position on the grid at which the widget is
                placed

        Returns:

            The combobox widget created

        """

        store = Gtk.ListStore(str)

        count = -1
        active_index = 0
        for string in combo_list:
            store.append( [string] )

            count += 1
            if active_val is not None and active_val == string:
                active_index = count

        combo = Gtk.ComboBox.new_with_model(store)
        grid.attach(combo, x, y, wid, hei)
        renderer_text = Gtk.CellRendererText()
        combo.pack_start(renderer_text, True)
        combo.add_attribute(renderer_text, 'text', 0)
        combo.set_entry_text_column(0)
        combo.set_active(active_index)

        return combo


    def add_entry(self, grid, text, edit_flag, x, y, wid, hei):

        """Called by various functions in the child edit window.

        Adds a Gtk.Entry to the tab's Gtk.Grid.

        Args:

            grid (Gtk.Grid): The grid on which this widget will be placed

            text (string or None): The initial contents of the entry.

            edit_flag (True or False): True if the contents of the entry can be
                edited

            x, y, wid, hei (int): Position on the grid at which the widget is
                placed

        Returns:

            The entry widget created

        """

        entry = Gtk.Entry()
        grid.attach(entry, x, y, wid, hei)
        entry.set_hexpand(True)

        if text is not None:
            entry.set_text(str(text))

        if not edit_flag:
            entry.set_editable(False)

        return entry


    def add_label(self, grid, text, x, y, wid, hei):

        """Called by various functions in the child edit window.

        Adds a Gtk.Label to the tab's Gtk.Grid.

        Args:

            grid (Gtk.Grid): The grid on which this widget will be placed

            text (string): Pango markup displayed in the label

            x, y, wid, hei (int): Position on the grid at which the widget is
                placed

        Returns:

            The label widget created

        """

        label = Gtk.Label()
        grid.attach(label, x, y, wid, hei)
        label.set_markup(text)
        label.set_hexpand(True)
        label.set_alignment(0, 0.5)

        return label


    def add_radiobutton(self, grid, prev_button, text, x, y, wid, hei):

        """Called by various functions in the child edit window.

        Adds a Gtk.RadioButton to the tab's Gtk.Grid.

        Args:

            grid (Gtk.Grid): The grid on which this widget will be placed

            prev_button (Gtk.RadioButton or None): When this is the first
                radio button in the group, None. Otherwise, the previous
                radio button in the group. Use of this IV links the radio
                buttons together, ensuring that only one of them can be active
                at any time

            text (string or None): The text to display in the radiobutton's
                label. No label is used if 'text' is an empty string or None

            x, y, wid, hei (int): Position on the grid at which the widget is
                placed

        Returns:

            The radiobutton widget created

        """

        radiobutton = Gtk.RadioButton.new_from_widget(prev_button)
        grid.attach(radiobutton, x, y, wid, hei)
        radiobutton.set_hexpand(True)
        if text is not None and text != '':
            radiobutton.set_label(text)

        return radiobutton


    def add_spinbutton(self, grid, min_val, max_val, step, val, x, y, wid, \
    hei):

        """Called by various functions in the child edit window.

        Adds a Gtk.SpinButton to the tab's Gtk.Grid.

        Args:

            grid (Gtk.Grid): The grid on which this widget will be placed

            min_val (int): The minimum permitted in the spinbutton

            max_val (int or None): The maximum values permitted in the
                spinbutton. If None, this function assigns a very large maximum
                value (a billion)

            step (int): Clicking the up/down arrows in the spin button
                increments/decrements the value by this much

            value (int): The current value of the spinbutton

            x, y, wid, hei (int): Position on the grid at which the widget is
                placed

        Returns:

            The spinbutton widget created

        """

        # If the specified value of 'max_valu' was none, just use a very big
        #   number (as Gtk.SpinButton won't accept the None argument)
        if max_val is None:
            max_val = 1000000000

        spinbutton = Gtk.SpinButton.new_with_range(min_val, max_val, step)
        grid.attach(spinbutton, x, y, wid, hei)
        spinbutton.set_value(val)
        spinbutton.set_hexpand(False)

        return spinbutton


    # Callback class methods


    def on_button_ok_clicked(self, button):

        """Called from a callback in self.setup_button_strip().

        Closes the window.

        Args:

            button (Gtk.Button): The button clicked

        """

        # Destroy the window
        self.destroy()


class OptionsEditWin(GenericEditWin):

    """Python class for an 'edit window' to modify values in an
    options.OptionsManager object.

    Args:

        app_obj (mainapp.TartubeApp): The main application object

        edit_obj (options.OptionsManager): The object whose attributes will be
            edited in this window

        media_data_obj (media.Video, media.Channel, media.Playlist,
            media.Folder or None): The media data object which is the parent of
            the object being edited. None if we're editing the General Options
            Manager

    """


    # Standard class methods


    def __init__(self, app_obj, edit_obj, media_data_obj=None):

        Gtk.Window.__init__(self, title='Download options')

        # IV list - class objects
        # -----------------------
        # The mainapp.TartubeApp object
        self.app_obj = app_obj
        # The options.OptionManager object being edited
        self.edit_obj = edit_obj
        # The media data object which is the parent of the options manager
        #   object. Set to None if we are editing the General Options Manager
        self.media_data_obj = media_data_obj


        # IV list - Gtk widgets
        # ---------------------
        self.grid = None                        # Gtk.Grid
        self.notebook = None                    # Gtk.Notebook
        self.reset_button = None                # Gtk.Button
        self.apply_button = None                # Gtk.Button
        self.ok_button = None                   # Gtk.Button
        self.cancel_button = None               # Gtk.Button


        # IV list - other
        # ---------------
        # Size (in pixels) of gaps between edit window widgets
        self.spacing_size = self.app_obj.default_spacing_size
        # Flag set to True if all four buttons ('Reset', 'Apply', 'Cancel' and
        #   'OK' are required, or False if just the 'OK' button is required
        self.multi_button_flag = True

        # When the user changes a value, it is not applied to self.edit_obj
        #   immediately; instead, it is stored temporarily in this dictionary
        # If the user clicks the 'OK' or 'Apply' buttons at the bottom of the
        #   window, the changes are applied to self.edit_obj
        # If the user clicks the 'Reset' or 'Cancel' buttons, the dictionary
        #   is emptied and the changes are lost
        # In this edit window, the key-value pairs directly correspond to those
        #   in options.OptionsManager.options_dict, rather than corresponding
        #   directly to attributes in the options.OptionsManager object
        # Because of that, we use our own .apply_changes() and .retrieve_val()
        #   functions, rather than relying on the generic functions
        # Key-value pairs are added to this dictionary whenever the user
        #   makes a change (so if no changes are made when the window is
        #   closed, the dictionary will still be empty)
        self.edit_dict = {}

        # IVs used to keep track of widget changes in the 'Files' tab
        # Flag set to to False when that tab's output template widgets are
        #   desensitised, True when sensitised
        self.template_flag = False
        # A list of Gtk widgets to (de)sensitise in when the flag changes
        self.template_widget_list = []

        # IVs used to change label text consistently in the 'Formats' tab
        self.video_only_text = 'Available video formats'
        self.video_audio_text = 'Available video/audio formats'

        # Code
        # ----

        # Set up the edit window
        self.setup()


    # Public class methods


#   def setup():                # Inherited from GenericConfigWin


#   def setup_grid():           # Inherited from GenericConfigWin


#   def setup_notebook():       # Inherited from GenericConfigWin


#   def add_notebook_tab():     # Inherited from GenericConfigWin


#   def setup_button_strip():   # Inherited from GenericEditWin


#   def setup_gap():            # Inherited from GenericConfigWin


    # (Non-widget functions)


    def apply_changes(self):

        """Called by self.on_button_ok_clicked() and
        self.on_button_apply_clicked().

        Any changes the user has made are temporarily stored in self.edit_dict.
        Apply to those changes to the object being edited.

        In this edit window we apply changes to self.edit_obj.options_dict
        (rather than to self.edit_obj's attributes directly, as in the generic
        function.)
        """

        # Apply any changes the user has made
        for key in self.edit_dict.keys():
            self.edit_obj.options_dict[key] = self.edit_dict[key]

        # The changes can now be cleared
        self.edit_dict = {}


    def retrieve_val(self, name):

        """Can be called by anything.

        Any changes the user has made are temporarily stored in self.edit_dict.

        In the generic function, each key corresponds to an attribute in the
        object being edited, self.edit_obj. In this window, it corresponds to a
        key in self.edit_obj.options_dict.

        If 'name' exists as a key in that dictionary, retrieve the
        corresponding value and return it. Otherwise, the user hasn't yet
        modified the value, so retrieve directly from the attribute in the
        object being edited.

        Args:

            name (string): The name of the attribute in the object being
                edited

        Returns:

            The original or modified value of that attribute.

        """

        if name in self.edit_dict:
            return self.edit_dict[name]
        elif name in self.edit_obj.options_dict:
            return self.edit_obj.options_dict[name]
        else:
            return self.app_obj.system_error(
                404,
                'Unrecognised property name \'' + name + '\'',
            )


    # (Setup tabs)


    def setup_tabs(self):

        """Called by self.setup(), .on_button_apply_clicked() and
        .on_button_reset_clicked().

        Sets up the tabs for this edit window.
        """

        self.setup_general_tab()
        self.setup_files_tab()
        self.setup_formats_tab()
        self.setup_downloads_tab()
        if not self.app_obj.simple_options_flag:
            self.setup_post_process_tab()
        self.setup_subtitles_tab()
        self.setup_others_tab()
        if not self.app_obj.simple_options_flag:
            self.setup_advanced_tab()
        else:
            self.setup_sound_only_tab()


    def setup_general_tab(self):

        """Called by self.setup_tabs().

        Sets up the 'General' tab.
        """

        tab, grid = self.add_notebook_tab('_General')

        if self.media_data_obj:
            if isinstance(self.media_data_obj, media.Video):
                parent_type = 'video'
            elif isinstance(self.media_data_obj, media.Channel):
                parent_type = 'channel'
            elif isinstance(self.media_data_obj, media.Playlist):
                parent_type = 'playlist'
            else:
                parent_type = 'folder'

        self.add_label(grid,
            '<u>General options</u>',
            0, 0, 2, 1,
        )

        label = self.add_label(grid,
            '',
            0, 1, 2, 1,
        )

        if self.media_data_obj is None:

            label.set_text('These options have been applied to:')

            entry = self.add_entry(grid,
                None,
                0, 2, 2, 1,
            )
            entry.set_text('All channels, playlists and folders')

        else:

            label.set_text(
                'These options have been applied to the ' + parent_type + ':',
            )

            entry = self.add_entry(grid,
                None,
                0, 2, 1, 1,
            )
            entry.set_editable(False)
            entry.set_hexpand(False)
            entry.set_width_chars(8)

            entry2 = self.add_entry(grid,
                None,
                1, 2, 1, 1,
            )
            entry2.set_editable(False)

            entry.set_text('#' + str(self.media_data_obj.dbid))
            entry2.set_text(self.media_data_obj.name)

        self.add_label(grid,
            'Extra youtube-dl command line options (e.g. --help; do not use' \
            + ' -o or --output)',
            0, 3, 2, 1,
        )

        self.add_textview(grid,
            'extra_cmd_string',
            0, 4, 2, 1,
        )

        if self.app_obj.simple_options_flag:
            frame = self.add_pixbuf(grid,
                'hand_right_large',
                0, 5, 1, 1,
            )
            frame.set_hexpand(False)

        else:
            frame = self.add_pixbuf(grid,
                'hand_left_large',
                0, 5, 1, 1,
            )
            frame.set_hexpand(False)

        button = Gtk.Button()
        grid.attach(button, 1, 5, 1, 1)
        if not self.app_obj.simple_options_flag:
            button.set_label('Hide advanced download options')
        else:
            button.set_label('Show advanced download options')
        button.connect('clicked', self.on_simple_options_clicked)

        frame2 = self.add_pixbuf(grid,
            'copy_large',
            0, 6, 1, 1,
        )
        frame2.set_hexpand(False)

        button2 = Gtk.Button(
            'Import general download options into this window',
        )
        grid.attach(button2, 1, 6, 1, 1)
        button2.connect('clicked', self.on_clone_options_clicked)
        if self.edit_obj == self.app_obj.general_options_obj:
            # No point cloning the General Options Manager onto itself
            button2.set_sensitive(False)

        frame3 = self.add_pixbuf(grid,
            'warning_large',
            0, 7, 1, 1,
        )
        frame3.set_hexpand(False)

        button3 = Gtk.Button(
            'Completely reset all download options to their default values',
        )
        grid.attach(button3, 1, 7, 1, 1)
        button3.connect('clicked', self.on_reset_options_clicked)


    def setup_files_tab(self):

        """Called by self.setup_tabs().

        Sets up the 'Files' tab.
        """

        tab, grid = self.add_notebook_tab('_Files')
        grid_width = 5

        # File output options
        self.add_label(grid,
            '<u>File output options</u>',
            0, 0, grid_width, 1,
        )

        self.add_label(grid,
            'Format for video file names',
            0, 1, grid_width, 1,
        )

        store = Gtk.ListStore(int, str)
        num_list = [0, 1, 2, 4, 5, 3]
        for num in num_list:
            store.append( [num, formats.FILE_OUTPUT_NAME_DICT[num]] )

        current_format = self.edit_obj.options_dict['output_format']
        current_template = formats.FILE_OUTPUT_CONVERT_DICT[current_format]
        if current_template is None:
            current_template = self.edit_obj.options_dict['output_template']

        combo = Gtk.ComboBox.new_with_model(store)
        grid.attach(combo, 0, 2, grid_width, 1)
        renderer_text = Gtk.CellRendererText()
        combo.pack_start(renderer_text, True)
        combo.add_attribute(renderer_text, "text", 1)
        combo.set_entry_text_column(1)
        combo.set_active(num_list.index(current_format))
        # Signal connect appears below

        self.add_label(grid,
            'youtube-dl file output template',
            0, 3, grid_width, 1,
        )

        entry = self.add_entry(grid,
            None,
            0, 4, grid_width, 1,
        )
        entry.set_text(current_template)
        # Signal connect appears below

        self.add_label(grid,
            'Add to template:',
            0, 5, 1, 1,
        )

        store2 = Gtk.ListStore(str)
        for string in (
            'ID',
            'Title',
            'Ext',
            'Uploader',
            'Resolution',
            'Autonumber',
        ):
            store2.append( [string] )

        combo2 = Gtk.ComboBox.new_with_model(store2)
        grid.attach(combo2, 1, 5, 1, 1)
        renderer_text2 = Gtk.CellRendererText()
        combo2.pack_start(renderer_text2, True)
        combo2.add_attribute(renderer_text2, "text", 0)
        combo2.set_entry_text_column(0)
        combo2.set_active(0)

        button2 = Gtk.Button('Add')
        grid.attach(button2, 2, 5, 1, 1)
        # Signal connect appears below

        store3 = Gtk.ListStore(str)
        for string in (
            'View Count',
            'Like Count',
            'Dislike Count',
            'Comment Count',
            'Average Rating',
            'Age Limit',
            'Width',
            'Height',
            'Extractor',
        ):
            store3.append( [string] )

        combo3 = Gtk.ComboBox.new_with_model(store3)
        grid.attach(combo3, 3, 5, 1, 1)
        renderer_text3 = Gtk.CellRendererText()
        combo3.pack_start(renderer_text3, True)
        combo3.add_attribute(renderer_text3, "text", 0)
        combo3.set_entry_text_column(0)
        combo3.set_active(0)

        button3 = Gtk.Button('Add')
        grid.attach(button3, 4, 5, 1, 1)
        # Signal connect appears below

        store4 = Gtk.ListStore(str)
        for string in (
            'View Count',
            'Like Count',
            'Dislike Count',
            'Comment Count',
            'Average Rating',
            'Age Limit',
            'Width',
            'Height',
            'Extractor',
        ):
            store4.append( [string] )

        combo4 = Gtk.ComboBox.new_with_model(store4)
        grid.attach(combo4, 1, 6, 1, 1)
        renderer_text4 = Gtk.CellRendererText()
        combo4.pack_start(renderer_text4, True)
        combo4.add_attribute(renderer_text4, "text", 0)
        combo4.set_entry_text_column(0)
        combo4.set_active(0)

        button4 = Gtk.Button('Add')
        grid.attach(button4, 2, 6, 1, 1)
        # Signal connect appears below

        # Signal connects from above
        combo.connect('changed', self.on_file_tab_combo_changed, entry)
        entry.connect('changed', self.on_file_tab_entry_changed)
        button2.connect(
            'clicked',
            self.on_file_tab_button_clicked,
            entry,
            combo2,
        )
        button3.connect(
            'clicked',
            self.on_file_tab_button_clicked,
            entry,
            combo3,
        )
        button4.connect(
            'clicked',
            self.on_file_tab_button_clicked,
            entry,
            combo4,
        )

        # Add widgets to a list, so we can sensitise them when a custom
        #   template is selected, and desensitise them the rest of the time
        self.template_widget_list = [
            entry,
            combo2,
            combo3,
            combo4,
            button2,
            button3,
            button4,
        ]

        if current_format == 3:
            self.file_tab_sensitise_widgets(True)
        else:
            self.file_tab_sensitise_widgets(False)

        # Filesystem options
        if not self.app_obj.simple_options_flag:

            self.add_label(grid,
                '<u>Filesystem options</u>',
                0, 7, grid_width, 1,
            )

            self.add_checkbutton(grid,
                'Restrict filenames to using ASCII characters',
                'restrict_filenames',
                0, 8, grid_width, 1,
            )

            self.add_checkbutton(grid,
                'Set the file modification time from the server',
                'nomtime',
                0, 9, grid_width, 1,
            )

        # Filesystem overrides
        self.add_label(grid,
            '<u>Filesystem overrides</u>',
            0, 10, grid_width, 1,
        )

        checkbutton = self.add_checkbutton(grid,
            'Download all videos into this folder',
            None,
            0, 11, 2, 1,
        )
        # Signal connect below

        # (Currently, only two fixed folders are elligible for this mode, so
        #   we'll just add them individually)
        store5 = Gtk.ListStore(GdkPixbuf.Pixbuf, str)
        pixbuf = self.app_obj.main_win_obj.pixbuf_dict['folder_green_small']
        store5.append( [pixbuf, self.app_obj.fixed_misc_folder.name] )
        pixbuf = self.app_obj.main_win_obj.pixbuf_dict['folder_blue_small']
        store5.append( [pixbuf, self.app_obj.fixed_temp_folder.name] )

        combo5 = Gtk.ComboBox.new_with_model(store5)
        grid.attach(combo5, 2, 11, (grid_width - 2), 1)
        renderer_pixbuf5 = Gtk.CellRendererPixbuf()
        combo5.pack_start(renderer_pixbuf5, False)
        combo5.add_attribute(renderer_pixbuf5, 'pixbuf', 0)
        renderer_text5 = Gtk.CellRendererText()
        combo5.pack_start(renderer_text5, True)
        combo5.add_attribute(renderer_text5, 'text', 1)
        combo5.set_entry_text_column(1)
        # Signal connect below

        current_override = self.edit_obj.options_dict['use_fixed_folder']
        if current_override is None:
            checkbutton.set_active(False)
            combo5.set_sensitive(False)
            combo5.set_active(0)
        else:
            checkbutton.set_active(True)
            combo5.set_sensitive(True)
            if current_override == self.app_obj.fixed_temp_folder.name:
                combo5.set_active(1)
            else:
                # The value should be either None, 'Unsorted Videos' or
                #   'Temporary Videos'. In case the value is anything else,
                #   use 'Unsorted Videos'
                combo5.set_active(0)

        # Signal connects from above
        checkbutton.connect('toggled', self.on_fixed_folder_toggled, combo5)
        combo5.connect('changed', self.on_fixed_folder_changed)


    def setup_formats_tab(self):

        """Called by self.setup_tabs().

        Sets up the 'Formats' tab.
        """

        tab, grid = self.add_notebook_tab('F_ormats')
        grid_width = 4
        grid.set_column_homogeneous(True)

        # The first format must be a video format. The second and third formats
        #   can be either video or audio formats
        # Work out how many formats we have right now
        format_count = self.formats_tab_count_formats()

        # Format options
        self.add_label(grid,
            '<u>Format options</u>',
            0, 0, 4, 1,
        )

        self.add_checkbutton(grid,
            'Download all available video formats',
            'all_formats',
            0, 1, grid_width, 1,
        )

        if format_count == 0:

            label = self.add_label(grid,
                self.video_only_text,
                0, 2, 2, 1,
            )

        else:

            label = self.add_label(grid,
                self.video_audio_text,
                0, 2, 2, 1,
            )

        treeview, liststore = self.add_treeview(grid,
            0, 3, 2, 1,
        )

        if format_count == 0:
            for key in formats.VIDEO_ONLY_OPTION_LIST:
                liststore.append([key])
        else:
            for key in formats.VIDEO_OPTION_LIST:
                liststore.append([key])

        button = Gtk.Button('Add format >>>')
        grid.attach(button, 0, 4, 2, 1)
        # Signal connect below

        label2 = self.add_label(grid,
            'Preference list (up to three formats)',
            2, 2, 2, 1,
        )

        treeview2, liststore2 = self.add_treeview(grid,
            2, 3, 2, 1,
        )

        # (Need to reverse formats.VIDEO_OPTION_DICT for quick lookup)
        rev_dict = {}
        for key in formats.VIDEO_OPTION_DICT:
            rev_dict[formats.VIDEO_OPTION_DICT[key]] = key

        # There are three video format options, any or all of which might be
        #   set
        val1 = self.retrieve_val('video_format')
        val2 = self.retrieve_val('second_video_format')
        val3 = self.retrieve_val('third_video_format')
        if val1 != '0':
            liststore2.append([rev_dict[val1]])
        if val2 != '0':
            liststore2.append([rev_dict[val2]])
        if val3 != '0':
            liststore2.append([rev_dict[val3]])

        button2 = Gtk.Button('<<< Remove format')
        grid.attach(button2, 2, 4, 2, 1)
        # Signal connect below

        button3 = Gtk.Button('^ Move up')
        grid.attach(button3, 2, 5, 1, 1)
        # Signal connect below

        button4 = Gtk.Button('v Move down')
        grid.attach(button4, 3, 5, 1, 1)
        # Signal connect below

        # Signal connects from above
        button.connect(
            'clicked',
            self.on_formats_tab_add_clicked,
            button2,
            button3,
            button4,
            treeview,
            liststore,
            liststore2,
            label,
        )
        button2.connect(
            'clicked',
            self.on_formats_tab_remove_clicked,
            button,
            button3,
            button4,
            liststore,
            treeview2,
            label,
        )
        button3.connect(
            'clicked',
            self.on_formats_tab_up_clicked,
            treeview2,
        )
        button4.connect(
            'clicked',
            self.on_formats_tab_down_clicked,
            treeview2,
        )

        # Desensitise buttons, as appropriate
        if format_count == 0:
            button2.set_sensitive(False)
            button3.set_sensitive(False)
            button4.set_sensitive(False)

        if format_count == 3:
            button.set_sensitive(False)

        # Now add other widgets
        if not self.app_obj.simple_options_flag:

            self.add_checkbutton(grid,
                'Prefer free video formats, unless one is specified above',
                'prefer_free_formats',
                0, 6, grid_width, 1,
            )

            self.add_checkbutton(grid,
                'Do not download DASH-related data on YouTube videos',
                'yt_skip_dash',
                0, 7, grid_width, 1,
            )

            self.add_label(grid,
                'Output to this format, if merge required',
                0, 8, 2, 1,
            )

            combo_list = ['', 'flv', 'mkv', 'mp4', 'ogg', 'webm']
            self.add_combo(grid,
                combo_list,
                'merge_output_format',
                2, 8, 2, 1,
            )


    def setup_downloads_tab(self):

        """Called by self.setup_tabs().

        Sets up the 'Downloads' tab.
        """

        tab, grid = self.add_notebook_tab('_Downloads')
        grid_width = 6

        # Download options
        self.add_label(grid,
            '<u>Download options</u>',
            0, 0, grid_width, 1,
        )

        if not self.app_obj.simple_options_flag:

            self.add_checkbutton(grid,
                'Prefer HLS (HTTP Live Streaming)',
                'native_hls',
                0, 1, (grid_width - 2), 1,
            )

            self.add_checkbutton(grid,
                'Prefer FFMpeg over native HLS downloader',
                'hls_prefer_ffmpeg',
                (grid_width - 2), 1, 2, 1,
            )

            self.add_checkbutton(grid,
                'Include advertisements (experimental feature)',
                'include_ads',
                0, 2, grid_width, 1,
            )

            self.add_checkbutton(grid,
                'Ignore errors and continue the download operation',
                'ignore_errors',
                0, 3, grid_width, 1,
            )

            self.add_label(grid,
                'Number of retries',
                0, 4, (grid_width - 2), 1,
            )

            self.add_spinbutton(grid,
                1, 99, 1,
                'retries',
                (grid_width - 2), 4, 1, 1,
            )

        self.add_label(grid,
            'Download videos suitable for this age',
            0, 5, (grid_width - 2), 1,
        )

        self.add_entry(grid,
            'age_limit',
            (grid_width - 2), 5, 1, 1,
        )

        # Playlist options
        if not self.app_obj.simple_options_flag:

            self.add_label(grid,
                '<u>Playlist options</u>',
                0, 6, grid_width, 1,
            )

            self.add_label(grid,
                'Start downloading playlist from index',
                0, 7, (grid_width - 2), 1,
            )

            self.add_spinbutton(grid,
                1, None, 1,
                'playlist_start',
                (grid_width - 2), 7, 1, 1,
            )

            self.add_label(grid,
                'Stop downloading playlist at index',
                0, 8, (grid_width - 2), 1,
            )

            self.add_spinbutton(grid,
                0, None, 1,
                'playlist_end',
                (grid_width - 2), 8, 1, 1,
            )

            self.add_label(grid,
                'Maximum downloads from a playlist',
                0, 9, (grid_width - 2), 1,
            )

            self.add_spinbutton(grid,
                0, None, 1,
                'max_downloads',
                (grid_width - 2), 9, 1, 1,
            )

            self.add_checkbutton(grid,
                'Abort downloading the playlist if an error occurs',
                'abort_on_error',
                0, 10, grid_width, 1,
            )

            self.add_checkbutton(grid,
                'Download playlist in reverse order',
                'playlist_reverse',
                0, 11, grid_width, 1,
            )

            self.add_checkbutton(grid,
                'Download playlist in random order',
                'playlist_random',
                (grid_width - 2), 11, 1, 1,
            )

        # Video size limit options
        if not self.app_obj.simple_options_flag:

            self.add_label(grid,
                '<u>Video size limit options</u>',
                0, 12, grid_width, 1,
            )

            self.add_label(grid,
                'Minimum file size for video downloads',
                0, 13, (grid_width - 2), 1,
            )

            self.add_spinbutton(grid,
                0, None, 1,
                'min_filesize',
                (grid_width - 2), 13, 1, 1,
            )

            self.add_combo_with_data(grid,
                formats.FILE_SIZE_UNIT_LIST,
                'min_filesize_unit',
                (grid_width - 1), 13, 1, 1,
            )

            self.add_label(grid,
                'Maximum file size for video downloads',
                0, 14, (grid_width - 2), 1,
            )

            self.add_spinbutton(grid,
                0, None, 1,
                'max_filesize',
                (grid_width - 2), 14, 1, 1,
            )

            self.add_combo_with_data(grid,
                formats.FILE_SIZE_UNIT_LIST,
                'max_filesize_unit',
                (grid_width - 1), 14, 1, 1,
            )

        # Video date options
        self.add_label(grid,
            '<u>Video date options</u>',
            0, 15, grid_width, 1,
        )

        self.add_label(grid,
            'Only videos uploaded on this date',
            0, 16, (grid_width - 2), 1,
        )

        entry = self.add_entry(grid,
            'date',
            (grid_width - 2), 16, 1, 1,
        )
        entry.set_editable(False)

        button = Gtk.Button('Set')
        grid.attach(button, (grid_width - 1), 16, 1, 1)
        button.connect(
            'clicked',
            self.on_button_set_date_clicked,
            entry,
            'date',
        )

        self.add_label(grid,
            'Only videos uploaded before this date',
            0, 17, (grid_width - 2), 1,
        )

        entry2 = self.add_entry(grid,
            'date_before',
            (grid_width - 2), 17, 1, 1,
        )
        entry2.set_editable(False)

        button2 = Gtk.Button('Set')
        grid.attach(button2, (grid_width - 1), 17, 1, 1)
        button2.connect(
            'clicked',
            self.on_button_set_date_clicked,
            entry2,
            'date_before',
        )

        self.add_label(grid,
            'Only videos uploaded after this date',
            0, 18, (grid_width - 2), 1,
        )

        entry3 = self.add_entry(grid,
            'date_after',
            (grid_width - 2), 18, 1, 1,
        )
        entry3.set_editable(False)

        button3 = Gtk.Button('Set')
        grid.attach(button3, (grid_width - 1), 18, 1, 1)
        button3.connect(
            'clicked',
            self.on_button_set_date_clicked,
            entry3,
            'date_after',
        )

        # Video views options
        self.add_label(grid,
            '<u>Video views options</u>',
            0, 19, grid_width, 1,
        )

        self.add_label(grid,
            'Minimum number of views',
            0, 20, (grid_width - 2), 1,
        )

        self.add_spinbutton(grid,
            0, None, 1,
            'min_views',
            (grid_width - 2), 20, 1, 1,
        )

        self.add_label(grid,
            'Maximum number of views',
            0, 21, (grid_width - 2), 1,
        )

        self.add_spinbutton(grid,
            0, None, 1,
            'max_views',
            (grid_width - 2), 21, 1, 1,
        )

        # Video filtering options
        if not self.app_obj.simple_options_flag:

            self.add_label(grid,
                '<u>Video filtering options</u>',
                0, 22, grid_width, 1,
            )

            self.add_label(grid,
                'Download only matching titles (regex or caseless substring)',
                0, 23, grid_width, 1,
            )

            self.add_textview(grid,
                'match_title_list',
                0, 24, grid_width, 1,
            )

            self.add_label(grid,
                'Don\'t download only matching titles (regex or caseless' \
                + ' substring)',
                0, 25, grid_width, 1,
            )

            self.add_textview(grid,
                'reject_title_list',
                0, 26, grid_width, 1,
            )

            self.add_label(grid,
                'Generic video filter, for example: like_count > 100',
                0, 27, grid_width, 1,
            )

            self.add_entry(grid,
                'match_filter',
                0, 28, grid_width, 1,
            )

        # External downloader options
        if not self.app_obj.simple_options_flag:

            self.add_label(grid,
                '<u>External downloader options</u>',
                0, 29, grid_width, 1,
            )

            self.add_label(grid,
                'Use this external downloader',
                0, 30, (grid_width - 2), 1,
            )

            ext_list = [
                '', 'aria2c', 'avconv', 'axel', 'curl', 'ffmpeg', 'httpie',
                'wget',
            ]

            self.add_combo(grid,
                ext_list,
                'external_downloader',
                (grid_width - 2), 30, 1, 1,
            )

            self.add_label(grid,
                'Arguments to pass to external downloader',
                0, 31, (grid_width - 2), 1,
            )

            self.add_entry(grid,
                'external_arg_string',
                0, 32, grid_width, 1,
            )


    def setup_post_process_tab(self):

        """Called by self.setup_tabs().

        Sets up the 'Post-processing' tab.
        """

        tab, grid = self.add_notebook_tab('_Post-processing')
        grid_width = 2
        grid.set_column_homogeneous(True)

        # Post-processing options
        self.add_label(grid,
            '<u>Post-processing options</u>',
            0, 0, grid_width, 1,
        )

        self.add_checkbutton(grid,
            'Post-process video files to convert them to audio-only files',
            'extract_audio',
            0, 1, grid_width, 1,
        )

        button = self.add_checkbutton(grid,
            'Prefer avconv over ffmpeg',
            'prefer_avconv',
            0, 2, 1, 1,
        )
        if os.name == 'nt':
            button.set_sensitive(False)

        button2 = self.add_checkbutton(grid,
            'Prefer ffmpeg over avconv (default)',
            'prefer_ffmpeg',
            1, 2, 1, 1,
        )
        if os.name == 'nt':
            button2.set_sensitive(False)

        self.add_label(grid,
            'Audio format of the post-processed file',
            0, 3, 1, 1,
        )

        combo_list = formats.AUDIO_FORMAT_LIST
        combo_list.insert(0, '')
        self.add_combo(grid,
            combo_list,
            'audio_format',
            1, 3, 1, 1,
        )

        self.add_label(grid,
            'Audio quality of the post-processed file',
            0, 4, 1, 1,
        )

        combo2_list = [
            ['High', '0'],
            ['Medium', '5'],
            ['Low', '9'],
        ]

        self.add_combo_with_data(grid,
            combo2_list,
            'audio_quality',
            1, 4, 1, 1,
        )

        self.add_label(grid,
            'Encode video to another format, if necessary',
            0, 5, 1, 1,
        )

        combo_list3 = ['', 'avi', 'flv', 'mkv', 'mp4', 'ogg', 'webm']
        self.add_combo(grid,
            combo_list3,
            'recode_video',
            1, 5, 1, 1,
        )

        self.add_label(grid,
            'Arguments to pass to postprocessor',
            0, 6, 1, 1,
        )

        self.add_entry(grid,
            'pp_args',
            1, 6, 1, 1,
        )

        self.add_checkbutton(grid,
            'Keep video file after post-processing it',
            'keep_video',
            0, 7, grid_width, 1,
        )

        self.add_checkbutton(grid,
            'Merge subtitles file with video (.mp4 files only)',
            'embed_subs',
            0, 8, grid_width, 1,
        )

        self.add_checkbutton(grid,
            'Embed thumbnail in audio file as cover art',
            'embed_thumbnail',
            0, 9, grid_width, 1,
        )

        self.add_checkbutton(grid,
            'Write metadata to the video file',
            'add_metadata',
            0, 10, grid_width, 1,
        )

        self.add_label(grid,
            'Automatically correct known faults of the file',
            0, 11, 1, 1,
        )

        combo_list4 = ['', 'never', 'warn', 'detect_or_warn']
        self.add_combo(grid,
            combo_list4,
            'fixup_policy',
            1, 11, 1, 1,
        )


    def setup_subtitles_tab(self):

        """Called by self.setup_tabs().

        Sets up the 'Subtitles' tab.
        """

        tab, grid = self.add_notebook_tab('_Subtitles')
        grid.set_column_homogeneous(True)

        # Subtitles options
        self.add_label(grid,
            '<u>Subtitles options</u>',
            0, 0, 2, 1,
        )

        radio_flag = False
        radiobutton = self.add_radiobutton(grid,
            None,
            'Don\'t download the subtitles file',
            None,
            None,
            0, 1, 2, 1,
        )
        if self.retrieve_val('write_subs') is False:
            radiobutton.set_active(True)
            radio_flag = True
        # Signal connect appears below

        radiobutton2 = self.add_radiobutton(grid,
            radiobutton,
            'Download the automatic subtitles file (YouTube only)',
            None,
            None,
            0, 2, 2, 1,
        )
        if self.retrieve_val('write_auto_subs') is True:
            radiobutton.set_active(True)
            radio_flag = True
        # Signal connect appears below

        radiobutton3 = self.add_radiobutton(grid,
            radiobutton2,
            'Download all available subtitles files',
            None,
            None,
            0, 3, 2, 1,
        )
        if self.retrieve_val('write_all_subs') is True:
            radiobutton2.set_active(True)
            radio_flag = True
        # Signal connect appears below

        radiobutton4 = self.add_radiobutton(grid,
            radiobutton3,
            'Download subtitles file for this language',
            None,
            None,
            0, 4, 1, 1,
        )
        if not radio_flag:
            radiobutton.set_active(True)
        # Signal connect appears below

        combo = self.add_combo_with_data(grid,
            formats.LANGUAGE_CODE_LIST,
            'subs_lang',
            1, 4, 1, 1,
        )
        if radio_flag:
            combo.set_sensitive(False)

        # Signal connects from above
        radiobutton.connect(
            'toggled',
            self.on_subtitles_toggled,
            combo,
            'write_subs',
        )
        radiobutton2.connect(
            'toggled',
            self.on_subtitles_toggled,
            combo,
            'write_auto_subs',
        )
        radiobutton3.connect(
            'toggled',
            self.on_subtitles_toggled,
            combo,
            'write_all_subs',
        )
        radiobutton4.connect(
            'toggled',
            self.on_subtitles_toggled,
            combo,
            'subs_lang',
        )

        # Subtitle format options
        self.add_label(grid,
            '<u>Subtitle format options</u>',
            0, 5, 2, 1,
        )

        self.add_label(grid,
            'Preferred subtitle format(s), e.g. \'srt\', \'vtt\',' \
            + ' \'srt/ass/vtt/lrc/best\'',
            0, 6, 2, 1,
        )

        self.add_entry(grid,
            'subs_format',
            1, 7, 1, 1,
        )


    def setup_others_tab(self):

        """Called by self.setup_tabs().

        Sets up the 'Other files' tab.
        """

        tab, grid = self.add_notebook_tab('O_ther files')
        script = __main__.__packagename__.title()

        # Other file options
        self.add_label(grid,
            '<u>Other file options</u>',
            0, 0, 1, 1,
        )

        self.add_checkbutton(grid,
            'Write video\'s description to a .description file',
            'write_description',
            0, 1, 1, 1,
        )

        self.add_checkbutton(grid,
            'Write video\'s metadata to an .info.json file',
            'write_info',
            0, 2, 1, 1,
        )

        self.add_checkbutton(grid,
            'Write video\'s annotations to an .annotations.xml file',
            'write_annotations',
            0, 3, 1, 1,
        )

        self.add_checkbutton(grid,
            'Write the video\'s thumbnail to the same folder',
            'write_thumbnail',
            0, 4, 1, 1,
        )

        # Options during real (not simulated) downloads
        self.add_label(grid,
            '<u>Options during real (not simulated) downloads</u>',
            0, 5, 1, 1,
        )

        self.add_checkbutton(grid,
            'Keep the description file after ' +  script + ' shuts down',
            'keep_description',
            0, 6, 1, 1,
        )

        self.add_checkbutton(grid,
            'Keep the metadata file after ' +  script + ' shuts down',
            'keep_info',
            0, 7, 1, 1,
        )

        self.add_checkbutton(grid,
            'Keep the annotations file after ' +  script + ' shuts down',
            'keep_annotations',
            0, 8, 1, 1,
        )

        self.add_checkbutton(grid,
            'Keep the thumbnail file after ' +  script + ' shuts down',
            'keep_thumbnail',
            0, 9, 1, 1,
        )

        # Options during simulated (not real) downloads
        self.add_label(grid,
            '<u>Options during simulated (not real) downloads</u>',
            0, 10, 1, 1,
        )

        self.add_checkbutton(grid,
            'Keep the description file after ' +  script + ' shuts down',
            'sim_keep_description',
            0, 11, 1, 1,
        )

        self.add_checkbutton(grid,
            'Keep the metadata file after ' +  script + ' shuts down',
            'sim_keep_info',
            0, 12, 1, 1,
        )

        self.add_checkbutton(grid,
            'Keep the annotations file after ' +  script + ' shuts down',
            'sim_keep_annotations',
            0, 13, 1, 1,
        )

        self.add_checkbutton(grid,
            'Keep the thumbnail file after ' +  script + ' shuts down',
            'sim_keep_thumbnail',
            0, 14, 1, 1,
        )


    def setup_advanced_tab(self):

        """Called by self.setup_tabs().

        Sets up the 'Advanced' tab.
        """

        tab, grid = self.add_notebook_tab('_Advanced')
        grid_width = 2

        # Authentification options
        self.add_label(grid,
            '<u>Authentification options</u>',
            0, 0, grid_width, 1,
        )

        self.add_label(grid,
            'Username with which to log in',
            0, 1, 1, 1,
        )

        self.add_entry(grid,
            'username',
            1, 1, 1, 1,
        )

        self.add_label(grid,
            'Password with which to log in',
            0, 2, 1, 1,
        )

        self.add_entry(grid,
            'password',
            1, 2, 1, 1,
        )

        self.add_label(grid,
            'Password required for this URL',
            0, 3, 1, 1,
        )

        self.add_entry(grid,
            'video_password',
            1, 3, 1, 1,
        )

        self.add_label(grid,
            'Two-factor authentication code',
            0, 4, 1, 1,
        )

        self.add_entry(grid,
            'two_factor',
            1, 4, 1, 1,
        )

        self.add_checkbutton(grid,
            'Use .netrc authentication data',
            'force_ipv4',
            0, 5, grid_width, 1,
        )

        # Network options
        self.add_label(grid,
            '<u>Network options</u>',
            0, 6, grid_width, 1,
        )

        self.add_label(grid,
            'Use this HTTP/HTTPS proxy',
            0, 7, 1, 1,
        )

        self.add_entry(grid,
            'proxy',
            1, 7, 1, 1,
        )

        self.add_label(grid,
            'Time to wait for socket connection, before giving up',
            0, 8, 1, 1,
        )

        self.add_entry(grid,
            'socket_timeout',
            1, 8, 1, 1,
        )

        self.add_label(grid,
            'Client-side IP address to which to bind',
            0, 9, 1, 1,
        )

        self.add_entry(grid,
            'source_address',
            1, 9, 1, 1,
        )

        self.add_checkbutton(grid,
            'Make all connections via IPv4',
            'force_ipv4',
            0, 10, 1, 1,
        )

        self.add_checkbutton(grid,
            'Make all connections via IPv6',
            'force_ipv6',
            1, 10, 1, 1,
        )

        # Geo-restriction options
        self.add_label(grid,
            '<u>Geo-restriction options</u>',
            0, 11, grid_width, 1,
        )

        self.add_label(grid,
            'Use this proxy to verify IP address',
            0, 12, 1, 1,
        )

        self.add_entry(grid,
            'geo_verification_proxy',
            1, 12, 1, 1,
        )

        self.add_checkbutton(grid,
            'Bypass via fake X-Forwarded-For HTTP header',
            'geo_bypass',
            0, 13, 1, 1,
        )

        self.add_checkbutton(grid,
            'Don\'t bypass via fake HTTP header',
            'no_geo_bypass',
            1, 13, 1, 1,
        )

        self.add_label(grid,
            'Bypass geo-restriction with ISO 3166-2 country code',
            0, 14, 1, 1,
        )

        self.add_entry(grid,
            'geo_bypass_country',
            1, 14, 1, 1,
        )

        self.add_label(grid,
            'Bypass with explicit IP block in CIDR notation',
            0, 15, 1, 1,
        )

        self.add_entry(grid,
            'geo_bypass_ip_block',
            1, 15, 1, 1,
        )

        # Workaround options
        self.add_label(grid,
            '<u>Workaround options</u>',
            0, 16, grid_width, 1,
        )

        self.add_label(grid,
            'Custom user agent for youtube-dl',
            0, 17, 1, 1,
        )

        self.add_entry(grid,
            'user_agent',
            1, 17, 1, 1,
        )

        self.add_label(grid,
            'Custom referer if video access has restricted domain',
            0, 18, 1, 1,
        )

        self.add_entry(grid,
            'referer',
            1, 18, 1, 1,
        )

        self.add_label(grid,
            'Force this encoding (experimental)',
            0, 19, 1, 1,
        )

        self.add_entry(grid,
            'force_encoding',
            1, 19, 1, 1,
        )

        self.add_checkbutton(grid,
            'Suppress HTTPS certificate validation',
            'no_check_certificate',
            0, 20, grid_width, 1,
        )

        self.add_checkbutton(grid,
            'Use an unencrypted connection to retrieve information about' \
            + ' videos (YouTube only)',
            'prefer_insecure',
            0, 21, grid_width, 1,
        )


    def setup_sound_only_tab(self):

        """Called by self.setup_tabs().

        Sets up the 'Sound Only' tab.
        """

        tab, grid = self.add_notebook_tab('_Sound only')
        grid_width = 4

        # Sound only options
        self.add_label(grid,
            '<u>Sound only options</u>',
            0, 0, grid_width, 1,
        )

        # (The MS Windows installer includes FFmpeg)
        text = 'Download each video, extract the sound, and then discard the' \
        + ' original videos'
        if os.name != 'nt':
            text += '\n(requires that FFmpeg or AVConv is installed on your' \
            + ' system)'

        self.add_checkbutton(grid,
            text,
            'extract_audio',
            0, 1, grid_width, 1,
        )

        label = self.add_label(grid,
            'Use this audio format: ',
            0, 2, 1, 1,
        )
        label.set_hexpand(False)

        combo_list = formats.AUDIO_FORMAT_LIST
        combo_list.insert(0, '')
        combo = self.add_combo(grid,
            combo_list,
            'audio_format',
            1, 2, 1, 1,
        )
        combo.set_hexpand(True)

        label2 = self.add_label(grid,
            'Use this audio quality: ',
            2, 2, 1, 1,
        )
        label2.set_hexpand(False)

        combo2_list = [
            ['High', '0'],
            ['Medium', '5'],
            ['Low', '9'],
        ]

        combo2 = self.add_combo_with_data(grid,
            combo2_list,
            'audio_quality',
            3, 2, 1, 1,
        )
        combo2.set_hexpand(True)


    # (Tab support functions)


    def file_tab_sensitise_widgets(self, flag):

        """Called by self.setup_files_tab().

        Sensitises or desensitises a list of widgets in response to the user's
        interactions with widgets on that tab.

        Args:

            flag (True, False): True to sensitise the widgets, False to
                desensitise them

        """

        self.template_flag = flag
        for widget in self.template_widget_list:
            widget.set_sensitive(flag)


    def formats_tab_count_formats(self):

        """Called by several parts of self.setup_formats_tab().

        Counts the number of video/audio formats that are set.

        Return values:

            An integer in the range 0-3

        """

        if self.retrieve_val('video_format') == '0':
            return 0
        elif self.retrieve_val('second_video_format') == '0':
            return 1
        elif self.retrieve_val('third_video_format') == '0':
            return 2
        else:
            return 3


    # Callback class methods


    def on_button_set_date_clicked(self, button, entry, prop):

        """Called by callback in self.setup_downloads_tab().

        Args:

            button (Gtk.Button): The widget clicked

            entry (Gtk.Entry): Another widget to be modified by this function

            prop (string): The attribute in self.edit_dict to modify

        """

        # Prompt the user for a new calendar date
        dialogue_win = mainwin.CalendarDialogue(
            self,
            self.retrieve_val(prop),
        )

        response = dialogue_win.run()

        # Retrieve user choices from the dialogue window, before destroying it
        if response == Gtk.ResponseType.OK:
            date_tuple = dialogue_win.calendar.get_date()

        dialogue_win.destroy()

        if response == Gtk.ResponseType.OK and date_tuple:

            year = str(date_tuple[0])           # e.g. 2011
            month = str(date_tuple[1] + 1)      # Values in range 0-11
            day = str(date_tuple[2])            # Values in range 1-31

            entry.set_text(
                year.zfill(4) + month.zfill(2) + day.zfill(2)
            )

        else:

            entry.set_text('')


    def on_clone_options_clicked(self, button):

        """Called by callback in self.setup_general_tab().

        Args:

            button (Gtk.Button): The widget clicked

        """

        # Editing an Options Manager object attached to a particular media
        #   data object (this function can't be called for the General Options
        #   Manager)
        self.app_obj.dialogue_manager_obj.show_msg_dialogue(
            'This operation cannot be reversed.\n' \
            + 'Are you sure you want to continue?',
            'question',
            'yes-no',
            self,           # Parent window is this window
            {
                'yes': 'clone_general_options_manager',
                'data': [self, self.edit_obj],
            },
        )


    def on_fixed_folder_toggled(self, checkbutton, combo):

        """Called by callback in self.setup_files_tab().

        Args:

            checkbutton (Gtk.CheckButton): The widget clicked

            combo (Gtk.ComboBox): Another widget to be modified by this
                function

        """

        if not checkbutton.get_active():
            self.edit_dict['use_fixed_folder'] = None
            combo.set_sensitive(False)

        else:

            tree_iter = combo.get_active_iter()
            model = combo.get_model()
            pixbuf, name = model[tree_iter][:2]
            self.edit_dict['use_fixed_folder'] = name
            combo.set_sensitive(True)


    def on_fixed_folder_changed(self, combo):

        """Called by callback in self.setup_files_tab().

        Args:

            combo (Gtk.ComboBox): The widget clicked

        """

        tree_iter = combo.get_active_iter()
        model = combo.get_model()
        pixbuf, name = model[tree_iter][:2]
        self.edit_dict['use_fixed_folder'] = name


    def on_file_tab_button_clicked(self, button, entry, combo):

        """Called by callback in self.setup_files_tab().

        Args:

            button (Gtk.Button): The widget clicked

            entry (Gtk.Entry): Another widget to be modified by this function

            combo (Gtk.ComboBox): Another widget to be modified by this
                function

        """

        tree_iter = combo.get_active_iter()
        model = combo.get_model()
        label = model[tree_iter][0]

        # (Code adapted from youtube-dl-gui's GeneralTab._on_template)
        label = label.lower().replace(' ', '_')
        if label == "ext":
            prefix = '.'
        else:
            prefix = '-'

        # If the output template is empty or ends with a file path separator,
        #   remove the prefix
        output_template = self.retrieve_val('output_template')
        if not output_template or output_template[-1] == os.sep:
            prefix = ''

        formatted = '{0}%({1})s'.format(prefix, label)
        # (Setting the entry updates self.edit_dict)
        entry.set_text(output_template + formatted)


    def on_file_tab_combo_changed(self, combo, entry):

        """Called by callback in self.setup_files_tab().

        Args:

            combo (Gtk.ComboBox): The widget clicked

            entry (Gtk.Entry): Another widget to be modified by this function

        """

        tree_iter = combo.get_active_iter()
        model = combo.get_model()
        row_id, name = model[tree_iter][:2]

        self.edit_dict['output_format'] = row_id

        if row_id == 3:
            self.file_tab_sensitise_widgets(True)
            entry.set_text(self.retrieve_val('output_template'))

        else:
            self.file_tab_sensitise_widgets(False)
            entry.set_text(formats.FILE_OUTPUT_CONVERT_DICT[row_id])


    def on_file_tab_entry_changed(self, entry):

        """Called by callback in self.setup_files_tab().

        Args:

            entry (Gtk.Entry): The widget clicked

        """

        # Only set 'output_template' when option 3 is selected, which is when
        #   the entry is sensitised
        if self.template_flag:
            self.edit_dict['output_template'] = entry.get_text()


    def on_formats_tab_add_clicked(self, add_button, remove_button, \
    up_button, down_button, treeview, liststore, other_liststore, label):

        """Called by callback in self.setup_formats_tab().

        Args:

            add_button (Gtk.Button): The widget clicked

            remove_button, up_button, down_button (Gtk.Button): Other widgets
                to be modified by this function

            treeview (Gtk.TreeView): The treeview on the left side of the tab

            liststore (Gtk.TreeView): That treeview's liststore

            other_liststore (Gtk.ListStore): The liststore belonging to the
                treeview on the right side of the tab

            label (Gtk.Label): Another widget to be modified by this function

        """

        selection = treeview.get_selection()
        (model, iter) = selection.get_selected()
        if iter is None:

            # Nothing selected
            return

        else:

            name = model[iter][0]
            # Convert e.g. 'mp4 [360p]' to the extractor code e.g. '18'
            extract_code = formats.VIDEO_OPTION_DICT[name]

        # There are three video format options; set the first one whose value
        #   is not already 0
        val1 = self.retrieve_val('video_format')
        val2 = self.retrieve_val('second_video_format')
        val3 = self.retrieve_val('third_video_format')
        # Check the user's choice of format hasn't already been added
        if extract_code == val1 or extract_code == val2 \
        or extract_code == val3:
            return

        if val1 == '0':
            self.edit_dict['video_format'] = extract_code
        elif val2 == '0':
            self.edit_dict['second_video_format'] = extract_code
        elif val3 == '0':
            self.edit_dict['third_video_format'] = extract_code
            add_button.set_sensitive(False)
        else:
            # 'add_button' should be desensitised, but if clicked, just ignore
            #   it
            return

        # Update the other treeview, adding the format to it (and don't modify
        #   this treeview)
        other_liststore.append([name])

        # Update other widgets, as required
        remove_button.set_sensitive(True)
        up_button.set_sensitive(True)
        down_button.set_sensitive(True)

        label.set_text(self.video_audio_text)

        if self.retrieve_val('second_video_format') == '0':
            # The first format has just been added, so the left-hand side
            #   treeview must be reset
            liststore.clear()
            for key in formats.VIDEO_OPTION_LIST:
                liststore.append([key])


    def on_formats_tab_down_clicked(self, down_button, treeview):

        """Called by callback in self.setup_formats_tab().

        Args:

            down_button (Gtk.Button): The widget clicked

            treeview (Gtk.TreeView): Another widget to be modified by this
                function

        """

        selection = treeview.get_selection()
        (model, path_list) = selection.get_selected_rows()
        if not path_list:

            # Nothing selected
            return

        else:

            this_iter = model.get_iter(path_list[0])
            name = model[this_iter][0]
            # Convert e.g. 'mp4 [360p]' to the extractor code e.g. '18'
            extract_code = formats.VIDEO_OPTION_DICT[name]

        # There are three video format options; the selected one might be any
        #   of them
        val1 = self.retrieve_val('video_format')
        val2 = self.retrieve_val('second_video_format')
        val3 = self.retrieve_val('third_video_format')

        if extract_code == val3:
            # Can't move the last item down
            return

        else:

            if extract_code == val2:
                self.edit_dict['second_video_format'] = val3
                self.edit_dict['third_video_format'] = val2

            elif extract_code == val1:
                self.edit_dict['video_format'] = val2
                self.edit_dict['second_video_format'] = val1

            else:
                # This should not be possible
                return

            this_path = path_list[0]
            next_path = this_path[0]+1
            model.move_after(
                model.get_iter(this_path),
                model.get_iter(next_path),
            )


    def on_formats_tab_remove_clicked(self, remove_button, add_button, \
    up_button, down_button, liststore, other_treeview, label):

        """Called by callback in self.setup_formats_tab().

        Args:

            remove_button (Gtk.Button): The widget clicked

            add_button, up_button, down_button (Gtk.Button): Other widgets to
                be modified by this function

            liststore (Gtk.ListStore): The liststore belonging to the treeview
                on the left side of the tab

            other_treeview (Gtk.TreeView): The treeview on the right side of
                the tab

            label (Gtk.Label): Another widget to be modified by this function

        """

        selection = other_treeview.get_selection()
        (model, iter) = selection.get_selected()
        if iter is None:

            # Nothing selected
            return

        else:

            name = model[iter][0]
            # Convert e.g. 'mp4 [360p]' to the extractor code e.g. '18'
            extract_code = formats.VIDEO_OPTION_DICT[name]

        # There are three video format options; the selected one might be any
        #   of them
        val1 = self.retrieve_val('video_format')
        val2 = self.retrieve_val('second_video_format')
        val3 = self.retrieve_val('third_video_format')

        if extract_code == val1:
            self.edit_dict['video_format'] = val2
            self.edit_dict['second_video_format'] = val3
            self.edit_dict['third_video_format'] = '0'
        elif extract_code == val2:
            self.edit_dict['second_video_format'] = val3
            self.edit_dict['third_video_format'] = '0'
        elif extract_code == val3:
            self.edit_dict['third_video_format'] = '0'
        else:
            # This should not be possible
            return

        # Update the right-hand side treeview
        model.remove(iter)

        # Update other widgets, as required
        add_button.set_sensitive(True)
        if self.retrieve_val('video_format') == '0':

            # No formats left to remove
            remove_button.set_sensitive(False)
            up_button.set_sensitive(False)
            down_button.set_sensitive(False)

            label.set_text(self.video_only_text)

            liststore.clear()
            for key in formats.VIDEO_ONLY_OPTION_LIST:
                liststore.append([key])


    def on_formats_tab_up_clicked(self, up_button, treeview):

        """Called by callback in self.setup_formats_tab().

        Args:

            button (Gtk.Button): The widget clicked

            treeview (Gtk.TreeView): Another widget to be modified by this
                function

        """

        selection = treeview.get_selection()
        (model, path_list) = selection.get_selected_rows()
        if not path_list:

            # Nothing selected
            return

        else:

            this_iter = model.get_iter(path_list[0])
            name = model[this_iter][0]
            # Convert e.g. 'mp4 [360p]' to the extractor code e.g. '18'
            extract_code = formats.VIDEO_OPTION_DICT[name]

        # There are three video format options; the selected one might be any
        #   of them
        val1 = self.retrieve_val('video_format')
        val2 = self.retrieve_val('second_video_format')
        val3 = self.retrieve_val('third_video_format')

        if extract_code == val1:
            # Can't move the first item up
            return

        else:

            if extract_code == val2:
                self.edit_dict['video_format'] = val2
                self.edit_dict['second_video_format'] = val1

            elif extract_code == val3:
                self.edit_dict['second_video_format'] = val3
                self.edit_dict['third_video_format'] = val2

            else:
                # This should not be possible
                return

            this_path = path_list[0]
            prev_path = this_path[0]-1
            model.move_before(
                model.get_iter(this_path),
                model.get_iter(prev_path),
            )


    def on_reset_options_clicked(self, button):

        """Called by callback in self.setup_general_tab().

        Args:

            button (Gtk.Button): The widget clicked

        """

        msg = 'This operation cannot be reversed.\n' \
        + 'Are you sure you want to continue?',

        if self.media_data_obj is None:

            # Editing the General Options Manager object
            self.app_obj.dialogue_manager_obj.show_msg_dialogue(
                msg,
                'question',
                'yes-no',
                self,           # Parent window is this window
                {
                    'yes': 'reset_options_manager',
                    # (Reset this edit window, if the user clicks 'yes')
                    'data': [self],
                },
            )

        else:

            # Editing an Options Manager object attached to a particular media
            #   data object
            self.app_obj.dialogue_manager_obj.show_msg_dialogue(
                msg,
                'question',
                'yes-no',
                self,           # Parent window is this window
                {
                    'yes': 'reset_options_manager',
                    'data': [self, self.media_data_obj],
                },
            )


    def on_simple_options_clicked(self, button):

        """Called by callback in self.setup_general_tab().

        Args:

            button (Gtk.Button): The widget clicked

        """

        if not self.app_obj.simple_options_flag:

            self.app_obj.set_simple_options_flag(True)

            if not self.edit_dict:
                # User has not changed any options, so redraw the window to
                #   show the same options.OptionsManager object.
                self.reset_with_new_edit_obj(self.edit_obj)

            else:
                # User has already changed some options. We don't want to lose
                #   them, so wait for the window to close and be re-opened,
                #   before switching between simple/advanced options
                self.app_obj.dialogue_manager_obj.show_msg_dialogue(
                    'When the window is re-opened, some\ndownload options' \
                    + ' will be hidden',
                    'info',
                    'ok',
                    self,           # Parent window is this window
                )

                button.set_label(
                    'Show advanced download options (when window re-opens)',
                )

        else:

            self.app_obj.set_simple_options_flag(False)

            if not self.edit_dict:
                self.reset_with_new_edit_obj(self.edit_obj)

            else:
                self.app_obj.dialogue_manager_obj.show_msg_dialogue(
                    'When the window is re-opened, all\ndownload options' \
                    + ' will bevisible',
                    'info',
                    'ok',
                    self,           # Parent window is this window
                )

                button.set_label(
                    'Hide advanced download options (when window re-opens)',
                )


    def on_subtitles_toggled(self, radiobutton, combo, prop):

        """Called by callback in self.setup_subtitles_tab().

        Args:

            radiobutton (Gtk.RadioButton): The widget clicked

            combo (Gtk.ComboBox): Another widget to be modified by this
                function

            prop (string): The attribute in self.edit_dict to modify

        """

        if radiobutton.get_active():

            if prop == 'write_subs':
                self.edit_dict['write_subs'] = False
                self.edit_dict['write_auto_subs'] = False
                self.edit_dict['write_all_subs'] = False
                combo.set_sensitive(False)

            elif prop == 'write_auto_subs':
                self.edit_dict['write_subs'] = True
                self.edit_dict['write_auto_subs'] = True
                self.edit_dict['write_all_subs'] = False
                combo.set_sensitive(False)

            elif prop == 'write_all_subs':
                self.edit_dict['write_subs'] = True
                self.edit_dict['write_auto_subs'] = False
                self.edit_dict['write_all_subs'] = True
                combo.set_sensitive(False)

            elif prop == 'subs_lang':
                self.edit_dict['write_subs'] = True
                self.edit_dict['write_auto_subs'] = False
                self.edit_dict['write_all_subs'] = False
                combo.set_sensitive(True)


class VideoEditWin(GenericEditWin):

    """Python class for an 'edit window' to modify values in a media.Video
    object.

    Args:

        app_obj (mainapp.TartubeApp): The main application object

        edit_obj (media.Video): The object whose attributes will be edited in
            this window

    """


    # Standard class methods


    def __init__(self, app_obj, edit_obj):

        Gtk.Window.__init__(self, title='Video properties')

        # IV list - class objects
        # -----------------------
        # The mainapp.TartubeApp object
        self.app_obj = app_obj
        # The media.Video object being edited
        self.edit_obj = edit_obj


        # IV list - Gtk widgets
        # ---------------------
        self.grid = None                        # Gtk.Grid
        self.notebook = None                    # Gtk.Notebook
        self.reset_button = None                # Gtk.Button
        self.apply_button = None                # Gtk.Button
        self.ok_button = None                   # Gtk.Button
        self.cancel_button = None               # Gtk.Button
        # (Non-standard widgets)
        self.apply_options_button = None        # Gtk.Button
        self.edit_options_button = None         # Gtk.Button
        self.remove_options_button = None       # Gtk.Button


        # IV list - other
        # ---------------
        # Size (in pixels) of gaps between edit window widgets
        self.spacing_size = self.app_obj.default_spacing_size
        # Flag set to True if all four buttons ('Reset', 'Apply', 'Cancel' and
        #   'OK' are required, or False if just the 'OK' button is required
        self.multi_button_flag = False

        # When the user changes a value, it is not applied to self.edit_obj
        #   immediately; instead, it is stored temporarily in this dictionary
        # If the user clicks the 'OK' or 'Apply' buttons at the bottom of the
        #   window, the changes are applied to self.edit_obj
        # If the user clicks the 'Reset' or 'Cancel' buttons, the dictionary
        #   is emptied and the changes are lost
        # The key-value pairs in the dictionary correspond directly to
        #   the names of attributes, and their balues in self.edit_obj
        # Key-value pairs are added to this dictionary whenever the user
        #   makes a change (so if no changes are made when the window is
        #   closed, the dictionary will still be empty)
        self.edit_dict = {}

        # String identifying the media type
        self.media_type = 'video'


        # Code
        # ----

        # Set up the edit window
        self.setup()


    # Public class methods


#   def setup():                # Inherited from GenericConfigWin


#   def setup_grid():           # Inherited from GenericConfigWin


#   def setup_notebook():       # Inherited from GenericConfigWin


#   def add_notebook_tab():     # Inherited from GenericConfigWin


#   def setup_button_strip():   # Inherited from GenericEditWin


#   def setup_gap():            # Inherited from GenericConfigWin


    # (Non-widget functions)


#   def apply_changes():        # Inherited from GenericConfigWin


#   def retrieve_val():         # Inherited from GenericConfigWin


    # (Setup tabs)


    def setup_tabs(self):

        """Called by self.setup(), .on_button_apply_clicked() and
        .on_button_reset_clicked().

        Sets up the tabs for this edit window.
        """

        self.setup_general_tab()
        self.setup_download_options_tab()
        self.setup_descrip_tab()
        self.setup_errors_warnings_tab()


    def setup_general_tab(self):

        """Called by self.setup_tabs().

        Sets up the 'General' tab.
        """

        tab, grid = self.add_notebook_tab('_General')

        self.add_label(grid,
            '<u>General properties</u>',
            0, 0, 2, 1,
        )

        # The first sets of widgets are shared by multiple edit windows
        self.add_container_properties(grid)
        self.add_source_properties(grid)

        label3 = self.add_label(grid,
            'File',
            0, 5, 1, 1,
        )
        label3.set_hexpand(False)

        entry6 = self.add_entry(grid,
            None,
            1, 5, 2, 1,
        )
        entry6.set_editable(False)
        if self.edit_obj.file_dir:
            entry6.set_text(
                os.path.abspath(
                    os.path.join(
                        self.app_obj.downloads_dir,
                        self.edit_obj.file_dir,
                        self.edit_obj.file_name + self.edit_obj.file_ext,
                    ),
                )
            )

        # To avoid messing up the neat format of the rows above, add another
        #   grid, and put the next set of widgets inside it
        grid3 = Gtk.Grid()
        grid.attach(grid3, 0, 6, 3, 1)
        grid3.set_vexpand(False)
        grid3.set_border_width(self.spacing_size)
        grid3.set_column_spacing(self.spacing_size)
        grid3.set_row_spacing(self.spacing_size)

        checkbutton = self.add_checkbutton(grid3,
            'Always simulate download of this video',
            'dl_sim_flag',
            0, 0, 1, 1,
        )
        checkbutton.set_sensitive(False)

        label4 = self.add_label(grid3,
            'Duration',
            1, 0, 1, 1,
        )
        label4.set_hexpand(False)

        entry7 = self.add_entry(grid3,
            None,
            2, 0, 1, 1,
        )
        entry7.set_editable(False)
        if self.edit_obj.duration is not None:
            entry7.set_text(
                utils.convert_seconds_to_string(self.edit_obj.duration),
            )

        checkbutton2 = self.add_checkbutton(grid3,
            'Video is marked as unwatched',
            'new_flag',
            0, 1, 1, 1,
        )
        checkbutton2.set_sensitive(False)

        label5 = self.add_label(grid3,
            'File size',
            1, 1, 1, 1,
        )
        label5.set_hexpand(False)

        entry8 = self.add_entry(grid3,
            None,
            2, 1, 1, 1,
        )
        entry8.set_editable(False)
        if self.edit_obj.file_size is not None:
            entry8.set_text(self.edit_obj.get_file_size_string())

        checkbutton3 = self.add_checkbutton(grid3,
            'Video is marked as favourite',
            'fav_flag',
            0, 2, 1, 1,
        )
        checkbutton3.set_sensitive(False)

        label6 = self.add_label(grid3,
            'Upload time',
            1, 2, 1, 1,
        )
        label6.set_hexpand(False)

        entry9 = self.add_entry(grid3,
            None,
            2, 2, 1, 1,
        )
        entry9.set_editable(False)
        if self.edit_obj.upload_time is not None:
            entry9.set_text(self.edit_obj.get_upload_time_string())

        checkbutton4 = self.add_checkbutton(grid3,
            'Video has been downloaded',
            'dl_flag',
            0, 3, 1, 1,
        )
        checkbutton4.set_sensitive(False)

        label7 = self.add_label(grid3,
            'Receive time',
            1, 3, 1, 1,
        )
        label7.set_hexpand(False)

        entry10 = self.add_entry(grid3,
            None,
            2, 3, 1, 1,
        )
        entry10.set_editable(False)
        if self.edit_obj.receive_time is not None:
            entry10.set_text(self.edit_obj.get_receive_time_string())


#   def setup_download_options_tab():   # Inherited from GenericConfigWin


    def setup_descrip_tab(self):

        """Called by self.setup_tabs().

        Sets up the 'Description' tab.
        """

        tab, grid = self.add_notebook_tab('_Description')

        self.add_label(grid,
            '<u>Video description</u>',
            0, 0, 1, 1,
        )

        self.add_textview(grid,
            'descrip',
            0, 1, 1, 1,
        )


    def setup_errors_warnings_tab(self):

        """Called by self.setup_tabs().

        Sets up the 'Errors / Warnings' tab.
        """

        tab, grid = self.add_notebook_tab('_Errors / Warnings')

        self.add_label(grid,
            '<u>Errors / Warnings</u>',
            0, 0, 1, 1,
        )

        self.add_label(grid,
            '<i>Error messages produced the last time this video was' \
            + ' checked/downloaded</i>',
            0, 1, 1, 1,
        )

        textview, textbuffer = self.add_textview(grid,
            'error_list',
            0, 2, 1, 1,
        )
        textview.set_editable(False)
        textview.set_wrap_mode(Gtk.WrapMode.WORD)

        self.add_label(grid,
            '<i>Warning messages produced the last time this video was' \
            + ' checked/downloaded</i>',
            0, 3, 1, 1,
        )

        textview2, textbuffer2 = self.add_textview(grid,
            'warning_list',
            0, 4, 1, 1,
        )
        textview2.set_editable(False)
        textview2.set_wrap_mode(Gtk.WrapMode.WORD)


    # Callback class methods


#   def on_button_apply_clicked():  # Inherited from GenericConfigWin


#   def on_button_edit_clicked():   # Inherited from GenericConfigWin


#   def on_button_remove_clicked(): # Inherited from GenericConfigWin


    def never_called_func(self):

        """Function that is never called, but which makes this class object
        collapse neatly in my IDE."""

        pass


class ChannelPlaylistEditWin(GenericEditWin):

    """Python class for an 'edit window' to modify values in a media.Channel or
    media.Playlist object.

    Args:

        app_obj (mainapp.TartubeApp): The main application object

        edit_obj (media.Channel, media.Playlist): The object whose attributes
            will be edited in this window

    """


    # Standard class methods


    def __init__(self, app_obj, edit_obj):

        if isinstance(edit_obj, media.Channel):
            media_type = 'channel'
            win_title = 'Channel properties'
        else:
            media_type = 'playlist'
            win_title = 'Playlist properties'

        Gtk.Window.__init__(self, title=win_title)

        # IV list - class objects
        # -----------------------
        # The mainapp.TartubeApp object
        self.app_obj = app_obj
        # The media.Channel or media.Playlist object being edited
        self.edit_obj = edit_obj


        # IV list - Gtk widgets
        # ---------------------
        self.grid = None                        # Gtk.Grid
        self.notebook = None                    # Gtk.Notebook
        self.reset_button = None                # Gtk.Button
        self.apply_button = None                # Gtk.Button
        self.ok_button = None                   # Gtk.Button
        self.cancel_button = None               # Gtk.Button
        # (Non-standard widgets)
        self.apply_options_button = None        # Gtk.Button
        self.edit_options_button = None         # Gtk.Button
        self.remove_options_button = None       # Gtk.Button


        # IV list - other
        # ---------------
        # Size (in pixels) of gaps between edit window widgets
        self.spacing_size = self.app_obj.default_spacing_size
        # Flag set to True if all four buttons ('Reset', 'Apply', 'Cancel' and
        #   'OK' are required, or False if just the 'OK' button is required
        self.multi_button_flag = False

        # When the user changes a value, it is not applied to self.edit_obj
        #   immediately; instead, it is stored temporarily in this dictionary
        # If the user clicks the 'OK' or 'Apply' buttons at the bottom of the
        #   window, the changes are applied to self.edit_obj
        # If the user clicks the 'Reset' or 'Cancel' buttons, the dictionary
        #   is emptied and the changes are lost
        # The key-value pairs in the dictionary correspond directly to
        #   the names of attributes, and their balues in self.edit_obj
        # Key-value pairs are added to this dictionary whenever the user
        #   makes a change (so if no changes are made when the window is
        #   closed, the dictionary will still be empty)
        self.edit_dict = {}

        # String set to 'channel' or 'playlist'
        self.media_type = media_type


        # Code
        # ----

        # Set up the edit window
        self.setup()


    # Public class methods


#   def setup():                # Inherited from GenericConfigWin


#   def setup_grid():           # Inherited from GenericConfigWin


#   def setup_notebook():       # Inherited from GenericConfigWin


#   def add_notebook_tab():     # Inherited from GenericConfigWin


#   def setup_button_strip():   # Inherited from GenericEditWin


#   def setup_gap():            # Inherited from GenericConfigWin


    # (Non-widget functions)


#   def apply_changes():        # Inherited from GenericConfigWin


#   def retrieve_val():         # Inherited from GenericConfigWin


    # (Setup tabs)


    def setup_tabs(self):

        """Called by self.setup(), .on_button_apply_clicked() and
        .on_button_reset_clicked().

        Sets up the tabs for this edit window.
        """

        self.setup_general_tab()
        self.setup_download_options_tab()
        self.setup_errors_warnings_tab()


    def setup_general_tab(self):

        """Called by self.setup_tabs().

        Sets up the 'General' tab.
        """

        tab, grid = self.add_notebook_tab('_General')

        self.add_label(grid,
            '<u>General properties</u>',
            0, 0, 3, 1,
        )

        # The first sets of widgets are shared by multiple edit windows
        self.add_container_properties(grid)
        self.add_source_properties(grid)
        self.add_destination_properties(grid)

        # To avoid messing up the neat format of the rows above, add another
        #   grid, and put the next set of widgets inside it
        grid3 = Gtk.Grid()
        grid.attach(grid3, 0, 6, 3, 1)
        grid3.set_vexpand(False)
        grid3.set_column_spacing(self.spacing_size)
        grid3.set_row_spacing(self.spacing_size)

        checkbutton = self.add_checkbutton(grid3,
            'Always simulate download of videos in this ' + self.media_type,
            'dl_sim_flag',
            0, 0, 1, 1,
        )
        checkbutton.set_sensitive(False)

        checkbutton2 = self.add_checkbutton(grid3,
            'Disable checking/downloading for this ' + self.media_type,
            'dl_disable_flag',
            0, 1, 1, 1,
        )
        checkbutton2.set_sensitive(False)

        checkbutton3 = self.add_checkbutton(grid3,
            'This ' + self.media_type + ' is marked as a favourite',
            'fav_flag',
            0, 2, 1, 1,
        )
        checkbutton3.set_sensitive(False)

        self.add_label(grid3,
            'Total videos',
            1, 0, 1, 1,
        )
        entry8 = self.add_entry(grid3,
            'vid_count',
            2, 0, 1, 1,
        )
        entry8.set_editable(False)
        entry8.set_width_chars(8)
        entry8.set_hexpand(False)

        self.add_label(grid3,
            'New videos',
            1, 1, 1, 1,
        )
        entry9 = self.add_entry(grid3,
            'new_count',
            2, 1, 1, 1,
        )
        entry9.set_editable(False)
        entry9.set_width_chars(8)
        entry9.set_hexpand(False)

        self.add_label(grid3,
            'Favourite videos',
            1, 2, 1, 1,
        )
        entry10 = self.add_entry(grid3,
            'fav_count',
            2, 2, 1, 1,
        )
        entry10.set_editable(False)
        entry10.set_width_chars(8)
        entry10.set_hexpand(False)

        self.add_label(grid3,
            'Downloaded videos',
            1, 3, 1, 1,
        )
        entry11 = self.add_entry(grid3,
            'dl_count',
            2, 3, 1, 1,
        )
        entry11.set_editable(False)
        entry11.set_width_chars(8)
        entry11.set_hexpand(False)


#   def setup_download_options_tab():   # Inherited from GenericConfigWin


    def setup_errors_warnings_tab(self):

        """Called by self.setup_tabs().

        Sets up the 'Errors / Warnings' tab.
        """

        tab, grid = self.add_notebook_tab('_Errors / Warnings')

        self.add_label(grid,
            '<u>Errors / Warnings</u>',
            0, 0, 1, 1,
        )

        self.add_label(grid,
            '<i>Error messages produced the last time this ' \
            + self.media_type + ' was checked/downloaded</i>',
            0, 1, 1, 1,
        )

        textview, textbuffer = self.add_textview(grid,
            'error_list',
            0, 2, 1, 1,
        )
        textview.set_editable(False)
        textview.set_wrap_mode(Gtk.WrapMode.WORD)

        self.add_label(grid,
            '<i>Warning messages produced the last time this ' \
            + self.media_type + ' was checked/downloaded</i>',
            0, 3, 1, 1,
        )

        textview2, textbuffer2 = self.add_textview(grid,
            'warning_list',
            0, 4, 1, 1,
        )
        textview2.set_editable(False)
        textview2.set_wrap_mode(Gtk.WrapMode.WORD)


    # Callback class methods


#   def on_button_apply_clicked():  # Inherited from GenericConfigWin


#   def on_button_edit_clicked():   # Inherited from GenericConfigWin


#   def on_button_remove_clicked(): # Inherited from GenericConfigWin


    def never_called_func(self):

        """Function that is never called, but which makes this class object
        collapse neatly in my IDE."""

        pass


class FolderEditWin(GenericEditWin):

    """Python class for an 'edit window' to modify values in a media.Folder
    object.

    Args:

        app_obj (mainapp.TartubeApp): The main application object

        edit_obj (media.Folder): The object whose attributes will be edited in
            this window

    """


    # Standard class methods


    def __init__(self, app_obj, edit_obj):

        Gtk.Window.__init__(self, title='Folder properties')

        # IV list - class objects
        # -----------------------
        # The mainapp.TartubeApp object
        self.app_obj = app_obj
        # The media.Folder object being edited
        self.edit_obj = edit_obj


        # IV list - Gtk widgets
        # ---------------------
        self.grid = None                        # Gtk.Grid
        self.notebook = None                    # Gtk.Notebook
        self.reset_button = None                # Gtk.Button
        self.apply_button = None                # Gtk.Button
        self.ok_button = None                   # Gtk.Button
        self.cancel_button = None               # Gtk.Button
        # (Non-standard widgets)
        self.apply_options_button = None        # Gtk.Button
        self.edit_options_button = None         # Gtk.Button
        self.remove_options_button = None       # Gtk.Button


        # IV list - other
        # ---------------
        # Size (in pixels) of gaps between edit window widgets
        self.spacing_size = self.app_obj.default_spacing_size
        # Flag set to True if all four buttons ('Reset', 'Apply', 'Cancel' and
        #   'OK' are required, or False if just the 'OK' button is required
        self.multi_button_flag = False

        # When the user changes a value, it is not applied to self.edit_obj
        #   immediately; instead, it is stored temporarily in this dictionary
        # If the user clicks the 'OK' or 'Apply' buttons at the bottom of the
        #   window, the changes are applied to self.edit_obj
        # If the user clicks the 'Reset' or 'Cancel' buttons, the dictionary
        #   is emptied and the changes are lost
        # The key-value pairs in the dictionary correspond directly to
        #   the names of attributes, and their balues in self.edit_obj
        # Key-value pairs are added to this dictionary whenever the user
        #   makes a change (so if no changes are made when the window is
        #   closed, the dictionary will still be empty)
        self.edit_dict = {}

        # String identifying the media type
        self.media_type = 'folder'


        # Code
        # ----

        # Set up the edit window
        self.setup()


    # Public class methods


#   def setup():                # Inherited from GenericConfigWin


#   def setup_grid():           # Inherited from GenericConfigWin


#   def setup_notebook():       # Inherited from GenericConfigWin


#   def add_notebook_tab():     # Inherited from GenericConfigWin


#   def setup_button_strip():   # Inherited from GenericEditWin


#   def setup_gap():            # Inherited from GenericConfigWin


    # (Non-widget functions)


#   def apply_changes():        # Inherited from GenericConfigWin


#   def retrieve_val():         # Inherited from GenericConfigWin


    # (Setup tabs)


    def setup_tabs(self):

        """Called by self.setup(), .on_button_apply_clicked() and
        .on_button_reset_clicked().

        Sets up the tabs for this edit window.
        """

        self.setup_general_tab()
        self.setup_download_options_tab()


    def setup_general_tab(self):

        """Called by self.setup_tabs().

        Sets up the 'General' tab.
        """

        tab, grid = self.add_notebook_tab('_General')

        self.add_label(grid,
            '<u>General properties</u>',
            0, 0, 2, 1,
        )

        # The first sets of widgets are shared by multiple edit windows
        self.add_container_properties(grid)
        self.add_destination_properties(grid)

        # To avoid messing up the neat format of the rows above, add another
        #   grid, and put the next set of widgets inside it
        grid3 = Gtk.Grid()
        grid.attach(grid3, 0, 6, 3, 1)
        grid3.set_vexpand(False)
        grid3.set_border_width(self.spacing_size)
        grid3.set_column_spacing(self.spacing_size)
        grid3.set_row_spacing(self.spacing_size)

        checkbutton = self.add_checkbutton(grid3,
            'Always simulate download of videos',
            'dl_sim_flag',
            0, 0, 1, 1,
        )
        checkbutton.set_sensitive(False)

        checkbutton2 = self.add_checkbutton(grid3,
            'Disable checking/downloading for this folder',
            'dl_disable_flag',
            0, 1, 1, 1,
        )
        checkbutton2.set_sensitive(False)

        checkbutton3 = self.add_checkbutton(grid3,
            'This folder is marked as a favourite',
            'fav_flag',
            0, 2, 1, 1,
        )
        checkbutton3.set_sensitive(False)

        checkbutton4 = self.add_checkbutton(grid3,
            'This folder is hidden',
            'hidden_flag',
            0, 3, 1, 1,
        )
        checkbutton4.set_sensitive(False)

        checkbutton5 = self.add_checkbutton(grid3,
            'This folder can\'t be deleted by the user',
            'fixed_flag',
            1, 0, 1, 1,
        )
        checkbutton5.set_sensitive(False)

        checkbutton6 = self.add_checkbutton(grid3,
            'This is a system-controlled folder',
            'priv_flag',
            1, 1, 1, 1,
        )
        checkbutton6.set_sensitive(False)

        checkbutton7 = self.add_checkbutton(grid3,
            'Only videos can be added to this folder',
            'restrict_flag',
            1, 2, 1, 1,
        )
        checkbutton7.set_sensitive(False)

        checkbutton8 = self.add_checkbutton(grid3,
            'All contents deleted when ' \
            + utils.upper_case_first(__main__. __packagename__) \
            + ' shuts down',
            'temp_flag',
            1, 3, 1, 1,
        )
        checkbutton8.set_sensitive(False)


#   def setup_download_options_tab():   # Inherited from GenericConfigWin


    # Callback class methods


#   def on_button_apply_clicked():  # Inherited from GenericConfigWin


#   def on_button_edit_clicked():   # Inherited from GenericConfigWin


#   def on_button_remove_clicked(): # Inherited from GenericConfigWin


    def never_called_func(self):

        """Function that is never called, but which makes this class object
        collapse neatly in my IDE."""

        pass


class SystemPrefWin(GenericPrefWin):

    """Python class for a 'preference window' to modify various system
    settings.

    Args:

        app_obj (mainapp.TartubeApp): The main application object

    """


    # Standard class methods


    def __init__(self, app_obj):


        Gtk.Window.__init__(self, title='System preferences')

        # IV list - class objects
        # -----------------------
        # The mainapp.TartubeApp object
        self.app_obj = app_obj


        # IV list - Gtk widgets
        # ---------------------
        self.grid = None                        # Gtk.Grid
        self.notebook = None                    # Gtk.Notebook
        self.ok_button = None                   # Gtk.Button
        # (IVs used to handle widget changes in the 'Videos' tab)
        self.radiobutton = None                 # Gkt.RadioButton
        self.radiobutton2 = None                # Gkt.RadioButton
        self.radiobutton3 = None                # Gkt.RadioButton
        self.spinbutton = None                  # Gkt.SpinButton
        self.spinbutton2 = None                 # Gkt.SpinButton


        # IV list - other
        # ---------------
        # Size (in pixels) of gaps between preference window widgets
        self.spacing_size = self.app_obj.default_spacing_size


        # Code
        # ----

        # Set up the preference window
        self.setup()


    # Public class methods


#   def setup():                # Inherited from GenericConfigWin


#   def setup_grid():           # Inherited from GenericConfigWin


#   def setup_notebook():       # Inherited from GenericConfigWin


#   def add_notebook_tab():     # Inherited from GenericConfigWin


#   def setup_button_strip():   # Inherited from GenericPrefWin


#   def setup_gap():            # Inherited from GenericConfigWin


    # (Setup tabs)


    def setup_tabs(self):

        """Called by self.setup(), .on_button_apply_clicked() and
        .on_button_reset_clicked().

        Sets up the tabs for this preference window.
        """

        self.setup_general_tab()
        self.setup_backups_tab()
        self.setup_windows_tab()
        self.setup_videos_tab()
        self.setup_scheduling_tab()
        self.setup_operations_tab()
        self.setup_ytdl_tab()
        self.setup_output_tab()


    def setup_general_tab(self):

        """Called by self.setup_tabs().

        Sets up the 'General' tab.
        """

        tab, grid = self.add_notebook_tab('_General')
        grid_width = 3

        # General preferences
        self.add_label(grid,
            '<u>General preferences</u>',
            0, 0, grid_width, 1,
        )

        label = self.add_label(grid,
            'Language',
            0, 1, 1, 1,
        )
        label.set_hexpand(False)

        # (This is a placeholder, to be replaced when we add translations)
        store = Gtk.ListStore(GdkPixbuf.Pixbuf, str)
        pixbuf = self.app_obj.main_win_obj.pixbuf_dict['flag_uk']
        store.append( [pixbuf, 'English'] )

        combo = Gtk.ComboBox.new_with_model(store)
        grid.attach(combo, 1, 1, (grid_width - 1), 1)
        combo.set_hexpand(True)

        renderer_pixbuf = Gtk.CellRendererPixbuf()
        combo.pack_start(renderer_pixbuf, False)
        combo.add_attribute(renderer_pixbuf, 'pixbuf', 0)

        renderer_text = Gtk.CellRendererText()
        combo.pack_start(renderer_text, True)
        combo.add_attribute(renderer_text, 'text', 1)

        combo.set_active(0)
        # (End of placeholder)

        label2 = self.add_label(grid,
            utils.upper_case_first(__main__. __packagename__) \
            + ' data directory',
            0, 2, 1, 1,
        )
        label2.set_hexpand(False)

        entry = self.add_entry(grid,
            self.app_obj.data_dir,
            False,
            1, 2, 1, 1,
        )
        entry.set_sensitive(False)

        button = Gtk.Button('Change')
        grid.attach(button, 2, 2, 1, 1)
        if self.app_obj.disable_load_save_flag:
            button.set_sensitive(False)
        # (signal_connect appears below)

        self.add_label(grid,
            'Size of device (in Mb)',
            0, 3, 1, 1,
        )

        entry2 = self.add_entry(grid,
            str(utils.disk_get_total_space(self.app_obj.data_dir)),
            False,
            1, 3, 2, 1,
        )
        entry2.set_sensitive(False)

        self.add_label(grid,
            'Free space on device (in Mb)',
            0, 4, 1, 1,
        )

        entry3 = self.add_entry(grid,
            str(utils.disk_get_free_space(self.app_obj.data_dir)),
            False,
            1, 4, 2, 1,
        )
        entry3.set_sensitive(False)

        # (signal_connect from above)
        button.connect(
            'clicked',
            self.on_data_dir_button_clicked,
            entry,
            entry2,
            entry3,
        )

        checkbutton = self.add_checkbutton(grid,
            'Warn user if disk space is below (Mb)',
            self.app_obj.disk_space_warn_flag,
            True,                   # Can be toggled by user
            0, 5, 1, 1,
        )
        # (signal_connect appears below)

        spinbutton = self.add_spinbutton(grid,
            0, None,
            self.app_obj.disk_space_increment,
            self.app_obj.disk_space_warn_limit,
            1, 5, 2, 1,
        )
        if not self.app_obj.disk_space_warn_flag:
            spinbutton.set_sensitive(False)
        # (signal_connect appears below)

        checkbutton2 = self.add_checkbutton(grid,
            'Halt downloads if disk space is below (Mb)',
            self.app_obj.disk_space_stop_flag,
            True,                   # Can be toggled by user
            0, 6, 1, 1,
        )
        # (signal_connect appears below)

        spinbutton2 = self.add_spinbutton(grid,
            0, None,
            self.app_obj.disk_space_increment,
            self.app_obj.disk_space_stop_limit,
            1, 6, 2, 1,
        )
        if not self.app_obj.disk_space_stop_flag:
            spinbutton2.set_sensitive(False)
        # (signal_connect appears below)

        # (signal_connect from above)
        checkbutton.connect(
            'toggled',
            self.on_disk_warn_button_toggled,
            spinbutton,
        )
        spinbutton.connect(
            'value-changed',
            self.on_disk_warn_spinbutton_changed,
        )
        checkbutton2.connect(
            'toggled',
            self.on_disk_stop_button_toggled,
            spinbutton2,
        )
        spinbutton2.connect(
            'value-changed',
            self.on_disk_stop_spinbutton_changed,
        )

        # Module preferences
        self.add_label(grid,
            '<u>Module preferences</u>',
            0, 7, grid_width, 1,
        )

        checkbutton3 = self.add_checkbutton(grid,
            'Use \'moviepy\' module to get a video\'s duration, if not known'
            + ' (may be slow)',
            self.app_obj.use_module_moviepy_flag,
            True,                   # Can be toggled by user
            0, 8, grid_width, 1,
        )
        checkbutton3.connect('toggled', self.on_moviepy_button_toggled)
        if not mainapp.HAVE_MOVIEPY_FLAG:
            checkbutton3.set_sensitive(False)

        self.add_label(grid,
            'Timeout applied when moviepy checks a video file',
            0, 9, grid_width, 1,
        )

        spinbutton3 = self.add_spinbutton(grid,
            0,
            60,
            1,                  # Step
            self.app_obj.refresh_moviepy_timeout,
            1, 9, 2, 1,
        )
        spinbutton3.connect(
            'value-changed',
            self.on_moviepy_timeout_spinbutton_changed,
        )

        # Gtk support
        self.add_label(grid,
            '<u>Gtk support</u>',
            0, 10, grid_width, 1,
        )

        self.add_label(grid,
            'Current version of the system\'s Gtk library',
            0, 11, 1, 1
        )

        entry4 = self.add_entry(grid,
            'v' + str(self.app_obj.gtk_version_major) + '.' \
            + str(self.app_obj.gtk_version_minor) + '.' \
            + str(self.app_obj.gtk_version_micro),
            False,
            1, 11, 2, 1,
        )
        entry4.set_sensitive(False)

        checkbutton4 = self.add_checkbutton(grid,
            'Some features are disabled because this version of the library' \
            + ' is broken',
            self.app_obj.gtk_broken_flag,
            False,               # Can't be toggled by user
            0, 12, grid_width, 1,
        )
        checkbutton4.set_hexpand(False)


    def setup_backups_tab(self):

        """Called by self.setup_tabs().

        Sets up the 'Backups' tab.
        """

        tab, grid = self.add_notebook_tab('_Backups')

        # Backup preferences
        self.add_label(grid,
            '<u>Backup preferences</u>',
            0, 0, 1, 1,
        )
        self.add_label(grid,
            'When saving a database file, ' \
            + utils.upper_case_first(__main__. __packagename__) \
            + ' makes a backup copy of it (in case something goes wrong)',
            0, 1, 1, 1,
        )

        radiobutton = self.add_radiobutton(grid,
            None,
            'Delete the backup file as soon as the save procedure is' \
            + ' finished',
            0, 2, 1, 1,
        )
        # Signal connect appears below

        radiobutton2 = self.add_radiobutton(grid,
            radiobutton,
            'Keep the backup file, replacing any previous backup file',
            0, 3, 1, 1,
        )
        if self.app_obj.db_backup_mode == 'single':
            radiobutton2.set_active(True)
        # Signal connect appears below

        radiobutton3 = self.add_radiobutton(grid,
            radiobutton2,
            'Make a new backup file once per day, after the day\'s first' \
            + ' save procedure',
            0, 4, 1, 1,
        )
        if self.app_obj.db_backup_mode == 'daily':
            radiobutton3.set_active(True)
        # Signal connect appears below

        radiobutton4 = self.add_radiobutton(grid,
            radiobutton3,
            'Make a new backup file for every save procedure',
            0, 5, 1, 1,
        )
        if self.app_obj.db_backup_mode == 'always':
            radiobutton4.set_active(True)
        # Signal connect appears below

        # Signal connects from above
        radiobutton.connect(
            'toggled',
            self.on_backup_button_toggled,
            'default',
        )

        radiobutton2.connect(
            'toggled',
            self.on_backup_button_toggled,
            'single',
        )

        radiobutton3.connect(
            'toggled',
            self.on_backup_button_toggled,
            'daily',
        )

        radiobutton4.connect(
            'toggled',
            self.on_backup_button_toggled,
            'always',
        )


    def setup_windows_tab(self):

        """Called by self.setup_tabs().

        Sets up the 'Windows' tab.
        """

        tab, grid = self.add_notebook_tab('_Windows')

        # Main window preferences
        self.add_label(grid,
            '<u>Main window preferences</u>',
            0, 0, 1, 1,
        )

        checkbutton = self.add_checkbutton(grid,
            'Don\'t show labels in the toolbar',
            self.app_obj.toolbar_squeeze_flag,
            True,                   # Can be toggled by user
            0, 1, 1, 1,
        )
        checkbutton.connect('toggled', self.on_squeeze_button_toggled)

        checkbutton2 = self.add_checkbutton(grid,
            'Show tooltips for videos, channels, playlists and folders',
            self.app_obj.show_tooltips_flag,
            True,                   # Can be toggled by user
            0, 2, 1, 1,
        )
        checkbutton2.connect('toggled', self.on_show_tooltips_toggled)

        checkbutton3 = self.add_checkbutton(grid,
            'Show smaller icons in the Video Index (left side of the' \
            + ' \'Videos\' tab)',
            self.app_obj.show_small_icons_in_index,
            True,                   # Can be toggled by user
            0, 3, 1, 1,
        )
        checkbutton3.connect('toggled', self.on_show_small_icons_toggled)

        checkbutton4 = self.add_checkbutton(grid,
            'After clicking on a folder, automatically expand the Video' \
            + ' Index beneath it',
            self.app_obj.auto_expand_video_index_flag,
            True,                   # Can be toggled by user
            0, 4, 1, 1,
        )
        checkbutton4.connect('toggled', self.on_expand_tree_toggled)

        checkbutton5 = self.add_checkbutton(grid,
            'Disable the \'Download all\' buttons in the toolbar and the' \
            + ' \'Videos\' tab',
            self.app_obj.disable_dl_all_flag,
            True,                   # Can be toggled by user
            0, 5, 1, 1,
        )
        checkbutton5.connect('toggled', self.on_disable_dl_all_toggled)

        checkbutton6 = self.add_checkbutton(grid,
            'Show results in reverse order (most recently checked/' \
            + 'downloaded video first)',
            self.app_obj.results_list_reverse_flag,
            True,                   # Can be toggled by user
            0, 6, 1, 1,
        )
        checkbutton6.connect('toggled', self.on_reverse_button_toggled)

        checkbutton7 = self.add_checkbutton(grid,
            'Don\'t remove number of system messages from tab label until' \
            + ' \'Clear\' button is clicked',
            self.app_obj.system_msg_keep_totals_flag,
            True,                   # Can be toggled by user
            0, 7, 1, 1,
        )
        checkbutton7.connect('toggled', self.on_system_keep_button_toggled)

        # System tray preferences
        self.add_label(grid,
            '<u>System tray preferences</u>',
            0, 8, 1, 1,
        )

        checkbutton8 = self.add_checkbutton(grid,
            'Show icon in system tray',
            self.app_obj.show_status_icon_flag,
            True,               # Can be toggled by user
            0, 9, 1, 1,
        )
        checkbutton8.set_hexpand(False)
        # signal connnect appears below

        checkbutton9 = self.add_checkbutton(grid,
            'Close to the tray, rather than closing the application',
            self.app_obj.close_to_tray_flag,
            True,               # Can be toggled by user
            0, 10, 1, 1,
        )
        checkbutton9.set_hexpand(False)
        checkbutton9.connect('toggled', self.on_close_to_tray_toggled)
        if not self.app_obj.show_status_icon_flag:
            checkbutton9.set_sensitive(False)

        # signal connect from above
        checkbutton8.connect(
            'toggled',
            self.on_show_status_icon_toggled,
            checkbutton9,
        )

        # Dialogue window preferences
        self.add_label(grid,
            '<u>Dialogue window preferences</u>',
            0, 11, 1, 1,
        )

        checkbutton10 = self.add_checkbutton(grid,
            'When adding channels/playlists, keep the dialogue window open',
            self.app_obj.dialogue_keep_open_flag,
            True,               # Can be toggled by user
            0, 12, 1, 1,
        )
        checkbutton10.set_hexpand(False)
        # signal connnect appears below

        checkbutton11 = self.add_checkbutton(grid,
            'When adding videos/channels/playlists, copy URLs from the' \
            + ' system clipboard',
            self.app_obj.dialogue_copy_clipboard_flag,
            True,               # Can be toggled by user
            0, 13, 1, 1,
        )
        checkbutton11.set_hexpand(False)
        checkbutton11.connect('toggled', self.on_clipboard_button_toggled)
        if self.app_obj.dialogue_keep_open_flag:
            checkbutton11.set_sensitive(False)

        # signal connect from above
        checkbutton10.connect(
            'toggled',
            self.on_keep_open_button_toggled,
            checkbutton11,
        )

        # Error/warning preferences
        self.add_label(grid,
            '<u>Error/warning preferences</u>',
            0, 14, 1, 1,
        )

        checkbutton12 = self.add_checkbutton(grid,
            'Show system error messages in the \'Errors/Warnings\' tab',
            self.app_obj.system_error_show_flag,
            True,                   # Can be toggled by user
            0, 15, 1, 1,
        )
        checkbutton12.connect('toggled', self.on_error_button_toggled)

        checkbutton13 = self.add_checkbutton(grid,
            'Show system warning messages in the \'Errors/Warnings\' tab',
            self.app_obj.system_warning_show_flag,
            True,                   # Can be toggled by user
            0, 16, 1, 1,
        )
        checkbutton13.connect('toggled', self.on_warning_button_toggled)

        checkbutton14 = self.add_checkbutton(grid,
            'Ignore \'Requested formats are incompatible for merge\' warnings',
            self.app_obj.ignore_merge_warning_flag,
            True,                   # Can be toggled by user
            0, 17, 1, 1,
        )
        checkbutton14.connect('toggled', self.on_merge_button_toggled)

        checkbutton15 = self.add_checkbutton(grid,
            'Ignore YouTube copyright errors',
            self.app_obj.ignore_yt_copyright_flag,
            True,                   # Can be toggled by user
            0, 18, 1, 1,
        )
        checkbutton15.connect('toggled', self.on_copyright_button_toggled)

        checkbutton16 = self.add_checkbutton(grid,
            'Ignore \'Child process exited with non-zero code\' errors',
            self.app_obj.ignore_child_process_exit_flag,
            True,                   # Can be toggled by user
            0, 19, 1, 1,
        )
        checkbutton16.connect('toggled', self.on_child_process_button_toggled)

        checkbutton17 = self.add_checkbutton(grid,
            'Ignore \'There are no annotations to write\' warnings',
            self.app_obj.ignore_no_annotations_flag,
            True,                   # Can be toggled by user
            0, 20, 1, 1,
        )
        checkbutton17.connect('toggled', self.on_no_annotations_button_toggled)

        checkbutton18 = self.add_checkbutton(grid,
            'Ignore \'Video doesn\'t have subtitles\' warnings',
            self.app_obj.ignore_no_subtitles_flag,
            True,                   # Can be toggled by user
            0, 21, 1, 1,
        )
        checkbutton18.connect('toggled', self.on_no_subtitles_button_toggled)


    def setup_videos_tab(self):

        """Called by self.setup_tabs().

        Sets up the 'Videos' tab.
        """

        tab, grid = self.add_notebook_tab('_Videos')
        grid_width = 2

        # Video matching preferences
        self.add_label(grid,
            '<u>Video matching preferences</u>',
            0, 0, grid_width, 1,
        )

        self.add_label(grid,
            'When matching videos on the filesystem:',
            0, 1, grid_width, 1,
        )

        self.radiobutton = self.add_radiobutton(grid,
            None,
            'The video names must match exactly',
            0, 2, grid_width, 1,
        )
        # Signal connect appears below

        self.radiobutton2 = self.add_radiobutton(grid,
            self.radiobutton,
            'The first n characters must match exactly',
            0, 3, (grid_width - 1), 1,
        )
        # Signal connect appears below

        self.spinbutton = self.add_spinbutton(grid,
            1, 999, 1, self.app_obj.match_first_chars,
            2, 3, 1, 1,
        )
        # Signal connect appears below

        self.radiobutton3 = self.add_radiobutton(grid,
            self.radiobutton2,
            'Ignore the last n characters; the remaining name must match' \
            + ' exactly',
            0, 4, (grid_width - 1), 1,
        )
        # Signal connect appears below

        self.spinbutton2 = self.add_spinbutton(grid,
            1, 999, 1, self.app_obj.match_ignore_chars,
            2, 4, 1, 1,
        )
        # Signal connect appears below

        self.add_label(grid,
            'In the Video Index (the left side of the \'Videos\' tab):',
            0, 5, grid_width, 1,
        )

        checkbutton = self.add_checkbutton(grid,
            'Show detailed statistics about the videos in each channel' \
            + ' / playlist / folder',
            self.app_obj.complex_index_flag,
            True,               # Can be toggled by user
            0, 6, grid_width, 1,
        )
        checkbutton.connect('toggled', self.on_complex_button_toggled)

        # (Widgets are sensitised/desensitised, based on the radiobutton)
        if self.app_obj.match_method == 'exact_match':
            self.spinbutton.set_sensitive(False)
            self.spinbutton2.set_sensitive(False)
        elif self.app_obj.match_method == 'match_first':
            self.radiobutton2.set_active(True)
            self.spinbutton2.set_sensitive(False)
        else:
            self.radiobutton3.set_active(True)
            self.spinbutton.set_sensitive(False)

        # Signal connects from above
        self.radiobutton.connect('toggled', self.on_match_button_toggled)
        self.radiobutton2.connect('toggled', self.on_match_button_toggled)
        self.radiobutton3.connect('toggled', self.on_match_button_toggled)
        self.spinbutton.connect(
            'value-changed',
            self.on_match_spinbutton_changed,
        )
        self.spinbutton2.connect(
            'value-changed',
            self.on_match_spinbutton_changed,
        )

        # Automatic video deletion preferences
        self.add_label(grid,
            '<u>Automatic video deletion preferences</u>',
            0, 7, grid_width, 1,
        )

        checkbutton2 = self.add_checkbutton(grid,
            'Automatically delete downloaded videos after this many days',
            self.app_obj.auto_delete_flag,
            True,               # Can be toggled by user
            0, 8, (grid_width - 1), 1,
        )
        # Signal connect appears below

        spinbutton3 = self.add_spinbutton(grid,
            1, 999, 1, self.app_obj.auto_delete_days,
            2, 8, 1, 1,
        )
        # Signal connect appears below

        checkbutton3 = self.add_checkbutton(grid,
            '...but only delete videos which have been watched',
            self.app_obj.auto_delete_watched_flag,
            True,               # Can be toggled by user
            0, 9, grid_width, 1,
        )
        # Signal connect appears below

        # Signal connects from above
        checkbutton2.connect(
            'toggled',
            self.on_auto_delete_button_toggled,
            spinbutton3,
            checkbutton2,
        )
        spinbutton3.connect(
            'value-changed',
            self.on_auto_delete_spinbutton_changed,
        )
        checkbutton3.connect('toggled', self.on_delete_watched_button_toggled)

        # Temporary folder preferences
        self.add_label(grid,
            '<u>Temporary folder preferences</u>',
            0, 10, grid_width, 1,
        )

        checkbutton4 = self.add_checkbutton(grid,
            'Empty temporary folders when ' \
            + utils.upper_case_first(__main__. __packagename__) \
            + ' shuts down',

            self.app_obj.delete_on_shutdown_flag,
            True,               # Can be toggled by user
            0, 11, grid_width, 1,
        )
        checkbutton4.connect('toggled', self.on_delete_shutdown_button_toggled)

        self.add_label(grid,
            '<i>(N.B. Temporary folders are always emptied when ' \
            + utils.upper_case_first(__main__. __packagename__) \
            + ' starts up)</i>',
            0, 12, grid_width, 1,
        )


    def setup_scheduling_tab(self):

        """Called by self.setup_tabs().

        Sets up the 'Scheduling' tab.
        """

        tab, grid = self.add_notebook_tab('_Scheduling')
        grid_width = 2

        # Scheduling preferences
        self.add_label(grid,
            '<u>Scheduling preferences</u>',
            0, 0, grid_width, 1,
        )

        self.add_label(grid,
            'Automatic \'Download all\' operations',
            0, 1, 1, 1,
        )

        store = Gtk.ListStore(str, str)

        script = utils.upper_case_first(__main__.__packagename__)
        store.append( ['none', 'Disabled'] )
        store.append( ['start', 'Performed when ' + script + ' starts'] )
        store.append( ['scheduled', 'Performed at regular intervals'] )

        combo = Gtk.ComboBox.new_with_model(store)
        grid.attach(combo, 1, 1, 1, 1)
        combo.set_hexpand(True)

        renderer_text = Gtk.CellRendererText()
        combo.pack_start(renderer_text, True)
        combo.add_attribute(renderer_text, 'text', 1)
        combo.set_entry_text_column(1)

        if self.app_obj.scheduled_dl_mode == 'start':
            combo.set_active(1)
        elif self.app_obj.scheduled_dl_mode == 'scheduled':
            combo.set_active(2)
        else:
            combo.set_active(0)
        # Signal connect appears below

        self.add_label(grid,
            'Time (in hours) between operations',
            0, 2, 1, 1,
        )

        spinbutton = self.add_spinbutton(grid,
            1, 999, 1, self.app_obj.scheduled_dl_wait_hours,
            1, 2, 1, 1,
        )
        if self.app_obj.scheduled_dl_mode != 'scheduled':
             spinbutton.set_sensitive(False)
        # Signal connect appears below

        self.add_label(grid,
            'Automatic \'Check all\' operations',
            0, 3, 1, 1,
        )

        store2 = Gtk.ListStore(str, str)

        script = utils.upper_case_first(__main__.__packagename__)
        store2.append( ['none', 'Disabled'] )
        store2.append( ['start', 'Performed when ' + script + ' starts'] )
        store2.append( ['scheduled', 'Performed at regular intervals'] )

        combo2 = Gtk.ComboBox.new_with_model(store2)
        grid.attach(combo2, 1, 3, 1, 1)
        combo.set_hexpand(True)

        renderer_text = Gtk.CellRendererText()
        combo2.pack_start(renderer_text, True)
        combo2.add_attribute(renderer_text, 'text', 1)
        combo2.set_entry_text_column(1)

        if self.app_obj.scheduled_check_mode == 'start':
            combo2.set_active(1)
        elif self.app_obj.scheduled_check_mode == 'scheduled':
            combo2.set_active(2)
        else:
            combo2.set_active(0)
        # Signal connect appears below

        self.add_label(grid,
            'Time (in hours) between operations',
            0, 4, 1, 1,
        )

        spinbutton2 = self.add_spinbutton(grid,
            1, 999, 1, self.app_obj.scheduled_check_wait_hours,
            1, 4, 1, 1,
        )
        if self.app_obj.scheduled_check_mode != 'scheduled':
            spinbutton2.set_sensitive(False)
        # Signal connect appears below

        checkbutton = self.add_checkbutton(grid,
            'After an automatic \'Download/Check all\' operation, shut down' \
            + script,
            self.app_obj.scheduled_stop_flag,
            True,                   # Can be toggled by user
            0, 5, grid_width, 1,
        )

        # Signal connects from above
        combo.connect('changed', self.on_dl_mode_combo_changed, spinbutton)
        spinbutton.connect('value-changed', self.on_dl_wait_spinbutton_changed)
        combo2.connect(
            'changed',
            self.on_check_mode_combo_changed,
            spinbutton2,
        )
        spinbutton2.connect(
            'value-changed',
            self.on_check_wait_spinbutton_changed,
        )
        checkbutton.connect('toggled', self.on_scheduled_stop_button_toggled)


    def setup_operations_tab(self):

        """Called by self.setup_tabs().

        Sets up the 'Operations' tab.
        """

        tab, grid = self.add_notebook_tab('_Operations')
        grid_width = 3

        # Operation preferences
        self.add_label(grid,
            '<u>Operation preferences</u>',
            0, 0, grid_width, 1,
        )

        checkbutton = self.add_checkbutton(grid,
            'Automatically update youtube-dl before every download operation',
            self.app_obj.operation_auto_update_flag,
            True,                   # Can be toggled by user
            0, 1, grid_width, 1,
        )
        checkbutton.connect('toggled', self.on_auto_update_button_toggled)
        if __main__.__debian_install_flag__:
            checkbutton.set_sensitive(False)

        checkbutton2 = self.add_checkbutton(grid,
            'Automatically save files at the end of a download/update/' \
            + 'refresh operation',
            self.app_obj.operation_save_flag,
            True,                   # Can be toggled by user
            0, 2, grid_width, 1,
        )
        checkbutton2.connect('toggled', self.on_save_button_toggled)

        # Notification preferences
        self.add_label(grid,
            '<u>Notification preferences</u>',
            0, 3, grid_width, 1,
        )

        radiobutton = self.add_radiobutton(grid,
            None,
            'Show a dialogue window at the end of a download/update/refresh' \
            + ' operation',
            0, 4, grid_width, 1,
        )
        # Signal connect appears below

        radiobutton2 = self.add_radiobutton(grid,
            radiobutton,
            'Show a desktop notification at the end of a download/update/' \
            + ' refresh operation',
            0, 5, grid_width, 1,
        )
        if self.app_obj.operation_dialogue_mode == 'desktop':
            radiobutton2.set_active(True)
        if os.name == 'nt':
            radiobutton2.set_sensitive(False)
        # Signal connect appears below

        radiobutton3 = self.add_radiobutton(grid,
            radiobutton2,
            'Don\'t notify the user at the end of a download/update/refresh' \
            + ' operation',
            0, 6, grid_width, 1,
        )
        if self.app_obj.operation_dialogue_mode == 'default':
            radiobutton3.set_active(True)
        # Signal connect appears below

        # Signal connects from above
        radiobutton.connect(
            'toggled',
            self.on_dialogue_button_toggled,
            'dialogue',
        )
        radiobutton2.connect(
            'toggled',
            self.on_dialogue_button_toggled,
            'desktop',
        )
        radiobutton3.connect(
            'toggled',
            self.on_dialogue_button_toggled,
            'default',
        )

        # URL flexibility preferences
        self.add_label(grid,
            '<u>URL flexibility preferences</u>',
            0, 7, grid_width, 1,
        )

        radiobutton4 = self.add_radiobutton(grid,
            None,
            'If a video\'s URL represents a channel/playlist, not a video,' \
            + ' don\'t download it',
            0, 8, grid_width, 1,
        )
        # Signal connect appears below

        radiobutton5 = self.add_radiobutton(grid,
            radiobutton4,
#            'If a URL represents a channel/playlist, not a video, download' \
#            + ' multiple videos',
            '...or, download multiple videos into the containing folder',
            0, 9, grid_width, 1,
        )
        if self.app_obj.operation_convert_mode == 'multi':
            radiobutton5.set_active(True)
        # Signal connect appears below

        radiobutton6 = self.add_radiobutton(grid,
            radiobutton5,
#            'If a URL represents a channel/playlist, not a video, convert' \
#            + ' the video to a channel',
            '...or, create a new channel, and download the videos into that',
            0, 10, grid_width, 1,
        )
        if self.app_obj.operation_convert_mode == 'channel':
            radiobutton6.set_active(True)
        # Signal connect appears below

        radiobutton7 = self.add_radiobutton(grid,
            radiobutton6,
#            'If a URL represents a channel/playlist, not a video, convert' \
#            + ' the video to a playlist',
            '...or, create a new playlist, and download the videos into that',
            0, 11, grid_width, 1,
        )
        if self.app_obj.operation_convert_mode == 'playlist':
            radiobutton7.set_active(True)
        # Signal connect appears below

        # Signal connects from above
        radiobutton4.connect(
            'toggled',
            self.on_convert_from_button_toggled,
            'disable',
        )
        radiobutton5.connect(
            'toggled',
            self.on_convert_from_button_toggled,
            'multi',
        )
        radiobutton6.connect(
            'toggled',
            self.on_convert_from_button_toggled,
            'channel',
        )
        radiobutton7.connect(
            'toggled',
            self.on_convert_from_button_toggled,
            'playlist',
        )

        # Performance limits
        self.add_label(grid,
            '<u>Performance limits</u>',
            0, 12, grid_width, 1,
        )

        checkbutton3 = self.add_checkbutton(grid,
            'Limit simultaneous downloads to',
            self.app_obj.num_worker_apply_flag,
            True,               # Can be toggled by user
            0, 13, 1, 1,
        )
        checkbutton3.set_hexpand(False)
        checkbutton3.connect('toggled', self.on_worker_button_toggled)

        spinbutton = self.add_spinbutton(grid,
            self.app_obj.num_worker_min,
            self.app_obj.num_worker_max,
            1,                  # Step
            self.app_obj.num_worker_default,
            1, 13, 1, 1,
        )
        spinbutton.connect('value-changed', self.on_worker_spinbutton_changed)

        checkbutton4 = self.add_checkbutton(grid,
            'Limit download speed to',
            self.app_obj.bandwidth_apply_flag,
            True,               # Can be toggled by user
            0, 14, 1, 1,
        )
        checkbutton4.set_hexpand(False)
        checkbutton4.connect('toggled', self.on_bandwidth_button_toggled)

        spinbutton2 = self.add_spinbutton(grid,
            self.app_obj.bandwidth_min,
            self.app_obj.bandwidth_max,
            1,                  # Step
            self.app_obj.bandwidth_default,
            1, 14, 1, 1,
        )
        spinbutton2.connect(
            'value-changed',
            self.on_bandwidth_spinbutton_changed,
        )

        self.add_label(grid,
            'KiB/s',
            2, 14, 1, 1,
        )

        checkbutton5 = self.add_checkbutton(grid,
            'Limit video resolution (overriding video format options) to',
            self.app_obj.video_res_apply_flag,
            True,               # Can be toggled by user
            0, 15, 1, 1,
        )
        checkbutton5.set_hexpand(False)
        checkbutton5.connect('toggled', self.on_video_res_button_toggled)

        combo = self.add_combo(grid,
            formats.VIDEO_RESOLUTION_LIST,
            None,
            1, 15, 1, 1,
        )
        combo.set_active(
            formats.VIDEO_RESOLUTION_LIST.index(
                self.app_obj.video_res_default,
            )
        )
        combo.connect('changed', self.on_video_res_combo_changed)

        # Time-saving preferences
        self.add_label(grid,
            '<u>Time-saving preferences</u>',
            0, 16, grid_width, 1,
        )

        checkbutton6 = self.add_checkbutton(grid,
            'Stop checking/downloading a channel/playlist when it starts' \
            + ' sending videos we already have',
            self.app_obj.operation_limit_flag,
            True,               # Can be toggled by user
            0, 17, grid_width, 1,
        )
        checkbutton6.set_hexpand(False)
        # Signal connect appears below

        self.add_label(grid,
            'Stop after this many videos (when checking)',
            0, 18, 1, 1,
        )

        entry = self.add_entry(grid,
            self.app_obj.operation_check_limit,
            True,
            1, 18, 1, 1,
        )
        entry.set_hexpand(False)
        entry.set_width_chars(4)
        entry.connect('changed', self.on_check_limit_changed)
        if not self.app_obj.operation_limit_flag:
            entry.set_sensitive(False)

        self.add_label(grid,
            'Stop after this many videos (when downloading)',
            0, 19, 1, 1,
        )

        entry2 = self.add_entry(grid,
            self.app_obj.operation_download_limit,
            True,
            1, 19, 1, 1,
        )
        entry2.set_hexpand(False)
        entry2.set_width_chars(4)
        entry2.connect('changed', self.on_download_limit_changed)
        if not self.app_obj.operation_limit_flag:
            entry2.set_sensitive(False)

        # Signal connect from above
        checkbutton6.connect(
            'toggled',
            self.on_limit_button_toggled,
            entry,
            entry2,
        )

        # Download options preferences
        self.add_label(grid,
            '<u>Download options preferences</u>',
            0, 20, grid_width, 1,
        )

        checkbutton7 = self.add_checkbutton(grid,
            'When applying download options, automatically clone general' \
            + ' download options',
            self.app_obj.auto_clone_options_flag,
            True,               # Can be toggled by user
            0, 21, grid_width, 1,
        )
        checkbutton7.set_hexpand(False)
        checkbutton7.connect('toggled', self.on_auto_clone_button_toggled)


    def setup_ytdl_tab(self):

        """Called by self.setup_tabs().

        Sets up the 'youtube-dl' tab.
        """

        tab, grid = self.add_notebook_tab('_youtube-dl')
        grid_width = 4

        # youtube-dl preferences
        self.add_label(grid,
            '<u>youtube-dl preferences</u>',
            0, 0, grid_width, 1,
        )


        label = self.add_label(grid,
            'youtube-dl executable (system-dependant)',
            0, 1, 1, 1,
        )

        entry = self.add_entry(grid,
            self.app_obj.ytdl_bin,
            False,
            1, 1, (grid_width - 1), 1,
        )
        entry.set_sensitive(True)
        entry.set_editable(False)

        label2 = self.add_label(grid,
            'Default path to youtube-dl executable',
            0, 2, 1, 1,
        )

        entry2 = self.add_entry(grid,
            self.app_obj.ytdl_path_default,
            False,
            1, 2, (grid_width - 1), 1,
        )
        entry2.set_sensitive(True)
        entry2.set_editable(False)

        label3 = self.add_label(grid,
            'Actual path to use',
            0, 3, 1, 1,
        )

        combo_list = [
            [
                'Use default path (' + self.app_obj.ytdl_path_default \
                + ')',
                self.app_obj.ytdl_path_default,
            ],
            [
                'Use local path (' + self.app_obj.ytdl_bin + ')',
                self.app_obj.ytdl_bin,
            ],
        ]

        store = Gtk.ListStore(str, str)
        for mini_list in combo_list:
            store.append( [ mini_list[0], mini_list[1] ] )

        combo = Gtk.ComboBox.new_with_model(store)
        grid.attach(combo, 1, 3, (grid_width - 1), 1)
        renderer_text = Gtk.CellRendererText()
        combo.pack_start(renderer_text, True)
        combo.add_attribute(renderer_text, 'text', 0)
        combo.set_entry_text_column(0)

        if self.app_obj.ytdl_path == self.app_obj.ytdl_path_default:
            combo.set_active(0)
        else:
            combo.set_active(1)

        combo.connect('changed', self.on_ytdl_path_combo_changed)

        label4 = self.add_label(grid,
            'Shell command for update operations',
            0, 4, 1, 1,
        )

        combo2 = self.add_combo(grid,
            self.app_obj.ytdl_update_list,
            self.app_obj.ytdl_update_current,
            1, 4, (grid_width - 1), 1,
        )
        combo2.connect('changed', self.on_update_combo_changed)

        if __main__.__debian_install_flag__:
            combo.set_sensitive(False)
            combo2.set_sensitive(False)

        # Post-processing preferences
        self.add_label(grid,
            '<u>Post-processing preferences</u>',
            0, 5, grid_width, 1,
        )

        self.add_label(grid,
            'Path to the ffmpeg/avconv binary',
            0, 6, 1, 1,
        )

        entry3 = self.add_entry(grid,
            self.app_obj.ffmpeg_path,
            False,
            1, 6, 1, 1,
        )
        entry3.set_sensitive(True)
        entry3.set_editable(False)
        entry3.set_hexpand(True)

        button = Gtk.Button('Set')
        grid.attach(button, 2, 6, 1, 1)
        button.connect('clicked', self.on_set_ffmpeg_button_clicked, entry3)

        button2 = Gtk.Button('Reset')
        grid.attach(button2, 3, 6, 1, 1)
        button2.connect('clicked', self.on_reset_ffmpeg_button_clicked, entry3)

        if os.name == 'nt':
            entry3.set_sensitive(False)
            entry3.set_text('Install from main menu')
            button.set_sensitive(False)
            button2.set_sensitive(False)

        # Other preferences
        self.add_label(grid,
            '<u>Other preferences</u>',
            0, 7, grid_width, 1,
        )

        checkbutton = self.add_checkbutton(grid,
            'Allow youtube-dl to create its own archive (so deleted videos' \
            + ' are not re-downloaded)',
            self.app_obj.allow_ytdl_archive_flag,
            True,                   # Can be toggled by user
            0, 8, grid_width, 1,
        )
        checkbutton.connect('toggled', self.on_archive_button_toggled)

        checkbutton2 = self.add_checkbutton(grid,
            'When checking videos, apply a 60-second timeout while fetching' \
            + ' JSON data',
            self.app_obj.apply_json_timeout_flag,
            True,                   # Can be toggled by user
            0, 9, grid_width, 1,
        )
        checkbutton2.connect('toggled', self.on_json_button_toggled)


    def setup_output_tab(self):

        """Called by self.setup_tabs().

        Sets up the 'Output' tab.
        """

        tab, grid = self.add_notebook_tab('O_utput')

        # Output Tab preferences
        self.add_label(grid,
            '<u>Output Tab preferences</u>',
            0, 0, 1, 1,
        )


        checkbutton = self.add_checkbutton(grid,
            'Display youtube-dl system commands in the Output Tab',
            self.app_obj.ytdl_output_system_cmd_flag,
            True,               # Can be toggled by user
            0, 1, 1, 1,
        )
        checkbutton.set_hexpand(False)
        checkbutton.connect('toggled', self.on_output_system_button_toggled)

        checkbutton2 = self.add_checkbutton(grid,
            'Display output from youtube-dl\'s STDOUT in the Output Tab',
            self.app_obj.ytdl_output_stdout_flag,
            True,               # Can be toggled by user
            0, 2, 1, 1,
        )
        checkbutton2.set_hexpand(False)
        # Signal connect appears below

        checkbutton3 = self.add_checkbutton(grid,
            '...but don\'t write each video\'s JSON data',
            self.app_obj.ytdl_output_ignore_json_flag,
            True,               # Can be toggled by user
            0, 3, 1, 1,
        )
        checkbutton3.set_hexpand(False)
        checkbutton3.connect('toggled', self.on_output_json_button_toggled)
        if not self.app_obj.ytdl_output_stdout_flag:
            checkbutton3.set_sensitive(False)

        checkbutton4 = self.add_checkbutton(grid,
            '...but don\'t write each video\'s download progress',
            self.app_obj.ytdl_output_ignore_progress_flag,
            True,               # Can be toggled by user
            0, 4, 1, 1,
        )
        checkbutton4.set_hexpand(False)
        checkbutton4.connect('toggled', self.on_output_progress_button_toggled)
        if not self.app_obj.ytdl_output_stdout_flag:
            checkbutton4.set_sensitive(False)

        # Signal connect from above
        checkbutton2.connect(
            'toggled',
            self.on_output_stdout_button_toggled,
            checkbutton3,
            checkbutton4,
        )

        checkbutton5 = self.add_checkbutton(grid,
            'Display output from youtube-dl\'s STDERR in the Output Tab',
            self.app_obj.ytdl_output_stderr_flag,
            True,               # Can be toggled by user
            0, 5, 1, 1,
        )
        checkbutton5.set_hexpand(False)
        checkbutton5.connect('toggled', self.on_output_stderr_button_toggled)

        checkbutton6 = self.add_checkbutton(grid,
            'Empty pages in the Output Tab at the start of every operation',
            self.app_obj.ytdl_output_start_empty_flag,
            True,               # Can be toggled by user
            0, 6, 1, 1,
        )
        checkbutton6.set_hexpand(False)
        checkbutton6.connect('toggled', self.on_output_empty_button_toggled)

        checkbutton7 = self.add_checkbutton(grid,
            'Show a summary of active threads (changes are applied when ' \
            + utils.upper_case_first(__main__.__packagename__) + ' restarts',
            self.app_obj.ytdl_output_show_summary_flag,
            True,               # Can be toggled by user
            0, 7, 1, 1,
        )
        checkbutton7.set_hexpand(False)
        checkbutton7.connect('toggled', self.on_output_summary_button_toggled)

        # Terminal window preferences
        self.add_label(grid,
            '<u>Terminal window preferences</u>',
            0, 8, 1, 1,
        )

        checkbutton8 = self.add_checkbutton(grid,
            'Write youtube-dl system commands to the terminal window',
            self.app_obj.ytdl_write_system_cmd_flag,
            True,               # Can be toggled by user
            0, 9, 1, 1,
        )
        checkbutton8.set_hexpand(False)
        checkbutton8.connect('toggled', self.on_terminal_system_button_toggled)

        checkbutton9 = self.add_checkbutton(grid,
            'Write output from youtube-dl\'s STDOUT to the terminal window',
            self.app_obj.ytdl_write_stdout_flag,
            True,               # Can be toggled by user
            0, 10, 1, 1,
        )
        checkbutton9.set_hexpand(False)
        # Signal connect appears below

        checkbutton10 = self.add_checkbutton(grid,
            '...but don\'t write each video\'s JSON data',
            self.app_obj.ytdl_write_ignore_json_flag,
            True,               # Can be toggled by user
            0, 11, 1, 1,
        )
        checkbutton10.set_hexpand(False)
        checkbutton10.connect('toggled', self.on_terminal_json_button_toggled)
        if not self.app_obj.ytdl_write_stdout_flag:
            checkbutton10.set_sensitive(False)

        checkbutton11 = self.add_checkbutton(grid,
            '...but don\'t write each video\'s download progress',
            self.app_obj.ytdl_write_ignore_progress_flag,
            True,               # Can be toggled by user
            0, 12, 1, 1,
        )
        checkbutton11.set_hexpand(False)
        checkbutton11.connect(
            'toggled',
            self.on_terminal_progress_button_toggled,
        )
        if not self.app_obj.ytdl_write_stdout_flag:
            checkbutton11.set_sensitive(False)

        # Signal connect from above
        checkbutton9.connect(
            'toggled',
            self.on_terminal_stdout_button_toggled,
            checkbutton10,
            checkbutton11,
        )

        checkbutton12 = self.add_checkbutton(grid,
            'Write output from youtube-dl\'s STDERR to the terminal window',
            self.app_obj.ytdl_write_stderr_flag,
            True,               # Can be toggled by user
            0, 13, 1, 1,
        )
        checkbutton12.set_hexpand(False)
        checkbutton12.connect(
            'toggled',
            self.on_terminal_stderr_button_toggled,
        )

        # Special preferences
        self.add_label(grid,
            '<u>Special preferences (applies to both the Output Tab and the' \
            + ' terminal window)</u>',
            0, 14, 1, 1,
        )

        checkbutton13 = self.add_checkbutton(grid,
            'Write verbose output (youtube-dl debugging mode)',
            self.app_obj.ytdl_write_verbose_flag,
            True,               # Can be toggled by user
            0, 15, 1, 1,
        )
        checkbutton13.set_hexpand(False)
        checkbutton13.connect('toggled', self.on_verbose_button_toggled)

        # Refresh operation preferences
        self.add_label(grid,
            '<u>Refresh operation preferences</u>',
            0, 16, 1, 1,
        )

        checkbutton14 = self.add_checkbutton(grid,
            'During a refresh operation, show all matching videos in the' \
            + ' Output Tab',
            self.app_obj.refresh_output_videos_flag,
            True,               # Can be toggled by user
            0, 17, 1, 1,
        )
        checkbutton14.set_hexpand(False)
        # Signal connect appears below

        checkbutton15 = self.add_checkbutton(grid,
            '...also show all non-matching videos',
            self.app_obj.refresh_output_verbose_flag,
            True,               # Can be toggled by user
            0, 18, 1, 1,
        )
        checkbutton15.set_hexpand(False)
        checkbutton15.connect(
            'toggled',
            self.on_refresh_verbose_button_toggled,
        )
        if not self.app_obj.refresh_output_videos_flag:
            checkbutton11.set_sensitive(False)

        # Signal connect from above
        checkbutton14.connect(
            'toggled',
            self.on_refresh_videos_button_toggled,
            checkbutton15,
        )


    # Callback class methods


    def on_archive_button_toggled(self, checkbutton):

        """Called from callback in self.setup_ytdl_tab().

        Enables/disables creation of youtube-dl's archive file,
        ytdl-archive.txt.

        Args:

            checkbutton (Gtk.CheckButton): The widget clicked

        """

        if checkbutton.get_active() \
        and not self.app_obj.allow_ytdl_archive_flag:
            self.app_obj.set_allow_ytdl_archive_flag(True)
        elif not checkbutton.get_active() \
        and self.app_obj.allow_ytdl_archive_flag:
            self.app_obj.set_allow_ytdl_archive_flag(False)


    def on_auto_clone_button_toggled(self, checkbutton):

        """Called from callback in self.setup_operations_tab().

        Enables/disables auto-cloning of the General Options Manager.

        Args:

            checkbutton (Gtk.CheckButton): The widget clicked

        """

        if checkbutton.get_active() \
        and not self.app_obj.auto_clone_options_flag:
            self.app_obj.set_auto_clone_options_flag(True)
        elif not checkbutton.get_active() \
        and self.app_obj.auto_clone_options_flag:
            self.app_obj.set_auto_clone_options_flag(False)


    def on_auto_delete_button_toggled(self, checkbutton, spinbutton,
    checkbutton2):

        """Called from callback in self.setup_videos_tab().

        Enables/disables automatic deletion of downloaded videos.

        Args:

            checkbutton (Gtk.CheckButton): The widget clicked

            spinbutton (Gtk.SpinButton): A widget to be (de)sensitised

            checkbutton2 (Gtk.CheckButton): Another widget to be
                (de)sensitised

        """

        if checkbutton.get_active() \
        and not self.app_obj.auto_delete_flag:
            self.app_obj.set_auto_delete_flag(True)
            spinbutton.set_sensitive(True)
            checkbutton2.set_sensitive(True)

        elif not checkbutton.get_active() \
        and self.app_obj.auto_delete_flag:
            self.app_obj.set_auto_delete_flag(False)
            spinbutton.set_sensitive(False)
            checkbutton2.set_sensitive(False)


    def on_auto_delete_spinbutton_changed(self, spinbutton):

        """Called from callback in self.setup_videos_tab().

        Sets the number of days after which downloaded videos should be
        deleted.

        Args:

            spinbutton (Gtk.SpinButton): The widget clicked

        """

        self.app_obj.set_auto_delete_days(spinbutton.get_value())


    def on_auto_update_button_toggled(self, checkbutton):

        """Called from callback in self.setup_general_tab().

        Enables/disables automatic update operation before every download
        operation.

        Args:

            checkbutton (Gtk.CheckButton): The widget clicked

        """

        if checkbutton.get_active() \
        and not self.app_obj.operation_auto_update_flag:
            self.app_obj.set_operation_auto_update_flag(True)
        elif not checkbutton.get_active() \
        and self.app_obj.operation_auto_update_flag:
            self.app_obj.set_operation_auto_update_flag(False)


    def on_backup_button_toggled(self, radiobutton, value):

        """Called from callback in self.setup_backups_tab().

        Updates IVs in the main application.

        Args:

            radiobutton (Gtk.RadioButton): The widget clicked

            value (string): The new value of the IV

        """

        if radiobutton.get_active():
            self.app_obj.set_db_backup_mode(value)


    def on_bandwidth_button_toggled(self, checkbutton):

        """Called from callback in self.setup_general_tab().

        Enables/disables the download speed limit. Toggling the corresponding
        Gtk.CheckButton in the Progress Tab sets the IV (and makes sure the two
        checkbuttons have the same status).

        Args:

            checkbutton (Gtk.CheckButton): The widget clicked

        """

        other_flag \
        = self.app_obj.main_win_obj.bandwidth_checkbutton.get_active()

        if (checkbutton.get_active() and not other_flag):
            self.app_obj.main_win_obj.bandwidth_checkbutton.set_active(True)
        elif (not checkbutton.get_active() and other_flag):
            self.app_obj.main_win_obj.bandwidth_checkbutton.set_active(False)


    def on_bandwidth_spinbutton_changed(self, spinbutton):

        """Called from callback in self.setup_general_tab().

        Sets the simultaneous download limit. Setting the value of the
        corresponding Gtk.SpinButton in the Progress Tab sets the IV (and
        makes sure the two spinbuttons have the same value).

        Args:

            spinbutton (Gtk.SpinButton): The widget clicked

        """

        self.app_obj.main_win_obj.bandwidth_spinbutton.set_value(
            spinbutton.get_value(),
        )


    def on_check_limit_changed(self, entry):

        """Called from callback in self.setup_performance_tab().

        Sets the limit at which a download operation will stop checking a
        channel or playlist.

        Args:

            entry (Gtk.Entry): The widget changed

        """

        text = entry.get_text()
        if text.isdigit() and int(text) >= 0:
            self.app_obj.set_operation_check_limit(int(text))


    def on_check_mode_combo_changed(self, combo, spinbutton):

        """Called from a callback in self.setup_scheduling_tab().

        Extracts the value visible in the combobox, converts it into another
        value, and uses that value to update the main application's IV.

        Args:

            combo (Gtk.ComboBox): The widget clicked

            spinbutton (Gtk.SpinButton): Another widget to be (de)sensitised

        """

        tree_iter = combo.get_active_iter()
        model = combo.get_model()
        self.app_obj.set_scheduled_check_mode(model[tree_iter][0])
        if self.app_obj.scheduled_check_mode != 'scheduled':
            spinbutton.set_sensitive(False)
        else:
            spinbutton.set_sensitive(True)


    def on_check_wait_spinbutton_changed(self, spinbutton):

        """Called from callback in self.setup_scheduling_tab().

        Sets the interval between scheduled 'Check all' operations.

        Args:

            spinbutton (Gtk.SpinButton): The widget clicked

        """

        self.app_obj.set_scheduled_check_wait_hours(spinbutton.get_value())


    def on_complex_button_toggled(self, checkbutton):

        """Called from callback in self.setup_videos_tab().

        Switches between simple/complex views in the Video Index.

        Args:

            checkbutton (Gtk.CheckButton): The widget clicked

        """

        redraw_flag = False
        if checkbutton.get_active() and not self.app_obj.complex_index_flag:
            self.app_obj.set_complex_index_flag(True)
            redraw_flag = True
        elif not checkbutton.get_active() and self.app_obj.complex_index_flag:
            self.app_obj.set_complex_index_flag(False)
            redraw_flag = True

        if redraw_flag:
            # Redraw the Video Index and the Video Catalogue (since nothing in
            #   the Video Index will be selected)
            self.app_obj.main_win_obj.video_index_reset()
            self.app_obj.main_win_obj.video_catalogue_reset()
            self.app_obj.main_win_obj.video_index_populate()


    def on_child_process_button_toggled(self, checkbutton):

        """Called from callback in self.setup_ytdl_tab().

        Enables/disables ignoring of child process exit error messages.

        Args:

            checkbutton (Gtk.CheckButton): The widget clicked

        """

        if checkbutton.get_active() \
        and not self.app_obj.ignore_child_process_exit_flag:
            self.app_obj.set_ignore_child_process_exit_flag(True)
        elif not checkbutton.get_active() \
        and self.app_obj.ignore_child_process_exit_flag:
            self.app_obj.set_ignore_child_process_exit_flag(False)


    def on_clipboard_button_toggled(self, checkbutton):

        """Called from a callback in self.setup_windows_tab().

        Enables/disables copying from the system clipboard in various dialogue
        windows.

        Args:

            checkbutton (Gtk.CheckButton): The widget clicked

        """

        if checkbutton.get_active() \
        and not self.app_obj.dialogue_copy_clipboard_flag:
            self.app_obj.set_dialogue_copy_clipboard_flag(True)
        elif not checkbutton.get_active() \
        and self.app_obj.dialogue_copy_clipboard_flag:
            self.app_obj.set_dialogue_copy_clipboard_flag(False)


    def on_close_to_tray_toggled(self, checkbutton):

        """Called from a callback in self.setup_windows_tab().

        Enables/disables closing to the system tray, rather than closing the
        application.

        Args:

            checkbutton (Gtk.CheckButton): The widget clicked

        """

        if checkbutton.get_active() \
        and not self.app_obj.close_to_tray_flag:
            self.app_obj.set_close_to_tray_flag(True)
        elif not checkbutton.get_active() \
        and self.app_obj.close_to_tray_flag:
            self.app_obj.set_close_to_tray_flag(False)


    def on_convert_from_button_toggled(self, radiobutton, mode):

        """Called from callback in self.setup_operations_tab().

        Set what happens when downloading a media.Video object whose URL
        represents a channel/playlist.

        Args:

            radiobutton (Gtk.RadioButton): The widget clicked

            mode (str): The new value for the IV: 'disable', 'multi',
                'channel' or 'playlist'

        """

        if radiobutton.get_active():
            self.app_obj.set_operation_convert_mode(mode)


    def on_copyright_button_toggled(self, checkbutton):

        """Called from callback in self.setup_ytdl_tab().

        Enables/disables ignoring of YouTube copyright errors messages.

        Args:

            checkbutton (Gtk.CheckButton): The widget clicked

        """

        if checkbutton.get_active() \
        and not self.app_obj.ignore_yt_copyright_flag:
            self.app_obj.set_ignore_yt_copyright_flag(True)
        elif not checkbutton.get_active() \
        and self.app_obj.ignore_yt_copyright_flag:
            self.app_obj.set_ignore_yt_copyright_flag(False)


    def on_data_dir_button_clicked(self, button, entry, entry2, entry3):

        """Called from callback in self.setup_general_tab().

        Opens a window in which the user can select Tartube's data directoy.
        If the user actually selects it, call the main application to take
        action.

        Args:

            button (Gtk.Button): The widget clicked

            entry, entry2, entry3 (Gtk.Entry): Additional widget to be modified
                by this function

        """

        dialogue_win = Gtk.FileChooserDialog(
            'Please select ' \
            + utils.upper_case_first(__main__.__packagename__) \
            + '\'s data directory',
            self,
            Gtk.FileChooserAction.SELECT_FOLDER,
            (
                Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                Gtk.STOCK_OPEN, Gtk.ResponseType.OK,
            ),
        )

        response = dialogue_win.run()
        if response == Gtk.ResponseType.OK:
            new_path = dialogue_win.get_filename()

        dialogue_win.destroy()

        if response == Gtk.ResponseType.OK:

            # In the past, I accidentally created a new database directory
            #   just inside an existing one, rather than switching to the
            #   existing one
            # If no database file exists, prompt the user to create a new one
            db_path = os.path.abspath(
                os.path.join(new_path, self.app_obj.db_file_name),
            )

            if not os.path.isfile(db_path):

                self.app_obj.dialogue_manager_obj.show_msg_dialogue(
                    'Are you sure you want to create\na new database at this' \
                    + ' location?\n\n' + new_path,
                    'question',
                    'yes-no',
                    self,           # Parent window is this window
                    {
                        'yes': 'switch_db',
                        'data': [new_path, self],
                    },
                )

            # Database file already exists, so try to load it now
            elif not self.app_obj.switch_db([new_path, self]):

                if self.app_obj.disable_load_save_flag:
                    button.set_sensitive(False)

                self.app_obj.dialogue_manager_obj.show_msg_dialogue(
                    'Database file not loaded',
                    'error',
                    'ok',
                    self,           # Parent window is this window
                )

            else:

                entry.set_text(self.app_obj.data_dir)
                entry2.set_text(
                    str(utils.disk_get_total_space(self.app_obj.data_dir)),
                )

                entry3.set_text(
                    str(utils.disk_get_free_space(self.app_obj.data_dir)),
                )

                if self.app_obj.disable_load_save_flag:
                    button.set_sensitive(False)

                self.app_obj.dialogue_manager_obj.show_msg_dialogue(
                    'Database file loaded',
                    'info',
                    'ok',
                    self,           # Parent window is this window
                )


    def on_delete_shutdown_button_toggled(self, checkbutton):

        """Called from callback in self.setup_videos_tab().

        Enables/disables emptying temporary folders when Tartube shuts down.

        Args:

            checkbutton (Gtk.CheckButton): The widget clicked

        """

        if checkbutton.get_active() \
        and not self.app_obj.delete_on_shutdown_flag:
            self.app_obj.set_delete_on_shutdown_flag(True)
        elif not checkbutton.get_active() \
        and self.app_obj.delete_on_shutdown_flag:
            self.app_obj.set_delete_on_shutdown_flag(False)


    def on_delete_watched_button_toggled(self, checkbutton):

        """Called from callback in self.setup_videos_tab().

        Enables/disables automatic deletion of videos, but only those that have
        been watched.

        Args:

            checkbutton (Gtk.CheckButton): The widget clicked

        """

        if checkbutton.get_active() \
        and not self.app_obj.auto_delete_watched_flag:
            self.app_obj.set_auto_delete_watched_flag(True)
        elif not checkbutton.get_active() \
        and self.app_obj.auto_delete_watched_flag:
            self.app_obj.set_auto_delete_watched_flag(False)


    def on_dialogue_button_toggled(self, radiobutton, mode):

        """Called from callback in self.setup_general_tab().

        Sets whether a desktop notification, dialogue window or neither should
        be shown to the user at the end of a download/update/refresh operation.

        Args:

            radiobutton (Gtk.RadioButton): The widget clicked

            mode (str): The new value for the IV: 'default', 'desktop' or
                'dialogue'

        """

        if radiobutton.get_active():
            self.app_obj.set_operation_dialogue_mode(mode)


    def on_disable_dl_all_toggled(self, checkbutton):

        """Called from callback in self.setup_general_tab().

        Enables/disables the 'Download all' buttons in the main window toolbar
        and in the Videos Tab.

        Args:

            checkbutton (Gtk.CheckButton): The widget clicked

        """

        if checkbutton.get_active() \
        and not self.app_obj.disable_dl_all_flag:
            self.app_obj.set_disable_dl_all_flag(True)
        elif not checkbutton.get_active() \
        and self.app_obj.disable_dl_all_flag:
            self.app_obj.set_disable_dl_all_flag(False)


    def on_disk_stop_button_toggled(self, checkbutton, spinbutton):

        """Called from a callback in self.setup_general_tab().

        Enables/disables halting a download operation when the system is
        running out of disk space.

        Args:

            checkbutton (Gtk.CheckButton): The widget clicked

            spinbutton (Gtk.CheckButton): Another widget to be (de)sensitised

        """

        if checkbutton.get_active() \
        and not self.app_obj.disk_space_stop_flag:
            self.app_obj.set_disk_space_stop_flag(True)
            spinbutton.set_sensitive(True)
        elif not checkbutton.get_active() \
        and self.app_obj.disk_space_stop_flag:
            self.app_obj.set_disk_space_stop_flag(False)
            spinbutton.set_sensitive(False)


    def on_disk_stop_spinbutton_changed(self, spinbutton):

        """Called from callback in self.setup_general_tab().

        Sets the amount of free disk space below which download operations
        will be halted.

        Args:

            spinbutton (Gtk.SpinButton): The widget clicked

        """

        self.app_obj.set_disk_space_stop_limit(spinbutton.get_value())


    def on_disk_warn_button_toggled(self, checkbutton, spinbutton):

        """Called from a callback in self.setup_general_tab().

        Enables/disables warnings when the system is running out of disk space.

        Args:

            checkbutton (Gtk.CheckButton): The widget clicked

            spinbutton (Gtk.CheckButton): Another widget to be (de)sensitised

        """

        if checkbutton.get_active() \
        and not self.app_obj.disk_space_warn_flag:
            self.app_obj.set_disk_space_warn_flag(True)
            spinbutton.set_sensitive(True)
        elif not checkbutton.get_active() \
        and self.app_obj.disk_space_warn_flag:
            self.app_obj.set_disk_space_warn_flag(False)
            spinbutton.set_sensitive(False)


    def on_disk_warn_spinbutton_changed(self, spinbutton):

        """Called from callback in self.setup_general_tab().

        Sets the amount of free disk space below which a warning will be
        issued.

        Args:

            spinbutton (Gtk.SpinButton): The widget clicked

        """

        self.app_obj.set_disk_space_warn_limit(spinbutton.get_value())


    def on_dl_mode_combo_changed(self, combo, spinbutton):

        """Called from a callback in self.setup_scheduling_tab().

        Extracts the value visible in the combobox, converts it into another
        value, and uses that value to update the main application's IV.

        Args:

            combo (Gtk.ComboBox): The widget clicked

            spinbutton (Gtk.SpinButton): Another widget to be (de)sensitised

        """

        tree_iter = combo.get_active_iter()
        model = combo.get_model()
        self.app_obj.set_scheduled_dl_mode(model[tree_iter][0])
        if self.app_obj.scheduled_dl_mode != 'scheduled':
            spinbutton.set_sensitive(False)
        else:
            spinbutton.set_sensitive(True)


    def on_dl_wait_spinbutton_changed(self, spinbutton):

        """Called from callback in self.setup_scheduling_tab().

        Sets the interval between scheduled 'Download all' operations.

        Args:

            spinbutton (Gtk.SpinButton): The widget clicked

        """

        self.app_obj.set_scheduled_dl_wait_hours(spinbutton.get_value())


    def on_download_limit_changed(self, entry):

        """Called from callback in self.setup_performance_tab().

        Sets the limit at which a download operation will stop downloading a
        channel or playlist.

        Args:

            entry (Gtk.Entry): The widget changed

        """

        text = entry.get_text()
        if text.isdigit() and int(text) >= 0:
            self.app_obj.set_operation_download_limit(int(text))


    def on_error_button_toggled(self, checkbutton):

        """Called from callback in self.setup_windows_tab().

        Enables/disables system errors in the 'Errors/Warnings' tab. Toggling
        the corresponding Gtk.CheckButton in the Errors/Warnings tab sets the
        IV (and makes sure the two checkbuttons have the same status).

        Args:

            checkbutton (Gtk.CheckButton): The widget clicked

        """

        other_flag \
        = self.app_obj.main_win_obj.show_error_checkbutton.get_active()

        if (checkbutton.get_active() and not other_flag):
            self.app_obj.main_win_obj.show_error_checkbutton.set_active(True)
        elif (not checkbutton.get_active() and other_flag):
            self.app_obj.main_win_obj.show_error_checkbutton.set_active(False)


    def on_expand_tree_toggled(self, checkbutton):

        """Called from callback in self.setup_general_tab().

        Enables/disables auto-expansion of the Video Index after a folder is
        selected (clicked).

        Args:

            checkbutton (Gtk.CheckButton): The widget clicked

        """

        if checkbutton.get_active() \
        and not self.app_obj.auto_expand_video_index_flag:
            self.app_obj.set_auto_expand_video_index_flag(True)
        elif not checkbutton.get_active() \
        and self.app_obj.auto_expand_video_index_flag:
            self.app_obj.set_auto_expand_video_index_flag(False)


    def on_json_button_toggled(self, checkbutton):

        """Called from callback in self.setup_ytdl_tab().

        Enables/disables apply a 60-second timeout when fetching a video's JSON
        data.

        Args:

            checkbutton (Gtk.CheckButton): The widget clicked

        """

        if checkbutton.get_active() \
        and not self.app_obj.apply_json_timeout_flag:
            self.app_obj.set_apply_json_timeout_flag(True)
        elif not checkbutton.get_active() \
        and self.app_obj.apply_json_timeout_flag:
            self.app_obj.set_apply_json_timeout_flag(False)


    def on_keep_open_button_toggled(self, checkbutton, checkbutton2):

        """Called from a callback in self.setup_windows_tab().

        Enables/disables keeping the dialogue window open when adding channels/
        playlists/folders.

        Args:

            checkbutton (Gtk.CheckButton): The widget clicked

            checkbutton2 (Gtk.CheckButton): Another checkbutton to sensitise/
                desensitise, according to the new value of the flag

        """

        if checkbutton.get_active() \
        and not self.app_obj.dialogue_keep_open_flag:
            self.app_obj.set_dialogue_keep_open_flag(True)
            checkbutton2.set_sensitive(False)

        elif not checkbutton.get_active() \
        and self.app_obj.dialogue_keep_open_flag:
            self.app_obj.set_dialogue_keep_open_flag(False)
            checkbutton2.set_sensitive(True)


    def on_limit_button_toggled(self, checkbutton, entry, entry2):

        """Called from callback in self.setup_performance_tab().

        Sets the limit at which a download operation will stop downloading a
        channel or playlist.

        Args:

            checkbutton (Gtk.CheckButton): The widget clicked
            entry, entry2 (Gtk.Entry): The entry boxes which must be
                sensitised/desensitised, according to the new setting of the IV

        """

        if checkbutton.get_active() and not self.app_obj.operation_limit_flag:
            self.app_obj.set_operation_limit_flag(True)
            entry.set_sensitive(True)
            entry2.set_sensitive(True)

        elif not checkbutton.get_active() \
        and self.app_obj.operation_limit_flag:
            self.app_obj.set_operation_limit_flag(False)
            entry.set_sensitive(False)
            entry2.set_sensitive(False)


    def on_match_button_toggled(self, radiobutton):

        """Called from callback in self.setup_videos_tab().

        Updates IVs in the main application and sensities/desensities widgets.

        Args:

            radiobutton (Gtk.RadioButton): The widget clicked

        """

        default_val = self.app_obj.match_default_chars

        if radiobutton.get_active():

            if radiobutton == self.radiobutton:
                self.app_obj.set_match_method('exact_match')
                # (Changing the contents of the widgets automatically updates
                #   mainapp.TartubeApp IVs)
                self.spinbutton.set_value(default_val)
                self.spinbutton.set_sensitive(False)
                self.spinbutton2.set_value(default_val)
                self.spinbutton2.set_sensitive(False)

            elif radiobutton == self.radiobutton2:
                self.app_obj.set_match_method('match_first')
                self.spinbutton.set_sensitive(True)
                self.spinbutton2.set_value(default_val)
                self.spinbutton2.set_sensitive(False)

            else:
                self.app_obj.set_match_method('ignore_last')
                self.spinbutton.set_value(default_val)
                self.spinbutton.set_sensitive(False)
                self.spinbutton2.set_sensitive(True)


    def on_match_spinbutton_changed(self, spinbutton):

        """Called from callback in self.setup_general_tab().

        Updates IVs in the main application and sensities/desensities widgets.

        Args:

            spinbutton (Gtk.SpinButton): The widget clicked

        """

        if spinbutton == self.spinbutton:
            self.app_obj.set_match_first_chars(spinbutton.get_value())
        else:
            self.app_obj.set_match_ignore_chars(spinbutton.get_value())


    def on_merge_button_toggled(self, checkbutton):

        """Called from callback in self.setup_ytdl_tab().

        Enables/disables ignoring of 'Requested formats are incompatible for
        merge and will be merged into mkv' warning messages.

        Args:

            checkbutton (Gtk.CheckButton): The widget clicked

        """

        if checkbutton.get_active() \
        and not self.app_obj.ignore_merge_warning_flag:
            self.app_obj.set_ignore_merge_warning_flag(True)
        elif not checkbutton.get_active() \
        and self.app_obj.ignore_merge_warning_flag:
            self.app_obj.set_ignore_merge_warning_flag(False)


    def on_moviepy_button_toggled(self, checkbutton):

        """Called from callback in self.setup_general_tab().

        Enables/disables use of the moviepy.editor module.

        Args:

            checkbutton (Gtk.CheckButton): The widget clicked

        """

        if checkbutton.get_active() \
        and not self.app_obj.use_module_moviepy_flag:
            self.app_obj.set_use_module_moviepy_flag(True)
        elif not checkbutton.get_active() \
        and self.app_obj.use_module_moviepy_flag:
            self.app_obj.set_use_module_moviepy_flag(False)


    def on_moviepy_timeout_spinbutton_changed(self, spinbutton):

        """Called from callback in self.setup_general_tab().

        Sets the timeout to apply to threads using the moviepy module.

        Args:

            spinbutton (Gtk.SpinButton): The widget clicked

        """

        self.app_obj.set_refresh_moviepy_timeout(
            spinbutton.get_value(),
        )


    def on_no_annotations_button_toggled(self, checkbutton):

        """Called from callback in self.setup_ignore_tab().

        Enables/disables ignoring of the 'no annotations' warning messages.

        Args:

            checkbutton (Gtk.CheckButton): The widget clicked

        """

        if checkbutton.get_active() \
        and not self.app_obj.ignore_no_annotations_flag:
            self.app_obj.set_ignore_no_annotations_flag(True)
        elif not checkbutton.get_active() \
        and self.app_obj.ignore_no_annotations_flag:
            self.app_obj.set_ignore_no_annotations_flag(False)


    def on_no_subtitles_button_toggled(self, checkbutton):

        """Called from callback in self.setup_ignore_tab().

        Enables/disables ignoring of the 'no subtitles' warning messages.

        Args:

            checkbutton (Gtk.CheckButton): The widget clicked

        """

        if checkbutton.get_active() \
        and not self.app_obj.ignore_no_subtitles_flag:
            self.app_obj.set_ignore_no_subtitles_flag(True)
        elif not checkbutton.get_active() \
        and self.app_obj.ignore_no_subtitles_flag:
            self.app_obj.set_ignore_no_subtitles_flag(False)


    def on_output_empty_button_toggled(self, checkbutton):

        """Called from a callback in self.setup_ytdl_tab().

        Enables/disables emptying pages in the Output Tab at the start of every
        operation.

        Args:

            checkbutton (Gtk.CheckButton): The widget clicked

        """

        if checkbutton.get_active() \
        and not self.app_obj.ytdl_output_start_empty_flag:
            self.app_obj.set_ytdl_output_start_empty_flag(True)
        elif not checkbutton.get_active() \
        and self.app_obj.ytdl_output_start_empty_flag:
            self.app_obj.set_ytdl_output_start_empty_flag(False)


    def on_output_summary_button_toggled(self, checkbutton):

        """Called from a callback in self.setup_output_tab().

        Enables/disables displaying a summary page in the Output Tab.

        Args:

            checkbutton (Gtk.CheckButton): The widget clicked

        """

        if checkbutton.get_active() \
        and not self.app_obj.ytdl_output_show_summary_flag:
            self.app_obj.set_ytdl_output_show_summary_flag(True)
        elif not checkbutton.get_active() \
        and self.app_obj.ytdl_output_show_summary_flag:
            self.app_obj.set_ytdl_output_show_summary_flag(False)


    def on_output_stderr_button_toggled(self, checkbutton):

        """Called from a callback in self.setup_ytdl_tab().

        Enables/disables writing output from youtube-dl's STDERR to the Output
        Tab.

        Args:

            checkbutton (Gtk.CheckButton): The widget clicked

        """

        if checkbutton.get_active() \
        and not self.app_obj.ytdl_output_stderr_flag:
            self.app_obj.set_ytdl_output_stderr_flag(True)
        elif not checkbutton.get_active() \
        and self.app_obj.ytdl_output_stderr_flag:
            self.app_obj.set_ytdl_output_stderr_flag(False)


    def on_output_stdout_button_toggled(self, checkbutton, checkbutton2, \
    checkbutton3):

        """Called from a callback in self.setup_ytdl_tab().

        Enables/disables writing output from youtube-dl's STDOUT to the Output
        Tab.

        Args:

            checkbutton (Gtk.CheckButton): The widget clicked

            checkbutton2, checkbutton3 (Gtk.CheckButton): Additional
                checkbuttons to sensitise/desensitise, according to the new
                value of the flag

        """

        if checkbutton.get_active() \
        and not self.app_obj.ytdl_output_stdout_flag:
            self.app_obj.set_ytdl_output_stdout_flag(True)
            checkbutton2.set_sensitive(True)
            checkbutton3.set_sensitive(True)

        elif not checkbutton.get_active() \
        and self.app_obj.ytdl_output_stdout_flag:
            self.app_obj.set_ytdl_output_stdout_flag(False)
            checkbutton2.set_sensitive(False)
            checkbutton3.set_sensitive(False)


    def on_output_json_button_toggled(self, checkbutton):

        """Called from a callback in self.setup_ytdl_tab().

        Enables/disables writing output from youtube-dl's STDOUT to the Output
        Tab.

        Args:

            checkbutton (Gtk.CheckButton): The widget clicked

        """

        if checkbutton.get_active() \
        and not self.app_obj.ytdl_output_ignore_json_flag:
            self.app_obj.set_ytdl_output_ignore_json_flag(True)
        elif not checkbutton.get_active() \
        and self.app_obj.ytdl_output_ignore_json_flag:
            self.app_obj.set_ytdl_output_ignore_json_flag(False)


    def on_output_progress_button_toggled(self, checkbutton):

        """Called from a callback in self.setup_ytdl_tab().

        Enables/disables writing output from youtube-dl's STDOUT to the Output
        Tab.

        Args:

            checkbutton (Gtk.CheckButton): The widget clicked

        """

        if checkbutton.get_active() \
        and not self.app_obj.ytdl_output_ignore_progress_flag:
            self.app_obj.set_ytdl_output_ignore_progress_flag(True)
        elif not checkbutton.get_active() \
        and self.app_obj.ytdl_output_ignore_progress_flag:
            self.app_obj.set_ytdl_output_ignore_progress_flag(False)


    def on_output_system_button_toggled(self, checkbutton):

        """Called from a callback in self.setup_ytdl_tab().

        Enables/disables writing youtube-dl system commands to the Output Tab.

        Args:

            checkbutton (Gtk.CheckButton): The widget clicked

        """

        if checkbutton.get_active() \
        and not self.app_obj.ytdl_output_system_cmd_flag:
            self.app_obj.set_ytdl_output_system_cmd_flag(True)
        elif not checkbutton.get_active() \
        and self.app_obj.ytdl_output_system_cmd_flag:
            self.app_obj.set_ytdl_output_system_cmd_flag(False)


    def on_refresh_videos_button_toggled(self, checkbutton, checkbutton2):

        """Called from a callback in self.setup_output_tab().

        Enables/disables displaying matching videos in the Output Tab during a
        refresh operation.

        Args:

            checkbutton (Gtk.CheckButton): The widget clicked

            checkbutton2 (Gtk.CheckButton): A different checkbutton to
                sensitise/desensitise, according to the new value of the flag

        """

        if checkbutton.get_active() \
        and not self.app_obj.refresh_output_videos_flag:
            self.app_obj.set_refresh_output_videos_flag(True)
            checkbutton2.set_sensitive(True)

        elif not checkbutton.get_active() \
        and self.app_obj.refresh_output_videos_flag:
            self.app_obj.set_refresh_output_videos_flag(False)
            checkbutton2.set_sensitive(False)


    def on_refresh_verbose_button_toggled(self, checkbutton):

        """Called from a callback in self.setup_ytdl_tab().

        Enables/disables displaying non-matching videos in the Output Tab
        during a refresh operation.

        Args:

            checkbutton (Gtk.CheckButton): The widget clicked

        """

        if checkbutton.get_active() \
        and not self.app_obj.refresh_output_verbose_flag:
            self.app_obj.set_refresh_output_verbose_flag(True)
        elif not checkbutton.get_active() \
        and self.app_obj.refresh_output_verbose_flag:
            self.app_obj.set_refresh_output_verbose_flag(False)


    def on_reset_ffmpeg_button_clicked(self, button, entry):

        """Called from callback in self.setup_ytdl_tab().

        Resets the path to the ffmpeg binary.

        Args:

            button (Gtk.Button): The widget clicked

            entry (Gtk.Entry): Another widget to be modified by this function

        """

        self.app_obj.set_ffmpeg_path(None)
        entry.set_text('')


    def on_reverse_button_toggled(self, checkbutton):

        """Called from callback in self.setup_general_tab().

        Enables/disables display of videos in the Results List in the reverse
        order.

        Args:

            checkbutton (Gtk.CheckButton): The widget clicked

        """

        if checkbutton.get_active() \
        and not self.app_obj.results_list_reverse_flag:
            self.app_obj.set_results_list_reverse_flag(True)
        elif not checkbutton.get_active() \
        and self.app_obj.results_list_reverse_flag:
            self.app_obj.set_results_list_reverse_flag(False)


    def on_save_button_toggled(self, checkbutton):

        """Called from callback in self.setup_general_tab().

        Enables/disables automatic saving of files at the end of a download/
        update/refresh operation.

        Args:

            checkbutton (Gtk.CheckButton): The widget clicked

        """

        if checkbutton.get_active() and not self.app_obj.operation_save_flag:
            self.app_obj.set_operation_save_flag(True)
        elif not checkbutton.get_active() and self.app_obj.operation_save_flag:
            self.app_obj.set_operation_save_flag(False)


    def on_scheduled_stop_button_toggled(self, checkbutton):

        """Called from a callback in self.setup_scheduling_tab().

        Enables/disables shutting down Tartube after a scheduled 'Download all'
        or 'Check all' operation.

        Args:

            checkbutton (Gtk.CheckButton): The widget clicked

        """

        if checkbutton.get_active() \
        and not self.app_obj.scheduled_stop_flag:
            self.app_obj.set_scheduled_stop_flag(True)
        elif not checkbutton.get_active() \
        and self.app_obj.scheduled_stop_flag:
            self.app_obj.set_scheduled_stop_flag(False)


    def on_set_ffmpeg_button_clicked(self, button, entry):

        """Called from callback in self.setup_ytdl_tab().

        Opens a window in which the user can select the ffmpeg binary, if it is
        installed (and if the user wants it).

        Args:

            button (Gtk.Button): The widget clicked

            entry (Gtk.Entry): Another widget to be modified by this function

        """

        dialogue_win = Gtk.FileChooserDialog(
            'Please select the ffmpeg executable',
            self,
            Gtk.FileChooserAction.OPEN,
            (
                Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                Gtk.STOCK_OPEN, Gtk.ResponseType.OK,
            ),
        )

        response = dialogue_win.run()
        if response == Gtk.ResponseType.OK:
            new_path = dialogue_win.get_filename()

        dialogue_win.destroy()

        if response == Gtk.ResponseType.OK and new_path:

            self.app_obj.set_ffmpeg_path(new_path)
            entry.set_text(self.app_obj.ffmpeg_path)


    def on_show_small_icons_toggled(self, checkbutton):

        """Called from callback in self.setup_general_tab().

        Enables/disables smaller icons in the Video Index.

        Args:

            checkbutton (Gtk.CheckButton): The widget clicked

        """

        if checkbutton.get_active() \
        and not self.app_obj.show_small_icons_in_index:
            self.app_obj.set_show_small_icons_in_index(True)
        elif not checkbutton.get_active() \
        and self.app_obj.show_small_icons_in_index:
            self.app_obj.set_show_small_icons_in_index(False)


    def on_show_status_icon_toggled(self, checkbutton, checkbutton2):

        """Called from a callback in self.setup_windows_tab().

        Shows/hides the status icon in the system tray.

        Args:

            checkbutton (Gtk.CheckButton): The widget clicked

            checkbutton2 (Gtk.CheckButton): Another checkbutton to sensitise/
                desensitise, according to the new value of the flag

        """

        if checkbutton.get_active() \
        and not self.app_obj.show_status_icon_flag:
            self.app_obj.set_show_status_icon_flag(True)
            checkbutton2.set_sensitive(True)

        elif not checkbutton.get_active() \
        and self.app_obj.show_status_icon_flag:
            self.app_obj.set_show_status_icon_flag(False)
            checkbutton2.set_sensitive(False)


    def on_show_tooltips_toggled(self, checkbutton):

        """Called from callback in self.setup_general_tab().

        Enables/disables tooltips for videos/channels/playlists/folders.

        Args:

            checkbutton (Gtk.CheckButton): The widget clicked

        """

        if checkbutton.get_active() \
        and not self.app_obj.show_tooltips_flag:
            self.app_obj.set_show_tooltips_flag(True)
        elif not checkbutton.get_active() \
        and self.app_obj.show_tooltips_flag:
            self.app_obj.set_show_tooltips_flag(False)


    def on_squeeze_button_toggled(self, checkbutton):

        """Called from callback in self.setup_general_tab().

        Enables/disables labels in the main window's main toolbar.

        Args:

            checkbutton (Gtk.CheckButton): The widget clicked

        """

        if checkbutton.get_active() \
        and not self.app_obj.toolbar_squeeze_flag:
            self.app_obj.set_toolbar_squeeze_flag(True)
        elif not checkbutton.get_active() \
        and self.app_obj.toolbar_squeeze_flag:
            self.app_obj.set_toolbar_squeeze_flag(False)


    def on_system_keep_button_toggled(self, checkbutton):

        """Called from callback in self.setup_general_tab().

        Enables/disables keeping the total number of system messages in the tab
        label until the clear button is explicitly clicked.

        Args:

            checkbutton (Gtk.CheckButton): The widget clicked

        """

        if checkbutton.get_active() \
        and not self.app_obj.system_msg_keep_totals_flag:
            self.app_obj.set_system_msg_keep_totals_flag(True)
        elif not checkbutton.get_active() \
        and self.app_obj.system_msg_keep_totals_flag:
            self.app_obj.set_system_msg_keep_totals_flag(False)


    def on_terminal_stderr_button_toggled(self, checkbutton):

        """Called from a callback in self.setup_ytdl_tab().

        Enables/disables writing output from youtube-dl's STDERR to the
        terminal.

        Args:

            checkbutton (Gtk.CheckButton): The widget clicked

        """

        if checkbutton.get_active() \
        and not self.app_obj.ytdl_write_stderr_flag:
            self.app_obj.set_ytdl_write_stderr_flag(True)
        elif not checkbutton.get_active() \
        and self.app_obj.ytdl_write_stderr_flag:
            self.app_obj.set_ytdl_write_stderr_flag(False)


    def on_terminal_stdout_button_toggled(self, checkbutton, checkbutton2, \
    checkbutton3):

        """Called from a callback in self.setup_ytdl_tab().

        Enables/disables writing output from youtube-dl's STDOUT to the
        terminal.

        Args:

            checkbutton (Gtk.CheckButton): The widget clicked

            checkbutton2, checkbutton3 (Gtk.CheckButton): Additional
                checkbuttons to sensitise/desensitise, according to the new
                value of the flag

        """

        if checkbutton.get_active() \
        and not self.app_obj.ytdl_write_stdout_flag:
            self.app_obj.set_ytdl_write_stdout_flag(True)
            checkbutton2.set_sensitive(True)
            checkbutton3.set_sensitive(True)

        elif not checkbutton.get_active() \
        and self.app_obj.ytdl_write_stdout_flag:
            self.app_obj.set_ytdl_write_stdout_flag(False)
            checkbutton2.set_sensitive(False)
            checkbutton3.set_sensitive(False)


    def on_terminal_json_button_toggled(self, checkbutton):

        """Called from a callback in self.setup_ytdl_tab().

        Enables/disables writing output from youtube-dl's STDOUT to the
        terminal.

        Args:

            checkbutton (Gtk.CheckButton): The widget clicked

        """

        if checkbutton.get_active() \
        and not self.app_obj.ytdl_write_ignore_json_flag:
            self.app_obj.set_ytdl_write_ignore_json_flag(True)
        elif not checkbutton.get_active() \
        and self.app_obj.ytdl_write_ignore_json_flag:
            self.app_obj.set_ytdl_write_ignore_json_flag(False)


    def on_terminal_progress_button_toggled(self, checkbutton):

        """Called from a callback in self.setup_ytdl_tab().

        Enables/disables writing output from youtube-dl's STDOUT to the
        terminal.

        Args:

            checkbutton (Gtk.CheckButton): The widget clicked

        """

        if checkbutton.get_active() \
        and not self.app_obj.ytdl_write_ignore_progress_flag:
            self.app_obj.set_ytdl_write_ignore_progress_flag(True)
        elif not checkbutton.get_active() \
        and self.app_obj.ytdl_write_ignore_progress_flag:
            self.app_obj.set_ytdl_write_ignore_progress_flag(False)


    def on_terminal_system_button_toggled(self, checkbutton):

        """Called from a callback in self.setup_ytdl_tab().

        Enables/disables writing youtube-dl system commands to the terminal.

        Args:

            checkbutton (Gtk.CheckButton): The widget clicked

        """

        if checkbutton.get_active() \
        and not self.app_obj.ytdl_write_system_cmd_flag:
            self.app_obj.set_ytdl_write_system_cmd_flag(True)
        elif not checkbutton.get_active() \
        and self.app_obj.ytdl_write_system_cmd_flag:
            self.app_obj.set_ytdl_write_system_cmd_flag(False)


    def on_update_combo_changed(self, combo):

        """Called from a callback in self.setup_ytdl_tab().

        Extracts the value visible in the combobox, converts it into another
        value, and uses that value to update the main application's IV.

        Args:

            combo (Gtk.ComboBox): The widget clicked

        """

        tree_iter = combo.get_active_iter()
        model = combo.get_model()
        self.app_obj.set_ytdl_update_current(model[tree_iter][0])


    def on_verbose_button_toggled(self, checkbutton):

        """Called from a callback in self.setup_ytdl_tab().

        Enables/disables writing verbose output (youtube-dl debugging mode).

        Args:

            checkbutton (Gtk.CheckButton): The widget clicked

        """

        if checkbutton.get_active() \
        and not self.app_obj.ytdl_write_verbose_flag:
            self.app_obj.set_ytdl_write_verbose_flag(True)
        elif not checkbutton.get_active() \
        and self.app_obj.ytdl_write_verbose_flag:
            self.app_obj.set_ytdl_write_verbose_flag(False)


    def on_warning_button_toggled(self, checkbutton):

        """Called from callback in self.setup_general_tab().

        Enables/disables system warnings in the 'Errors/Warnings' tab. Toggling
        the corresponding Gtk.CheckButton in the Errors/Warnings tab sets the
        IV (and makes sure the two checkbuttons have the same status).

        Args:

            checkbutton (Gtk.CheckButton): The widget clicked

        """

        main_win_obj = self.app_obj.main_win_obj

        other_flag \
        = self.app_obj.main_win_obj.show_warning_checkbutton.get_active()

        if (checkbutton.get_active() and not other_flag):
            main_win_obj.show_warning_checkbutton.set_active(True)
        elif (not checkbutton.get_active() and other_flag):
            main_win_obj.show_warning_checkbutton.set_active(False)


    def on_worker_button_toggled(self, checkbutton):

        """Called from callback in self.setup_general_tab().

        Enables/disables the simultaneous download limit. Toggling the
        corresponding Gtk.CheckButton in the Progress Tab sets the IV (and
        makes sure the two checkbuttons have the same status).

        Args:

            checkbutton (Gtk.CheckButton): The widget clicked

        """

        other_flag \
        = self.app_obj.main_win_obj.num_worker_checkbutton.get_active()

        if (checkbutton.get_active() and not other_flag):
            self.app_obj.main_win_obj.num_worker_checkbutton.set_active(True)
        elif (not checkbutton.get_active() and other_flag):
            self.app_obj.main_win_obj.num_worker_checkbutton.set_active(False)


    def on_worker_spinbutton_changed(self, spinbutton):

        """Called from callback in self.setup_general_tab().

        Sets the simultaneous download limit. Setting the value of the
        corresponding Gtk.SpinButton in the Progress Tab sets the IV (and
        makes sure the two spinbuttons have the same value).

        Args:

            spinbutton (Gtk.SpinButton): The widget clicked

        """

        self.app_obj.main_win_obj.num_worker_spinbutton.set_value(
            spinbutton.get_value(),
        )


    def on_video_res_button_toggled(self, checkbutton):

        """Called from callback in self.setup_operations_tab().

        Enables/disables the video resolution limit. Toggling the corresponding
        Gtk.CheckButton in the Progress Tab sets the IV (and makes sure the two
        checkbuttons have the same status).

        Args:

            checkbutton (Gtk.CheckButton): The widget clicked

        """

        other_flag \
        = self.app_obj.main_win_obj.video_res_checkbutton.get_active()

        if (checkbutton.get_active() and not other_flag):
            self.app_obj.main_win_obj.video_res_checkbutton.set_active(True)
        elif (not checkbutton.get_active() and other_flag):
            self.app_obj.main_win_obj.video_res_checkbutton.set_active(False)


    def on_video_res_combo_changed(self, combo):

        """Called from a callback in self.setup_operations_tab().

        Extracts the value visible in the combobox, converts it into another
        value, and uses that value to update the main application's IV.

        Args:

            combo (Gtk.ComboBox): The widget clicked

        """

        tree_iter = combo.get_active_iter()
        model = combo.get_model()
        self.app_obj.main_win_obj.set_video_res(model[tree_iter][0])


    def on_ytdl_path_combo_changed(self, combo):

        """Called from a callback in self.setup_ytdl_tab().

        Extracts the value visible in the combobox, converts it into another
        value, and uses that value to update the main application's IV.

        Args:

            combo (Gtk.ComboBox): The widget clicked

        """

        tree_iter = combo.get_active_iter()
        model = combo.get_model()
        self.app_obj.set_ytdl_path(model[tree_iter][1])

