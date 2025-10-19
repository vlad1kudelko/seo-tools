import csv
import sys

# для кластеризации ключей
# на основе выгрузки Ahrefs

def main(file):
    res = ''
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
                curl = row['Current URL']
                if curl == '':
                    curl = row['Previous URL']
                if curl not in cluster:
                    cluster[curl] = []
                cluster[curl].append({
                    'Keyword':  row['Keyword'],
                    'Volume':   row['Volume'],
                    'KD':       row['KD'],
                    'traffic':  row['Current organic traffic'],
                })
                count += 1
        res += str(count)
        for url, rows in cluster.items():
            res += '\n'
            res += str([url]) + '\n'
            for row in rows:
                res += (' '*4 + ' '.join([
                    'V: '  + row['Volume' ].rjust(4, '_'),
                    'KD: ' + row['KD'     ].rjust(4, '_'),
                    'T: '  + row['traffic'].rjust(4, '_'),
                    'K: '  + row['Keyword'],
                ]) + '\n')
        return res

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python main.py <file>')
        sys.exit(1)
    else:
        print_str = main(sys.argv[1])
        with open('out.txt', 'w') as f:
            f.write(print_str)
