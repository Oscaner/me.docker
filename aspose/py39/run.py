import jpype
jpype.startJVM()

import os
import gc
from pathlib import Path
from natsort import natsorted
import aspose.words as aw
import aspose.slides as slides
import asposecells.api as cells

aw.License().set_license(os.getenv('AW_LIC', ''))

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
    if from_path.suffix in ['.pptx', '.ppt']:
      presentation = slides.Presentation(str(from_path))
      presentation.save(to_path, slides.export.SaveFormat[TO_EXT.upper()])
    if from_path.suffix in ['.xlsx', '.xls']:
      workbook = cells.Workbook(str(from_path))
      workbook.save(to_path, cells.SaveFormat['MARKDOWN' if TO_EXT == 'md' else TO_EXT.upper()])
    else:
      doc = aw.Document(str(from_path))
      doc.save(to_path)
  except Exception as err:
    print(f'❌ {to_path}: {err}')
    continue

  if TO_EXT == 'md':
    file = open(to_path, mode='r')
    lines = file.readlines()[1:]
    lines = [line for line in lines if 'Evaluation Only. Created with Aspose' not in line]
    lines = [line for line in lines if 'Created with an evaluation copy of Aspose' not in line]
    file.close()

    file = open(to_path, mode='w')
    file.writelines(lines)
    file.close()

    del file, lines

  # delete aspose logo
  aspose_logo = to_path.replace(f".{TO_EXT}", '.001.png')
  if os.path.exists(aspose_logo):
    os.remove(aspose_logo)

  print(f'✅ {to_path}')

  # free memory every 5 files
  if from_index % 5 == 0:
    gc.collect()

jpype.shutdownJVM()
