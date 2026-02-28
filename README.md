# Encrypted Multi-User Chat System

Real-time multi-user chat system secured by a hybrid encryption model using **RSA (2048-bit)** and **AES-256 (CFB)**. 

---

##  Features

* **Hybrid Encryption Architecture**: Combines the security of RSA with the speed of AES.
* **Real-Time Communication**: Multi-threaded TCP server for simultaneous client handling.
* **Server Discovery**: Uses UDP broadcasting to identify the server on the network.
* **High Security Standards**:
    * **RSA-2048**: Used for secure AES key exchange with OAEP padding and SHA256.
    * **AES-256 (CFB mode)**: Used for encrypting message content with unique Initialization Vectors (IV) per message.

##  Technical Stack

* **Language**: Python 3.x
* **GUI Library**: `customtkinter`
* **Cryptography**: `cryptography` (hazmat primitives)
* **Networking**: `socket`, `threading`

##  Security Workflow

1.  **Handshake**: Upon connection, the server sends its **RSA Public Key** to the client.
2.  **Key Exchange**: The client generates a random **32-byte AES-256 key**, encrypts it using the server's public key, and sends it back.
3.  **Encrypted Tunnel**: All chat messages are encrypted using the shared AES key.
4.  **Unique IVs**: Every message sent includes a unique 16-byte Initialization Vector to prevent pattern recognition in ciphertext.

##  Getting Started

### Requirements
Install the required dependencies:
```bash
pip install customtkinter cryptography
