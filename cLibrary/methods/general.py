import os
import pandas as pd
from typing import List, Tuple, Set, Optional


def open_excel(file_path, output=None):
    """
    open most recently created excel doc
    :return: None (prints update to Output console)
    """
    try:
        output.r_insert("Opening file...") if output is not None else 'pass'
        output.update()
        assert file_path is not None, "ObjectError: No consolidations run yet"
        os.system('start excel.exe "{}"'.format(file_path))
    except AssertionError as e:
        output.r_insert(e) if output is not None else AssertionError(e)


def create_xlsx(data: List, cols: List, outfile: str) -> str:
    """
    create a xlsx file
    :param data: sheet data
    :param cols: sheet columns
    :param outfile: output location
    :return: outfile string
    """
    outfile = xlsx_ft(outfile)
    df1 = pd.DataFrame(data, columns=cols)
    writer = pd.ExcelWriter(outfile)
    df1.to_excel(writer, 'Sheet1')
    writer.save()
    return outfile


def data_to_dataframe(data: List, cols: List, sheet_name=None) -> Tuple[Optional[str], pd.DataFrame]:
    df = pd.DataFrame(data, columns=cols)
    if sheet_name is not None:
        sheet_name = sheet_name.replace('/', '.')
    return sheet_name, df


def dataframes_to_xlsx(dfs: List[Tuple[Optional[str], pd.DataFrame]], outfile: str) -> str:
    writer = pd.ExcelWriter(xlsx_ft(outfile))
    for i, df in enumerate(dfs):
        sheet_name = str(df[0]) if df[0] is not None else ('Sheet_' + str(i + 1))
        df[1].to_excel(writer, sheet_name)
    writer.save()
    return outfile


def intersperse(lst, item=""):
    """
    intersperse a list with a set character
    :param lst: list to intersperse
    :param item: character to intersperse with
    :return: resulting list
    """
    result = [item] * (len(lst) * 2)
    result[0::2] = lst
    return result


def center_to_screen(window, adj=0) -> None:
    """
    Set a Tk window to the centre of the screen
    :param window: Tk or Toplevel object
    :param adj: amount to adjust vertically
    :return: None
    """
    width = window.winfo_reqwidth()
    height = window.winfo_reqheight()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2) - adj
    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))


def center_to_win(window, master) -> None:
    """
    Set window to the center of another window
    :param window: Tk or Toplevel object to set location
    :param master: Tk or Toplevel to center on
    :return: None
    """
    window.update()
    x = master.winfo_x()
    y = master.winfo_y()
    w = window.winfo_reqwidth()
    h = window.winfo_reqheight()
    total_x = x + (master.winfo_width() // 2) - (w // 2)
    total_y = y + (master.winfo_height() // 2) - (h // 2)
    window.geometry("%dx%d+%d+%d" % (int(w), int(h), int(total_x), int(total_y)))


def relocate_window(window, x, y) -> None:
    """
    relocate windows
    :param window: Tk or Toplevel for relocation
    :param x: x pos to move to
    :param y: y pos to move to
    :return: None
    """
    window.geometry("%dx%d+%d+%d" % (int(window.winfo_width()), int(window.winfo_height()), int(x), int(y)))


def flatten_list_of_lists(list_of_lists):
    return [inner for outer in list_of_lists for inner in outer]


def xlsx_ft(filepath: str) -> str:
    if len(filepath) < 5 or filepath[-5:] != ".xlsx":
        return filepath + '.xlsx'
    else:
        return filepath
