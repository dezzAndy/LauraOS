import os
import msvcrt
from clear_screen import clear_screen

def logo():
   clear_screen()
   print("""          .-.                                           .-.
         / (_)                          .--.    .-.--.-'   
        /      .-.  )  (   ).--..-.    /    )`-' (  (_)    
       /      (  | (    ) /    (  |   /    /      `-.      
    .-/.    .-.`-'-'`--':/      `-'-'(    /     _    )     
   (_/ `-._.                          `-.'     (_.--'      
   """)
   print("Presiona cualquier tecla para continuar...")
   msvcrt.getch()
   clear_screen()
