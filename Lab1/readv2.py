import sys
from scapy.all import rdpcap, ICMP, Raw

def descifrar_cesar(texto, corrimiento):
    resultado = ""
    for char in texto:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            resultado += chr((ord(char) - base - corrimiento) % 26 + base)
        else:
            resultado += char
    return resultado

def extraer_mensaje(pcap_file):
    try:
        paquetes = rdpcap(pcap_file)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {pcap_file}")
        sys.exit(1)

    mensaje_cifrado = ""
    for pkt in paquetes:
        # Filtramos por ICMP Request (type=8) y el ID de nuestro modo stealth
        if ICMP in pkt and pkt[ICMP].type == 8 and pkt[ICMP].id == 4321:
            if pkt.haslayer(Raw):
                payload = pkt[Raw].load
                # Extraemos el primer byte inyectado y lo convertimos a texto
                char = chr(payload[0])
                mensaje_cifrado += char
    return mensaje_cifrado

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso correcto: sudo python3 readv2.py <archivo.pcapng>")
        sys.exit(1)
    
    archivo_pcap = sys.argv[1]
    cifrado = extraer_mensaje(archivo_pcap)
    
    print(f"\n{cifrado}\n")
    
    # Fuerza bruta para descubrir el corrimiento
    for shift in range(1, 26):
        texto_descifrado = descifrar_cesar(cifrado, shift)
        
        # Imprimimos en verde si coincide con el texto en claro esperado
        if "criptografia" in texto_descifrado.lower():
            print(f"\033[92m{texto_descifrado}\033[0m")
        else:
            print(texto_descifrado)