# This is a sample Python script.
from band_edge_filter import BandEdgeFilter


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # print_hi('PyCharm')
    band_edge_filter = BandEdgeFilter(16.0, 321, 0.5)
    band_edge_filter.design()
    band_edge_filter.print()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
