import os
import msvcrt

def logo():
   os.system('clear')
   print("""          .-.                                           .-.
         / (_)                          .--.    .-.--.-'   
        /      .-.  )  (   ).--..-.    /    )`-' (  (_)    
       /      (  | (    ) /    (  |   /    /      `-.      
    .-/.    .-.`-'-'`--':/      `-'-'(    /     _    )     
   (_/ `-._.                          `-.'     (_.--'      
   """)
   print("Presiona cualquier tecla para continuar...")
   msvcrt.getch()
   os.system('clear')
