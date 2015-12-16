import csv, psycopg2
from datetime import datetime

def load_ucar():
    conn = psycopg2.connect(host='192.168.20.30', user='dbadm', database='crawler', password='P@ssw0rd')
    cur = conn.cursor()

    cur.execute('''drop table if exists ucar''')

    cur.execute('''
            create table ucar (
                post_ts       timestamp,
                author        varchar(32),
                title         varchar(300),
                content       varchar(30000),
                url           varchar(120)
            )'''
               )

    cur.execute('''create index on ucar (post_ts)''')
    cur.execute('''create index on ucar (author)''')
    cur.execute('''create index on ucar (title)''')
    cur.execute('''create index on ucar (url)''')
    
    ucar_csv_reader = csv.reader(open('u-car.csv'))
    
    for row in ucar_csv_reader:
        cur.execute('''insert into ucar values (
            %s,
            %s, 
            %s, 
            %s, 
            %s
        )''', (
            datetime.strptime(row[0], '%Y/%m/%d %H:%M:%S'),
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
    load_ucar()
