import seaborn as sns
import matplotlib.pyplot as plt


def plot_barchart(x, y, color="teal"):
    print("Lott")
    # Create a bar chart using Seaborn
    sns.barplot(x=x, y=y, color=color)

    # Customize the plot
    plt.title("Bar Chart Example")
    plt.xlabel("Date")
    plt.ylabel("Returns")

    # Show the plot
    plt.show()
    print("Lott")
