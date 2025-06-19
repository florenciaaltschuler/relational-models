import os
import matplotlib.pyplot as plt
import seaborn as sns

import utils

sns.set_context("talk")


def plot_hist(arr_vals, n_bins, title, xlabel, ylabel, show=False, save_fn=None):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(arr_vals, bins=n_bins, color="skyblue", edgecolor="black")
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.tight_layout()
    if save_fn is not None:
        save_fp = os.path.join(utils.PLOTS_DIRPATH_, save_fn)
        plt.savefig(save_fp)
        print(f'Saved plot to "{save_fp}".')
    if show:
        plt.show()
    plt.close(fig)


def plot_pie(arr_vals, arr_labels, title, show=False, save_fn=None):
    fig, ax = plt.subplots(figsize=(10, 6))
    wedges, text_labels, autotexts = ax.pie(
        arr_vals, labels=arr_labels, autopct="%1.1f%%", startangle=140
    )
    for at in autotexts:
        at.set_fontsize(10)

    ax.set_title(title)
    plt.tight_layout()
    if save_fn is not None:
        save_fp = os.path.join(utils.PLOTS_DIRPATH_, save_fn)
        plt.savefig(save_fp)
        print(f'Saved plot to "{save_fp}".')
    if show:
        plt.show()
    plt.close(fig)


def plot_barh(y_vals, w_vals, title, xlabel, color="salmon", show=False, save_fn=None):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(y_vals, w_vals, color=color)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    plt.tight_layout()
    if save_fn is not None:
        save_fp = os.path.join(utils.PLOTS_DIRPATH_, save_fn)
        plt.savefig(save_fp)
        print(f'Saved plot to "{save_fp}".')
    if show:
        plt.show()
    plt.close(fig)
