import os
import gc
from pathlib import Path
import aspose.words as aw
from natsort import natsorted

TO_EXT = os.getenv('TO_EXT')

print(f'ENV: FROM source TO [.{TO_EXT}]')

# list all files in source and subfolders
source_files = []
for root, dirs, files in os.walk(f'/workspace/source'):
  for file in files:
    if file.startswith('.'): continue
    source_files.append(os.path.join(root, file))
source_files = natsorted(source_files)

for from_index, from_file in enumerate(source_files):
  from_path = Path(from_file)
  to_path = str(from_path.with_suffix('.' + TO_EXT)).replace('/workspace/source', f'/workspace/{TO_EXT}')

  print(f'⌛️ {from_file}')

  basename = os.path.basename(to_path).replace('.' + TO_EXT, '')

  if os.path.exists(to_path):
    print(f'👉 {to_path} already exists')
    continue

  try:
    doc = aw.Document(str(from_path))
    doc.save(to_path)
  except Exception as err:
    print(f'❌ {to_path}: {err}')
    continue

  if TO_EXT == 'md':
    file = open(to_path, mode='r')
    lines = file.readlines()[1:]
    lines = [line for line in lines if 'Evaluation Only. Created with Aspose.Words' not in line]
    lines = [line for line in lines if 'Created with an evaluation copy of Aspose.Words' not in line]
    file.close()

    file = open(to_path, mode='w')
    file.writelines(lines)
    file.close()

    del file, lines

  print(f'✅ {to_path}')

  # free memory every 5 files
  if from_index % 5 == 0:
    gc.collect()
