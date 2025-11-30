#!/usr/bin/env python3
from nicegui import ui
from contextlib import redirect_stdout

dark = ui.dark_mode()


def my_function():
    print(f"Name")
    print(f"Age")
    print(f"City")

def run_and_capture():
    with redirect_stdout(log):
        my_function()

with ui.header().classes(replace='row items-center') as header:
    with ui.tabs() as tabs:
        ui.tab('A')
        ui.tab('B')
        ui.tab('C')
    ui.switch('Dark mode').bind_value(dark)

with ui.right_drawer(elevated=True) as drawer:
    ui.label('Side menu')

with ui.page_sticky(position='bottom-right', x_offset=20, y_offset=20):
    ui.button(on_click=drawer.toggle, icon='contact_support').props('fab')

with ui.tab_panels(tabs, value='A').classes('w-full'):
    with ui.tab_panel('A'):
        ui.label('Content of A')
        ui.button('Run', on_click=run_and_capture)
        log = ui.log()
    with ui.tab_panel('B'):
        ui.label('Content of B')
    with ui.tab_panel('C'):
        ui.label('Content of C')




ui.run(title="Test App")