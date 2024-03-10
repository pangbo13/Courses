#include "Enclave.h"
#include "Enclave_t.h" /* print_string */
#include <stdarg.h>
#include <stdio.h> /* vsnprintf */
#include <string.h>

/* 
 * printf: 
 *   Invokes OCALL to display the enclave buffer to the terminal.
 */
int printf(const char* fmt, ...)
{
    char buf[BUFSIZ] = { '\0' };
    va_list ap;
    va_start(ap, fmt);
    vsnprintf(buf, BUFSIZ, fmt, ap);
    va_end(ap);
    ocall_print_string(buf);
    return (int)strnlen(buf, BUFSIZ - 1) + 1;
}

const char* key = "gosecgosec";
char T[256];
unsigned char S[256];
char keystream[256];

template <typename T>
void swap(T& a, T& b)
{
    T temp = a;
    a = b;
    b = temp;
}

void ecall_sbox_generation()
{
    size_t keylen = strlen(key);
    for (size_t i = 0; i < 256; i++)
    {
        S[i] = (unsigned char)i;
        T[i] = key[i % keylen];
    }
    int j = 0;
    for (size_t i = 0; i < 256; i++) {
        j = (j + S[i] + T[i]) % 256;
        swap(S[i], S[j]);
    }
}

void ecall_keystream_generation()
{
    int i = 0;
    int j = 0;
    for (int k = 0; k < 256; k++)
    {
        i = (i + 1) % 256;
        j = (j + S[i]) % 256;

        swap(S[i], S[j]);

        int t = (S[i] + S[j]) % 256;
        keystream[k] = S[t];
    }
}

void ecall_decryption(char* ciphertext, char* plaintext, size_t len)
{   
    for (size_t i = 0; i < len - 1; i++)
    {
        plaintext[i] = ciphertext[i] ^ keystream[i];
    }
}
