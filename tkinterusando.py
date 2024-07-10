import tkinter as tk
from tkinter import font
import serial
from PIL import Image, ImageTk
import threading
import re
import time

class ContadorBotellasApp:
    def __init__(self, ventana):
        
        color_ventana_principal = "gray"
        color_demas_widgets = "darkgray"
        color_texto = "darkred"
        
        self.tamano_fuente_numero = 0.45
        self.cifras = 2
        
        self.ser = None  # Inicializa la variable ser
        
        self.timer_id = None
        self.tiempo_inactividad = 15000  # 10 s en milisegundos
        
        self.iniciado_con_mostrar = False
        self.mensaje_bienvenida = None
        self.parpadeo_activo = False
        self.pantalla_activa = False

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
        # Ocultar la interfaz al inicio
        self.ocultar_interfaz()

    def actualizar_contador(self):
        self.etiqueta_contador.config(text=self.contador, font=self.fuente_contador)
        self.ventana.after(500, self.actualizar_contador)

    def cambiar_contador(self, num):
        self.contador = num
        if self.parpadeo_activo:
            self.ocultar_mensaje_bienvenida()
            self.marco_principal.place(relx=0.02, rely=0.02, relwidth=0.95, relheight=0.95)
        self.mostrar_animacion_botella()
        self.ventana.after(500, self.ocultar_animacion_botella)

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
        self.ventana.bind("<KeyPress-x>", lambda event: self.cerrar_aplicacion())

    def cerrar_aplicacion(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
        self.ventana.destroy()
        
    def set_serial_connection(self, ser):
        self.ser = ser
        
    def cambiar_tamano_fuente(self):
        self.tamano_fuente_numero = self.tamano_fuente_numero * 0.8
        self.fuente_contador.configure(size=int(self.alto_pantalla * self.tamano_fuente_numero))
        self.cifras += 1
        
    def ocultar_interfaz(self):
        self.marco_principal.place_forget()
        self.ventana.configure(bg="black")
        self.pantalla_activa = False

    def mostrar_interfaz(self):
        if not self.pantalla_activa:
            self.ventana.configure(bg="gray")
            if self.iniciado_con_mostrar:
                self.mostrar_mensaje_bienvenida()
            else:
                self.marco_principal.place(relx=0.02, rely=0.02, relwidth=0.95, relheight=0.95)
            self.reiniciar_temporizador()
            self.pantalla_activa = True
                
    def reiniciar_temporizador(self):
        if self.timer_id:
            self.ventana.after_cancel(self.timer_id)
        self.timer_id = self.ventana.after(self.tiempo_inactividad, self.ocultar_interfaz)

    def actividad_detectada(self):
        self.reiniciar_temporizador()
        self.mostrar_interfaz()
        
    def mostrar_mensaje_bienvenida(self):
        # Crear un nuevo frame que cubra toda la pantalla
        self.frame_bienvenida = tk.Frame(self.ventana, bg="darkgray")
        self.frame_bienvenida.place(relx=0, rely=0, relwidth=1, relheight=1)

        if not self.mensaje_bienvenida:
            self.mensaje_bienvenida = tk.Label(self.frame_bienvenida, 
                                               text="¡Hola!\nIngrese botella por favor", 
                                               font=self.fuente_titulo, 
                                               fg="darkred", 
                                               bg="darkgray")
        self.mensaje_bienvenida.place(relx=0.5, rely=0.5, anchor="center")
        self.parpadeo_activo = True
        self.parpadear_mensaje()

    def parpadear_mensaje(self):
        if self.parpadeo_activo:
            current_color = self.mensaje_bienvenida.cget("fg")
            new_color = "darkgray" if current_color == "darkred" else "darkred"
            self.mensaje_bienvenida.config(fg=new_color)
            self.ventana.after(500, self.parpadear_mensaje)

    def ocultar_mensaje_bienvenida(self):
        if self.mensaje_bienvenida:
            self.frame_bienvenida.place_forget()
        self.parpadeo_activo = False


def intentar_conexion_serial(puerto, baudrate, app):
    """Función para intentar conectarse al puerto serial repetidamente."""
    while True:
        try:
            ser = serial.Serial(puerto, baudrate, timeout=1)
            print(f"Conexión exitosa al puerto {puerto}")
            app.set_serial_connection(ser)  # Actualiza la referencia en la app
            recibir_datos_serial(ser, app)
        except serial.SerialException as e:
            print(f"Error al abrir el puerto serial {puerto}: {e}")
            print("Reintentando en 5 segundos...")
            time.sleep(5)
            

def recibir_datos_serial(ser, app):
    while True:
        try:
            if ser.in_waiting > 0:
                linea = ser.readline().decode('utf-8').rstrip()
                print(f"Recibido: {linea}")
                
                if linea.strip().lower() == "mostrar":
                    if not app.pantalla_activa:
                        app.iniciado_con_mostrar = True
                        app.ventana.after(0, app.actividad_detectada)
                    continue
                
                # Reiniciar el temporizador y mostrar la interfaz
                app.ventana.after(0, app.actividad_detectada)
                
                # Separar la línea en etiqueta y número
                partes = linea.split(':')
                if len(partes) == 2:
                    etiqueta = partes[0].strip()
                    numero = partes[1].strip()
                    
                    print("etiqueta:", etiqueta)
                    print("numero:", numero)
                    
                    # Actualizar el contador si la etiqueta es "CUENTA" y el número es un dígito
                    if etiqueta == "CUENTA" and re.match(r"\d+", numero):
                        if len(numero) >= app.cifras:
                            print("Hola debería cambiar")
                            app.cambiar_tamano_fuente()
                        
                        app.cambiar_contador(numero)
        except serial.SerialException:
            print("Conexión serial perdida. Reiniciando...")
            break

def iniciar_conexion_serial(puerto, baudrate, app):
    """Función para iniciar el hilo de conexión serial."""
    hilo_serial = threading.Thread(target=intentar_conexion_serial, args=(puerto, baudrate, app))
    hilo_serial.daemon = True
    hilo_serial.start()

if __name__ == "__main__":
    # Crear la ventana principal de Tkinter
    ventana_principal = tk.Tk()
    
    # Inicializar la aplicación del contador de botellas
    app = ContadorBotellasApp(ventana_principal)
    
    # Iniciar la conexión serial en un hilo separado
    iniciar_conexion_serial('COM7', 9600, app)
    
    # Iniciar el bucle principal de la interfaz gráfica
    ventana_principal.mainloop()