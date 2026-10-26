"""
Privacy Score / SSIM / PSNR comparison, split into two separate figures:
  1) Block conditions (10 points)
  2) Blur conditions (10 points)
No title, English-only, Poppins font matched to the reference figure's
weight hierarchy: SemiBold axis titles, Bold ticks/data labels, Regular legend.
"""
import os
import urllib.request
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# ---------------------------------------------------------------------------
# Font: Poppins (Google Fonts, OFL license) — downloaded once, then registered
# ---------------------------------------------------------------------------
FONT_DIR = "./_fonts"
os.makedirs(FONT_DIR, exist_ok=True)
FONT_BASE = "https://raw.githubusercontent.com/google/fonts/main/ofl/poppins/"
FONT_FILES = {
    "bold": "Poppins-Bold.ttf",
    "semibold": "Poppins-SemiBold.ttf",
    "regular": "Poppins-Regular.ttf",
}

FP = {}
try:
    for key, fname in FONT_FILES.items():
        fpath = os.path.join(FONT_DIR, fname)
        if not os.path.exists(fpath):
            urllib.request.urlretrieve(FONT_BASE + fname, fpath)
        fm.fontManager.addfont(fpath)
        FP[key] = fm.FontProperties(fname=fpath)
except Exception as e:
    print(f"[warn] Poppins download failed, using fallback font ({e})")
    FP = {k: fm.FontProperties(family="DejaVu Sans",
                                weight=("bold" if k != "regular" else "normal"))
          for k in FONT_FILES}

# ---------------------------------------------------------------------------
# Data (from the user-provided table)
# ---------------------------------------------------------------------------
block_labels = ["Original", "256", "128", "64", "32", "16", "8", "4", "2", "1"]
block_privacy = [0.00, 49.65, 45.99, 47.70, 47.40, 49.20, 49.57, 49.27, 48.82, 47.14]
block_ssim    = [1.0000, 0.2407, 0.3183, 0.2969, 0.2752, 0.2115, 0.1166, 0.0358, 0.0095, 0.0078]
block_psnr    = [100.00, 6.03, 7.15, 7.38, 7.78, 7.51, 7.50, 7.51, 7.50, 7.50]

blur_labels = ["0", "1", "2", "4", "8", "16", "32", "64", "128", "256"]
blur_privacy = [0.00, 0.75, 2.48, 6.10, 11.45, 17.70, 24.75, 30.33, 32.36, 34.62]
blur_ssim    = [1.0000, 0.8973, 0.7748, 0.6578, 0.5958, 0.5761, 0.5635, 0.5427, 0.5145, 0.5033]
blur_psnr    = [100.00, 32.67, 26.21, 22.22, 19.62, 17.34, 14.99, 13.10, 11.60, 10.14]

# ---------------------------------------------------------------------------
# Style constants
# ---------------------------------------------------------------------------
C_PRIVACY = "#08519c"   # navy  - Privacy Score  (left axis)
C_SSIM    = "#6a51a3"   # purple- SSIM x100      (left axis)
C_PSNR    = "#e6550d"   # orange- PSNR, dB       (right axis, log scale)

LABEL_FS  = 34   # axis title font size      -> SemiBold
TICK_FS   = 26   # tick label font size       -> Bold
LEGEND_FS = 30   # legend font size           -> Regular
ANNOT_FS  = 26   # in-plot data-value labels  -> Bold
LW        = 4.2
MS        = 13


def make_figure(labels, privacy, ssim, psnr, x_title, out_path):
    fig, ax = plt.subplots(figsize=(15, 9.5))
    ax2 = ax.twinx()
    x = range(len(labels))

    l1, = ax.plot(x, privacy, color=C_PRIVACY, marker="o", linewidth=LW,
                   markersize=MS, label="Privacy Score")
    l2, = ax.plot(x, [s * 100 for s in ssim], color=C_SSIM, marker="^",
                   linewidth=LW, markersize=MS, linestyle="--",
                   label="Single-scale SSIM x100 (ref.)")
    l3, = ax2.plot(x, psnr, color=C_PSNR, marker="s", linewidth=LW,
                    markersize=MS, linestyle=":", label="PSNR, dB (ref.)")

    for i, (xi, yi) in enumerate(zip(x, privacy)):
        dy = 20 if i % 2 == 0 else -28
        va = "bottom" if dy > 0 else "top"
        ax.annotate(f"{yi:.1f}", (xi, yi), textcoords="offset points",
                    xytext=(0, dy), ha="center", va=va, fontsize=ANNOT_FS,
                    color=C_PRIVACY, fontproperties=FP["bold"])

    ax.set_xticks(list(x))
    ax.set_xticklabels(labels, fontsize=TICK_FS, fontproperties=FP["bold"])
    ax.set_xlabel(x_title, fontsize=LABEL_FS, fontproperties=FP["semibold"],
                  labelpad=16)
    ax.set_ylabel("Privacy Score / SSIM x100", fontsize=LABEL_FS,
                   fontproperties=FP["semibold"], labelpad=16)
    ax2.set_ylabel("PSNR (dB, log scale)", fontsize=LABEL_FS,
                    fontproperties=FP["semibold"], labelpad=20)

    ax.set_ylim(-10, 112)
    ax2.set_yscale("log")
    ax2.set_ylim(4, 140)

    plt.setp(ax.get_yticklabels(), fontsize=TICK_FS, fontproperties=FP["bold"])
    plt.setp(ax2.get_yticklabels(), fontsize=TICK_FS, fontproperties=FP["bold"])
    ax.grid(alpha=0.25)

    legend = fig.legend(handles=[l1, l2, l3], loc="upper center", ncol=1,
                         frameon=True, framealpha=0.92,
                         bbox_to_anchor=(0.5, 1.13),
                         bbox_transform=ax.transAxes)
    for text in legend.get_texts():
        text.set_fontproperties(FP["regular"])
        text.set_fontsize(LEGEND_FS)

    plt.tight_layout()
    plt.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close(fig)


make_figure(block_labels, block_privacy, block_ssim, block_psnr,
            "Block Size (px)",
            "/mnt/user-data/outputs/privacy_score_block.png")

make_figure(blur_labels, blur_privacy, blur_ssim, blur_psnr,
            "Gaussian Blur sigma",
            "/mnt/user-data/outputs/privacy_score_blur.png")

print("saved.")
