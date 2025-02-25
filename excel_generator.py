import pandas as pd

def generate_excel(data, filename):
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)