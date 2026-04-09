
"""
Version: 0.0.2



"""

import pandas as pd
import os
from IPython.display import HTML, display
from src.config import OUTPUT_DIR, SAVE_MODE


def plt_savefig(plt,file_name, html_print = True, plt_show = True):
    plt.tight_layout()
    if SAVE_MODE:
        of = OUTPUT_DIR  / file_name
        plt.savefig(of)
        if html_print is True:
            link = f'<p>✅ picture saved: <a href="{of}" target="_blank">{os.path.basename(of)}</a></p>'
            display(HTML(link))
        else:
            print(f"✅  `{os.path.basename(of)}` as picture saved.")
    if plt_show is True:
        plt.show()


def dataframe_to_markdown(df: pd.DataFrame,
                        print_this = True,
                        table_name = "",
                        write_to_temp_file = True,
                        include_index= False
                        ) -> str:


    if include_index:
        # Reset index name if it's None
        index_name = df.index.name if df.index.name else "Index"
        # Build header with index
        header = '| ' + index_name + ' | ' + ' | '.join(df.columns.astype(str)) + ' |'
        separator = '| ' + '--- |' * (len(df.columns) + 1)
        # Build rows
        rows = df.astype(str).apply(
            lambda row: '| ' + str(row.name) + ' | ' + ' | '.join(row.values) + ' |', axis=1
        )
    else:
        # Create header
        header = '| ' + ' | '.join(df.columns.astype(str)) + ' |'
        # Create separator
        separator = '| ' + ' | '.join(['---'] * len(df.columns)) + ' |'
        # Create data rows
        rows = df.astype(str).apply(lambda row: '| ' + ' | '.join(row) + ' |', axis=1)

    markdown_table = '\n'.join([header, separator] + rows.tolist())


    # Combine all parts
    markdown_table = '\n'.join([header, separator] + rows.tolist())
    if print_this is True:
        print()
        if table_name != "":
            print(table_name)
        print(markdown_table)
        print()

    # for write to temp markdown file
    if write_to_temp_file:
        filename = "bibliometric-result-markdown-table.md"
    with open(filename, "a", encoding="utf-8") as file:
        file.write('\n\n')  # optional spacing between tables
        file.write(table_name)
        file.write('\n') 
        file.write(markdown_table) 
        file.write('\n')       
    return markdown_table

def dataframe_to_csv(df: pd.DataFrame,file_name:str, include_index= False, additional_description = ""):
    if SAVE_MODE:
        of = OUTPUT_DIR / file_name
        df.to_csv(of, index=include_index)
        print(f"✅ `{os.path.basename(of)}` as CSV saved. {additional_description}")

# Function to create a table with auto-sized columns and zebra stripes
def create_table(ax, data, title):
    # Create the table
    table = ax.table(cellText=data.values,
                     colLabels=data.columns,
                     cellLoc='center',
                     loc='center')
    ax.set_title(title, fontsize=16)  # Increased subtitle font size
    ax.axis('off')
    
    # Auto-size columns and set larger font size
    table.auto_set_font_size(False)
    # table.set_fontsize(12)  # Increased font size
    table.set_fontsize(20)  # Increased font size
    table.scale(1, 1.8)  # Adjusted scale for larger cells
    
    # Adjust column widths and add zebra stripes
    for (row, col), cell in table.get_celld().items():
        if row == 0:
            cell.set_text_props(weight='bold', color='white')
            cell.set_facecolor('#4472C4')  # Header color
        else:
            cell.set_facecolor('#D9E1F2' if row % 2 == 0 else 'white')  # Alternating row colors
        cell.set_height(0.1)
        cell._text.set_wrap(True)
    
    # Get the maximum width for each column
    col_widths = [max([len(str(data.iloc[i, j])) for i in range(len(data))] + [len(str(data.columns[j]))]) 
                  for j in range(len(data.columns))]
    
    # Set column widths
    for j, width in enumerate(col_widths):
        table.auto_set_column_width(j)
    
    return table

