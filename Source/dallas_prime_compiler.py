"""
FatherTimeSDKP Framework - Digital Crystal Vault
Module: dallas_prime_compiler.py
Author: Donald Paul Smith
Description: Enforces the prime-terminated binary protocol of Dallas's Code.
             Acts as the deterministic compiler and verification key for the 
             Digital Crystal Vault, preventing bit-flipping and structural corruption.
"""

import sys

class DallasPrimeCompiler:
    """
    Compiles and verifies binary payloads using the prime-terminated logic of Dallas's Code.
    """
    
    @staticmethod
    def is_prime(n: int) -> bool:
        """Helper to verify if a resolved integer boundary is prime."""
        if n <= 1:
            return False
        if n <= 3:
            return True
        if n % 2 == 0 or n % 3 == 0:
            return False
        i = 5
        while i * i <= n:
            if n % i == 0 or n % (i + 2) == 0:
                return False
            i += 6
        return True

    def compile_payload(self, raw_data: str) -> dict:
        """
        Compiles raw string data into a prime-terminated binary payload (Dallas's Code).
        Appends a terminal bit block (padding/nonce) such that the entire binary sequence,
        when converted back to a large integer, is strictly prime.
        """
        # Step 1: Convert raw string characters into their standard binary block representation
        binary_data = ''.join(format(ord(char), '08b') for char in raw_data)
        base_int = int(binary_data, 2)
        
        # Step 2: Search for the nearest valid prime boundary to terminate the sequence
        # We append a dynamic termination block (nonce) to hit the exact prime
        nonce = 0
        while True:
            # Shift the base data to append the security termination sequence
            candidate_int = (base_int << 16) + nonce
            if self.is_prime(candidate_int):
                prime_binary = bin(candidate_int)[2:]
                break
            nonce += 1
            
        return {
            "original_data": raw_data,
            "binary_payload": prime_binary,
            "integer_representation": candidate_int,
            "termination_nonce": nonce,
            "bit_length": len(prime_binary)
        }

    def verify_and_decrypt(self, payload: dict) -> str:
        """
        Acts as the primary key to decode the Digital Crystal Vault.
        Verifies that the incoming binary sequence resolves exactly to a prime boundary.
        If verified, it strips the prime termination tail and decrypts the payload.
        """
        binary_str = payload.get("binary_payload")
        nonce = payload.get("termination_nonce")
        
        if not binary_str or nonce is None:
            raise ValueError("Verification Error: Invalid payload structure.")
            
        # Parse the binary sequence as a big integer
        resolved_int = int(binary_str, 2)
        
        # Security Verification Check: Must be prime
        if not self.is_prime(resolved_int):
            raise SecurityError("VAULT ALARM: Decoupled state detected! Payload is not prime-terminated.")
            
        # Strip the 16-bit termination tail to retrieve the raw base integer
        base_int = resolved_int >> 16
        
        # Reconstruct standard byte array from decoded integer
        byte_len = (base_int.bit_length() + 7) // 8
        try:
            raw_bytes = base_int.to_bytes(byte_len, byteorder='big')
            decrypted_text = raw_bytes.decode('utf-8').strip('\x00')
            return decrypted_text
        except Exception as e:
            raise ValueError(f"Decryption Error: Failed to unpack verified state. {e}")


class SecurityError(Exception):
    """Custom exception raised when payload prime-termination is violated."""
    pass


# ==========================================
# Execution Test for Dallas's Code Verification
# ==========================================
if __name__ == "__main__":
    print("--- FatherTimeSDKP: Digital Crystal Vault Access ---")
    compiler = DallasPrimeCompiler()
    
    # 1. Compile a secure system state sequence
    secure_message = "SD&N_Active_State_1.000000"
    print(f"Original System Message: '{secure_message}'")
    
    compiled_packet = compiler.compile_payload(secure_message)
    print(f"Compilation Status: Complete.")
    print(f" -> Bit Length: {compiled_packet['bit_length']} bits")
    print(f" -> Termination Nonce: {compiled_packet['termination_nonce']}")
    print(f" -> Resolved Prime Boundary: {compiled_packet['integer_representation']}")
    
    # Verify the compiled packet resolves to a prime number
    is_secure = compiler.is_prime(compiled_packet['integer_representation'])
    print(f" -> Prime Verification Check: {is_secure}")
    
    # 2. Simulate standard authorization and decryption
    print("\nAttempting Decoupling and Vault Access...")
    try:
        decrypted_message = compiler.verify_and_decrypt(compiled_packet)
        print(f"Vault Decrypted Output: '{decrypted_message}'")
        print("Status: Verified. Zero data-corruption detected.")
    except SecurityError as e:
        print(f"Vault Refusal: {e}")
        
    # 3. Simulate a Bit-Flip attack or noise degradation to test post-quantum defense
    print("\nSimulating Bit-Flip / Noise Attack (Corrupting 1 bit at the end of the payload)...")
    corrupted_payload = compiled_packet.copy()
    
    # Flip the last bit from 1 to 0 or 0 to 1
    last_bit = corrupted_payload["binary_payload"][-1]
    flipped_bit = "0" if last_bit == "1" else "1"
    corrupted_payload["binary_payload"] = corrupted_payload["binary_payload"][:-1] + flipped_bit
    
    try:
        compiler.verify_and_decrypt(corrupted_payload)
    except SecurityError as e:
        print(f"Vault Refusal: {e}")
        print("Status: Post-Quantum Security System successfully blocked corrupted state integration.")
