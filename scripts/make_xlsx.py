"""Write data/mjepa_japan_schedule.xlsx from the CSV files.

Standard library only (no openpyxl): an .xlsx file is a zip of XML parts.
Run from the repository root:  python3 scripts/make_xlsx.py
"""
import csv
import zipfile
from xml.sax.saxutils import escape

SHEETS = [
    ('README', None),
    ('hs6', 'data/mjepa_japan_schedule_hs6.csv'),
    ('schedule_rows', 'data/mjepa_japan_schedule_rows.csv'),
    ('categories', 'data/categories.csv'),
]
README_ROWS = [
    ['MJEPA (2006): Schedule of Japan, parsed to HS6'],
    ['Source', 'Japan - Schedule of Tariff Commitments, MJEPA Annex 1 Part 2 '
               '(MITI Malaysia copy): https://fta.miti.gov.my/miti-fta/resources/'
               'Malaysia-Japan/Japan_-_Schedule_of_Tariff_Commitments.pdf'],
    ['Sheet hs6', 'One row per HS 2002 six-digit code (5,223 codes): the '
                  'schedule row that sets its category and the category(ies).'],
    ['Sheet schedule_rows', 'Every category row parsed from the schedule '
                            '(chapter, heading or HS6 level), with PDF page.'],
    ['Sheet categories', 'Meaning of each staging category (General Notes).'],
    ['Documentation', 'See README.md in the repository.'],
]


def col(n):
    s = ''
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def sheet_xml(rows):
    out = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
           '<worksheet xmlns="http://schemas.openxmlformats.org/'
           'spreadsheetml/2006/main"><sheetData>']
    for i, row in enumerate(rows, 1):
        cells = []
        for j, v in enumerate(row, 1):
            ref = f'{col(j)}{i}'
            if v is None or v == '':
                continue
            cells.append(f'<c r="{ref}" t="inlineStr"><is><t xml:space='
                         f'"preserve">{escape(str(v))}</t></is></c>')
        out.append(f'<row r="{i}">{"".join(cells)}</row>')
    out.append('</sheetData></worksheet>')
    return ''.join(out)


def main():
    data = []
    for name, path in SHEETS:
        rows = README_ROWS if path is None else \
            list(csv.reader(open(path, encoding='utf-8')))
        data.append((name, rows))
    ns = 'http://schemas.openxmlformats.org'
    with zipfile.ZipFile('data/mjepa_japan_schedule.xlsx', 'w',
                         zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml',
                   '<?xml version="1.0" encoding="UTF-8"?>'
                   f'<Types xmlns="{ns}/package/2006/content-types">'
                   '<Default Extension="rels" ContentType="application/'
                   'vnd.openxmlformats-package.relationships+xml"/>'
                   '<Default Extension="xml" ContentType="application/xml"/>'
                   '<Override PartName="/xl/workbook.xml" ContentType="'
                   'application/vnd.openxmlformats-officedocument.'
                   'spreadsheetml.sheet.main+xml"/>' +
                   ''.join(f'<Override PartName="/xl/worksheets/sheet{i}.xml"'
                           ' ContentType="application/vnd.openxmlformats-'
                           'officedocument.spreadsheetml.worksheet+xml"/>'
                           for i in range(1, len(data) + 1)) + '</Types>')
        z.writestr('_rels/.rels',
                   '<?xml version="1.0" encoding="UTF-8"?>'
                   f'<Relationships xmlns="{ns}/package/2006/relationships">'
                   '<Relationship Id="rId1" Type="http://schemas.'
                   'openxmlformats.org/officeDocument/2006/relationships/'
                   'officeDocument" Target="xl/workbook.xml"/>'
                   '</Relationships>')
        z.writestr('xl/workbook.xml',
                   '<?xml version="1.0" encoding="UTF-8"?>'
                   f'<workbook xmlns="{ns}/spreadsheetml/2006/main" '
                   'xmlns:r="http://schemas.openxmlformats.org/'
                   'officeDocument/2006/relationships"><sheets>' +
                   ''.join(f'<sheet name="{n}" sheetId="{i}" r:id="rId{i}"/>'
                           for i, (n, _) in enumerate(data, 1)) +
                   '</sheets></workbook>')
        z.writestr('xl/_rels/workbook.xml.rels',
                   '<?xml version="1.0" encoding="UTF-8"?>'
                   f'<Relationships xmlns="{ns}/package/2006/relationships">' +
                   ''.join(f'<Relationship Id="rId{i}" Type="http://schemas.'
                           'openxmlformats.org/officeDocument/2006/'
                           'relationships/worksheet" Target="worksheets/'
                           f'sheet{i}.xml"/>' for i in range(1, len(data) + 1))
                   + '</Relationships>')
        for i, (_, rows) in enumerate(data, 1):
            z.writestr(f'xl/worksheets/sheet{i}.xml', sheet_xml(rows))
    print('wrote data/mjepa_japan_schedule.xlsx')


if __name__ == '__main__':
    main()
