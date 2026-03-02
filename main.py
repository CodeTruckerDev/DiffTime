#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
DiffTime - minimalistyczny kalkulator różnicy czasu
Autor: CodeTruckerDev
Data: 2026
"""

from datetime import datetime
from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.core.window import Window
from kivy.metrics import dp

Window.clearcolor = (0.96, 0.96, 0.97, 1)


class NumInput(TextInput):
    """Pole na 2 cyfry – klawiatura numeryczna, auto-focus na następne pole"""

    next_widget = None  # ustawiany po build

    def insert_text(self, substring, from_undo=False):
        if not substring.isdigit():
            return
        if len(self.text) >= 2:
            return
        super().insert_text(substring, from_undo=from_undo)
        # Po wpisaniu 2 cyfr przejdź do następnego pola
        if len(self.text) == 2 and self.next_widget:
            self.next_widget.focus = True


class DiffTimeRoot(BoxLayout):
    pass


class DiffTimeApp(App):
    result_text = StringProperty('--h --min')

    def build(self):
        root = DiffTimeRoot()
        # Podpięcie kolejności focusu
        ids = root.ids
        fields = [ids.d1_dd, ids.d1_mm, ids.d1_hh, ids.d1_min,
                  ids.d2_dd, ids.d2_mm, ids.d2_hh, ids.d2_min]
        for i, f in enumerate(fields[:-1]):
            f.next_widget = fields[i + 1]
        return root

    # ------------------------------------------------------------------ #

    def is_leap_year(self, year):
        return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

    def days_in_month(self, month, year):
        table = [31, 29 if self.is_leap_year(year) else 28,
                 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        return table[month - 1]

    def get_int(self, widget_id, lo, hi, year=None, month=None):
        """Zwraca int jeśli wartość w przedziale, inaczej None"""
        text = self.root.ids[widget_id].text
        if len(text) != 2:
            return None
        try:
            v = int(text)
        except ValueError:
            return None
        if lo <= v <= hi:
            # Dodatkowa kontrola dla dnia
            if month is not None and year is not None:
                if v > self.days_in_month(month, year):
                    return None
            return v
        return None

    def update_result(self, *args):
        ids = self.root.ids
        year = datetime.now().year

        mm1 = self.get_int('d1_mm', 1, 12)
        mm2 = self.get_int('d2_mm', 1, 12)

        dd1 = self.get_int('d1_dd', 1, 31, year, mm1) if mm1 else None
        dd2 = self.get_int('d2_dd', 1, 31, year, mm2) if mm2 else None
        hh1 = self.get_int('d1_hh', 0, 23)
        mi1 = self.get_int('d1_min', 0, 59)
        hh2 = self.get_int('d2_hh', 0, 23)
        mi2 = self.get_int('d2_min', 0, 59)

        if None in (dd1, mm1, hh1, mi1, dd2, mm2, hh2, mi2):
            self.result_text = '--h --min'
            return

        try:
            dt1 = datetime(year, mm1, dd1, hh1, mi1)
            dt2 = datetime(year, mm2, dd2, hh2, mi2)
            diff = abs(dt2 - dt1)
            total_min = int(diff.total_seconds() // 60)
            self.result_text = f'{total_min // 60}h {total_min % 60}min'
        except ValueError:
            self.result_text = '--h --min'


if __name__ == '__main__':
    DiffTimeApp().run()
