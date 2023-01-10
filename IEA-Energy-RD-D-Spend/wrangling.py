from email.policy import default
import click
import pandas as pd
from pathlib import Path


@click.command()
@click.argument("input", type=click.Path(exists=True, path_type=Path))
@click.option("--output", default=Path("./output.csv"), type=click.Path(path_type=Path))
def wrangle(input: Path(), output: Path()) -> None:
    df = pd.read_excel(input, skiprows=[0])
    df = pd.melt(frame=df, id_vars=[
        'Country', 'Currency', 'Economic Indicators'], var_name='Year', value_name='Value')
    df["Year"] = df["Year"].astype(float).astype(int)
    df.rename(columns={"Currency": "Measure"}, inplace=True)
    df['Measure'] = df.apply(
        lambda x: "Percentage of GDP" if x['Measure'] == '-' else x['Measure'], axis=1)
    df['Unit'] = df.apply(lambda x: 'Millions of GBP' if x['Measure']
                        == 'National currency (nominal)' else "%", axis=1)
    df['Value'] = df.apply(lambda x: "{0:.4f}".format(x['Value']*100) if x['Unit'] == "%" else "{0:.4f}".format(x['Value']), axis=1)

    df['Economic Indicators'] = df['Economic Indicators'].str.rstrip()
    df = df.replace({'Country': {"United Kingdom": "K02000001"}})
    df.to_csv(output, index=False)
    return

if __name__ == "__main__":
    wrangle()