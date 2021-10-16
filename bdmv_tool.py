#!/usr/bin/env python3
import argparse, logging, os, shutil


length_offset = 0x0C
length_sizeof = 4 # bytes
min_length = length_offset + length_sizeof
endianness = 'big'
index_name = 'index.bdmv'
backup_name = 'BACKUP'
end_bytes = bytearray([
  # 00    01    02    03    04    05    06    07    08    09    0A    0B    0C    0D    0E    0F 
  0x00, 0x00, 0x00, 0x18, 0x00, 0x00, 0x00, 0x18, 0x00, 0x00, 0x00, 0x01, 0x10, 0x00, 0x01, 0x00,
  0x00, 0x00, 0x00, 0x18, 0x00, 0x00, 0x00, 0x00
])


def process_data(data):
  length = len(data)
  assert length >= min_length

  stored_length = int.from_bytes(
    data[length_offset:length_offset+length_sizeof],
    endianness
  )

  if (stored_length == 0):
    logging.info('Length bytes from 0x0C to 0x0F are all 0x00, writing file length and '
                 'appending special end bytes')
    length_as_bytes = length.to_bytes(length_sizeof, endianness)

    data[length_offset:length_offset+length_sizeof] = length_as_bytes
    data += end_bytes

    return data
  else:
    logging.info('Length bytes are set, verifying file structure')
  
    if (stored_length < min_length):
      logging.error('Stored length %d less than minimum length %d', stored_length, min_length)
    elif (stored_length > length):
      logging.error('Stored length %d greater than file length %d', stored_length, length)      
    elif (length != stored_length + len(end_bytes)):
      logging.warning('File has contains %d bytes beyond stored length offset, but %d were '
                      'expected', length - stored_length, len(end_bytes))
    elif (data[-len(end_bytes):] != end_bytes):
      logging.error('Last %d bytes do not match expected end bytes', len(end_bytes))

    return None


def process_index(index):
  with open(index, 'rb') as f:
    data = bytearray(f.read())
    if (len(data) < min_length):
      logging.error('File length less than minimum length %d', min_length) 
      return

  processed_data = process_data(data)
  if (processed_data):
    with open(index, 'wb') as f:
      f.write(data)


def process_bdmv(bdmv):
  with os.scandir(bdmv) as entries:
    index = None
    backup = None
    for entry in entries:
      if entry.name == index_name:
        index = entry.path
      elif entry.name == backup_name:
        backup = entry.path

    if not index:
      logging.error('No %s file found', index_name)
      return

    if not backup:
      logging.info('Creating backup directory')      
      backup = os.path.join(bdmv, backup_name)
      os.makedirs(backup)

    backup_index = None
    with os.scandir(backup) as backup_entries:
      for entry in backup_entries:
        if entry.name == index_name:
          backup_index = entry.path

    if not backup_index:
      logging.info('Copying index to backup')      
      shutil.copy(index, os.path.join(backup, index_name))

    process_index(index)


def process_top_dir(directory):
  with os.scandir(directory) as entries:
    for entry in entries:
      if entry.name == 'AVCHD':
        process_top_dir(entry.path)
      if entry.name == 'BDMV':
        process_bdmv(entry.path)


def main():
  parser = argparse.ArgumentParser(description='Modify BDMV backups to be playable in Oppo file browser')
  parser.add_argument('dirs', metavar='DIR', type=str, nargs='+',
                      help='Directories to process, contain a BDMV or AVCHD/BDMV subdirectory')
  parser.add_argument('--verbose', '-v', action='store_true')
  args = parser.parse_args()
  for d in args.dirs:
    level = logging.INFO if args.verbose else logging.WARNING
    logging.basicConfig(level=logging.INFO, format='[{}]: %(levelname)s: %(message)s'.format(d))
    process_top_dir(d)


if __name__ == '__main__':
  main()

      
