# CPUanalytics
# v0.1.0
# KiryxaProger

import ctypes
import json
import os
import sys

import cpuinfo
import customtkinter as ctk
import keyboard
import psutil
import pywinstyles
from PIL import Image

class Main(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Open settings.json file
        with open('settings.json', 'r') as file:
            self.settings = json.load(file)

        # Settings variables
        # -------------------------------------------------------------------------------
        self.THEME = self.settings['Theme']                         # Application theme
        self.CPU_NAME = cpuinfo.get_cpu_info()\
            ['brand_raw'].replace('(R)', '®').replace('(TM)', '™')  # CPU name

        self.LIST_BARS = []                                         # List of bars
        self.LIST_HEIGHTS = []                                      # List of bar heights
        self.COLOR = None                                           # Default color
        # -------------------------------------------------------------------------------

        # Theme settings
        # -----------------------------------------------
        self.set_theme(self.THEME)
        self.set_color_theme(self.settings['ColorTheme'])
        # -----------------------------------------------
        self.THEME = ctk.get_appearance_mode()

        # Application settings
        # ----------------------------------------
        self.title('CPUanalytics')
        self.geometry('700x400')
        self.resizable(False, False)
        self.iconbitmap(f'{self.THEME}\\icon.ico')
        # ----------------------------------------

        colors = self.settings['Colors'][self.settings['Theme']]
        # Color depending
        self.text_color = colors['text']
        self.hover_color = colors['hover']
        self.active_color = colors['active']
        self.frame_color = colors['main_frame']
        self.menu_frame_color = colors['menu_frame']
        self.transparent_color = 'transparent'

        # -----------------------------------------------------------------
        # MENU FRAME
        # -----------------------------------------------------------------
        self.menu_frame = ctk.CTkFrame(                            #  Frame
            master=self,
            width=48,
            height=400,
            corner_radius=0,
            border_width=0,
            bg_color=self.menu_frame_color
        )

        # 'Home' button
        self.home_menu_el = ctk.CTkButton(                         # Button
            master=self.menu_frame,
            image=self.open_image('analytics_menu_el.png'),
            text='',
            width=30,
            height=30,
            corner_radius=7,
            bg_color=self.transparent_color,
            fg_color=self.active_color,
            hover_color=self.active_color,
            command=self.home_menu_open
        )

        # 'History' button
        self.history_menu_el = ctk.CTkButton(                      # Button
            master=self.menu_frame,
            image=self.open_image('history_menu_el.png'),
            text='',
            width=30,
            height=30,
            corner_radius=7,
            bg_color=self.transparent_color,
            fg_color=self.transparent_color,
            hover_color=self.hover_color
        )

        # 'History' button
        self.settings_menu_el = ctk.CTkButton(                    # Button
            master=self.menu_frame,
            image=self.open_image('settings_menu_el.png'),
            text='',
            width=30,
            height=30,
            corner_radius=7,
            bg_color='transparent',
            fg_color='transparent',
            hover_color=self.hover_color
        )

        # Placement of objects --------------------------------------------
        self.menu_frame.place(x=0, y=0)                            #  Frame
        self.home_menu_el.place(x=5, y=5)                          # Button
        self.history_menu_el.place(x=5, y=40)                      # Button
        self.settings_menu_el.place(x=5, y=365)                    # Button

        # -----------------------------------------------------------------
        #
        # HOME PAGE FRAME -------------------------------------------- HOME
        #
        # -----------------------------------------------------------------
        self.home_frame = ctk.CTkFrame(                            #  Frame
            master=self,
            width=652,
            height=400,
            corner_radius=0,
            border_width=0,
            fg_color=self.frame_color
        )

        # 'Home' label
        self.home_label = ctk.CTkLabel(                            #  Label
            master=self.home_frame,
            width=700,
            height=35,
            text='',
            font=('Segoe UI Bold', 25),
            text_color=self.text_color,
            anchor='w'
        )

        # Placement of objects --------------------------------------------
        self.home_frame.place(x=48, y=0)                           #  Frame
        self.home_label.place(x=20, y=20, relx=0, anchor='w')      #  Label

        # -----------------------------------------------------------------
        # CPU MONITORING FRAME
        # -----------------------------------------------------------------
        self.monitoring_frame = ctk.CTkFrame(                      #  Frame
            master=self.home_frame,
            width=620,
            height=240,
            corner_radius=7,
            border_width=0
        )

        # CPU name in the middle
        self.cpu_name_label = ctk.CTkLabel(                        #  Label
            master=self.monitoring_frame,
            width=619,
            height=35,
            text=self.CPU_NAME,
            font=('Segoe UI', 15),
            text_color=self.text_color,
            bg_color=self.frame_color
        )

        # CPU percentages
        self.cpu_percent_label = ctk.CTkLabel(                     #  Label
                master=self.monitoring_frame,
                width=30,
                height=30,
                text='',
                font=('Segoe UI Bold', 15),
                text_color=self.COLOR,
                anchor='e'
            )

        # Placement of objects --------------------------------------------
        self.monitoring_frame.place(x=17, y=50)                    #  Frame
        self.cpu_name_label.place(x=0, y=25, anchor='w')           #  Label
        self.cpu_percent_label.place(x=600, y=220, anchor='e')     #  Label

        for i in range(0, 153, 38):                                #   line
            line = ctk.CTkFrame(
                self.monitoring_frame,
                width=620,
                height=2,
                corner_radius=0,
                fg_color=self.frame_color
            )
            line.place(x=0, y=48+i)

        # -----------------------------------------------------------------
        # CPU RELOAD FRAME
        # -----------------------------------------------------------------
        self.reload_frame = ctk.CTkFrame(                          #  Frame
            master=self.home_frame,
            width=620,
            height=50,
            corner_radius=7,
            border_width=0
        )

        self.reload_label = ctk.CTkLabel(
            master=self.reload_frame,
            width=400,
            height=35,
            text=self.CPU_NAME,
            font=('Segoe UI', 15),
            anchor='w'
        )

        self.reload_button = ctk.CTkButton(                        # Button
            master=self.reload_frame,
            text='',
            width=80,
            height=30,
            corner_radius=7,
            border_width=1,
            border_color='grey',
            hover_color=self.hover_color,
            command=self.cpu_reload
        )

        # Placement of objects --------------------------------------------
        self.reload_frame.place(x=17, y=305)                       #  Frame
        self.reload_button.place(x=505, y=10)                      # Button
        self.reload_label.place(x=10, y=7.5)                       # Button

        # -----------------------------------------------------------------
        #
        # ФРЕЙМ ЖУРНАЛ ПРИЛОЖЕНИЙ ---------------------------------- ЖУРНАЛ
        #
        # -----------------------------------------------------------------
        


        # Set language
        self.install_language(self.settings['Language'])

        # Monitoring CPU percent and create Frames (bars)
        self.cpu_monitoring()

        if self.settings['Blur']:
            self.set_blur()

    def open_image(self, path: str) -> ctk.CTkImage:
        '''
        return CTkImage for 2 themes
        '''

        return ctk.CTkImage(
            light_image=Image.open(f'Light\\{path}'),
            dark_image=Image.open(f'Dark\\{path}')
        )
    

    def install_language(self, language: str) -> None:
        '''
        set language
        '''
        
        # Открытие languages.json на чтение
        with open('languages.json', 'r', encoding='utf-8') as file:
            languages = json.load(file)
        
        self.home_label.configure(text=languages[language]['Home'])
        self.reload_button.configure(text=languages[language]['Reload'])

    def set_theme(self, theme: str) -> None:
        '''
        Set theme.
        '''
        ctk.set_appearance_mode(theme)

    def set_color_theme(self, color_theme):
        '''
        Set color theme on color_theme.
        '''
        pass

        # Check the color theme and set it accordingly
        if color_theme == 'default':
            if ctk.get_appearance_mode() == 'Light':
                ctk.set_default_color_theme('blue')
            elif ctk.get_appearance_mode() == 'Dark':
                ctk.set_default_color_theme('green')
        if color_theme == 'blue':
            ctk.set_default_color_theme('blue')
        elif color_theme == 'green':
            ctk.set_default_color_theme('green')

    def cpu_monitoring(self):
        '''
        The function is for monitoring CPU usage.
        It calculates the percentage of CPU usage,
        creates a bar on the graph with the corresponding
        height and color, and updates the graph every 500 milliseconds.
        '''
        
        # Get the percentage of CPU usage
        value = psutil.cpu_percent(percpu=True)
        value = round(sum(value) / len(value), 1)
        
        # Calculate the height of the bar for the graph
        height = (value / 100) * 150 if (value / 100) * 150 >= 5 else 5
        
        # Determine the color of the bar depending on the level of CPU usage
        if value < 26:
            self.COLOR = 'green'
        elif value < 51:
            self.COLOR = 'yellow'
        elif value < 76:
            self.COLOR = 'orange'
        elif value < 96:
            self.COLOR = 'red'
        else:
            self.COLOR = 'black'

        # Create a new bar with the calculated height and color
        bar = ctk.CTkFrame(
            master=self.monitoring_frame,
            height=height,
            width=8,
            fg_color=self.COLOR
        )        
        
        # Add the new bar to the beginning of the list of bars
        self.LIST_BARS = [bar] + self.LIST_BARS
        self.LIST_HEIGHTS = [height] + self.LIST_HEIGHTS

        # If the number of bars exceeds 29, remove the oldest one (last in the list)
        if len(self.LIST_BARS) > 29 and len(self.LIST_HEIGHTS) > 29:
            old_bar = self.LIST_BARS.pop()
            self.LIST_HEIGHTS.pop()
            old_bar.destroy()

        # Place all bars on the graph
        for i, widget in enumerate(self.LIST_BARS):
            widget.place(x=600-((i+1)*20), y=200-self.LIST_HEIGHTS[i])

        # Update the text label displaying the current CPU usage
        self.cpu_percent_label.configure(text=f'{value}%', text_color=self.COLOR)

        # Loop the function to update the graph every 500 milliseconds
        self.func_after = self.after(500, self.cpu_monitoring)
        #self.after_cancel(self.func_after)


    def cpu_reload(self):
        '''
        Reloads the CPU depending on the layout.
        '''
        
        # For debugging Windows error codes in the current thread
        user32 = ctypes.WinDLL('user32', use_last_error=True)
        # Get the handle of the current active window
        curr_window = user32.GetForegroundWindow()
        # Get the thread identifier for the current window
        thread_id = user32.GetWindowThreadProcessId(curr_window, 0)
        # Get the keyboard layout identifier
        klid = user32.GetKeyboardLayout(thread_id)
        lid = klid & (2**16 - 1)
        # Convert the language identifier from decimal to hexadecimal
        lid_hex = hex(lid)

        if lid_hex == '0x409':                  # English
            keyboard.send('ctrl+shift+win+b')
        if lid_hex == '0x419':                  # Russian
            keyboard.send('ctrl+shift+win+и')

    def home_menu_open(self):
        self.home_frame.place(x=48, y=0)

    def set_blur(self) -> None:
        pywinstyles.apply_style(self, 'aero') # Apply aero style
        pywinstyles.change_header_color(self, color='#172833') # Change header color

if __name__ == '__main__':
    app = Main() # Create an instance of the class