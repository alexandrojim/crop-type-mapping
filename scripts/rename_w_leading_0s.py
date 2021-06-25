import os
import argparse
import shutil

def rename(old_fname, tif_content, num_digits, dry_run, ftype, country):
    """
    This function assumes that old_fname of tif_content 
      'mask' ends with path/COUNTRY_DIMxDIM_###.tif 
      'data' ends with path/SOURCE_COUNTRY_ORBIT_###_YYYY-MM-DD.tif

    where ### corresponds to a grid ID, and can vary from # to ##### 
    """
    fname_split = old_fname.split('_')
    print(old_fname)

    if tif_content == 'mask':
        if ftype == 'tif':
            assert '.tif' in fname_split[-1]
            fname_split[-1] = fname_split[-1].replace('.tif', '').zfill(num_digits) + '.tif'
        elif ftype == 'npy':
            assert '.npy' in fname_split[-1] or '.json' in fname_split[-1]
            if '.npy' in fname_split[-1]:
                fname_split[-1] = fname_split[-1].replace('.npy', '').zfill(num_digits) + '.npy'
            elif '.json' in fname_split[-1]:
                fname_split[-1] = fname_split[-1].replace('.json', '').zfill(num_digits) + '.json'
    elif tif_content == 'data':
        if country in ['tanzania', 'southsudan', 'ghana']:
            assert fname_split[-3].isdigit()
            fname_split[-3] = fname_split[-3].zfill(num_digits)
        elif country == 'ghana':
            assert fname_split[-2].isdigit()
            fname_split[-2] = fname_split[-2].zfill(num_digits)

    new_fname = '_'.join(fname_split)
    if dry_run:
        print('Renaming {} to {}'.format(old_fname, new_fname))
    else:
        print('Not a dry run!')
        print('Renaming {} to {}'.format(old_fname, new_fname))
        os.rename(old_fname, new_fname)


def get_fnames(directory, ftype):
    """ 
    Returns a list of *.tif filenames given a directory
    """
    print('directory: ', directory)
    if ftype == 'tif':
        return [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.tif')]
    elif ftype == 'npy':
        return [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.npy') or f.endswith('.json')]

def copy_imgs_out(directory, flagCpy):
    if flagCpy:
        dirs4imgs = sorted(os.listdir(directory))
        #print(dirs4imgs)
        dirs4imgs = dirs4imgs[3:]
        #print(dirs4imgs)
        for i in dirs4imgs:
            print(i)
            original = directory + '/' + i + '/labels.tif'
            target = directory + '/alldata/' + i + '.tif'
            shutil.copyfile(original, target)
    else:
        print('Images were copied to alldata/')

def main(directory, tif_content, num_digits, dry_run, ftype, country, flagCpy):
    copy_imgs_out(directory, flagCpy)
    directory = directory + '/alldata'
    fnames = get_fnames(directory, ftype)
    print(fnames[1:5])
    for f in fnames:
        rename(f, tif_content, num_digits, dry_run, ftype, country)    


if __name__ == '__main__':
    """
    Renames grid IDs with leading 0's so that sorting of filenames is in ascending order

    To call on masks,
       python rename_w_leading_0s.py --dir /home/data/COUNTRY/raster --tif_content mask

    To call on data, 
       python rename_w_leading_0s.py --dir /home/data/COUNTRY/SOURCE --tif_content data 
  
    """
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--dir', type=str, default='/home/data/Ghana/s1',
        help='Directory in which to replace grid IDs with leading 0''s')
    parser.add_argument('--dry_run', dest='dry_run', action='store_true')
    parser.add_argument('--num_digits', type=int, default=6,
        help='Number of digits that ID should contain (default: 6). Given default of "6", ID "34" --> "000034"')
    parser.add_argument('--tif_content', type=str, default='data', 
        help='Defines what is contained in the tif (options: "mask", "data")')
    parser.add_argument('--ftype', type=str, default='tif',
        help='Defines type of data you want to rename (options: "tif", "npy")')
    parser.add_argument('--country', type=str, default='ghana',
        help='Country data is from (options: "tanzania", "ghana", "southsudan)')

    parser.add_argument('--flagCpy', dest='flagCpy', action='store_true',
        help='Copy images from each labeled folder to the directory and change its name.')

    args = parser.parse_args()

    main(args.dir, args.tif_content, args.num_digits, args.dry_run, args.ftype, args.country, args.flagCpy)

