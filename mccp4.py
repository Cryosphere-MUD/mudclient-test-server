from telnetconstants import IAC, SB, SE, WILL, WONT, DO, DONT, TELOPT_MCCP4, TELOPT_MCCP2, command_name, option_name
import zstandard as zstd
import zlib
import time
import select

MCCP4_ACCEPT_ENCODING = 1
MCCP4_BEGIN_ENCODING = 2
MCCP4_WONT = 3

def validate_telnet_message(data):
    """Validate telnet protocol message format"""
    if len(data) < 3:
        return False, "Message too short"
        
    if data[0] != IAC:
        return False, "Invalid IAC start"
        
    # Check for subnegotiation
    if len(data) >= 5 and data[1] == SB:
        if data[-2] != IAC or data[-1] != SE:
            return False, "Invalid subnegotiation end"
        return True, "Valid subnegotiation"
        
    # Check for simple telnet commands
    if len(data) == 3 and data[1] in [WILL, WONT, DO, DONT]:
        return True, "Valid telnet command"
        
    return False, "Unknown message format"

def read_telnet_responses(telnet, timeout=1.0):
    """Read and display telnet responses from client"""
    responses = []
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        # Check if data is available
        ready = select.select([telnet.sock], [], [], 0.1)
        if ready[0]:
            try:
                data = telnet.sock.recv(1024)
                if data:
                    responses.append(data)
                else:
                    break
            except:
                break
        elif responses:
            break
    
    return b''.join(responses)

def parse_telnet_commands(data):
    """Parse telnet commands from client"""
    i = 0
    messages = []
    mccp4_accept_encoding = None
    
    while i < len(data):
        if i < len(data) and data[i] == IAC:
            if i + 1 < len(data):
                cmd = data[i+1]
                
                # Handle WILL/WONT/DO/DONT
                if cmd in [WILL, WONT, DO, DONT]:
                    if i + 2 < len(data):
                        opt = data[i+2]
                        cmd_name = command_name(cmd)
                        opt_name = option_name(opt)
                        messages.append(f"Client sent: IAC {cmd_name} {opt_name}")
                        i += 3
                        continue
                        
                # Handle subnegotiation
                elif cmd == SB:
                    # Find the SE
                    se_pos = data.find(bytes([IAC, SE]), i)
                    if se_pos != -1 and i + 2 < len(data):
                        opt = data[i+2]
                        subneg_data = data[i+3:se_pos]
                        opt_name = option_name(opt)
                        messages.append(f"Client sent: IAC SB {opt_name} [{len(subneg_data)} bytes] IAC SE")
                        
                        # Parse MCCP4 subnegotiation
                        if opt == TELOPT_MCCP4 and subneg_data:
                            if subneg_data[0] == MCCP4_ACCEPT_ENCODING:
                                encodings = subneg_data[1:].decode('ascii', errors='ignore')
                                messages.append(f"  -> ACCEPT_ENCODING: {encodings}")
                                mccp4_accept_encoding = encodings
                            elif subneg_data[0] == MCCP4_BEGIN_ENCODING:
                                encoding = subneg_data[1:].decode('ascii', errors='ignore')
                                messages.append(f"  -> BEGIN_ENCODING: {encoding}")
                            elif subneg_data[0] == MCCP4_WONT:
                                reason = subneg_data[1:].decode('ascii', errors='ignore') if len(subneg_data) > 1 else ""
                                messages.append(f"  -> WONT: {reason}" if reason else "  -> WONT")
                                
                        i = se_pos + 2
                        continue
        i += 1
    
    return messages, mccp4_accept_encoding

def mccp4_handler_zstd(telnet):
    """MCCP4 handler with zstd compression"""
    
    # Send greeting (uncompressed)
    telnet.sendall(b"=== MCCP4 Test with zstd ===\r\n")
    telnet.sendall(b"Testing MCCP4 protocol with zstd compression\r\n\r\n")
    
    # Step 1: Send IAC WILL COMPRESS4
    print("1. Server sends: IAC WILL COMPRESS4")
    will_message = bytes([IAC, WILL, TELOPT_MCCP4])
    print(f"   -> Raw bytes: {' '.join(f'{b:02x}' for b in will_message)}")
    telnet.sock.sendall(will_message)  # Use raw socket
    
    # Step 2: Wait for client response
    print("2. Waiting for client response...")
    time.sleep(0.1)
    response = read_telnet_responses(telnet, timeout=1.0)
    
    client_supports_mccp4 = False
    client_accept_encoding = None
    
    if response:
        print(f"   -> Received {len(response)} bytes from client")
        print(f"   -> Raw bytes: {' '.join(f'{b:02x}' for b in response[:50])}{'...' if len(response) > 50 else ''}")
        
        commands, accept_encoding = parse_telnet_commands(response)
        for cmd in commands:
            print(f"   {cmd}")
        
        # Check if client sent DO COMPRESS4
        if bytes([IAC, DO, TELOPT_MCCP4]) in response:
            client_supports_mccp4 = True
            client_accept_encoding = accept_encoding
            print("   -> Client supports MCCP4!")
        else:
            print("   -> Client does not support MCCP4")
            return
    else:
        print("   -> No response from client")
        return
    
    # Step 3: Handle ACCEPT_ENCODING
    compression_method = "zstd"
    if client_accept_encoding:
        print(f"\n3. Client sent ACCEPT_ENCODING: {client_accept_encoding}")
        if "zstd" not in client_accept_encoding:
            print("   -> Client doesn't support zstd, sending WONT")
            telnet.sock.sendall(bytes([IAC, WONT, TELOPT_MCCP4]))
            return
    else:
        print("\n3. No ACCEPT_ENCODING received - using legacy fallback mode")
    
    # Step 4: Send BEGIN_ENCODING with "zstd" 
    begin_encoding = bytes([
        IAC, SB, TELOPT_MCCP4,
        MCCP4_BEGIN_ENCODING,
        ord('z'), ord('s'), ord('t'), ord('d'),  # Raw ASCII bytes for "zstd"
        IAC, SE
    ])
    
    print(f"\n4. Server sends: IAC SB COMPRESS4 BEGIN_ENCODING '{compression_method}' IAC SE")
    print(f"   -> Raw bytes: {' '.join(f'{b:02x}' for b in begin_encoding)}")
    
    telnet.sock.sendall(begin_encoding)  # Use raw socket
    
    # Give client time to initialize decompressor
    time.sleep(0.01)
    
    print("5. Starting zstd compression (level 8)")
    print("   -> Everything after BEGIN_ENCODING is compressed\n")
    
    # Step 6: Send compressed data using ZSTD streaming
    compressor = zstd.ZstdCompressor(level=8)
    
    test_messages = [
        b"[COMPRESSED] This message is compressed with zstd!\r\n",
        b"[COMPRESSED] You're now receiving MCCP4 compressed data.\r\n",
        b"[COMPRESSED] Compression level: 8 (optimal for MUDs)\r\n",
        b"[COMPRESSED] This demonstrates MCCP4 protocol functionality.\r\n",
        b"[COMPRESSED] Using streaming compression for efficiency.\r\n"
    ]
    
    # Create streaming context for compression
    ctx = compressor.chunker(chunk_size=8192)
    
    try:
        for msg in test_messages:
            # Compress this message with flush
            compressed_chunks = list(ctx.compress(msg))
            compressed_chunks.extend(ctx.flush())
            
            # Send all compressed chunks using raw socket
            for chunk in compressed_chunks:
                if chunk:
                    telnet.sock.sendall(chunk)
                    
            print(f"   Sent (compressed): {msg.decode().strip()}")
            time.sleep(0.1)
            
        # Finalize compression stream
        print("\n7. Ending MCCP4 compression frame")
        final_chunks = list(ctx.finish())
        for chunk in final_chunks:
            if chunk:
                telnet.sock.sendall(chunk)
                print("   -> Final compression frame data sent")
        
        print("   -> Compression frame properly closed")
        
    except Exception as e:
        print(f"   -> Compression error: {e}")
        return
    
    # Step 8: Send DONT signal (uncompressed)
    print("8. Server sends: IAC DONT COMPRESS4 (uncompressed)")
    telnet.sock.sendall(bytes([IAC, DONT, TELOPT_MCCP4]))
    
    # Step 9: Send uncompressed data
    print("9. Sending uncompressed data again\n")
    telnet.sock.sendall(b"\r\n[UNCOMPRESSED] Back to normal uncompressed text.\r\n")
    telnet.sock.sendall(b"[UNCOMPRESSED] MCCP4 test complete!\r\n")
    telnet.sock.sendall(b"[UNCOMPRESSED] If you saw the compressed messages, MCCP4 worked!\r\n\r\n")
    
    print("   -> MCCP4 test completed successfully")

def mccp4_handler_deflate(telnet):
    """MCCP4 handler with deflate - switches to MCCP2 protocol since they're equivalent"""
    
    telnet.sendall(b"=== MCCP4 Test with deflate (MCCP2 compatibility mode) ===\r\n")
    telnet.sendall(b"MCCP4 deflate is equivalent to MCCP2 - switching to MCCP2 protocol\r\n\r\n")
    
    print("MCCP4 deflate requested - switching to MCCP2 protocol")
    
    # Step 1: Send IAC WILL MCCP2 (not MCCP4)
    print("1. Server sends: IAC WILL MCCP2")
    will_message = bytes([IAC, WILL, TELOPT_MCCP2])
    print(f"   -> Raw bytes: {' '.join(f'{b:02x}' for b in will_message)}")
    telnet.sock.sendall(will_message)
    
    # Step 2: Wait for client response
    print("2. Waiting for client response...")
    time.sleep(0.1)
    response = read_telnet_responses(telnet, timeout=1.0)
    
    if response:
        print(f"   -> Received {len(response)} bytes from client")
        print(f"   -> Raw bytes: {' '.join(f'{b:02x}' for b in response[:50])}{'...' if len(response) > 50 else ''}")
        
        # Check if client sent DO MCCP2
        if bytes([IAC, DO, TELOPT_MCCP2]) in response:
            print("   -> Client supports MCCP2!")
        else:
            print("   -> Client does not support MCCP2")
            return
    else:
        print("   -> No response from client")
        return
    
    # Step 3: Start MCCP2 compression (simple IAC SB MCCP2 IAC SE)
    print("\n3. Server sends: IAC SB MCCP2 IAC SE")
    start_compression = bytes([IAC, SB, TELOPT_MCCP2, IAC, SE])
    print(f"   -> Raw bytes: {' '.join(f'{b:02x}' for b in start_compression)}")
    telnet.sock.sendall(start_compression)
    
    # Give client time to initialize decompressor
    time.sleep(0.01)
    
    print("4. Starting MCCP2 compression")
    print("   -> Everything after this is compressed\n")
    
    # Step 4: Send compressed data
    data_to_compress = (
        b"[COMPRESSED] This message is compressed with MCCP2/deflate!\r\n"
        b"[COMPRESSED] You're now receiving MCCP2 compressed data.\r\n"  
        b"[COMPRESSED] Using standard zlib deflate compression.\r\n"
        b"[COMPRESSED] This demonstrates MCCP2 protocol functionality.\r\n"
    )
    
    try:
        # Use standard zlib compression for MCCP2
        compressed_data = zlib.compress(data_to_compress)
        print(f"   -> Generated MCCP2 frame: {len(compressed_data)} bytes")
        print(f"   -> Frame header: {' '.join(f'{b:02x}' for b in compressed_data[:8])}")
        
        # Send the complete compressed frame using raw socket
        telnet.sock.sendall(compressed_data)
        print("   -> MCCP2 compressed data sent successfully")
        
        time.sleep(0.2)  # Give client time to decompress
        
    except Exception as e:
        print(f"   -> Compression error: {e}")
        return
    
    # Step 5: End compression - no explicit signal needed for MCCP2
    print("\n5. MCCP2 compression complete")
    print("6. Sending uncompressed data again\n")
    
    # Send uncompressed data
    telnet.sock.sendall(b"\r\n[UNCOMPRESSED] Back to normal uncompressed text.\r\n")
    telnet.sock.sendall(b"[UNCOMPRESSED] MCCP2 test complete!\r\n")  
    telnet.sock.sendall(b"[UNCOMPRESSED] If you saw the compressed messages, MCCP2 worked!\r\n\r\n")
    
    print("   -> MCCP2 test completed successfully")

def mccp4_handler_fallback(telnet):
    """Test MCCP4 fallback mode (no ACCEPT_ENCODING)"""
    telnet.sendall(b"=== MCCP4 Fallback Mode (backward compatibility) ===\r\n\r\n")
    telnet.sendall(b"Testing MCCP4 fallback mode (no ACCEPT_ENCODING)\r\n\r\n")
    
    # Send WILL MCCP4
    telnet.sendall(b"1. Server sends: IAC WILL MCCP4\r\n")
    telnet.sendall(bytes([IAC, WILL, TELOPT_MCCP4]))
    
    # Wait for DO response
    response = read_telnet_responses(telnet, timeout=1.0)
    if not response or bytes([IAC, DO, TELOPT_MCCP4]) not in response:
        telnet.sendall(b"   Client doesn't support MCCP4\r\n")
        return
        
    # Immediately start compression (fallback behavior)
    telnet.sendall(b"2. Starting compression immediately (fallback mode)\r\n")
    telnet.sendall(b"3. Server sends: IAC SB MCCP4 IAC SE\r\n")
    
    # Send old-style start sequence
    telnet.sendall(bytes([IAC, SB, TELOPT_MCCP4, IAC, SE]))
    time.sleep(0.01)
    
    # Send compressed data
    compressor = zstd.ZstdCompressor(level=8)
    compressed = compressor.compress(
        b"[FALLBACK COMPRESSED] This uses the fallback MCCP4 protocol\r\n"
        b"[FALLBACK COMPRESSED] No BEGIN_ENCODING subnegotiation\r\n"
    )
    telnet.sendall(compressed)
    
    # End compression
    telnet.sendall(bytes([IAC, DONT, TELOPT_MCCP4]))
    telnet.sendall(b"\r\n[UNCOMPRESSED] Fallback mode test complete.\r\n")