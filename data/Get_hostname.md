This document outlines the description and implementation of a Python program designed to verify the existence of a specific hostname (with a www prefix and .com suffix) and, if valid, retrieve its corresponding IP address.
The program uses core networking concepts, which are explained in the sections below.
Technical Definitions
Term        Description
====        ==============  	
Hostname:	A label assigned to a device connected to a network, used to identify it uniquely from other devices on that specific network. Examples: google.com, localhost, www.example.com.
IP Address:	An Internet Protocol address is a numerical label assigned to each device connected to a network that uses the Internet Protocol for communication. It serves two main functions: host or network interface identification and location addressing. Example: 142.250.186.46.
Socket:	    A programming endpoint for communication. Sockets provide the mechanism for data exchange between a client and a server, often used for network services like retrieving IP addresses. In Python, the socket module provides access to the BSD socket interface.
Prefix/Suffix:	In a URL or hostname context: A prefix is the beginning of the string (e.g., www in www.example.com), and a suffix is the end of the string (e.g., .com in www.example.com). Our program specifically mandates these components.

Program Description
The Python script takes a user input (e.g., just the domain name like "google") and constructs a fully qualified domain name (FQDN) using the strict format: www.[user_input].com.
It then leverages the socket library to attempt a DNS (Domain Name System) lookup. The DNS acts like an internet phonebook, translating human-readable hostnames into machine-readable IP addresses.
If the lookup succeeds, the program reports the constructed hostname and its associated IP address.
If the lookup fails (meaning the hostname does not exist or cannot be reached), the program handles the error gracefully and informs the user that the host is unreachable or invalid.

Python Source Code
The following Python script implements the described functionality. This code requires Python 3.x to run.

import socket

def get_ip_from_hostname(domain_core):
    """
    Constructs a hostname with specific prefix and suffix, 
    and attempts to resolve its IP address using DNS lookup.
    """
    prefix = "www"
    suffix = "com"
    
    # Construct the full hostname based on the requirements
    hostname = f"{prefix}.{domain_core}.{suffix}"
    
    print(f"\nAttempting to resolve hostname: {hostname}")

    try:
        # Perform the DNS lookup using socket.gethostbyname()
        # This function interacts with the operating system's networking stack
        ip_address = socket.gethostbyname(hostname)
        
        print("-" * 40)
        print(f"✅ Success: Hostname '{hostname}' exists.")
        print(f"🔗 IP Address: {ip_address}")
        print("-" * 40)

    except socket.gaierror:
        # gaierror stands for "Get Address Info Error", raised when DNS fails
        print("-" * 40)
        print(f"❌ Error: Hostname '{hostname}' could not be resolved.")
        print("Please check the domain name or your network connection.")
        print("-" * 40)
    except Exception as e:
        # Catch any other potential errors
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    print("--- Hostname IP Resolver ---")
    user_input = input("Enter the domain name (e.g., 'google', 'microsoft'): ")
    
    if user_input:
        get_ip_from_hostname(user_input.strip())
    else:
        print("Input cannot be empty.")
		
		
How to Run the Program
1. Save the code: Save the code above as a Python file (e.g., resolve_host.py).
2. Open your terminal or command prompt.
3. Navigate to the directory where you saved the file.
4. Execute the script using the following command: python resolve_host.py
5. Follow the prompt and enter a valid domain core (like apple or amazon) to see the results.