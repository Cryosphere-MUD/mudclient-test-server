from telnetconstants import IAC, SB, SE, WILL, WONT, DO, DONT, TELOPT_MCCP4, TELOPT_MCCP2
import zstandard as zstd
import zlib

MCCP4_ACCEPT_ENCODING = 1
MCCP4_BEGIN_ENCODING = 2
MCCP4_WONT = 3

def mccp4_handler_zstd(telnet):
    """MCCP4 handler following proper protocol from integration guide"""
    
    # State tracking 
    telnet.mccp4_state = {
        'client_supports_mccp4': False,
        'compression_started': False,
        'do_received': False,
        'accept_encoding_received': False,
        'test_completed': False
    }
    
    def neg_handler(command, option):
        """Handle telnet negotiation - this is called when client responds"""
        if option == TELOPT_MCCP4:
            if command == DO:
                print("Client sent: IAC DO MCCP4")
                telnet.mccp4_state['client_supports_mccp4'] = True
                telnet.mccp4_state['do_received'] = True
                telnet.sendall(">>> Client sent DO COMPRESS4! Waiting for ACCEPT_ENCODING...\n")
                    
            elif command == DONT:
                print("Client sent: IAC DONT MCCP4")
                telnet.sendall(">>> Client sent DONT COMPRESS4\n")
    
    def start_mccp4_compression(telnet_obj):
        """Start MCCP4 compression immediately when DO is received"""
        if telnet_obj.mccp4_state['compression_started']:
            return
            
        telnet_obj.mccp4_state['compression_started'] = True
        print(">>> Starting MCCP4 compression")
        
        # Send BEGIN_ENCODING with "zstd" (this is the key MCCP4 command)
        begin_encoding = bytes([
            IAC, SB, TELOPT_MCCP4,
            MCCP4_BEGIN_ENCODING,
            ord('z'), ord('s'), ord('t'), ord('d'),  # "zstd" as raw bytes
            IAC, SE
        ])
        
        telnet_obj.sendall(">>> Server sends: IAC SB COMPRESS4 BEGIN_ENCODING 'zstd' IAC SE\n", newline_replace=False)
        print(f">>> Sending BEGIN_ENCODING: {begin_encoding.hex()}")
        telnet_obj.sendall(begin_encoding, newline_replace=False)
        
        # IMMEDIATELY send compressed data after BEGIN_ENCODING
        print(">>> Sending compressed test data immediately...")
        send_compressed_test_data(telnet_obj)
        
        # CRITICAL: End compression AFTER the compressed data stream is closed
        # The end_mccp4_compression should be called AFTER stream is properly closed
        print(">>> Ending compression...")
        end_mccp4_compression(telnet_obj)
        
        # Mark that we've completed the compression test
        telnet_obj.mccp4_state['test_completed'] = True
    
    def send_compressed_test_data(telnet):
        """Send compressed test messages as a single complete zstd frame"""
        test_messages = [
            b"[COMPRESSED] This message is compressed with zstd!\r\n",
            b"[COMPRESSED] You're now receiving MCCP4 compressed data.\r\n",
            b"[COMPRESSED] This demonstrates MCCP4 protocol functionality.\r\n",
            b"[COMPRESSED] Using zstd compression for efficiency.\r\n"
        ]

        try:
            # Create compressor
            compressor = zstd.ZstdCompressor(
                level=8,
                write_content_size=False,
                write_checksum=False,
                write_dict_id=False
            )

            # Compress ALL messages into ONE complete frame
            all_data = b"".join(test_messages)
            compressed_frame = compressor.compress(all_data)

            print(f">>> Sending complete zstd frame: {len(compressed_frame)} bytes")
            telnet.sendall(compressed_frame, newline_replace=False)
            print(f">>> Sent {len(all_data)} bytes as single compressed frame")

        except Exception as e:
            print(f">>> Compression error: {e}")
            # Fallback to raw sending if streaming fails
            for msg in test_messages:
                telnet.sendall(msg, newline_replace=False)
    
    def end_mccp4_compression(telnet):
        """End MCCP4 compression like your MUD's compress4End function"""
        print(">>> Server sends: IAC DONT COMPRESS4 (ending compression)")
        telnet.sendall(bytes([IAC, DONT, TELOPT_MCCP4]), newline_replace=False)
        
        # Now send uncompressed data 
        telnet.sendall("\n[UNCOMPRESSED] Back to normal uncompressed text.\n", newline_replace=False)
        telnet.sendall("[UNCOMPRESSED] MCCP4 test complete!\n", newline_replace=False) 
        telnet.sendall("[UNCOMPRESSED] If you saw the compressed messages, MCCP4 worked!\n\n", newline_replace=False)
    
    def mccp4_subneg_handler(data):
        """Handle MCCP4 subnegotiation - looking for ACCEPT_ENCODING"""
        if not data:
            return
            
        if data[0] == MCCP4_ACCEPT_ENCODING:
            # Extract encodings from subneg data
            encodings = data[1:].decode('ascii', errors='ignore')
            print(f">>> Client sent ACCEPT_ENCODING: {encodings}")
            telnet.sendall(f">>> Client sent ACCEPT_ENCODING: {encodings}\n")
            telnet.mccp4_state['accept_encoding_received'] = True
            
            # Check if client supports zstd
            if 'zstd' in encodings:
                telnet.sendall(">>> Client supports zstd! Starting compression...\n")
                start_mccp4_compression(telnet)
            else:
                telnet.sendall(">>> Client does not support zstd, sending WONT\n")
                telnet.sendall(bytes([IAC, WONT, TELOPT_MCCP4]), newline_replace=False)
        else:
            print(f">>> Unknown MCCP4 subnegotiation: {data[0]}")
    
    # Set up telnet negotiation handlers
    telnet.neg_handler = neg_handler
    telnet.subneg_handlers[TELOPT_MCCP4] = mccp4_subneg_handler
    
    # Store function references for persistence
    telnet.mccp4_start_compression = start_mccp4_compression
    
    # Start MCCP4 protocol sequence
    telnet.sendall("=== MCCP4 Test with zstd (Proper Protocol) ===\n", newline_replace=False)
    telnet.sendall("Following integration guide protocol sequence\n\n", newline_replace=False)
    
    # Step 1: Send IAC WILL COMPRESS4 to offer compression
    telnet.sendall("1. Server sends: IAC WILL COMPRESS4\n", newline_replace=False)
    telnet.sendall(bytes([IAC, WILL, TELOPT_MCCP4]), newline_replace=False)
    print(">>> Sent IAC WILL COMPRESS4")
    
    # Step 2: Wait for client to respond with IAC DO COMPRESS4 and ACCEPT_ENCODING
    telnet.sendall("2. Waiting for client to send: IAC DO COMPRESS4\n", newline_replace=False)
    telnet.sendall("3. Then waiting for: IAC SB COMPRESS4 ACCEPT_ENCODING ... IAC SE\n", newline_replace=False)
    telnet.sendall("   (Proper MCCP4 protocol requires both steps)\n", newline_replace=False)
    telnet.sendall("   Press enter to continue...\n", newline_replace=False)
    
    # Process client response via readline (this triggers telnet negotiation)
    response = telnet.readline()
    
    # Check results
    if telnet.mccp4_state.get('test_completed'):
        telnet.sendall("4. SUCCESS: MCCP4 compression test completed!\n", newline_replace=False)
        telnet.sendall("   If you saw the compressed messages above, MCCP4 worked!\n", newline_replace=False)
    elif telnet.mccp4_state.get('do_received'):
        if telnet.mccp4_state.get('accept_encoding_received'):
            telnet.sendall("4. Client sent both DO and ACCEPT_ENCODING - check above for results\n", newline_replace=False)
        else:
            telnet.sendall("4. Client sent DO COMPRESS4 but no ACCEPT_ENCODING received\n", newline_replace=False)
            telnet.sendall("   This means client doesn't support full MCCP4 protocol\n", newline_replace=False)
            telnet.sendall("   (Some clients may need fallback mode)\n", newline_replace=False)
    else:
        telnet.sendall("4. Client does not support MCCP4 (no DO received)\n", newline_replace=False)

def mccp4_handler_deflate(telnet):
    """MCCP4 handler with deflate - uses MCCP2 protocol for deflate compression"""
    
    # Track client capabilities for MCCP2
    client_supports_mccp2 = False
    
    def neg_handler(command, option):
        nonlocal client_supports_mccp2
        if option == TELOPT_MCCP2:
            if command == DO:
                print("Client sent: IAC DO MCCP2")
                client_supports_mccp2 = True
                telnet.sendall("Client supports MCCP2!\n")
            elif command == DONT:
                print("Client sent: IAC DONT MCCP2")
                telnet.sendall("Client does not support MCCP2\n")
    
    def mccp2_subneg_handler(data):
        # MCCP2 doesn't use complex subnegotiation
        pass
    
    # Set up handlers
    telnet.neg_handler = neg_handler
    telnet.subneg_handlers[TELOPT_MCCP2] = mccp2_subneg_handler
    
    telnet.sendall("=== MCCP4 Test with deflate (MCCP2 compatibility mode) ===\n")
    telnet.sendall("MCCP4 deflate is equivalent to MCCP2 - switching to MCCP2 protocol\n\n")
    
    print("MCCP4 deflate requested - switching to MCCP2 protocol")
    
    # Step 1: Send IAC WILL MCCP2 (not MCCP4)
    telnet.sendall("1. Server sends: IAC WILL MCCP2\n")
    telnet.sendall(bytes([IAC, WILL, TELOPT_MCCP2]), newline_replace=False)
    
    # Step 2: Proceed with MCCP2 setup
    telnet.sendall("2. Proceeding with MCCP2 setup...\n")
    
    # Step 3: Start MCCP2 compression (simple IAC SB MCCP2 IAC SE)
    telnet.sendall("3. Server sends: IAC SB MCCP2 IAC SE\n")
    start_compression = bytes([IAC, SB, TELOPT_MCCP2, IAC, SE])
    telnet.sendall(start_compression, newline_replace=False)
    
    telnet.sendall("4. Starting MCCP2 compression\n")
    telnet.sendall("   Everything after this is compressed\n\n")
    
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
        
        # Send the complete compressed frame using telnet
        telnet.sendall(compressed_data, newline_replace=False)
        print("   -> MCCP2 compressed data sent successfully")
        
    except Exception as e:
        print(f"   -> Compression error: {e}")
        return
    
    # Step 5: End compression - no explicit signal needed for MCCP2
    print("5. MCCP2 compression complete")
    telnet.sendall("6. Sending uncompressed data again\n\n")
    
    # Send uncompressed data
    telnet.sendall("\n[UNCOMPRESSED] Back to normal uncompressed text.\n")
    telnet.sendall("[UNCOMPRESSED] MCCP2 test complete!\n")  
    telnet.sendall("[UNCOMPRESSED] If you saw the compressed messages, MCCP2 worked!\n\n")
    
    print("   -> MCCP2 test completed successfully")

def mccp4_handler_fallback(telnet):
    """Test MCCP4 fallback mode (no ACCEPT_ENCODING) using proper telnet state machine"""
    
    # Track client capabilities
    client_supports_mccp4 = False
    
    def neg_handler(command, option):
        nonlocal client_supports_mccp4
        if option == TELOPT_MCCP4:
            if command == DO:
                print("Client sent: IAC DO MCCP4")
                client_supports_mccp4 = True
                telnet.sendall("Client supports MCCP4!\n")
            elif command == DONT:
                print("Client sent: IAC DONT MCCP4")
                telnet.sendall("Client does not support MCCP4\n")
    
    def mccp4_subneg_handler(data):
        # Fallback mode doesn't expect subnegotiation
        if data:
            telnet.sendall(f"Unexpected subnegotiation in fallback mode: {data}\n")
    
    # Set up handlers
    telnet.neg_handler = neg_handler
    telnet.subneg_handlers[TELOPT_MCCP4] = mccp4_subneg_handler
    
    telnet.sendall("=== MCCP4 Fallback Mode (backward compatibility) ===\n\n")
    telnet.sendall("Testing MCCP4 fallback mode (no ACCEPT_ENCODING)\n\n")
    
    # Send WILL MCCP4
    telnet.sendall("1. Server sends: IAC WILL MCCP4\n")
    telnet.sendall(bytes([IAC, WILL, TELOPT_MCCP4]), newline_replace=False)
    
    # Proceed with fallback compression
    telnet.sendall("2. Starting compression immediately (fallback mode)\n")
    telnet.sendall("3. Server sends: IAC SB MCCP4 IAC SE\n")
    
    # Send old-style start sequence
    telnet.sendall(bytes([IAC, SB, TELOPT_MCCP4, IAC, SE]), newline_replace=False)
    
    # Send compressed data
    compressor = zstd.ZstdCompressor(level=8)
    compressed = compressor.compress(
        b"[FALLBACK COMPRESSED] This uses the fallback MCCP4 protocol\r\n"
        b"[FALLBACK COMPRESSED] No BEGIN_ENCODING subnegotiation\r\n"
    )
    telnet.sendall(compressed, newline_replace=False)
    
    # End compression
    telnet.sendall(bytes([IAC, DONT, TELOPT_MCCP4]), newline_replace=False)
    telnet.sendall("\n[UNCOMPRESSED] Fallback mode test complete.\n")

# Create static MCCP4 test data (like MCCP2_TEST) - but with proper protocol sequence
def create_mccp4_test_data():
    """Create static MCCP4 test data blob with proper protocol sequence"""
    try:
        compressor = zstd.ZstdCompressor(
            level=1,
            write_content_size=False,
            write_checksum=False,
            write_dict_id=False
        )
        
        # Test messages to compress
        test_data = (
            b"[COMPRESSED] This message is compressed with zstd!\r\n"
            b"[COMPRESSED] You're now receiving MCCP4 compressed data.\r\n"
            b"[COMPRESSED] This demonstrates MCCP4 protocol functionality.\r\n"
            b"[COMPRESSED] Using zstd compression for efficiency.\r\n"
        )
        
        compressed_data = compressor.compress(test_data)
        
        # Build the complete MCCP4 test sequence following proper protocol
        mccp4_test = (
            b"=== MCCP4 Test with zstd (Simple) ===\r\n"
            b"This test mimics MCCP2 approach - no negotiation waiting.\r\n"
            b"1. Server sends: IAC WILL COMPRESS4\r\n" +
            bytes([IAC, WILL, TELOPT_MCCP4]) +
            b"2. Server immediately sends: IAC SB COMPRESS4 BEGIN_ENCODING 'zstd' IAC SE\r\n" +
            bytes([IAC, SB, TELOPT_MCCP4, MCCP4_BEGIN_ENCODING, 
                   ord('z'), ord('s'), ord('t'), ord('d'), IAC, SE]) +
            b"3. Compressed data follows:\r\n" +
            compressed_data +
            bytes([IAC, DONT, TELOPT_MCCP4]) +  # End compression
            b"4. [UNCOMPRESSED] Back to normal uncompressed text.\r\n"
            b"5. [UNCOMPRESSED] MCCP4 test complete!\r\n"
            b"6. [UNCOMPRESSED] If you saw the compressed messages, MCCP4 worked!\r\n"
        )
        
        return mccp4_test
        
    except Exception as e:
        return b"MCCP4 test data creation failed: " + str(e).encode() + b"\r\n"

# Static MCCP4 test data
MCCP4_TEST = create_mccp4_test_data()