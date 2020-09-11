# %% load the part 4 data

import pandas as pd

df4 = pd.read_csv("data4.csv")

# %% editing some values in the general dataframe

df4["Mode of transportation"] = df4["Mode of transportation"].replace("Truck (for-hire)", "Truck")
df4["GEO"] = df4["GEO"].str.rsplit(",", n=1, expand=True)[0]

# %% measuring by weight heading for van

meas_by_weight = df4["UOM"] == "Kilograms"
heading_for_van = df4["Geography, destination of shipments"] == "Vancouver, British Columbia, destination of shipments"

df_van = df4[meas_by_weight & heading_for_van].reset_index(drop=True)

# %% filtering data

df_van = df_van[df_van["GEO"] != "Vancouver, British Columbia"]
df_van = df_van[~df_van["Commodity group"].isin(["Waste and scrap [41]"])]

# %% select cols

cols = [
    "REF_DATE",
    "GEO",
    "Geography, destination of shipments",
    "Mode of transportation",
    "Commodity group",
    "VALUE",
]

df_van = df_van[cols]

# %% fillnas # all nas are in values column

df_van = df_van.fillna(0)

# %% region dict used for Vancouver data frame

van_region_dict = dict(zip(
    df_van["GEO"].unique().tolist(),
    list(
        ["Atlantic"] * 5 + ["Quebec"] * 3 + ["Ontario"] * 5 + ["Prairies"] * 7 + \
        ["BC"] + ["Territories"] * 2 + ["USMX"] + ["OTH"] + ["Territories"])
    )
)

# %% create region column for grouping

df_van["Region"] = df_van["GEO"].map(van_region_dict)

# %% create grouped dataframe

can_regions = [
    "Atlantic",
    "Quebec",
    "Ontario",
    "Prairies",
    "BC",
    "Territories", # not important for analysis
    # "USMX",
]

van_regions = df_van[df_van['Region'].isin(can_regions)].groupby(by=['REF_DATE', 'Region', 'Mode of transportation', 'Commodity group']).sum()
van_regions = van_regions.reset_index()

# %% Vancouver plotting

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def convert_ton_label(value):
    converted_label = f"{round(value/10 ** 9, 1)}m"
    return converted_label

fig, ax = plt.subplots(figsize=(9, 7))

ax.set_ylim(0, 4.5 * 10 ** 9)
ax.set_yticks(np.linspace(0, 4.5 * 10 ** 9, 10))
ax.set_yticklabels([convert_ton_label(tick) for tick in range(0, 46 * 10 ** 8, 5 * 10 ** 8)])

sns.barplot(
    x='Region',
    y='VALUE',
    hue='Mode of transportation',
    data=van_regions[van_regions['REF_DATE'] == 2017],
    order=can_regions[:-1][::-1] + [can_regions[-1]],
    hue_order=["Air", "Rail", "Truck"],
    ax=ax,
    ci=None,
)

ax.set_xlabel("Regions")
ax.set_ylabel("Weight of Cargo Transported (millions of tons)")
ax.hlines(
    ax.get_yticks(),
    xmin=ax.get_xlim()[0],
    xmax=ax.get_xlim()[1],
    linestyles="solid",
    alpha=0.1,
)
fig.suptitle("Cargo Transported to Vancouver from Different Regions of Canada, by Tonnages and Mean of Transport")

plt.legend(loc=1)

# %% Montreal dataframe

heading_for_mon = df4["Geography, destination of shipments"] == "Montréal, Quebec, destination of shipments"
df_mon = df4[meas_by_weight & heading_for_mon].reset_index(drop=True)

df_mon = df_mon[df_mon["GEO"] != "Montréal, Quebec"]
df_mon = df_mon[~df_mon["Commodity group"].isin(["Waste and scrap [41]"])]

df_mon = df_mon[cols].fillna(0)

# %% Montreal region dict

mon_region_dict = dict(zip(
    df_mon["GEO"].unique().tolist(),
    list(
        ["Atlantic"] * 5 + ["Quebec"] * 2 + ["Ontario"] * 5 + ["Prairies"] * 7 + \
        ["BC"] * 2 + ["Territories"] * 3 + ["USMX"] + ["OTH"])
    )
)

df_mon["Region"] = df_mon["GEO"].map(mon_region_dict)

# %% Montreal grouped data frame

mon_regions = df_mon[df_mon['Region'].isin(can_regions)].groupby(by=['REF_DATE', 'Region', 'Mode of transportation', 'Commodity group']).sum()
mon_regions = mon_regions.reset_index()

# %% Montreal plotting

fig, ax = plt.subplots(figsize=(9, 7))

# Dimensions fitting Montreal graph, not used for comparison purpose
# ax.set_ylim(0, 1.6 * 10 ** 9)
# ax.set_yticks(np.linspace(0, 1.6 * 10 ** 9, 9))
# ax.set_yticklabels([convert_ton_label(tick) for tick in range(0, 17 * 10 ** 8, 2 * 10 ** 8)])

ax.set_ylim(0, 4.5 * 10 ** 9)
ax.set_yticks(np.linspace(0, 4.5 * 10 ** 9, 10))
ax.set_yticklabels([convert_ton_label(tick) for tick in range(0, 46 * 10 ** 8, 5 * 10 ** 8)])

sns.barplot(
    x='Region',
    y='VALUE',
    hue='Mode of transportation',
    data=mon_regions[mon_regions['REF_DATE'] == 2017],
    order=can_regions[:-1][::-1] + [can_regions[-1]],
    hue_order=["Air", "Rail", "Truck"],
    ax=ax,
    ci=None,
)

ax.set_xlabel("Regions")
ax.set_ylabel("Weight of Cargo Transported (millions of tons)")
ax.hlines(
    ax.get_yticks(),
    xmin=ax.get_xlim()[0],
    xmax=ax.get_xlim()[1],
    linestyles="solid",
    alpha=0.1,
)

fig.suptitle("Cargo Transported to Montreal from Different Regions of Canada, by Tonnages and Mean of Transport")
plt.legend(loc=1)

# %% Prairies products to Van by type - dataframe

pra_van = df_van[df_van["Region"]=="Prairies"]

pra_van_2017 = pra_van[pra_van["REF_DATE"]==2017][["Commodity group", "Mode of transportation", "VALUE"]].groupby(by=["Commodity group", "Mode of transportation"]).sum().reset_index()
pra_van_2017["Commodity group"] = pra_van_2017["Commodity group"].str.split("[", n=1, expand=True)[0].str.strip()
pra_van_2017 = pra_van_2017.pivot(
    index="Commodity group",
    columns="Mode of transportation",
    values="VALUE",
)

pra_van_2017["Total"] = pra_van_2017.sum(axis=1)
pra_van_2017["Index"] = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI"]
pra_van_2017 = pra_van_2017.sort_values(by="Total", ascending=False)

# %% Plotting

def convert_ton_label_mk(value):

    if value >= 10 ** 9:
        converted_label = f"{round(value/10 ** 9, 1)}m"
    else:
        converted_label = f"{round(value/10 ** 6, 1)}k"
    return converted_label

fig, ax = plt.subplots(figsize=(10, 13))

ax.set_ylim(0, 3 * 10 ** 10)
ax.set_yticks(np.linspace(0, 3 * 10 ** 10, 7))
ax.set_yticklabels([convert_ton_label(tick) for tick in ax.get_yticks()])

ax.bar(
    pra_van_2017.index,
    pra_van_2017["Truck"],
    width=0.7,
    color="#017371",
    label="Truck",
)

ax.bar(
    pra_van_2017.index,
    pra_van_2017["Rail"],
    width=0.7,
    color="#f7d560",
    bottom=pra_van_2017["Truck"],
    label="Rail",
)

ax.bar(
    pra_van_2017.index,
    pra_van_2017["Air"],
    width=0.7,
    color="#490648",
    bottom=pra_van_2017["Truck"]+pra_van_2017["Rail"],
    label="Air (yes, it is on the graph! only with type IX)"
)

ax.set_xticklabels(pra_van_2017["Index"])

for i in range(len(pra_van_2017.index)):

    index = pra_van_2017.index[i]
    type_total = pra_van_2017.loc[index]["Total"]
    rail_per = pra_van_2017["Rail"].loc[index]/type_total
    note = f"Total\n{convert_ton_label_mk(type_total)}\ntons,\n" + "{:.1%}".format(rail_per) + "\nby rail"


    if i >= 2:
        ax.annotate(
            note,
            xy=(ax.get_xticks()[i], type_total + 2 * 10 ** 9),
            ha="center",
        )

        ax.vlines(
            ax.get_xticks()[i],
            type_total + 5 * 10 ** 8,
            type_total + 15 * 10 ** 8,
            linestyles="solid",
            alpha=0.9,
        )

    else:
        ax.annotate(
            note,
            xy=(ax.get_xticks()[i], type_total + 5 * 10 ** 8),
            ha="center",
        )

ax.set_xlabel("Category of Commodities")
ax.set_ylabel("Tonnage of Cargos Transported")
ax.set_title(
    "Percentage of Commodities Transported by Rail from Prairie Provinces to Vancouver,\nby Commodity Types, in 2017",
    fontsize="x-large",
)

plt.legend(loc=1)
plt.show()

# %% Alberta dataframe

ab_geo = [
    "Calgary, Alberta",
    "Edmonton, Alberta",
    "Rest of Alberta",
]

ab_van = df_van[df_van["GEO"].isin(ab_geo)]
ab_van_2017 = ab_van[ab_van["REF_DATE"]==2017][["Commodity group", "Mode of transportation", "VALUE"]].groupby(by=["Commodity group", "Mode of transportation"]).sum().reset_index()
ab_van_2017["Commodity group"] = ab_van_2017["Commodity group"].str.split("[", n=1, expand=True)[0].str.strip()
ab_van_2017 = ab_van_2017.pivot(
    index="Commodity group",
    columns="Mode of transportation",
    values="VALUE",
)

ab_van_2017["Total"] = ab_van_2017.sum(axis=1)
ab_van_2017["Index"] = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI"]
spec = ab_van_2017[["Index"]] # creating unsorted spec list (used later)

ab_van_2017 = ab_van_2017.sort_values(by="Total", ascending=False)

# %% alberta plotting

fig, ax = plt.subplots(figsize=(10, 13))

ax.set_ylim(0, 3 * 10 ** 10)
ax.set_yticks(np.linspace(0, 3 * 10 ** 10, 7))
ax.set_yticklabels([convert_ton_label(tick) for tick in ax.get_yticks()])

ax.bar(
    ab_van_2017.index,
    ab_van_2017["Truck"],
    width=0.7,
    color="#017371",
    label="Truck",
)

ax.bar(
    ab_van_2017.index,
    ab_van_2017["Rail"],
    width=0.7,
    bottom=ab_van_2017["Truck"],
    color="#f7d560",
    label="Rail",
)

ax.bar(
    ab_van_2017.index,
    ab_van_2017["Air"],
    width=0.7,
    color="#490648",
    bottom=ab_van_2017["Truck"]+ab_van_2017["Rail"],
    label="Air (yes, it is on this graph as well and still only with type IX)"
)

ax.set_xticklabels(ab_van_2017["Index"])

for i in range(len(ab_van_2017.index)):

    index = ab_van_2017.index[i]
    type_total = ab_van_2017.loc[index]["Total"]
    rail_per = ab_van_2017["Rail"].loc[index]/type_total
    note = f"Total\n{convert_ton_label_mk(type_total)}\ntons,\n" + "{:.1%}".format(rail_per) + "\nby rail"


    if i != 0:
        ax.annotate(
            note,
            xy=(ax.get_xticks()[i], type_total + 2 * 10 ** 9),
            ha="center",
        )

        ax.vlines(
            ax.get_xticks()[i],
            type_total + 5 * 10 ** 8,
            type_total + 15 * 10 ** 8,
            linestyles="solid",
            alpha=0.9,
        )

    else:
        ax.annotate(
            note,
            xy=(ax.get_xticks()[i], type_total + 5 * 10 ** 8),
            ha="center",
        )

ax.set_xlabel("Category of Commodities")
ax.set_ylabel("Tonnage of Cargos Transported")
ax.set_title(
    "Percentage of Commodities Transported by Rail from Alberta to Vancouver,\nby Commodity Types, in 2017",
    fontsize="x-large",
)

plt.legend(loc=1)
plt.show()

# %% output spec for commodity groups

spec = spec.reset_index()[["Index", "Commodity group"]] # spec created when creating ab_van_2017
spec["Combined"] = spec["Index"].str.cat(spec["Commodity group"], sep=" - ")
spec.to_csv("data4spe.csv", index=False)

# %% Alberta all years data

df_ab_van = df_van[df_van["GEO"].isin(ab_geo)]
df_ab_van = df_ab_van[["REF_DATE", "Mode of transportation", "VALUE"]].groupby(by=["REF_DATE", "Mode of transportation"]).sum().reset_index()
df_ab_van = df_ab_van.pivot(
    index="REF_DATE",
    columns="Mode of transportation",
    values="VALUE",
)

df_ab_van["Total"] = df_ab_van.sum(axis=1)

for mean in df_ab_van.columns[:3]:
    df_ab_van[f"{mean}_p"] = df_ab_van[f"{mean}"] / df_ab_van["Total"]

# %% alberta multi years plotting

fig, ax = plt.subplots(figsize=(13, 6))

ax.set_xticks(df_ab_van.index)
ax.set_xticklabels(df_ab_van.index)

ax.set_ylim(0, 1)
ax.set_yticks(np.linspace(0, 1, 11))
ax.set_yticklabels(['{:.1%}'.format(tick) for tick in ax.get_yticks()])

ax.bar(
    df_ab_van.index,
    df_ab_van["Truck_p"],
    width=0.5,
    color="#8ab8fe",
    label="Truck %",
)

ax.bar(
    df_ab_van.index,
    df_ab_van["Rail_p"],
    width=0.5,
    color="#feb209",
    bottom=df_ab_van["Truck_p"],
    label="Rail %",
)

ax.bar(
    df_ab_van.index,
    df_ab_van["Air_p"],
    width=0.5,
    color="#5cb200",
    bottom=df_ab_van["Truck_p"]+df_ab_van["Rail_p"],
    label="Air %"
)

for i in range(len(df_ab_van.index)):

    index = df_ab_van.index[i]
    actual_rail = df_ab_van.loc[index]["Rail"]
    rail_per = df_ab_van.loc[index]["Rail_p"]
    note = f"{index}\nby rail:\n{convert_ton_label_mk(actual_rail)}\ntons,\n" + "{:.1%}".format(rail_per)



    ax.annotate(
        note,
        xy=(ax.get_xticks()[i], 0.5),
        xytext=(ax.get_xticks()[i], 0.42),
        ha="center",
    )


ax.set_xlabel("Year")
ax.set_ylabel("Percentage of Cargos Transported (by Tonnage)")
ax.set_title(
    "Percentage of Commodities Transported from Alberta to Vancouver by Rail, 2011-2017",
    fontsize="x-large",
)

plt.legend(loc=1)
plt.show()

# %%
