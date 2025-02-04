"""Produce histogram of discriminant from tagger output and labels."""

import numpy as np

from puma import Histogram, HistogramPlot
from puma.utils import get_dummy_2_taggers

# The line below generates dummy data which is similar to a NN output
df = get_dummy_2_taggers()

# Calculate discriminant scores for DIPS and RNNIP, and add them to the dataframe
FRAC_C = 0.018
df["disc_dips"] = np.log(
    df["dips_pb"] / (FRAC_C * df["dips_pc"] + (1 - FRAC_C) * df["dips_pu"])
)
df["disc_rnnip"] = np.log(
    df["rnnip_pb"] / (FRAC_C * df["rnnip_pc"] + (1 - FRAC_C) * df["rnnip_pu"])
)

# defining boolean arrays to select the different flavour classes
is_light = df["HadronConeExclTruthLabelID"] == 0
is_c = df["HadronConeExclTruthLabelID"] == 4
is_b = df["HadronConeExclTruthLabelID"] == 5

hist_dips_light = Histogram(
    df[is_light]["disc_dips"],
    flavour="ujets",
    label="DIPS",
    # if not set, the "ratio_group" argument would be set to the flavour "ujets"
    # so this is just done here for demonstration purposes
    ratio_group="ujets",
)
hist_dips_c = Histogram(
    df[is_c]["disc_dips"],
    flavour="cjets",
    label="DIPS",
    ratio_group="cjets",
)
hist_dips_b = Histogram(
    df[is_b]["disc_dips"],
    flavour="bjets",
    label="DIPS",
    ratio_group="bjets",
)
hist_rnnip_light = Histogram(
    df[is_light]["disc_rnnip"],
    flavour="ujets",
    label="RNNIP",
    linestyle="dashed",
    ratio_group="ujets",
)
hist_rnnip_c = Histogram(
    df[is_c]["disc_rnnip"],
    flavour="cjets",
    label="RNNIP",
    linestyle="dashed",
    ratio_group="cjets",
)
hist_rnnip_b = Histogram(
    df[is_b]["disc_rnnip"],
    flavour="bjets",
    label="RNNIP",
    linestyle="dashed",
    ratio_group="bjets",
)

# Initialise histogram plot
plot_histo = HistogramPlot(
    n_ratio_panels=1,
    ylabel="Normalised number of jets",
    ylabel_ratio_1="Ratio to DIPS",
    xlabel="$b$-jets discriminant",
    logy=False,
    leg_ncol=2,
    figsize=(6.8, 5),
    bins=np.linspace(-10, 10, 30),
    y_scale=1.5,
    ymax_ratio_1=1.5,
    ymin_ratio_1=0.5,
    atlas_second_tag="$\\sqrt{s}=13$ TeV, dummy jets \ndummy sample, $f_{c}=0.018$",
)

# Add the histograms
plot_histo.add(hist_dips_light, reference=True)
plot_histo.add(hist_dips_c, reference=True)
plot_histo.add(hist_dips_b, reference=True)
plot_histo.add(hist_rnnip_light)
plot_histo.add(hist_rnnip_c)
plot_histo.add(hist_rnnip_b)

plot_histo.draw()
plot_histo.savefig("histogram_discriminant.png", transparent=False)
