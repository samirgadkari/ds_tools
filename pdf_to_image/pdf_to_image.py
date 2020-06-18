'''
This is just a quick-and-dirty code to
convert a pdf file into a PNG file.
It will not work for Windows
since the path separator is different.
For that I would need path/pathlib.
I will leave that for another day,
as I need this now.
'''
import sys
from pdf2image import convert_from_path


if __name__ == "__main__":

    try:
        filename = sys.argv[1]
    except IndexError:
        raise SystemExit(f'Usage: python {sys.argv[0]} path_to_pdf_file')

    images = convert_from_path(filename)
    parts = filename.split('/')
    out_filename = parts[-1].split('.')[0] + '.' + 'PNG'
    out_filename = '/'.join(parts[:-1]) + '/' + out_filename
    print(out_filename)
    images[0].save(out_filename, 'PNG')
