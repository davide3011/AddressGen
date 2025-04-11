// vanity.cpp
// Programma per la generazione di indirizzi Bitcoin vanity con multithreading
//
// Scopo: Genera indirizzi Bitcoin che contengono uno specifico pattern (vanity address)
// utilizzando multiple thread per accelerare la ricerca. Supporta sia indirizzi legacy
// P2PKH (Base58) che native SegWit P2WPKH (Bech32).
//
// Dipendenze:
// - OpenSSL per operazioni crittografiche (SHA256, RIPEMD160, curve ellittiche)
// - C++17 per gestione moderna dei thread e delle risorse
//
// Strutture dati principali:
// - AddressData: Contiene chiave privata, pubblica e indirizzo generato
// - SearchParams: Parametri di ricerca configurati dall'utente
//
// Flusso principale:
// 1. Configurazione parametri via input utente
// 2. Avvio thread worker per la generazione indirizzi
// 3. Verifica pattern e gestione risultati
// 4. Output dei risultati con statistiche

// Sezione include per le dipendenze
#include <iostream>
#include <iomanip>
#include <sstream>
#include <string>
#include <vector>
#include <chrono>
#include <random>
#include <cstdint>
#include <stdexcept>

#include <algorithm>
#include <thread>
#include <mutex>
#include <atomic>
#include <condition_variable>
#include <queue>
#include <functional>
#include <memory>

// OpenSSL headers per SHA256, RIPEMD160 e operazioni EC
#include <openssl/sha.h>
#include <openssl/ripemd.h>
#include <openssl/ec.h>
#include <openssl/obj_mac.h>
#include <openssl/bn.h>
#include <openssl/rand.h>

// Charset per Bech32 e Base58
const std::string CHARSET = "qpzry9x8gf2tvdw0s3jn54khce6mua7l";
const std::string BASE58_CHARS = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz";

// Struttura per contenere i dati generati per un indirizzo
// Contiene tutti i dati relativi a un indirizzo generato
struct AddressData {
    std::string private_key_hex;  // Chiave privata in formato esadecimale (64 caratteri)
    std::string public_key_hex;   // Chiave pubblica serializzata in formato esadecimale
    std::string address;          // Indirizzo Bitcoin formattato (Base58 o Bech32)
};

// Struttura per i parametri di ricerca
// Parametri di ricerca configurati dall'utente
struct SearchParams {
    std::string tipo;          // Tipo indirizzo: "P2PKH" o "P2WPKH"
    std::string pattern;       // Sequenza di caratteri da cercare nell'indirizzo
    std::string posizione;     // Posizione del pattern: "inizio" o "ovunque"
    bool compressed;           // Flag per chiavi pubbliche compresse (solo P2PKH)
    bool case_sensitive;       // Distinzione maiuscole/minuscole (solo Base58)
};

// Variabili globali per la sincronizzazione tra thread
std::mutex mtx;                    // Mutex per l'accesso alle risorse condivise
std::condition_variable cv;        // Variabile condizionale per la notifica tra thread
std::atomic<bool> found{false};     // Flag atomico per indicare se l'indirizzo è stato trovato
std::atomic<uint64_t> total_count{0};
AddressData result_data;

//------------------------------------------------------------
// Helper: conversione tra byte vector e stringa esadecimale
//------------------------------------------------------------
std::string bytesToHex(const std::vector<uint8_t>& data) {
    std::ostringstream oss;
    oss << std::hex << std::setfill('0');
    for (uint8_t b : data) {
        oss << std::setw(2) << static_cast<int>(b);
    }
    return oss.str();
}

std::vector<uint8_t> hexToBytes(const std::string &hex) {
    std::vector<uint8_t> bytes;
    if (hex.size() % 2 != 0)
        throw std::runtime_error("Hex string length must be even.");
    for (size_t i = 0; i < hex.size(); i += 2) {
        std::string byteString = hex.substr(i, 2);
        uint8_t byte = static_cast<uint8_t>(std::stoul(byteString, nullptr, 16));
        bytes.push_back(byte);
    }
    return bytes;
}

//------------------------------------------------------------
// Funzione per incrementare di 1 una chiave privata espressa in hex (64 caratteri)
// Ottimizzata per essere più efficiente
//------------------------------------------------------------
// Incrementa una chiave privata esadecimale di 1 in modo sicuro
// Gestisce automaticamente l'overflow ripartendo da zero
// Complessità: O(n) dove n è la lunghezza della chiave (64 caratteri)
std::string increment_private_key(const std::string& private_key_hex) {
    std::string result = private_key_hex;
    int carry = 1;
    // Partiamo dal fondo della stringa
    for (int i = static_cast<int>(result.size()) - 1; i >= 0 && carry; i--) {
        char& c = result[i];
        int value;
        if (c >= '0' && c <= '9')
            value = c - '0';
        else if (c >= 'a' && c <= 'f')
            value = c - 'a' + 10;
        else if (c >= 'A' && c <= 'F')
            value = c - 'A' + 10;
        else
            throw std::runtime_error("Carattere non valido nella chiave privata.");

        value += carry;
        carry = value >> 4; // 1 se value >= 16
        value = value & 0xF;
        // Convertiamo il valore in carattere esadecimale (in minuscolo)
        c = (value < 10) ? ('0' + value) : ('a' + value - 10);
    }
    return result;
}

//------------------------------------------------------------
// Funzione per generare 32 byte casuali e restituisce il vettore di byte
//------------------------------------------------------------
std::vector<uint8_t> generateRandomBytes(size_t length) {
    std::vector<uint8_t> bytes(length);
    if (RAND_bytes(bytes.data(), static_cast<int>(length)) != 1) {
        throw std::runtime_error("Errore nella generazione dei byte casuali.");
    }
    return bytes;
}

//------------------------------------------------------------
// Funzione per convertire un vettore di byte in un std::vector<int>
// (utilizzata per il Bech32, che lavora con valori interi)
//------------------------------------------------------------
std::vector<int> vectorUint8ToInt(const std::vector<uint8_t>& data) {
    std::vector<int> result;
    result.reserve(data.size()); // Pre-allocazione per migliorare le prestazioni
    for (uint8_t b : data) {
        result.push_back(static_cast<int>(b));
    }
    return result;
}

//------------------------------------------------------------
// Funzione Base58Encode ottimizzata
//------------------------------------------------------------
// Codifica una sequenza di byte in formato Base58
// Implementazione ottimizzata che utilizza la libreria OpenSSL per le operazioni BN
// Passaggi:
// 1. Conversione byte array -> Big Number
// 2. Divisioni successive per 58
// 3. Mappatura caratteri Base58
// 4. Aggiunta '1' iniziali per gli zero bytes
std::string base58Encode(const std::vector<uint8_t>& input) {
    // Converti l'input in un grande numero a partire dai byte
    BIGNUM* bn = BN_new();
    BN_zero(bn);
    for (size_t i = 0; i < input.size(); i++) {
        BN_mul_word(bn, 256);
        BN_add_word(bn, input[i]);
    }

    // Conta i byte zero iniziali
    int zeroes = 0;
    for (size_t i = 0; i < input.size() && input[i] == 0; ++i)
        zeroes++;

    // Pre-allocazione della stringa risultato per migliorare le prestazioni
    // Stima approssimativa: ogni byte diventa circa 1.4 caratteri in Base58
    std::string result;
    result.reserve(input.size() * 2);
    
    BIGNUM* bn58 = BN_new();
    BN_set_word(bn58, 58);
    BIGNUM* dv = BN_new();
    BIGNUM* rem = BN_new();
    BN_CTX* ctx = BN_CTX_new();
    
    while (!BN_is_zero(bn)) {
        BN_div(dv, rem, bn, bn58, ctx);
        // Ottieni il resto
        unsigned long rem_ul = BN_get_word(rem);
        result.push_back(BASE58_CHARS[rem_ul]);
        BN_copy(bn, dv);
    }
    // Aggiungi i 0 iniziali codificati come '1'
    for (int i = 0; i < zeroes; i++)
        result.push_back('1');
    
    // Il risultato va invertito
    std::reverse(result.begin(), result.end());

    BN_free(bn);
    BN_free(bn58);
    BN_free(dv);
    BN_free(rem);
    BN_CTX_free(ctx);

    return result;
}

//------------------------------------------------------------
// Funzioni Bech32 ottimizzate
//------------------------------------------------------------
uint32_t bech32_polymod(const std::vector<int>& values) {
    uint32_t chk = 1;
    for (int v : values) {
        uint32_t b = chk >> 25;
        chk = ((chk & 0x1ffffff) << 5) ^ v;
        if (b & 1) chk ^= 0x3b6a57b2;
        if (b & 2) chk ^= 0x26508e6d;
        if (b & 4) chk ^= 0x1ea119fa;
        if (b & 8) chk ^= 0x3d4233dd;
        if (b & 16) chk ^= 0x2a1462b3;
    }
    return chk;
}

std::vector<int> bech32_hrp_expand(const std::string& hrp) {
    std::vector<int> ret;
    ret.reserve(hrp.size() * 2 + 1); // Pre-allocazione
    for (char c : hrp) {
        ret.push_back(c >> 5);
    }
    ret.push_back(0);
    for (char c : hrp) {
        ret.push_back(c & 31);
    }
    return ret;
}

std::vector<int> bech32_create_checksum(const std::string& hrp, const std::vector<int>& data) {
    std::vector<int> values = bech32_hrp_expand(hrp);
    values.insert(values.end(), data.begin(), data.end());
    // Aggiungiamo 6 zeri
    std::vector<int> zeros(6, 0);
    values.insert(values.end(), zeros.begin(), zeros.end());
    uint32_t polymod_val = bech32_polymod(values) ^ 1;
    std::vector<int> checksum(6);
    for (int i = 0; i < 6; i++) {
        checksum[i] = (polymod_val >> (5 * (5 - i))) & 31;
    }
    return checksum;
}

std::string bech32_encode(const std::string& hrp, const std::vector<int>& data) {
    std::vector<int> checksum = bech32_create_checksum(hrp, data);
    std::vector<int> combined = data;
    combined.insert(combined.end(), checksum.begin(), checksum.end());
    std::string encoded = hrp + "1";
    encoded.reserve(encoded.size() + combined.size()); // Pre-allocazione
    for (int d : combined) {
        if(d < 0 || d >= (int)CHARSET.size())
            throw std::runtime_error("Valore non valido in bech32_encode");
        encoded.push_back(CHARSET[d]);
    }
    return encoded;
}

std::vector<int> convertbits(const std::vector<int>& data, int frombits, int tobits, bool pad = true) {
    int acc = 0;
    int bits = 0;
    std::vector<int> ret;
    ret.reserve(data.size() * frombits / tobits + 1); // Pre-allocazione
    int maxv = (1 << tobits) - 1;
    for (int value : data) {
        if (value < 0 || (value >> frombits))
            return {}; // errore
        acc = (acc << frombits) | value;
        bits += frombits;
        while (bits >= tobits) {
            bits -= tobits;
            ret.push_back((acc >> bits) & maxv);
        }
    }
    if (pad) {
        if (bits) {
            ret.push_back((acc << (tobits - bits)) & maxv);
        }
    } else if (bits >= frombits || ((acc << (tobits - bits)) & maxv)) {
        return {}; // errore
    }
    return ret;
}

//------------------------------------------------------------
// Funzione per generare l'indirizzo P2PKH (Base58) ottimizzata
//------------------------------------------------------------
AddressData generate_p2pkh_address(bool compressed = true, const std::string& private_key_hex_in = "") {
    AddressData result;
    std::vector<uint8_t> private_key;
    std::string private_key_hex;

    if (private_key_hex_in.empty()) {
        // Genera 32 byte casuali
        private_key = generateRandomBytes(32);
        private_key_hex = bytesToHex(private_key);
    } else {
        private_key_hex = private_key_hex_in;
        private_key = hexToBytes(private_key_hex_in);
    }
    result.private_key_hex = private_key_hex;

    // Crea una chiave EC utilizzando la curva SECP256k1
    EC_KEY* ec_key = EC_KEY_new_by_curve_name(NID_secp256k1);
    if (!ec_key)
        throw std::runtime_error("Errore nella creazione della EC_KEY");
    BIGNUM* bn = BN_new();
    BN_bin2bn(private_key.data(), private_key.size(), bn);
    if (!EC_KEY_set_private_key(ec_key, bn))
        throw std::runtime_error("Errore nell'impostazione della chiave privata");

    // Calcola la chiave pubblica
    const EC_GROUP* group = EC_KEY_get0_group(ec_key);
    EC_POINT* pub_key = EC_POINT_new(group);
    if (!EC_POINT_mul(group, pub_key, bn, NULL, NULL, NULL))
        throw std::runtime_error("Errore nel calcolo della chiave pubblica");
    if (!EC_KEY_set_public_key(ec_key, pub_key))
        throw std::runtime_error("Errore nell'impostazione della chiave pubblica");

    // Imposta il formato della chiave pubblica (compressa o non compressa)
    if (compressed)
        EC_KEY_set_conv_form(ec_key, POINT_CONVERSION_COMPRESSED);
    else
        EC_KEY_set_conv_form(ec_key, POINT_CONVERSION_UNCOMPRESSED);

    // Serializza la chiave pubblica
    int len = i2o_ECPublicKey(ec_key, NULL);
    if(len <= 0)
        throw std::runtime_error("Errore nella serializzazione della chiave pubblica");
    std::vector<uint8_t> pub_key_bytes(len);
    unsigned char* pub_key_ptr = pub_key_bytes.data();
    i2o_ECPublicKey(ec_key, &pub_key_ptr);
    result.public_key_hex = bytesToHex(pub_key_bytes);

    // Calcola SHA256 della chiave pubblica
    std::vector<uint8_t> sha256_hash(SHA256_DIGEST_LENGTH);
    SHA256(pub_key_bytes.data(), pub_key_bytes.size(), sha256_hash.data());

    // Calcola RIPEMD160 sulla SHA256
    std::vector<uint8_t> ripemd_hash(RIPEMD160_DIGEST_LENGTH);
    RIPEMD160(sha256_hash.data(), sha256_hash.size(), ripemd_hash.data());

    // Crea il payload: version byte 0x00 + pubkey_hash
    std::vector<uint8_t> payload;
    payload.reserve(1 + ripemd_hash.size()); // Pre-allocazione
    payload.push_back(0x00);
    payload.insert(payload.end(), ripemd_hash.begin(), ripemd_hash.end());

    // Calcola il checksum (doppia SHA256, primi 4 byte)
    std::vector<uint8_t> hash1(SHA256_DIGEST_LENGTH);
    SHA256(payload.data(), payload.size(), hash1.data());
    std::vector<uint8_t> hash2(SHA256_DIGEST_LENGTH);
    SHA256(hash1.data(), hash1.size(), hash2.data());
    std::vector<uint8_t> checksum(hash2.begin(), hash2.begin() + 4);

    // Concatenazione payload + checksum
    std::vector<uint8_t> final_data = payload;
    final_data.insert(final_data.end(), checksum.begin(), checksum.end());

    // Codifica Base58
    result.address = base58Encode(final_data);

    // Libera le strutture
    EC_POINT_free(pub_key);
    BN_free(bn);
    EC_KEY_free(ec_key);
    
    return result;
}

//------------------------------------------------------------
// Funzione per generare l'indirizzo P2WPKH (Bech32) ottimizzata
//------------------------------------------------------------
AddressData generate_p2wpkh_address(const std::string& private_key_hex_in = "") {
    AddressData result;
    std::vector<uint8_t> private_key;
    std::string private_key_hex;

    if (private_key_hex_in.empty()) {
        private_key = generateRandomBytes(32);
        private_key_hex = bytesToHex(private_key);
    } else {
        private_key_hex = private_key_hex_in;
        private_key = hexToBytes(private_key_hex_in);
    }
    result.private_key_hex = private_key_hex;

    // Crea la EC_KEY (sempre usando la chiave compressa per P2WPKH)
    EC_KEY* ec_key = EC_KEY_new_by_curve_name(NID_secp256k1);
    if (!ec_key)
        throw std::runtime_error("Errore nella creazione della EC_KEY");
    BIGNUM* bn = BN_new();
    BN_bin2bn(private_key.data(), private_key.size(), bn);
    if (!EC_KEY_set_private_key(ec_key, bn))
        throw std::runtime_error("Errore nell'impostazione della chiave privata");
    const EC_GROUP* group = EC_KEY_get0_group(ec_key);
    EC_POINT* pub_key = EC_POINT_new(group);
    if (!EC_POINT_mul(group, pub_key, bn, NULL, NULL, NULL))
        throw std::runtime_error("Errore nel calcolo della chiave pubblica");
    if (!EC_KEY_set_public_key(ec_key, pub_key))
        throw std::runtime_error("Errore nell'impostazione della chiave pubblica");

    // Per P2WPKH la chiave deve essere compressa
    EC_KEY_set_conv_form(ec_key, POINT_CONVERSION_COMPRESSED);
    int len = i2o_ECPublicKey(ec_key, NULL);
    if(len <= 0)
        throw std::runtime_error("Errore nella serializzazione della chiave pubblica");
    std::vector<uint8_t> pub_key_bytes(len);
    unsigned char* pub_key_ptr = pub_key_bytes.data();
    i2o_ECPublicKey(ec_key, &pub_key_ptr);
    result.public_key_hex = bytesToHex(pub_key_bytes);

    // Calcola SHA256 e RIPEMD160 sulla chiave pubblica compressa
    std::vector<uint8_t> sha256_hash(SHA256_DIGEST_LENGTH);
    SHA256(pub_key_bytes.data(), pub_key_bytes.size(), sha256_hash.data());
    std::vector<uint8_t> ripemd_hash(RIPEMD160_DIGEST_LENGTH);
    RIPEMD160(sha256_hash.data(), sha256_hash.size(), ripemd_hash.data());

    // Preparazione per Bech32: converti il pubkey_hash (20 byte) in valori a 5 bit
    std::vector<int> pubkey_hash_int;
    pubkey_hash_int.reserve(ripemd_hash.size()); // Pre-allocazione
    for (uint8_t b : ripemd_hash)
        pubkey_hash_int.push_back(b);
    std::vector<int> converted = convertbits(pubkey_hash_int, 8, 5, true);
    if (converted.empty())
        throw std::runtime_error("Errore nella conversione dei bits per Bech32");
    // Prependere witness version (0)
    std::vector<int> data_bech32;
    data_bech32.reserve(1 + converted.size()); // Pre-allocazione
    data_bech32.push_back(0);
    data_bech32.insert(data_bech32.end(), converted.begin(), converted.end());
    // Encoding Bech32 con hrp "bc"
    result.address = bech32_encode("bc", data_bech32);

    EC_POINT_free(pub_key);
    BN_free(bn);
    EC_KEY_free(ec_key);
    
    return result;
}

//------------------------------------------------------------
// Funzione per verificare se un indirizzo corrisponde al pattern
//------------------------------------------------------------
bool check_address_match(const std::string& address, const std::string& pattern, 
                         const std::string& posizione, bool case_sensitive) {
    // Prepara le stringhe per il confronto
    std::string address_to_check = address;
    std::string pattern_to_check = pattern;
    if (!case_sensitive) {
        std::transform(address_to_check.begin(), address_to_check.end(), address_to_check.begin(), ::tolower);
        std::transform(pattern_to_check.begin(), pattern_to_check.end(), pattern_to_check.begin(), ::tolower);
    }
    
    if (posizione == "inizio") {
        return address_to_check.find(pattern_to_check) == 0;
    } else {
        return address_to_check.find(pattern_to_check) != std::string::npos;
    }
}

//------------------------------------------------------------
// Funzione di ricerca eseguita da ciascun thread
//------------------------------------------------------------
void search_thread(int thread_id, const SearchParams& params, uint64_t start_offset) {
    // Genera una chiave privata iniziale per questo thread
    std::vector<uint8_t> initial_private_key = generateRandomBytes(32);
    std::string private_key_hex = bytesToHex(initial_private_key);
    
    // Applica l'offset per evitare sovrapposizioni tra thread
    for (uint64_t i = 0; i < start_offset; i++) {
        private_key_hex = increment_private_key(private_key_hex);
    }
    
    uint64_t local_count = 0;
    AddressData addrData;
    
    while (!found.load()) {
        // Genera un nuovo indirizzo
        if (params.tipo == "P2PKH") {
            addrData = generate_p2pkh_address(params.compressed, private_key_hex);
        } else {
            addrData = generate_p2wpkh_address(private_key_hex);
        }
        
        // Incrementa i contatori
        local_count++;
        if (local_count % 100 == 0) {
            total_count.fetch_add(100, std::memory_order_relaxed);
        }
        
        // Verifica se l'indirizzo corrisponde al pattern
        if (check_address_match(addrData.address, params.pattern, params.posizione, params.case_sensitive)) {
            // Abbiamo trovato un match!
            std::lock_guard<std::mutex> lock(mtx);
            if (!found.load()) {  // Doppio controllo per evitare race condition
                found.store(true);
                result_data = addrData;
                cv.notify_all();  // Notifica tutti i thread di fermarsi
                return;
            }
        }
        
        // Incrementa la chiave privata per il prossimo tentativo
        private_key_hex = increment_private_key(private_key_hex);
        
        // Aggiorna il contatore globale e mostra lo stato ogni 5000 tentativi
        if (local_count % 5000 == 0 && thread_id == 0) {
            std::lock_guard<std::mutex> lock(mtx);
            std::cout << "\rTentativi: " << total_count.load() 
                      << "  -  Ultimo indirizzo generato: " << addrData.address << std::flush;
        }
    }
}

//------------------------------------------------------------
// MAIN: parte interattiva per il Vanity Address Generator
//------------------------------------------------------------
int main() {
    std::cout << "Generatore di Vanity Address (Versione Ottimizzata)" << std::endl;
    std::cout << "=================================================" << std::endl << std::endl;

    SearchParams params;
    
    // Selezione del tipo di indirizzo
    while (true) {
        std::cout << "Seleziona il tipo di indirizzo (P2PKH o P2WPKH): ";
        std::getline(std::cin, params.tipo);
        // Convertiamo in maiuscolo
        std::transform(params.tipo.begin(), params.tipo.end(), params.tipo.begin(), ::toupper);
        if (params.tipo == "P2PKH" || params.tipo == "P2WPKH")
            break;
        std::cout << "Tipo di indirizzo non valido. Scegli tra P2PKH o P2WPKH." << std::endl;
    }
    
    // Per P2PKH, chiedi se usare chiavi compresse o non compresse
    params.compressed = true;
    if (params.tipo == "P2PKH") {
        std::string compressed_input;
        while (true) {
            std::cout << "Vuoi usare chiavi compresse? (s/n): ";
            std::getline(std::cin, compressed_input);
            std::transform(compressed_input.begin(), compressed_input.end(), compressed_input.begin(), ::tolower);
            if (compressed_input == "s" || compressed_input == "si")
                break;
            else if (compressed_input == "n" || compressed_input == "no") {
                params.compressed = false;
                break;
            }
            std::cout << "Input non valido. Inserisci 's' per si o 'n' per no." << std::endl;
        }
    }
    
    // Input del pattern da cercare
    while (true) {
        std::cout << "Inserisci il pattern che l'indirizzo deve contenere: ";
        std::getline(std::cin, params.pattern);
        if (params.pattern.empty()) {
            std::cout << "Il pattern non puo' essere vuoto. Inserisci almeno un carattere." << std::endl;
            continue;
        }
        // Controllo validità dei caratteri
        const std::string& valid_chars = (params.tipo == "P2PKH") ? BASE58_CHARS : CHARSET;
        bool invalidFound = false;
        for (char c : params.pattern) {
            if (valid_chars.find(c) == std::string::npos) {
                std::cout << "Carattere non valido per indirizzo " << params.tipo << ": " << c << std::endl;
                std::cout << "Caratteri validi: " << valid_chars << std::endl;
                invalidFound = true;
                break;
            }
        }
        if (!invalidFound)
            break;
    }
    
    // Posizione del pattern: "inizio" oppure "ovunque"
    while (true) {
        std::cout << "Vuoi che il pattern sia all'inizio (digita 'inizio') o presente ovunque (digita 'ovunque')? ";
        std::getline(std::cin, params.posizione);
        std::transform(params.posizione.begin(), params.posizione.end(), params.posizione.begin(), ::tolower);
        if (params.posizione == "inizio" || params.posizione == "ovunque")
            break;
        std::cout << "Valore non valido per la posizione. Inserisci 'inizio' o 'ovunque'." << std::endl;
    }
    
    // Case sensitivity: per P2PKH, l'utente può decidere
    params.case_sensitive = false;
    if (params.tipo == "P2PKH") {
        std::string case_sensitive_input;
        while (true) {
            std::cout << "Vuoi che la ricerca rispetti maiuscole/minuscole come inserite? (s/n): ";
            std::getline(std::cin, case_sensitive_input);
            std::transform(case_sensitive_input.begin(), case_sensitive_input.end(), case_sensitive_input.begin(), ::tolower);
            if (case_sensitive_input == "s" || case_sensitive_input == "si" || case_sensitive_input == "sì") {
                params.case_sensitive = true;
                break;
            } else if (case_sensitive_input == "n" || case_sensitive_input == "no") {
                params.case_sensitive = false;
                break;
            }
            std::cout << "Input non valido. Inserisci 's' per si o 'n' per no." << std::endl;
        }
    }
    
    // Input del numero di core da utilizzare
    unsigned int max_threads = std::thread::hardware_concurrency();
    if (max_threads == 0) max_threads = 4; // Fallback se non è possibile determinare
    
    unsigned int num_threads;
    while (true) {
        std::cout << "\nNumero di core CPU disponibili: " << max_threads << std::endl;
        std::cout << "Inserisci il numero di core da utilizzare (1-" << max_threads << ", 0 per usare tutti): ";
        
        std::string input;
        std::getline(std::cin, input);
        
        try {
            unsigned int input_threads = std::stoi(input);
            if (input_threads == 0 || (input_threads >= 1 && input_threads <= max_threads)) {
                num_threads = input_threads == 0 ? max_threads : input_threads;
                break;
            }
        } catch (...) {}
        
        std::cout << "Numero non valido. Inserisci un valore tra 1 e " << max_threads << " o 0 per usare tutti." << std::endl;
    }
    
    std::cout << std::endl << "Ricerca in corso con " << num_threads << " thread... premi CTRL+C per interrompere" << std::endl;
    
    // Inizializza i contatori
    total_count.store(0);
    found.store(false);
    
    // Avvia il timer
    auto start_time = std::chrono::steady_clock::now();
    
    // Crea e avvia i thread
    std::vector<std::thread> threads;
    for (unsigned int i = 0; i < num_threads; i++) {
        threads.push_back(std::thread(search_thread, i, params, i));
    }
    
    // Attendi che uno dei thread trovi un match
    {
        std::unique_lock<std::mutex> lock(mtx);
        cv.wait(lock, [] { return found.load(); });
    }
    
    // Attendi che tutti i thread terminino
    for (auto& t : threads) {
        if (t.joinable()) t.join();
    }
    
    // Calcola il tempo trascorso
    auto elapsed = std::chrono::steady_clock::now() - start_time;
    double elapsed_sec = std::chrono::duration_cast<std::chrono::duration<double>>(elapsed).count();
    
    // Mostra i risultati
    std::cout << std::endl << std::endl;
    std::cout << "Trovato dopo " << total_count.load() << " tentativi in " << elapsed_sec << " secondi!" << std::endl;
    std::cout << "Velocità: " << static_cast<double>(total_count.load()) / elapsed_sec << " indirizzi/secondo" << std::endl;
    std::cout << "Indirizzo: " << result_data.address << std::endl;
    std::cout << "Chiave privata (hex): " << result_data.private_key_hex << std::endl;
    std::cout << "Chiave pubblica (hex): " << result_data.public_key_hex << std::endl;
    
    // Mostra i risultati in modo completo
    std::cout << "\nRisultati:\n";
    std::cout << "Indirizzo trovato: " << result_data.address << "\n";
    std::cout << "Chiave privata (hex): " << result_data.private_key_hex << "\n";
    std::cout << "Chiave pubblica (hex): " << result_data.public_key_hex << "\n";
    std::cout << "Tentativi: " << total_count.load() << "\n";
    std::cout << "Tempo impiegato: " << elapsed_sec << " secondi\n";
    std::cout << "Indirizzi al secondo: " << static_cast<double>(total_count.load()) / elapsed_sec << "\n";
    std::cout << "Thread utilizzati: " << num_threads << "\n\n";

    return 0;
}