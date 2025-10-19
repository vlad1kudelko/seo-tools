import csv
import sys

# для кластеризации ключей
# на основе выгрузки Ahrefs

def main(file):
    with open(file, encoding='utf-16') as f:
        reader = csv.reader(f, delimiter='\t')
        count = 0
        cluster = {}
        for key, row in enumerate(reader):
            if key == 0:
                keys = row
            else:
                row = dict(zip(keys, row))
                if row['Country'] != 'RU': continue
                if row['Location'] != 'Russian Federation': continue
                if row['Current URL'] not in cluster:
                    cluster[row['Current URL']] = []
                cluster[row['Current URL']].append({
                    'Keyword':  row['Keyword'],
                    'Volume':   row['Volume'],
                    'KD':       row['KD'],
                    'traffic':  row['Current organic traffic'],
                })
                count += 1
        print(count)
        for url, rows in cluster.items():
            print()
            print([url])
            for row in rows:
                print(' '*4 + ' '.join([
                    'V: '  + row['Volume'] .rjust(4),
                    'KD: ' + row['KD']     .rjust(4),
                    'T: '  + row['traffic'].rjust(4),
                    'K: '  + row['Keyword'],
                ]))

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python main.py <file>')
        sys.exit(1)
    else:
        main(sys.argv[1])
