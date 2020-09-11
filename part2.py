# %% import part 2 data

import pandas as pd

df2 = pd.read_csv("data2.csv")
df2 = df2.iloc[2:-1].set_index("Year")
df2[["Prince Rupert", "Quebec City"]] = df2[["Prince Rupert", "Quebec City"]].astype("float")
df2

# %% define ports and coasts

import matplotlib.pyplot as plt

ports = df2.columns.tolist()[:-2]
coasts = df2.columns.tolist()[-2:]

# %% line plot ports

fig, ax1 = plt.subplots(figsize=(10, 10))

annotate_list = []

for i in range(len(ports)):

    port = ports[i]

    ax1.plot(
        df2.index,
        df2[port],
        label=port,
        # color=colors[i],
        )

    ax1.fill_between(
        df2.index,
        df2[port],
        label=None,
        # color=colors[i],
        alpha=0.1
    )

    for year, tonnage in zip(df2.index, df2[port]):
        annotate_list.append((year, tonnage))

for x, y in annotate_list:

    ax1.annotate(
        f"{round((float(y)/1000000), 1)}m",
        xy=(x, y),
        xytext=(float(x), float(y)+0.01),
        ha="center",
    )

plt.xticks(df2.index)
plt.xlabel("Year")
plt.yticks(
    range(0, 180000000, 20000000),
    labels=range(0, 180, 20)
)
plt.ylabel("Cargos handled, in millions of metric tons")

plt.vlines(
    df2.index,
    0,
    160000000,
    linestyles="dashed",
    alpha=0.05,
)

plt.title("Cargo Handled by Major Canadian Ports by Tonnage, 2010-2019")
plt.legend(loc=7)

# %% line plot coast

fig, ax2 = plt.subplots(figsize=(10, 7))

colors=["#045c5a", "#b00149"]
annotate_list = []

for i in range(len(coasts)):

    coast = coasts[i]

    ax2.plot(
        df2.index[5:],
        df2[coast].loc[2015:],
        label=coast,
        color=colors[i],
        )

    ax2.fill_between(
        df2.index[5:],
        df2[coast].loc[2015:],
        label=None,
        color=colors[i],
        alpha=0.7,
    )

    for year, tonnage in zip(df2.index[5:], df2[coast].loc[2015:]):
        annotate_list.append((year, tonnage))

for x, y in annotate_list:

    ax2.annotate(
        f"{round((float(y)/1000000), 1)}m",
        xy=(x, y),
        xytext=(float(x), float(y)+3000000),
        ha="center",
    )

plt.xticks(df2.index[5:])
plt.xlabel("Year")

plt.ylim((0, 200000000))
plt.yticks(
    range(0, 210000000, 25000000),
    labels=range(0, 210, 25)
)
plt.ylabel("Cargos handled, in millions of metric tons")

plt.vlines(
    df2.index[5:],
    0,
    210000000,
    linestyles="dashed",
    alpha=0.05,
)

plt.title("Cargo Handled by Major Canadian Ports on Western and Eastern Coast\nBy Tonnage, 2015-2019")
plt.legend(loc=4)

# %%
