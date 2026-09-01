import matplotlib.pyplot as plt

def save_curve(
        x,
        y,
        title,
        filename,
        ylabel="Température (°C)"
):

    plt.figure(figsize=(8,5))

    plt.plot(x, y, lw=2)

    plt.grid(True)

    plt.title(title)

    plt.xlabel("Temps (min)")
    plt.ylabel(ylabel)

    plt.tight_layout()

    plt.savefig(filename)

    plt.close()