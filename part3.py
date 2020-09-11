# %% import the data file

import pandas as pd

df3 = pd.read_csv("data3.csv")

# %% major partner lists

major_partners = {
    "Pacific": [
        "China",
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

# %% create index

df3["Index"] = ["Total"] + [section.split(" - ")[0] for section in df3["Sections"][1:]]
df3.set_index("Index", inplace=True)

# %% donut chart total trading volume

Pacific_total = df3.loc["Total", major_partners["Pacific"]]
Atlantic_total = df3.loc["Total", major_partners["Atlantic"]]

# labels = Pacific_total.index.tolist() + Atlantic_total.index.tolist()

def generate_value_label(totals, country):

    if totals[country] >= 10 ** 9:
        label = f'{round(totals[country]/10 ** 9, 1)} billions'
    else:
        label = f'{round(totals[country]/10 ** 6, 1)} millions'

    return label

Pac_labels = [f'{country} - {generate_value_label(Pacific_total, country)}' for country in Pacific_total.index]
Atl_labels = [f'{country} - {generate_value_label(Atlantic_total, country)}' for country in Atlantic_total.index]

# %% dount chart

import numpy as np
from matplotlib import pyplot as plt

fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(aspect="equal"))

cm1 = plt.cm.GnBu
cm2 = plt.cm.RdPu
color1 = cm1(np.linspace(0.5, 1., 10))
color2 = cm2(np.linspace(0.5, 1., 10))

ax.pie(
    Pacific_total.tolist() + Atlantic_total.tolist(),
    labels=Pac_labels+Atl_labels,
    labeldistance=1,
    rotatelabels=True,
    colors=np.concatenate((color1, color2)),
    radius=1,
    wedgeprops=dict(
            width=0.35,
            edgecolor="w",
        ),
    startangle=27,
)

ax.pie(
    [Pacific_total.sum(), Atlantic_total.sum()],
    labels=[
        f"Pacific Partners\n{round(Pacific_total.sum()/10 ** 9, 1)} billions",
        f"Atlantic Partners\n{round(Atlantic_total.sum()/10 ** 9, 1)} billions"
    ],
    labeldistance=0.15,
    rotatelabels=True,
    colors=["#0f9b8e", "#990147"],
    radius=0.65,
    wedgeprops=dict(
            width=0.15,
            edgecolor="w",
        ),
    startangle=27,
)

plt.suptitle(
    "Alberta's Volume of Exports to Major Trans-Pacific and\nTrans-Atlantic Trading Partners, 2019, $CAD",
    ha="center"
)
plt.show()

# %% Pac & Atl data

df3_pac = df3[["Sections"] + major_partners["Pacific"]]
df3_atl = df3[["Sections"] + major_partners["Atlantic"]]

# %% Major partners top exporting categories charting

from math import log10, ceil, floor

def top_3_categories_plot(ocean):

    data = df3[["Sections"] + major_partners[ocean]]

    cmap = plt.cm.tab20_r
    indexs = data.index[1:].tolist()
    color_dict = dict(zip(indexs, cmap(np.linspace(0., 1., len(indexs)))))

    fig, axes = plt.subplots(2, 5, figsize=(18, 8))
    fig.tight_layout(pad=4.0)

    for i in range(10):

        country = data.columns[1:][i]
        ax = axes[i//5, i%5]

        max_type_value = data[country][1:].sort_values(ascending=False)[:1].values
        if max_type_value/(10 ** floor(log10(max_type_value))) <= 5:
            max_y = 5 * (10 ** floor(log10(max_type_value)))
        else:
            max_y = 10 ** ceil(log10(max_type_value))

        if max_y >= 10 ** 10:
            ylabels=[f"{round(tick / 10 ** 9, 1)}b" for tick in np.linspace(0, max_y, 5)]
        else:
            ylabels=[f"{round(tick / 10 ** 6, 1)}m" for tick in np.linspace(0, max_y, 5)]

        top_categories = data[1:].sort_values(by=country, ascending=False)[:3].index

        ax.set_ylabel("Volumes ($CAD)")
        ax.set_xlabel("Categories")
        ax.set_ylim(0, max_y)
        ax.set_yticks(np.linspace(0, max_y, 5))
        ax.set_yticklabels(ylabels)

        ax.bar(
            top_categories,
            data[country][top_categories],
            color=top_categories.map(color_dict),
        )
        ax.set_aspect(1.0/ax.get_data_ratio(), adjustable='box')
        ax.set_title(f"{country}")

    plt.suptitle(f"Alberta Export to Major Trans-{ocean} Trading Partners by Top 3 Commodity Types\nYear: 2019, UOM: $CAD")
    plt.show()

# %% chart on both sides

top_3_categories_plot("Pacific")
top_3_categories_plot("Atlantic")

# %% major types dict

major_types_dict = dict(zip(
    df3.index[1:].tolist(),
    ["Agricultural & Food"] * 4 + ["Mining, Energy, Metal & Chemical"] * 3 + ["Agricultural & Food"] + ["Forestery"] * 2 + \
    ["Manufacture & Miscellaneous"] * 3 +  ["Mining, Energy, Metal & Chemical"] * 2 + ["Manufacture & Miscellaneous"] * 6
))

major_types = [
    "Mining, Energy, Metal & Chemical",
    "Agricultural & Food",
    "Forestery",
    "Manufacture & Miscellaneous",
]

# %% group by major types

df3_pac["Types"] = df3_pac.index.map(major_types_dict)
df3_atl["Types"] = df3_atl.index.map(major_types_dict)

pac_types = df3_pac.iloc[1:, 1:].groupby(by="Types").sum().reindex(major_types)
atl_types = df3_atl.iloc[1:, 1:].groupby(by="Types").sum().reindex(major_types)

# %% major types piechart

def convert_value_label(value):
    if value >= 10 ** 9:
        converted_label = f"{round(value/10 ** 9, 1)}b"
    else:
        converted_label = f"{round(value/10 ** 6, 1)}m"

    return converted_label

def major_types_pie(data):

    fig, axes = plt.subplots(2, 5, figsize=(18, 9))
    fig.tight_layout(pad=4.0, h_pad=0)

    for i in range(10):

        country = data.columns[i]
        ax = axes[i//5, i%5]

        country_total = data[country].sum()

        labeling_types = [
            "Mining & Energy",
            "Agricultural",
            "Forestery",
            "Manu & Others",
        ]
        labeling_values = [convert_value_label(value) for value in data[country]]
        labels = [
            f"{label}\n{value_label} - " + '{:.1%}'.format(value/country_total) \
            for label, value_label, value in zip(labeling_types, labeling_values, data[country])
        ]
        colors = ["brown", "#fbdd7e", "green", "grey"]

        index_max = data[country].reset_index()[country].idxmax()

        explode_list = [0] * 4
        explode_value = 0.13 if data[country][index_max]/country_total > 0.7 else 0.1
        explode_list[index_max] = explode_value

        ocean = "Pacific" if "Australia" in data.columns else "Atlantic"
        basic_angle = 30 if ocean=="Pacific" else 0
        start_angle = basic_angle - 360 * (data[country][:index_max].sum() / country_total)

        ax.pie(
            data[country],
            labels=labels,
            labeldistance=1,
            colors=colors,
            startangle=start_angle,
            radius=np.sqrt(log10(country_total))/3,
            explode=explode_list,
        )

        ax.set_title(f"{country} - ${convert_value_label(country_total)} of Total Export")

    plt.suptitle(
        f"Albertan Exportation to Major Trans-{ocean} Trading Partners, by Major Commdity Categories\nYear: 2019; UOM: $CAD",
        fontsize="xx-large",
    )
    plt.show()

# %% charting

major_types_pie(pac_types)
major_types_pie(atl_types)

# %% output the spec for sections

df3_pac[["Sections", "Types"]].reset_index().to_csv("data3sec.csv", index=False)

# %%
