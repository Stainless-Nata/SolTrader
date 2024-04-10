import re

string = "#master Swapped **0.00010** #SOL ($0.019) for **7.86** #AART @ $0.0025 #solana [Cielo](https://app.cielo.finance/profile/G94qnKjWx9tgd2hrzF1uc98PZnqgzdvvzXiyRsm7Kzwd)  [ViewTx](https://solscan.io/tx/fN2QFQwUHwaUhJjVDMNXUn3mMsbEjLH1P7DNrvpeqGURCEQgLLcjp7HG9YToyL4nWJkpNudXwioWfZR8CBm7AaS)  [Chart](https://www.geckoterminal.com/solana/tokens/F3nefJBcejYbtdREjui1T9DPh5dBgpkKq7u2GAAMXs5B?utm_source=telegram&utm_medium=evmtrackerbot&utm_campaign=evmtrackerbot)"

label = re.search(r'#(\w+)', string).group(1)
amount1 = re.search(r'\*\*(.*?)\*\*', string.split(label)[1]).group(1)
currency1 = re.search(r'#(\w+)', string.split(amount1)[1]).group(1)
amount2 = re.search(r'\*\*(.*?)\*\*', string.split(currency1)[1]).group(1)
currency2 = re.search(r'#(\w+)', string.split(amount2)[1]).group(1)

print(label)       # output: master
print(amount1)      # Output: 0.00010
print(currency1)   # Output: SOL
print(amount2)     # Output: 7.86
print(currency2)   # Output: AART