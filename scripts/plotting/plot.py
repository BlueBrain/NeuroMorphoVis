##/computer/bbp-blender-development/nmv-blender-2.80/Blender-2.80.app/Contents/Resources/2.80/python/bin/python3.7m

import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

#x, y = np.random.randn(2, 1000).cumsum(axis=1)
#ax = sns.lineplot(x=x, y=y, sort=False, lw=2, color="coral")

#x, y = np.random.randn(2, 1000).cumsum(axis=1)
#ax = sns.lineplot(x=x, y=y, sort=False, lw=1, color="red")


directory = '/home/abdellah/neuromorphovis-output/analysis/'

import sys
from PIL import Image

images = [Image.open('%s/%s.TIFF' % (directory, x)) for x in
          ['02b_pyramidal1aACC.CNG-arbor-length',
           '02b_pyramidal1aACC.CNG-arbor-surface-area',
           '02b_pyramidal1aACC.CNG-arbor-volume']]
widths, heights = zip(*(i.size for i in images))

total_width = sum(widths)
max_height = max(heights)

new_im = Image.new('RGB', (total_width, max_height))

x_offset = 0
for im in images:
  new_im.paste(im, (x_offset,0))
  x_offset += im.size[0]

new_im.save('%s/arbor.TIFF' % directory)


images = [Image.open('%s/%s.TIFF' % (directory, x)) for x in
          ['02b_pyramidal1aACC.CNG-sections-length-range-per-arbor',
           '02b_pyramidal1aACC.CNG-sections-surface-area-range-per-arbor',
           '02b_pyramidal1aACC.CNG-sections-volume-range-per-arbor']]
widths, heights = zip(*(i.size for i in images))

total_width = sum(widths)
max_height = max(heights)

new_im = Image.new('RGB', (total_width, max_height))

x_offset = 0
for im in images:
  new_im.paste(im, (x_offset,0))
  x_offset += im.size[0]

new_im.save('%s/section.TIFF' % directory)


images = [Image.open('%s/%s.TIFF' % (directory, x)) for x in
          ['02b_pyramidal1aACC.CNG-segments-length-range-per-arbor',
           '02b_pyramidal1aACC.CNG-segments-surface-area-range-per-arbor',
           '02b_pyramidal1aACC.CNG-segments-volume-range-per-arbor']]
widths, heights = zip(*(i.size for i in images))

total_width = sum(widths)
max_height = max(heights)

new_im = Image.new('RGB', (total_width, max_height))

x_offset = 0
for im in images:
  new_im.paste(im, (x_offset,0))
  x_offset += im.size[0]

new_im.save('%s/segments.TIFF' % directory)

import datetime
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt

# Create the PdfPages object to which we will save the pages:
# The with statement makes sure that the PdfPages object is closed properly at
# the end of the block, even if an Exception occurs.
with PdfPages('%s/multipage_pdf.pdf' % directory) as pdf:

    plt.figure(figsize=(3, 3))
    plt.plot(range(7), [3, 1, 4, 1, 5, 9, 2], 'r-o')
    plt.title('Page One')
    pdf.savefig()  # saves the current figure into a pdf page
    plt.close()

    # if LaTeX is not installed or error caught, change to `usetex=False`
    plt.rc('text', usetex=True)
    plt.figure(figsize=(8, 6))
    x = np.arange(0, 5, 0.1)
    plt.plot(x, np.sin(x), 'b-')
    plt.title('Page Two')
    pdf.attach_note("plot of sin(x)")  # you can add a pdf note to
                                       # attach metadata to a page
    pdf.savefig()
    plt.close()

    plt.rc('text', usetex=False)
    fig = plt.figure(figsize=(4, 5))
    plt.plot(x, x ** 2, 'ko')
    plt.title('Page Three')
    pdf.savefig(fig)  # or you can pass a Figure object to pdf.savefig
    plt.close()

    # We can also set the file's metadata via the PdfPages object:
    d = pdf.infodict()
    d['Title'] = 'Multipage PDF Example'
    d['Author'] = 'Jouni K. Sepp\xe4nen'
    d['Subject'] = 'How to create a multipage pdf file and set its metadata'
    d['Keywords'] = 'PdfPages multipage keywords author title subject'
    d['CreationDate'] = datetime.datetime(2009, 11, 13)
    d['ModDate'] = datetime.datetime.today()