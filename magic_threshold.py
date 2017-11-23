from wand.image import Image
from wand.display import display


def convert_pdf(input_path, output_path, threshold=0.47):
    print('Reading file...')
    with Image(filename=input_path, resolution=300) as pdf_input, Image() as pdf_output:
        print('Opened {} with {} pages.'.format(input_path, len(pdf_input.sequence)))
        for i, page in enumerate(pdf_input.sequence):
            print('Processing page {} of {}...'.format(i + 1, len(pdf_input.sequence)))
            with Image(page) as img:
                img.threshold(threshold=threshold, channel='red')
                img.threshold(threshold=threshold, channel='green')
                img.threshold(threshold=threshold, channel='blue')
                pdf_output.sequence.extend([img])
                display(img)

        print('Writing to {}...'.format(output_path))
        pdf_output.save(filename=output_path)

if __name__ == '__main__':
    filenames = [
        'PGM_Sheet01.pdf',
        'PGM_Sheet02.pdf',
        'PGM_Sheet03_Corrections.pdf',
        'PGM_Sheet03.pdf',
        'PGM_Sheet04_Corrections.pdf'
    ]
    for name in filenames:
        convert_pdf('./convert/{}'.format(name), './convert/bin_{}'.format(name))
