import pandas as pd

twt = []
print(type(twt))
twt = twt + [[12,34],[56,78]]
twt = pd.DataFrame(twt, columns=['a', 'b'])
print(twt)

