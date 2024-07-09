import tkinter as tk
from tkinter import font
import serial
from PIL import Image, ImageTk
import threading
import re

class ContadorBotellasApp:
    def __init__(self, ventana):
        
        color_ventana_principal = "gray"
        color_demas_widgets = "darkgray"
        color_texto = "darkred"
        
        self.tamano_fuente_numero = 0.45
        self.cifras = 2
        
        self.ventana = ventana
        self.ventana.attributes('-fullscreen', True)
        self.ventana.title("Contador de Botellas")
        self.ventana.configure(bg=color_ventana_principal)
        
        titulo2 = "Cuenta de\nbotellas\nrecicladas"

        # Obtener dimensiones de la pantalla
        self.ancho_pantalla = self.ventana.winfo_screenwidth()
        self.alto_pantalla = self.ventana.winfo_screenheight()

        # Configuración del contador inicial
        self.contador = "X"
        
        # Cargar la imagen de la botella
        self.imagen_botella = Image.open("./bottle.png")
        self.imagen_botella = self.imagen_botella.resize((int(self.alto_pantalla * 0.35), int(self.alto_pantalla * 0.75)))
        self.foto_botella = ImageTk.PhotoImage(self.imagen_botella)
        
        # Crear marco principal
        self.marco_principal = tk.Frame(ventana, bg=color_demas_widgets, highlightthickness=6, highlightbackground="darkred")
        self.marco_principal.place(relx=0.02, rely=0.02, relwidth=0.95, relheight=0.95)

        # Crear frames izquierdo y derecho
        self.frame_izquierda = tk.Frame(self.marco_principal, bg=color_demas_widgets)
        self.frame_izquierda.place(relx=0, rely=0, relwidth=0.4, relheight=1)

        self.frame_derecha = tk.Frame(self.marco_principal, bg=color_demas_widgets)
        self.frame_derecha.place(relx=0.4, rely=0, relwidth=0.6, relheight=1)

        # Crear fuentes dinámicas
        self.fuente_titulo = font.Font(family="Roboto", size=int(self.alto_pantalla * 0.08), weight='bold')
        self.fuente_contador = font.Font(family="DSEG7 Classic", size=int(self.alto_pantalla * self.tamano_fuente_numero))

        # Configurar etiquetas
        self.etiqueta_texto = tk.Label(self.frame_izquierda, text=titulo2, 
                                       font=self.fuente_titulo, fg=color_texto, bg=color_demas_widgets)
        self.etiqueta_texto.place(relx=0.5, rely=0.5, anchor="center")

        self.etiqueta_contador = tk.Label(self.frame_derecha, text=self.contador, 
                                          font=self.fuente_contador, fg=color_texto, bg=color_demas_widgets)
        self.etiqueta_contador.place(relx=0.5, rely=0.5, anchor="center")
        
        # Crear etiquetas para la animación (inicialmente ocultas)
        self.etiqueta_imagen = tk.Label(self.frame_derecha, image=self.foto_botella, bg=color_demas_widgets)
        #self.etiqueta_nueva_botella = tk.Label(self.frame_derecha, text="+1", 
        #                                       font=self.fuente_titulo, 
        #                                       fg="green", bg=color_demas_widgets)

        # Actualizar el contador y crear botones
        self.actualizar_contador()
        self.crear_botones()

    def actualizar_contador(self):
        self.etiqueta_contador.config(text=self.contador, font=self.fuente_contador)
        self.ventana.after(500, self.actualizar_contador)

    def cambiar_contador(self, num):
        self.contador = num
        self.mostrar_animacion_botella()
        self.ventana.after(500, self.ocultar_animacion_botella)  # Ocultar después de 3 segundos

    def mostrar_animacion_botella(self):
        # Ocultar el contador actual
        self.etiqueta_contador.place_forget()

        # Mostrar la imagen de la botella y el texto
        self.etiqueta_imagen.place(relx=0.5, rely=0.5, anchor="center")
        #self.etiqueta_nueva_botella.place(relx=0.5, rely=0.75, anchor="center")
        
    def ocultar_animacion_botella(self):
        # Ocultar la imagen y el texto
        self.etiqueta_imagen.place_forget()
        #self.etiqueta_nueva_botella.place_forget()

        # Mostrar el contador actualizado
        self.etiqueta_contador.config(text=self.contador, font=self.fuente_contador)
        self.etiqueta_contador.place(relx=0.5, rely=0.5, anchor="center")

    def crear_botones(self):
        #boton_size = int(self.alto_pantalla * 0.02)  # Tamaño dinámico para el botón
        #self.boton_cerrar = tk.Button(self.frame_derecha, text="Cerrar", 
        #                              command=self.cerrar_aplicacion, 
        #                              font=('Arial', boton_size))
        #self.boton_cerrar.place(relx=0.5, rely=0.95, anchor="s")
        #
        self.ventana.bind("<KeyPress-x>", lambda event: self.cerrar_aplicacion())

    def cerrar_aplicacion(self):
        if ser and ser.is_open:
            ser.close()
        self.ventana.destroy()
        
    def cambiar_tamano_fuente(self):
        self.tamano_fuente_numero = self.tamano_fuente_numero * 0.8
        self.fuente_contador.configure(size=int(self.alto_pantalla * self.tamano_fuente_numero))
        self.cifras += 1


def recibir_datos_serial(ser, app):
    """Función para recibir datos seriales y actualizar el contador."""
    while True:
        if ser.in_waiting > 0:
            linea = ser.readline().decode('utf-8').rstrip()
            print(f"Recibido: {linea}")
            
            # Separar la línea en etiqueta y número
            partes = linea.split(':')
            etiqueta = partes[0].strip()
            numero = partes[1].strip()
            
            print("etiqueta:", etiqueta)
            print("numero:", numero)
            
            
            # Actualizar el contador si la etiqueta es "CUENTA" y el número es un dígito
            if etiqueta == "CUENTA" and re.match(r"\d+", numero):
                
                if len(numero) >= app.cifras:
                    print("Hola deberia cambiar")
                    app.cambiar_tamano_fuente()
                    
                app.cambiar_contador(numero)
                

if __name__ == "__main__":
    try:
        # Abrir el puerto serial
        ser = serial.Serial('COM7', 9600)
        
        # Crear la ventana principal de Tkinter
        ventana_principal = tk.Tk()
        
        # Inicializar la aplicación del contador de botellas
        app = ContadorBotellasApp(ventana_principal)
        
        # Crear un hilo para la recepción de datos seriales
        hilo_serial = threading.Thread(target=recibir_datos_serial, args=(ser, app))
        hilo_serial.daemon = True
        hilo_serial.start()
        
        # Iniciar el bucle principal de la interfaz gráfica
        ventana_principal.mainloop()
    
    except serial.SerialException as e:
        print(f"Error al abrir el puerto serial: {e}")
    
    finally:
        # Cerrar el puerto serial al salir
        if ser and ser.is_open:
            ser.close()
