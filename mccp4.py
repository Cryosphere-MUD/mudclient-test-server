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
                telnet.send_text(">>> Client sent DO COMPRESS4! Waiting for ACCEPT_ENCODING...\n")
                    
            elif command == DONT:
                print("Client sent: IAC DONT MCCP4")
                telnet.send_text(">>> Client sent DONT COMPRESS4\n")
    
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
        
        telnet_obj.send_text(">>> Server sends: IAC SB COMPRESS4 BEGIN_ENCODING 'zstd' IAC SE\n")
        print(f">>> Sending BEGIN_ENCODING: {begin_encoding.hex()}")
        telnet_obj.send_bytes(begin_encoding)
        
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
            telnet.send_bytes(compressed_frame)
            print(f">>> Sent {len(all_data)} bytes as single compressed frame")

        except Exception as e:
            print(f">>> Compression error: {e}")
            # Fallback to raw sending if streaming fails
            for msg in test_messages:
                telnet.send_bytes(msg)
    
    def end_mccp4_compression(telnet):
        """End MCCP4 compression like your MUD's compress4End function"""
        print(">>> Server sends: IAC DONT COMPRESS4 (ending compression)")
        telnet.send_bytes(bytes([IAC, DONT, TELOPT_MCCP4]))
        
        # Now send uncompressed data 
        telnet.send_text("\n[UNCOMPRESSED] Back to normal uncompressed text.\n")
        telnet.send_text("[UNCOMPRESSED] MCCP4 test complete!\n") 
        telnet.send_text("[UNCOMPRESSED] If you saw the compressed messages, MCCP4 worked!\n\n")
    
    def mccp4_subneg_handler(data):
        """Handle MCCP4 subnegotiation - looking for ACCEPT_ENCODING"""
        if not data:
            return
            
        if data[0] == MCCP4_ACCEPT_ENCODING:
            # Extract encodings from subneg data
            encodings = data[1:].decode('ascii', errors='ignore')
            print(f">>> Client sent ACCEPT_ENCODING: {encodings}")
            telnet.send_text(f">>> Client sent ACCEPT_ENCODING: {encodings}\n")
            telnet.mccp4_state['accept_encoding_received'] = True
            
            # Check if client supports zstd
            if 'zstd' in encodings:
                telnet.send_text(">>> Client supports zstd! Starting compression...\n")
                start_mccp4_compression(telnet)
            else:
                telnet.send_text(">>> Client does not support zstd, sending WONT\n")
                telnet.send_bytes(bytes([IAC, WONT, TELOPT_MCCP4]))
        else:
            print(f">>> Unknown MCCP4 subnegotiation: {data[0]}")
    
    # Set up telnet negotiation handlers
    telnet.neg_handler = neg_handler
    telnet.subneg_handlers[TELOPT_MCCP4] = mccp4_subneg_handler
    
    # Store function references for persistence
    telnet.mccp4_start_compression = start_mccp4_compression
    
    # Start MCCP4 protocol sequence
    telnet.send_text("=== MCCP4 Test with zstd (Proper Protocol) ===\n")
    telnet.send_text("Following integration guide protocol sequence\n\n")
    
    # Step 1: Send IAC WILL COMPRESS4 to offer compression
    telnet.send_text("1. Server sends: IAC WILL COMPRESS4\n")
    telnet.send_bytes(bytes([IAC, WILL, TELOPT_MCCP4]))
    print(">>> Sent IAC WILL COMPRESS4")
    
    # Step 2: Wait for client to respond with IAC DO COMPRESS4 and ACCEPT_ENCODING
    telnet.send_text("2. Waiting for client to send: IAC DO COMPRESS4\n")
    telnet.send_text("3. Then waiting for: IAC SB COMPRESS4 ACCEPT_ENCODING ... IAC SE\n")
    telnet.send_text("   (Proper MCCP4 protocol requires both steps)\n")
    telnet.send_text("   Press enter to continue...\n")
    
    # Process client response via readline (this triggers telnet negotiation)
    response = telnet.readline()
    
    # Check results
    if telnet.mccp4_state.get('test_completed'):
        telnet.send_text("4. SUCCESS: MCCP4 compression test completed!\n")
        telnet.send_text("   If you saw the compressed messages above, MCCP4 worked!\n")
    elif telnet.mccp4_state.get('do_received'):
        if telnet.mccp4_state.get('accept_encoding_received'):
            telnet.send_text("4. Client sent both DO and ACCEPT_ENCODING - check above for results\n")
        else:
            telnet.send_text("4. Client sent DO COMPRESS4 but no ACCEPT_ENCODING received\n")
            telnet.send_text("   This means client doesn't support full MCCP4 protocol\n")
            telnet.send_text("   (Some clients may need fallback mode)\n")
    else:
        telnet.send_text("4. Client does not support MCCP4 (no DO received)\n")
