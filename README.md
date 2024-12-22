# Distributed-Banking-System

**Overview:**

The project implements a Bank Account Manager using Remote Procedure Call (RPC) programming with **gRPC** in Python. 
It consists of a server that provides services to manage bank accounts and clients that interact with the server to perform various banking operations.

**Console Image:**

A screenshot of the console from multiple terminals shows multiple clients accessing the bank server.

![banking_distributed_system_console](https://github.com/user-attachments/assets/82a34796-7080-4d6c-b03c-0d2bfcf8faa0)


**Features:**

The system offers the following functionalities via RPC:

1. OpenAccount:
Creates a new bank account and returns a unique account identifier.

2. DepositAccount:
Deposits a specified amount into an account.

3. AddInterest:
Applies a specific interest percentage to the balance of an account.

4. WithdrawAccount:
Withdraws a specified amount of money from an account.

5. GetBalance:
Retrieves the balance of a specified account.


**Additional Features:**

* Thread Safety:
Bank server with semaphore python file (bank-server-sem.py) introduces the use of semaphores in the banking server to allow multiple clients/devices to safely access the same account's different functionalities concurrently.

* Rounded Balances:
All balances are maintained with precision up to two decimal points.

**Technologies:**

* Python 3.8+
* gRPC Python Tools: Install the required gRPC tools using ``` pip install grpcio grpcio-tools ```

**Setup and Instructions:**

1. Proto File Compilation
Compile the provided bank.proto file to generate the necessary Python files for gRPC. Use the following command:

```
python -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. bank.proto
```

2. Running the Server
Start the server by providing the machine name, port number, and number of threads as command-line arguments or just start the server without passing any parameter in command-line argument and it will start with default settings.
Example:

* Initiating bank server with parameters
```
python bank-server.py gaul.csd.uwo.ca 9001 4
python bank-server-sem.py gaul.csd.uwo.ca 9001 4
```
* Initiating bank server without parameters
```
python bank-server.py
python bank-server-sem.py
```

3. Running the Client
Clients can perform operations by interacting with the server. Use multiple clients to test concurrent access for bank-server-sem.py. Each client program should connect to the server using the same machine name and port number.
```
python bank-client.py
```

**Project Notes:**

* Account data is stored in an in-memory data structure (e.g. dictionary or list) for simplicity.
* OpenAccount generates sequential account identifiers starting from 1.
* The project is designed to simulate enterprise-grade account management in a distributed system without integrating a database backend.
