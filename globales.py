admin = False

from pyBCV import Currency
import customtkinter as ctk

ctk.set_default_color_theme("blue") # O el tema que prefieras
currency = Currency()
all_rates = currency.get_rate() # obtener todas las tasas de cambio de moneda
usd = currency.get_rate(currency_code='USD', prettify=False) # obtener la tasa de cambio del dólar estadounidense sin símbolo de moneda
last_update = currency.get_rate(currency_code='Fecha') # obtener la hora de la última actualización

usd_rate = round(float(usd), 2) 