from matplotlib import pyplot, ticker
savePngPath = "./graphic.png"
def createGraphics(groupedDictionary):
    fig, axes = pyplot.subplots(nrows=1, ncols=2, figsize=(20, 10))

    listToGraphic = []
    for key in groupedDictionary:
        dates = [record[0] for record in groupedDictionary[key]]
        buy = [record[3] for record in groupedDictionary[key]]
        sale = [record[4] for record in groupedDictionary[key]]
        listToGraphic.append([dates,key[0], key[1], buy, sale])
        # axes[index % 2].plot(dates, buy, label=f"{key[0]}{key[1]} Buy")
        # axes[index % 2].plot(dates, sale, label=f"{key[0]}{key[1]} Sale")

    for lst in listToGraphic:
        if lst[2] == "USD":
            index = 0
        else:
            index = 1
        axes[index].plot(lst[0], lst[3], label = f"{lst[1]} Buy")
        axes[index].plot(lst[0], lst[4], label = f"{lst[1]} Sale")

    for ax in axes:
        ax.grid()
        ax.set_xlabel("Dates")
        ax.set_ylabel("Values")
        ax.tick_params(axis='x', rotation=45)

    axes[0].set_title("USD")
    axes[1].set_title("EUR")

    handles = []
    labels = []
    for ax in axes:
        h, l = ax.get_legend_handles_labels()
        handles.extend(h)
        labels.extend(l)

    unique_labels_map = dict(zip(labels, handles))
    final_labels = unique_labels_map.keys()
    final_handles = unique_labels_map.values()

    fig.legend(
        final_handles,
        final_labels,
        loc='lower center',  # Position of the anchor point on the legend
        bbox_to_anchor=(0.5, 0.05),  # Coordinates for the anchor point (x, y)
        frameon=True
    )
    pyplot.subplots_adjust(bottom=0.2)


def showFigure():
    pyplot.show()
def saveFigure():
    pyplot.show()
    path = input("Enter path where save graphic: ")
    pyplot.savefig(path)
