import os
import aspose.words as aw
from natsort import natsorted

FROM_EXT = os.getenv('FROM_EXT')
TO_EXT = os.getenv('TO_EXT')

print(f'ENV: FROM [.{FROM_EXT}] TO [.{TO_EXT}]')

from_files = natsorted([
  f for f in os.listdir(f'/workspace/{FROM_EXT}') if f.endswith(f'.{FROM_EXT}')
])

for from_file in from_files:
  to_file = from_file.replace('.' + FROM_EXT, '.' + TO_EXT)

  print(f'⌛️ {from_file}')

  from_path = f'/workspace/{FROM_EXT}/{from_file}'
  to_path = f'/workspace/{TO_EXT}/{to_file}'
  basename = os.path.basename(to_path).replace('.' + TO_EXT, '')

  if os.path.exists(to_path):
    print(f'👉 {to_file} already exists')
    continue

  doc = aw.Document(from_path)
  doc.save(to_path)

  if TO_EXT == 'md':
    file = open(to_path, mode='r')
    lines = file.readlines()
    lines = [line for line in lines if f'![]({basename}.001.png)' not in line]
    lines = [line for line in lines if 'Evaluation Only. Created with Aspose.Words' not in line]
    lines = [line for line in lines if 'Created with an evaluation copy of Aspose.Words' not in line]

    file = open(to_path, mode='w')
    file.writelines(lines)

  print(f'✅ {to_file}')
