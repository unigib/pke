# RSA Public Key Encryption (Educational Implementation)

A minimalist Python implementation of the **RSA (Rivest–Shamir–Adleman)** algorithm. This project is designed for undergraduate students to understand the mathematical relationship between public and private keys without the abstraction of high-level cryptographic libraries.

## 🚀 Overview

This script demonstrates the three core phases of Public Key Encryption (PKE):
1.  **Key Generation**: Creating a public key for encryption and a private key for decryption using prime number theory.
2.  **Encryption**: Transforming plaintext into ciphertext using modular exponentiation.
3.  **Decryption**: Recovering the original message using the modular multiplicative inverse.

## 🧠 Core Concepts

To understand this code, you should be familiar with:
*   **Modular Arithmetic**: The "clock math" that keeps values within a fixed range.
*   **Euler’s Totient Function ($\phi$n)**: Calculating the number of integers coprime to $n$.
*   **Extended Euclidean Algorithm**: Used here to find the **Modular Inverse**, which allows us to "undo" the encryption.
*   **Prime Factorization**: The security foundation—while it's easy to multiply two primes, it is computationally "hard" to factor the result back into the original primes.

## 🛠️ How to Use

1. **Clone the repository**:
   ```bash
   git clone https://github.com/davyrob-clg/pke.git

## 🛠️ Exercises

There are also a number of GUI python tools to encrypt and decrypt - both  symmetric and  asymmetric keys - the idea is to show how to enrypt files and data with both types of keys and demo the idea of pre-shared keys.  We also cover diffie-hellman in this course and this also helps

