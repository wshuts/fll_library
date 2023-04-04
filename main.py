# This is a sample Python script.
from band_edge_filter_verifier import BandEdgeFilterVerifier
from filter import design_filter


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # print_hi('PyCharm')
    design_filter(16, 0.5, 321)
    band_edge_filter = BandEdgeFilterVerifier()
    band_edge_filter.load_coefficients()
    band_edge_filter.de_rotate_coefficients()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
