```python
from datetime import datetime
from collections import defaultdict
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch

def generate_invoice_pdf(work_entries, daily_rate, client_name="[Client Name]", project_name="Mwala cluster water project (transmission line)"):
    """Generates a PDF invoice based on the work entries and daily rate."""

    doc = SimpleDocTemplate("invoice.pdf", pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # --- Header Information ---
    ptext = f"**INVOICE**"
    story.append(Paragraph(ptext, styles['h1']))
    story.append(Spacer(1, 0.2 * inch))

    ptext = f"**Invoice To:** {client_name}"
    story.append(Paragraph(ptext, styles['normal']))
    ptext = f"**Project:** {project_name}"
    story.append(Paragraph(ptext, styles['normal']))
    ptext = f"**Invoice Date:** {datetime.now().strftime('%d/%m/%Y')}"
    story.append(Paragraph(ptext, styles['normal']))
    ptext = f"**Payment Terms:** Due upon receipt"
    story.append(Paragraph(ptext, styles['normal']))
    ptext = f"**Currency:** KES"
    story.append(Paragraph(ptext, styles['normal']))
    story.append(Spacer(1, 0.4 * inch))

    # --- Calculate Totals and Prepare Data for Table ---
    unique_dates = {entry[0] for entry in work_entries}
    num_days = len(unique_dates)
    total_amount = num_days * daily_rate

    daily_summary = defaultdict(list)
    for date_str, description in work_entries:
        date_obj = datetime.strptime(date_str, "%d/%m/%y")
        daily_summary[date_obj].append(description)

    sorted_summary = sorted(daily_summary.items())

    table_data = [["Date", "Description", "Rate (KES)", "Days", "Amount (KES)"]]
    for date, descriptions in sorted_summary:
        description_text = "\n".join(descriptions)
        table_data.append([
            date.strftime("%d/%m/%Y"),
            Paragraph(description_text, styles['normal']),
            f"{daily_rate:,.2f}",
            "1",
            f"{daily_rate:,.2f}"
        ])

    table_data.append(["", "", "", "**Total**", f"**{total_amount:,.2f}**"])

    # --- Create the Table ---
    table = Table(table_data, colWidths=[1 * inch, 3 * inch, 1 * inch, 0.7 * inch, 1 * inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(table)
    story.append(Spacer(1, 0.4 * inch))

    # --- Notes Section ---
    ptext = "**Notes:** Thank you for your business."
    story.append(Paragraph(ptext, styles['normal']))

    doc.build(story)
    print("Invoice generated successfully as 'invoice.pdf'")

# --- Define your data ---
daily_rate = 10000
work_entries = [
    ("26/4/25", "6 joints for 225mm pipes"),
    ("28/4/25", "7 joints for 225mm pipes, 2 joints for 90mm"),
    ("29/4/25", "2 joints reducer for 110mm to 90mm, 4 joints for 225mm pipes"),
    ("30/4/25", "6 joints for 225mm pipes"),
    ("1/5/25", "3 joints for 225mm pipes"),
    ("2/5/25", "5 joints for 225mm pipes"),
    ("3/5/25", "1 joint for 90mm, 2 joints for 225mm pipes"),
    ("5/5/25", "1 joint for 225mm pipes, 1 joint for 110mm pipes, joints for 160mm pipes"),
    ("6/5/25", "4 joints for 160mm pipes, 3 t joints for 225mm pipes"),
    ("7/5/25", "8 joints for 160mm pipes, 3 joints for 225mm pipes"),
    ("8/5/25", "6 joints for 160mm pipes, 2 joints for reducer 160mm to 110mm, 2 joints for 110mm pipes"),
    ("9/5/25", "5 joints for 110mm pipes"),
    ("10/5/25", "5 joints for 110mm pipes"),
    ("13/5/25", "4 joints for 110mm pipes"),
    ("14/5/25", "6 joints for 110mm pipes"),
    ("15/5/25", "3 joints for 110mm pipes"),
]

# --- Generate the PDF Invoice ---
generate_invoice_pdf(work_entries, daily_rate, client_name="[Client Name]", project_name="Mwala cluster water project (transmission line)")
```

**Explanation:**

1.  **Import Libraries:**
    * `datetime`: For handling dates.
    * `defaultdict`: For easily grouping work entries by date.
    * `reportlab.lib.pagesizes`: To define the page size for the PDF (letter size is common).
    * `reportlab.platypus`: Provides building blocks for creating PDF documents like `SimpleDocTemplate`, `Table`, `Paragraph`, and `Spacer`.
    * `reportlab.lib.styles`: To access predefined text styles.
    * `reportlab.lib`: Contains constants for colors and units.

2.  **`generate_invoice_pdf` Function:**
    * Takes `work_entries`, `daily_rate`, `client_name`, and `project_name` as arguments.
    * **Creates a PDF Document:** `SimpleDocTemplate("invoice.pdf", pagesize=letter)` initializes a PDF document named "invoice.pdf".
    * **Gets Styles:** `getSampleStyleSheet()` provides a set of standard text styles.
    * **`story` List:** This list will hold the elements (paragraphs, tables, etc.) that will be added to the PDF.
    * **Header Information:** Creates paragraphs with bold text for the invoice title, "Invoice To," "Project," "Invoice Date," "Payment Terms," and "Currency." Spacers are used to add vertical space.
    * **Calculate Totals and Prepare Table Data:**
        * Calculates the number of unique workdays and the total amount due (same logic as the previous script).
        * Groups work descriptions by date.
        * Creates `table_data` as a list of lists, which will be used to build the table in the PDF. The header row and rows for each workday are added.
        * A "Total" row is appended to the `table_data`.
    * **Create the Table:**
        * `Table(table_data, colWidths=...)` creates a table with the calculated data and sets the width for each column.
        * `TableStyle()` is used to define the appearance of the table (background colors, text colors, alignment, font, padding, grid lines).
        * The styled table is appended to the `story`.
    * **Notes Section:** Adds a "Notes" paragraph at the end.
    * **Build the PDF:** `doc.build(story)` processes the elements in the `story` list and generates the PDF file.
    * Prints a success message.

3.  **Define Data:** The `daily_rate` and `work_entries` list are defined as in your previous script.

4.  **Generate the PDF:** The `generate_invoice_pdf` function is called with your data.

**To run this code:**

1.  **Install `reportlab`:** If you don't have it installed, open your terminal or command prompt and run:
    ```bash
    pip install reportlab
    ```
2.  **Save the code:** Save the Python code as a `.py` file (e.g., `generate_invoice.py`).
3.  **Run the script:** Execute the script from your terminal:
    ```bash
    python generate_invoice.py
    ```

This will create a PDF file named `invoice.pdf` in the same directory where you saved the Python script. This PDF will contain a basic invoice with the work summary and the total amount due. You can further customize the layout and styling of the PDF by exploring the options available in the `reportlab` library.
Citations: [[1]](https://stackoverflow.com/questions/77808628/html-page-with-graphs-and-charts-through-python), [[2]](https://github.com/7MohamedAshraf10/Daily_Planner), [[3]](https://github.com/RonVol/Auto-Defense-ML)
