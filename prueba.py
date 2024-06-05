import tkinter as tk
from ttkthemes import ThemedStyle

root = tk.Tk()
style = ThemedStyle(root)

# Obtener y mostrar los temas disponibles
available_themes = style.theme_names()
print("Temas disponibles:", available_themes)

root.mainloop()
