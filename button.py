import PySimpleGUI as sg

 
#Draw the button
layout = [[sg.Button('Quit Game', size=(30,4))]]
 
#Draw the window
window = sg.Window('GUI SAMPLE', layout, size=(400,400))
 
#Define what happens when the button is clicked
event, values = window.read()
