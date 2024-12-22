from concurrent import futures
import sys

import grpc

import bank_pb2
import bank_pb2_grpc
import threading

class BankAccountService(bank_pb2_grpc.BankAccountServiceServicer):
    def __init__(self):
        self.currentId = 0
        self.accounts = {}
        self.openAccountSemaphore = threading.Semaphore(1)
        self.accountSemaphore = {}

    def OpenAccount(self, request, context):
        # opens account with incremental account id
        # Seperate semaphore used for open account so that there is no conflict in account id
        # while creating account from multiple threads simultaneously
        self.openAccountSemaphore.acquire()
        self.currentId += 1
        currentIdString = str(self.currentId)
        account_id = currentIdString
        self.accounts[account_id] = 0.00
        self.accountSemaphore[account_id] = threading.Semaphore(1)
        self.openAccountSemaphore.release()
        return bank_pb2.AccountIdentifier(account_id = account_id)

    def WithdrawAccount(self, request, context):
        # Withdraws amount of the requested account
        # Semaphore based on account id used so that balance withdrawal of a particular
        # account id can process one at a time, but different account id can process simultaneously
        account_id = request.account_id
        amount = request.amount

        # Validations
        if account_id not in self.accounts:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Account does not exist in the bank server")
            return bank_pb2.AccountBalance()

        if self.accounts[account_id] < amount:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("Not enough funds to withdraw from the account")
            return bank_pb2.AccountBalance()

        self.accountSemaphore[account_id].acquire()
        self.accounts[account_id] -= round(amount, 2)
        self.accountSemaphore[account_id].release()
        return bank_pb2.AccountBalance(balance = round(self.accounts[account_id], 2))

    def DepositAccount(self, request, context):
        # Deposits amount to the requested account
        # Semaphore based on account id used so that balance deposited to a particular
        # account id can process one at a time, but different account id can process simultaneously
        account_id = request.account_id
        amount = request.amount

         # Validations
        if account_id not in self.accounts:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Account does not exist in the bank server")
            return bank_pb2.AccountBalance()

        self.accountSemaphore[account_id].acquire()
        self.accounts[account_id] += round(amount, 2)
        self.accountSemaphore[account_id].release()
        return bank_pb2.AccountBalance(balance = round(self.accounts[account_id], 2))

    def GetBalance(self, request, context):
        # Gets balance of the requested account
        account_id = request.account_id

        # Validations
        if account_id not in self.accounts:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Account does not exist in the bank server")
            return bank_pb2.AccountBalance()

        return bank_pb2.AccountBalance(balance = round(self.accounts[account_id], 2))

    def AddInterest(self, request, context):
        # Adds interest to the account balance of the requested account
        # Semaphore based on account id used so that interest added to the balance of a particular
        # account id can process one at a time, but different account id can process simultaneously
        account_id = request.account_id
        interest_rate = request.interestRate

        # Validations
        if account_id not in self.accounts:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Account does not exist in the bank server")
            return bank_pb2.AccountBalance()
        
        if interest_rate < 0 or interest_rate > 100:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("Invalid input of interest rate")
            return bank_pb2.AccountBalance()

        self.accountSemaphore[account_id].acquire()
        interest_addedValue = float(self.accounts[account_id] * float(interest_rate / 100))
        self.accounts[account_id] += round(interest_addedValue , 2)
        self.accountSemaphore[account_id].release()
        return bank_pb2.AccountBalance(balance = round(self.accounts[account_id], 2))

def serve(machineName, portNumber, totalNumberOfThreads):
    server = grpc.server(
        options=[
            ('grpc.server_name', machineName),
        ],
        thread_pool=futures.ThreadPoolExecutor(max_workers = int(totalNumberOfThreads)),
    )
    bank_pb2_grpc.add_BankAccountServiceServicer_to_server(BankAccountService(), server)
    server.add_insecure_port('[::]:' + portNumber)
    server.start()
    print("Bank Server " + machineName + " Started, Listening on Port " + portNumber + " having number of threads = " + totalNumberOfThreads)
    server.wait_for_termination()

if __name__ == '__main__':
    if len(sys.argv) < 4:
        # Initializing some default parameters
        machineName = 'gaul.csd.uwo.ca.'
        portNumber = '9001'
        totalNumberOfThreads = '4'
    else:
        # Input parameters from command line
        machineName = sys.argv[1] 
        portNumber = sys.argv[2] 
        totalNumberOfThreads = sys.argv[3]
    
    serve(machineName = machineName, portNumber = portNumber, totalNumberOfThreads = totalNumberOfThreads)
