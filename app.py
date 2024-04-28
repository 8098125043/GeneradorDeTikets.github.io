import json
import os

class Ticket:
    PRIORIDADES = ["Baja", "Media", "Alta"]

    def __init__(self, id, cliente, asunto, prioridad="Media", estado="Abierto", agente_asignado=None):
        self.id = id
        self.cliente = cliente
        self.asunto = asunto
        self.prioridad = prioridad
        self.estado = estado
        self.agente_asignado = agente_asignado
        self.comentarios = []

    def __str__(self):
        return f"ID: {self.id}, Cliente: {self.cliente}, Asunto: {self.asunto}, Prioridad: {self.prioridad}, Estado: {self.estado}, Agente Asignado: {self.agente_asignado}"

    def agregar_comentario(self, comentario):
        self.comentarios.append(comentario)

    def ver_comentarios(self):
        if self.comentarios:
            print("Comentarios:")
            for comentario in self.comentarios:
                print(comentario)
        else:
            print("No hay comentarios para este ticket.")

class TicketManager:
    
    def __init__(self):
        self.tickets = []
        self.next_id = 1

    def crear_ticket(self, cliente, asunto, prioridad):
        ticket = Ticket(self.next_id, cliente, asunto, prioridad)
        self.tickets.append(ticket)
        self.next_id += 1
        print("Se creó su ticket.")
        return ticket

    def modificar_ticket(self, id_ticket):
        if not id_ticket.isdigit():
            print("El ID del ticket debe ser un número.")
            return

        id_ticket = int(id_ticket)

        if id_ticket < 1 or id_ticket > len(self.tickets):
            print("El ID del ticket no es válido.")
            return

        ticket = self.buscar_ticket_por_id(id_ticket)
        if ticket:
            print(f"Modificando ticket {id_ticket}:")
            cliente = input("Nuevo nombre del cliente (deje en blanco para mantener el actual): ")
            asunto = input("Nuevo asunto del ticket (deje en blanco para mantener el actual): ")
            prioridad = input("Nueva prioridad del ticket (Baja/Media/Alta, deje en blanco para mantener la actual): ")
            estado = input("Nuevo estado del ticket (Abierto/Cerrado, deje en blanco para mantener el actual): ")
            agente_asignado = input("Nuevo agente asignado al ticket (deje en blanco para mantener el actual): ")

            if cliente:
                ticket.cliente = cliente
            if asunto:
                ticket.asunto = asunto
            if prioridad:
                ticket.prioridad = prioridad
            if estado:
                ticket.estado = estado
            if agente_asignado:
                ticket.agente_asignado = agente_asignado

            print(f"Ticket {id_ticket} modificado con éxito.")
        else:
            print(f"No se encontró ningún ticket con ID {id_ticket}.")

    def eliminar_ticket(self, id_ticket):
        if not id_ticket.isdigit():
            print("El ID del ticket debe ser un número.")
            return

        id_ticket = int(id_ticket)

        if id_ticket < 1 or id_ticket > len(self.tickets):
            print("El ID del ticket no es válido.")
            return

        ticket = self.buscar_ticket_por_id(id_ticket)
        if ticket:
            self.tickets.remove(ticket)
            print(f"Ticket {id_ticket} eliminado.")
        else:
            print(f"No se encontró ningún ticket con ID {id_ticket}.")

    def listar_tickets(self):
        print("Lista de tickets:")
        for ticket in self.tickets:
            print(ticket)

    def buscar_tickets_por_cliente(self, cliente):
        encontrados = [ticket for ticket in self.tickets if ticket.cliente == cliente]
        if encontrados:
            print(f"Tickets para el cliente {cliente}:")
            for ticket in encontrados:
                print(ticket)
        else:
            print(f"No se encontraron tickets para el cliente {cliente}.")

    def buscar_tickets_por_estado(self, estado):
        encontrados = [ticket for ticket in self.tickets if ticket.estado == estado]
        if encontrados:
            print(f"Tickets en estado {estado}:")
            for ticket in encontrados:
                print(ticket)
        else:
            print(f"No se encontraron tickets en estado {estado}.")

    def asignar_agente(self, id_ticket, agente):
        try:
            id_ticket = int(id_ticket)
        except ValueError:
            print("El ID del ticket debe ser un número.")
            return

        if id_ticket < 1 or id_ticket > len(self.tickets):
            print("El ID del ticket no es válido.")
            return

        ticket = self.buscar_ticket_por_id(id_ticket)
        if ticket:
            ticket.agente_asignado = agente
            print(f"Agente {agente} asignado al ticket {id_ticket}.")
        else:
            print(f"No se encontró ningún ticket con ID {id_ticket}.")

    def cerrar_ticket(self, id_ticket):
        try:
            id_ticket = int(id_ticket)
        except ValueError:
            print("El ID del ticket debe ser un número.")
            return

        if id_ticket < 1 or id_ticket > len(self.tickets):
            print("El ID del ticket no es válido.")
            return

        ticket = self.buscar_ticket_por_id(id_ticket)
        if ticket:
            ticket.estado = "Cerrado"
            print(f"El ticket {id_ticket} ha sido cerrado.")
        else:
            print(f"No se encontró ningún ticket con ID {id_ticket}.")

    def buscar_ticket_por_id(self, id_ticket):
        for ticket in self.tickets:
            if ticket.id == id_ticket:
                return ticket
        print(f"No se encontró ningún ticket con ID {id_ticket}.")
        return None

    def exportar_tickets_json(self, nombre_archivo, ruta):
        ruta_completa = os.path.join(ruta, nombre_archivo)
        tickets_data = []
        for ticket in self.tickets:
            ticket_data = {
                "ID": ticket.id,
                "Cliente": ticket.cliente,
                "Asunto": ticket.asunto,
                "Prioridad": ticket.prioridad,
                "Estado": ticket.estado,
                "Agente Asignado": ticket.agente_asignado
            }
            tickets_data.append(ticket_data)

        with open(ruta_completa, 'w') as file:
            json.dump(tickets_data, file, indent=4)

        print(f"Los tickets se han exportado correctamente en {ruta_completa}.")

class TicketApp:
    def __init__(self):
        self.ticket_manager = TicketManager()
        self.registro_acciones = []

    def mostrar_menu(self):
        while True:
            print("\n--- Menú de Tickets ---")
            print("1. Crear un nuevo ticket")
            print("2. Modificar ticket")
            print("3. Eliminar ticket")
            print("4. Listar todos los tickets")
            print("5. Asignar un agente a un ticket")
            print("6. Cerrar un ticket")
            print("7. Buscar tickets por cliente")
            print("8. Buscar tickets por estado")
            print("9. Exportar tickets a JSON")
            print("0. Salir")
            opcion = input("Ingrese el número de la opción que desea realizar: ")

            if opcion == "1":
                self.crear_ticket()
            elif opcion == "2":
                self.modificar_ticket()
            elif opcion == "3":
                self.eliminar_ticket()
            elif opcion == "4":
                self.listar_tickets()
            elif opcion == "5":
                self.asignar_agente()
            elif opcion == "6":
                self.cerrar_ticket()
            elif opcion == "7":
                self.buscar_por_cliente()
            elif opcion == "8":
                self.buscar_por_estado()
            elif opcion == "9":
                self.exportar_tickets_json()
            elif opcion == "0":
                print("Saliendo del programa...")
                break
            else:
                print("Opción no válida. Por favor, ingrese un número válido.")

    def registrar_accion(self, accion):
        self.registro_acciones.append(accion)

    def crear_ticket(self):
        cliente = input("Ingrese el nombre del cliente: ")
        asunto = input("Ingrese el asunto del ticket: ")
        prioridad = input("Ingrese la prioridad del ticket (Baja/Media/Alta): ")
        self.ticket_manager.crear_ticket(cliente, asunto, prioridad)
        self.registrar_accion(f"Nuevo ticket creado por {cliente}")

    def modificar_ticket(self):
        id_ticket = input("Ingrese el ID del ticket que desea modificar: ")
        self.ticket_manager.modificar_ticket(id_ticket)
        self.registrar_accion(f"Modificación del ticket {id_ticket}")

    def eliminar_ticket(self):
        id_ticket = input("Ingrese el ID del ticket que desea eliminar: ")
        self.ticket_manager.eliminar_ticket(id_ticket)
        self.registrar_accion(f"Eliminación del ticket {id_ticket}")

    def listar_tickets(self):
        self.ticket_manager.listar_tickets()
        self.registrar_accion("Listado de todos los tickets")

    def asignar_agente(self):
        id_ticket = input("Ingrese el ID del ticket que desea asignar: ")
        agente = input("Ingrese el nombre del agente: ")
        self.ticket_manager.asignar_agente(id_ticket, agente)
        self.registrar_accion(f"Asignación de agente {agente} al ticket {id_ticket}")

    def cerrar_ticket(self):
        id_ticket = input("Ingrese el ID del ticket que desea cerrar: ")
        self.ticket_manager.cerrar_ticket(id_ticket)
        self.registrar_accion(f"Cierre del ticket {id_ticket}")

    def buscar_por_cliente(self):
        cliente = input("Ingrese el nombre del cliente: ")
        self.ticket_manager.buscar_tickets_por_cliente(cliente)
        self.registrar_accion(f"Búsqueda de tickets por cliente: {cliente}")

    def buscar_por_estado(self):
        estado = input("Ingrese el estado del ticket (Abierto/Cerrado): ")
        self.ticket_manager.buscar_tickets_por_estado(estado)
        self.registrar_accion(f"Búsqueda de tickets por estado: {estado}")

    def exportar_tickets_json(self):
        nombre_archivo = input("Ingrese el nombre del archivo JSON para exportar los tickets: ")
        ruta = "C:\\Users\\Ana Alcantara\\Desktop\\Archivos txt"  # Ruta donde se guarda el archivo
        self.ticket_manager.exportar_tickets_json(nombre_archivo, ruta)
        self.registrar_accion(f"Exportación de tickets a JSON: {nombre_archivo}")

if __name__ == "__main__":
    app = TicketApp()
    app.mostrar_menu()

    # Mostrar registro de acciones al salir del programa
    print("------------------------------------------------")
    print("\nRegistro de Acciones:")
    for accion in app.registro_acciones:
        print(accion)
    print("------------------------------------------------")