import pyshark

def analyze_dns_pcap(pcap_file_path):
    try:
        capture = pyshark.FileCapture(
            pcap_file_path,
            display_filter='dns'
        )
        
        print("DNS Traffic Analysis (Queries Only):")
        print("-" * 80)
        print(f"{'Pkt #':<6} {'Src IP':<15} {'Domain':<50} {'Type':<8}")
        print("-" * 80)
        
        packet_count = 0
        query_count = 0
        
        for packet in capture:
            packet_count += 1
            
            if not hasattr(packet, 'ip') or not hasattr(packet, 'dns'):
                continue
            
            src_ip = packet.ip.src
            
            # Check if it's a query using flags_tree
            is_query = False
            domain = "N/A"
            qtype = "N/A"
            
            if hasattr(packet.dns, 'flags_tree'):
                flags_tree = packet.dns.flags_tree
                if hasattr(flags_tree, 'dns_flags_response') and flags_tree.dns_flags_response == '0':
                    is_query = True
            
            # Alternative fallback: check raw flags hex (QR is MSB bit)
            elif hasattr(packet.dns, 'flags') and packet.dns.flags.startswith('0x0'):
                is_query = True
            
            if is_query:
                # Get domain name
                if hasattr(packet.dns, 'qry_name'):
                    domain = packet.dns.qry_name
                # Sometimes it's qry.name for older dissectors
                elif 'dns.qry.name' in packet.dns.field_names:
                    domain = packet.dns.get_field_value('dns.qry.name')
                
                if hasattr(packet.dns, 'qry_type'):
                    qtype = packet.dns.qry_type
                
                print(f"{packet_count:<6} {src_ip:<15} {domain:<50} {qtype:<8}")
                query_count += 1
        
        print(f"\nTotal DNS packets: {packet_count}")
        print(f"Queries found and printed: {query_count}")
        
        if query_count == 0:
            print("No DNS queries found. Check if capture contains queries (not just responses).")
        
        capture.close()
    
    except Exception as e:
        print(f"Error processing pcap: {e}")

if __name__ == "__main__":
    file_path = "/home/kali/Downloads/my_dns_new.pcap"  
    analyze_dns_pcap(file_path)
