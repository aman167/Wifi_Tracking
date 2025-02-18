from scapy.all import ARP, Ether, srp
import pywifi
from pywifi import const
import time

def get_rssi_values():
    """Scan for nearby Wi-Fi devices and return MAC-RSSI pairs"""
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]  # Use first wireless interface
    
    iface.scan()
    time.sleep(5)  # Wait for scan results
    
    scan_results = iface.scan_results()
    
    rssi_values = {}
    for result in scan_results:
        mac = result.bssid.upper().replace('-', ':')
        rssi_values[mac] = result.signal
    
    return rssi_values

def enhanced_network_scan(network):
    """Combine ARP scan with RSSI detection"""
    # Get device list from ARP scan
    arp_request = ARP(pdst=network)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = broadcast / arp_request

    result = srp(packet, timeout=3, verbose=0)[0]
    
    devices = []
    for sent, received in result:
        devices.append({'ip': received.psrc, 'mac': received.hwsrc.upper()})

    # Get RSSI values
    rssi_data = get_rssi_values()
    
    # Combine data
    for device in devices:
        device['rssi'] = rssi_data.get(device['mac'], 'N/A')
    
    return devices

if __name__ == "__main__":
    target_network = "192.168.2.0/24"
    print(f"Scanning {target_network} with RSSI...")
    
    devices = enhanced_network_scan(target_network)
    
    print("\nConnected Devices:")
    for device in devices:
        print(f"IP: {device['ip']:15} | MAC: {device['mac']} | RSSI: {device['rssi']}dBm")
