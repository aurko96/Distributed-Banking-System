import grpc
import bank_pb2
import bank_pb2_grpc

def run_client():
    with grpc.insecure_channel('localhost:9001') as channel:
        stub = bank_pb2_grpc.BankAccountServiceStub(channel)

        # Open an account
        open_response = stub.OpenAccount(bank_pb2.Empty())
        account_id = open_response.account_id
        print("Account {} is opened".format(account_id))
        
        # Deposit money to the account
        deposit_amount = float(input("Enter an amount to deposit: "))
        deposit_response = stub.DepositAccount(bank_pb2.DepositAccountRequest(account_id=account_id, amount=deposit_amount))
        print("Deposited {} to account {}. Balance: {}".format(deposit_amount, account_id, deposit_response.balance))

        # Add Interest to the account
        interest_value = float(input("Enter a percentage value as interest rate: "))
        interest_response = stub.AddInterest(bank_pb2.AddInterestRequest(account_id=account_id, interestRate=interest_value))
        print("{}% Interest added to account {}. Balance: {}".format(interest_value, account_id, interest_response.balance))

        # Withdraw money from the account
        withdraw_amount = float(input("Enter an amount to withdraw: "))
        withdraw_response = stub.WithdrawAccount(bank_pb2.WithdrawAccountRequest(account_id=account_id, amount=withdraw_amount))
        print("Withdrew {} from account {}. Balance: {}".format(withdraw_amount, account_id, withdraw_response.balance))

        # Get the balance of the account
        balance_response = stub.GetBalance(bank_pb2.BalanceAccountRequest(account_id=account_id))
        print("Balance of account {} is {}".format(account_id, balance_response.balance))
                
        
if __name__ == '__main__':
    run_client()
