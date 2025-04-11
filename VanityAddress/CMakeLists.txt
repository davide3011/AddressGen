cmake_minimum_required(VERSION 3.10)
project(vanity_generator)

# Imposta lo standard C++17
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Trova OpenSSL
find_package(OpenSSL REQUIRED)

# Trova Threads (necessario per il multithreading)
find_package(Threads REQUIRED)

# Aggiungi l'eseguibile
add_executable(vanity vanity.cpp)

# Collega le librerie OpenSSL e Threads
target_link_libraries(vanity OpenSSL::SSL OpenSSL::Crypto Threads::Threads)

# Imposta le opzioni del compilatore
if(MSVC)
    target_compile_options(vanity PRIVATE /W4 /O2)
else()
    target_compile_options(vanity PRIVATE -Wall -Wextra -O3 -march=native)
endif()