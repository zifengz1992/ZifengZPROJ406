# %% import part 1 data

import pandas as pd

df1 = pd.read_csv("data1.csv")
df1

# %% select columns

df1 = df1[
    [
        "REF_DATE",
        "Estimates",
        "Enterprise employment size",
        "Country of destination",
        "UOM",
        "SCALAR_FACTOR",
        "COORDINATE",
        "VALUE",
    ]
]

# %% fillna

df1 = df1.fillna(0)

# %% continents dataframe

continents = {
    "Asia": "Asia-Pacific",
    "Africa": "Europe & Africa",
    "Europe": "Europe & Africa",
    "Oceania and Antarctica": "Asia-Pacific",
}

df1_z = df1[df1["Country of destination"].isin(continents.keys())].reset_index(drop=True)
df1_z

# %% continential sum

select_values = df1_z["UOM"] == "Dollars"
select_counts = df1_z["UOM"] == "Number"
select_all_ents = df1_z["Enterprise employment size"] == "All enterprise employment sizes"

df1_z["Region"] = df1_z["Country of destination"].map(continents)

df1_zvalue = df1_z.loc[select_values & select_all_ents][["REF_DATE", "Region", "VALUE"]].groupby(by=["REF_DATE", "Region"]).sum()
df1_zvalue = df1_zvalue.reset_index().pivot(
    index="REF_DATE",
    columns="Region",
    values="VALUE",
)
df1_zvalue

# %% Four continents

df1_valuebyz = df1_z.loc[select_values & select_all_ents][["REF_DATE", "Country of destination", "VALUE"]].groupby(by=["REF_DATE", "Country of destination"]).sum()
df1_valuebyz = df1_valuebyz.reset_index().pivot(
    index="REF_DATE",
    columns="Country of destination",
    values="VALUE",
)

# %% Plotting west & east coast - continent

from matplotlib import pyplot as plt

fig, ax = plt.subplots(figsize=(15, 6))

ax.set_xlim(2009.4, 2019.6)
ax.set_xticks(df1_zvalue.index)
# for label in ax.get_xticklabels():
#     label.set_rotation(90)

ax.set_yticks(range(0, 80000000, 10000000))
ax.set_yticklabels(
    labels=[f'{value}.0' for value in range(0, 80, 10)],
)

ax.hlines(
    y=range(1, 80000000, 10000000),
    xmin=2009,
    xmax=2020,
    colors="#d8dcd6",
    linestyles="dashed",
    zorder=0,
)

ax.bar(
    x=df1_zvalue.index,
    height=df1_zvalue["Asia-Pacific"],
    width=-0.3,
    align="edge",
    color="#10a674",
    label="Asia-Pacific",
)

ax.bar(
    x=df1_zvalue.index,
    height=df1_zvalue["Europe & Africa"],
    width=0.3,
    align="edge",
    color="#cb0162",
    label="Europe & Africa",
)

ax.set_xlabel("Year")
ax.set_ylabel("Value of Exports ($CAD, billions)")
ax.legend()

# %% enterprise count dataframe

cols = [
    "REF_DATE",
    "Country of destination",
    "Enterprise employment size",
    "VALUE",
]

df1_zcount = df1_z.loc[select_counts][cols].groupby(by=cols[:-1]).sum()
df1_zcount = df1_zcount.reset_index().pivot_table(
    index="REF_DATE",
    columns=["Country of destination", "Enterprise employment size"],
    values="VALUE",
)
df1_zcount = df1_zcount.T.loc[["Asia", "Europe"]]
df1_zcount.columns = df1_zcount.columns.tolist()

# %% pie chart selecting year

df1_zc2019 = df1_zcount[2019]
df1_zc2019

# %% pie charting function

import numpy as np

def pie_entcount(continent, data, ax=None):

    entcates = [
        "0 or unreported employees",
        "1 to 9 employees",
        "10 to 49 employees",
        "50 to 99 employees",
        "100 to 249 employees",
        "250 to 499 employees",
        "Large enterprises (500 or more employees)",
        "All enterprise employment sizes",
        "Small and medium-sized enterprises (0 to 499 employees)"
    ]

    entsizes = [size.strip(" employees") for size in data[continent].reindex(entcates).index.tolist()[:6]] + ["500 or more"]

    labels = [
        (f"{size}\n{int(count)} - "+"{:.1%}".format(count/data[continent].values[6]))\
        for size, count in zip(entsizes, data[continent].reindex(entcates).values[:7])
    ]

    ax.pie(
        x=data[continent].reindex(entcates).values[:7],
        labels=labels,
        labeldistance=0.9,
        textprops={"fontsize": 12},
        startangle=0,
        radius=np.sqrt(data[continent].values[6])/100,
    )

    return ax

def pie_ent_annual(year):

    data = df1_zcount[year]
    asia_total = int(data["Asia"].values[6])
    euro_total = int(data["Europe"].values[6])
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 7))

    pie_entcount("Asia", data=data, ax=ax1)
    ax1.set_title(
        f"{year} - Asia - {asia_total} enterprises total"
    )

    pie_entcount("Europe", data=data, ax=ax2)
    ax2.set_title(
        f"{year} - Europe - {euro_total} enterprises total"
    )

    fig.suptitle(
        f'No. of Canadian Enterprises Exporting to European and Asian Markets\nBy: No. of Employees. Year: {year}.',
        fontsize="x-large",
    )

    plt.show()

# %% pie charting

# # pie chartings by year - not used
# pie_ent_annual(2019)
# pie_ent_annual(2015)
# pie_ent_annual(2010)

continents = ["Europe", "Asia"]
years = [2010, 2015, 2019]

fig, axes = plt.subplots(2, 3, figsize=(20, 13))

for i in range(2):
    for j in range(3):

        continent = continents[i]
        year = years[j]
        data = df1_zcount[year]
        total = int(data[continent].values[6])

        pie_entcount(
            continent=continent,
            data=data,
            ax=axes[i, j]
        )

        axes[i, j].set_title(
            f"{year} - {continent} - {total} enterprises total",
            fontdict={"fontsize": "x-large"}
        )

fig.suptitle(
    "No. of Canadian Enterprises Exporting to European and Asian Markets\nBy: No. of Employees. Year: 2010, 2015, 2019.",
    fontsize="xx-large",
)

# %% partner list

major_partners = {
    "Pacific": [
        "China",
        "Hong Kong",
        "Macao",
        "Japan",
        "South Korea",
        "India",
        "Indonesia",
        "Australia",
        "Singapore",
        "Viet Nam",
        "Philippines",
        "Malaysia",
    ],
    "Atlantic": [
        "United Kingdom",
        "Germany",
        "Belgium",
        "France",
        "Netherlands",
        "Italy",
        "Switzerland",
        "Norway",
        "Brazil",
        "Spain",
    ],
}

# for country in (list(major_partners.values())[0]+list(major_partners.values())[1]):
#     print(f'Country name: {country}')
#     print(f'In data: {country in df1["Country of destination"].tolist()}')


# %% pacific, atlantic, all major partners dataframes

select_values = df1["UOM"] == "Dollars"
select_all_ents = df1["Enterprise employment size"] == "All enterprise employment sizes"

df_pacific = df1.loc[select_values & select_all_ents]
df_atlantic = df_pacific

df_pacific = df_pacific[df_pacific["Country of destination"].isin(major_partners["Pacific"])]
df_pacific["Region"] = "Pacific"

df_atlantic = df_atlantic[df_atlantic["Country of destination"].isin(major_partners["Atlantic"])]
df_atlantic["Region"] = "Atlantic"

df_mp = pd.concat([df_pacific, df_atlantic], ignore_index=True)
df_mp["Country"] = df_mp["Country of destination"].replace(["Hong Kong", "Macao"], "China")

# %% Value sumup and treemapping by year function

def treemap_value(year=2019):

    df_mp_v = df_mp[df_mp["REF_DATE"] == year]
    df_mp_v = df_mp_v[["Region", "Country", "VALUE"]].groupby(by=["Region", "Country"]).sum()
    df_mp_v = df_mp_v.reset_index().sort_values(by="VALUE", ascending=False)
    df_mp_v

    import squarify
    import numpy as np

    colors = ["#98eff9" if region == "Pacific" else "#ffcfdc" for region in df_mp_v["Region"]]
    labels = [f"{country}\n${round(value/1000000, 1)} B" for country, value in zip(df_mp_v["Country"], df_mp_v["VALUE"])]
    size = round(np.sqrt(df_mp_v["VALUE"].sum() / 1000000), 0)

    fig, ax = plt.subplots(figsize=(size*1.2, size*0.8))
    squarify.plot(
        df_mp_v["VALUE"],
        color=colors,
        label=labels,
        ax=ax,
        alpha=1,
        bar_kwargs=dict(linewidth=1, edgecolor="#ffffff"),
        text_kwargs={"fontsize": 8}
    )

    ax.axis("off")
    ax.set_title(f"Canadian Exportation Volumes to Major Eastern / Western Coast Partners in {year}", fontsize=12)

    plt.show()

# %% treemapping

treemap_value(2019)
treemap_value(2015)
treemap_value(2010)

# %%
