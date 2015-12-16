import csv, psycopg2
from datetime import datetime

def load_autohome():
    conn = psycopg2.connect(host='192.168.20.30', user='dbadm', database='crawler', password='P@ssw0rd')
    cur = conn.cursor()

    cur.execute('''drop table if exists autohome''')

    cur.execute('''
            create table autohome (
                post_ts       timestamp,
                author        varchar(32),
                title         varchar(300),
                content       varchar(30000),
                url           varchar(120)
            )'''
               )

    cur.execute('''create index on autohome (post_ts)''')
    cur.execute('''create index on autohome (author)''')
    cur.execute('''create index on autohome (title)''')
    cur.execute('''create index on autohome (url)''')
    
    autohome_csv_reader = csv.reader(open('autohome.csv'))
    
    for row in autohome_csv_reader:
        cur.execute('''insert into autohome values (
            %s,
            %s,
            %s,
            %s,
            %s
        )''', (
            datetime.strptime(row[0], '%Y%m%d%H%M%S'),
            # author
            row[1],
            # title
            row[2],
            # content
            row[3],
            # url
            row[4]
        ))

    conn.commit()
    cur.close()
    
    conn.close()
    
if __name__ == '__main__':
    load_autohome()