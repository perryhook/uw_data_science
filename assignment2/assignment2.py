def write_answer(problem, answer):
    directory = 'answers'
    filename = 'problem_' + str(problem) + '.txt'
    path = directory + '/' + filename
    with open(path, 'w') as f:
        f.write(answer)


def problem_1a(conn):
    c = conn.cursor()
    c.execute(
        '''
        SELECT count(*)
        FROM Frequency
        WHERE docid='10398_txt_earn'
        ;
        ''')
    answer = c.fetchone()[0]
    print answer
    return str(answer)


def problem_1b(conn):
    c = conn.cursor()
    c.execute(
        '''
        SELECT count(term)
        FROM Frequency
        WHERE docid='10398_txt_earn' and count=1
        ;
        ''')
    answer = c.fetchone()[0]
    print answer
    return str(answer)


def problem_1c(conn):
    c = conn.cursor()
    c.execute(
        '''
        SELECT count(term)
        FROM (
          SELECT term
          FROM Frequency
          WHERE docid='10398_txt_earn' and count=1

          UNION

          SELECT term
          FROM Frequency
          WHERE docid='925_txt_trade' and count=1
        ) x
        ;
        ''')
    answer = c.fetchone()[0]
    print answer
    return str(answer)


def problem_1d(conn):
    c = conn.cursor()
    c.execute(
        '''
        SELECT count(docid)
        FROM Frequency
        WHERE term='parliament'
        ;
        ''')
    answer = c.fetchone()[0]
    print answer
    return str(answer)


def problem_1e(conn):
    c = conn.cursor()
    c.execute(
        '''
        SELECT count(*)
        FROM (
            SELECT docid
            FROM Frequency
            GROUP BY docid
            HAVING sum(count) > 300
        ) x
        ;
        ''')
    answer = c.fetchone()[0]
    print answer
    return str(answer)


def problem_1f(conn):
    # see alternate answer below
    c = conn.cursor()
    c.execute(
        '''
        SELECT count(y.docid) FROM
            (SELECT x.docid FROM
                (SELECT docid, term FROM Frequency WHERE docid in
                    (SELECT docid FROM Frequency WHERE term='world')
                ) x
            WHERE term='transactions'
            ) y
        ;
        ''')
    answer = c.fetchone()[0]
    print answer
    return str(answer)


def problem_1f_alt(conn):
    c = conn.cursor()
    c.execute(
        '''
        SELECT count(*) FROM
            (SELECT x.docid FROM
                (SELECT docid FROM Frequency WHERE term='world') x,
                (SELECT docid FROM Frequency WHERE term='transactions') y
            WHERE x.docid=y.docid) xy
        ;
        ''')
    answer = c.fetchone()[0]
    print answer
    return str(answer)


def problem_2(conn):
    c = conn.cursor()
    c.execute(
        '''
        SELECT x.value
        FROM (
            SELECT A.row_num, B.col_num, SUM(A.value * B.value) as value
            FROM A, B
            WHERE A.col_num = B.row_num
            GROUP BY A.row_num, B.col_num
        ) x
        WHERE x.row_num=2 AND x.col_num=3
        ;
        ''')
    answer = c.fetchone()[0]
    print answer
    return str(answer)


def problem_3h(conn):
    c = conn.cursor()
    c.execute(
        '''
        SELECT similarity
        FROM (
            SELECT
                F.docid AS F_docid,
                Ft.docid AS Ft_docid,
                SUM(F.count * Ft.count) AS similarity
            FROM Frequency AS F, Frequency AS Ft
            WHERE F.term = Ft.term AND F.docid < Ft.docid
            GROUP BY F.docid, Ft.docid
        )
        WHERE F_docid='10080_txt_crude' AND Ft_docid='17035_txt_earn'
        ;
        ''')
    answer = c.fetchone()[0]
    print answer
    return str(answer)


def problem_3i(conn):
    c = conn.cursor()
    c.execute(
        '''
        CREATE VIEW IF NOT EXISTS kw_query AS
            SELECT * FROM Frequency
            UNION
            SELECT 'q' as docid, 'washington' as term, 1 as count
            UNION
            SELECT 'q' as docid, 'taxes' as term, 1 as count
            UNION
            SELECT 'q' as docid, 'treasury' as term, 1 as count
        ;
        ''')
    c.execute(
        '''
        SELECT max(similarity) FROM (
            SELECT
                F.docid AS F_docid,
                Ft.docid AS Ft_docid,
                SUM(F.count * Ft.count) AS similarity
            FROM kw_query AS F, kw_query AS Ft
            WHERE F.term = Ft.term AND F.docid < Ft.docid
            GROUP BY F.docid, Ft.docid
        )
        WHERE Ft_docid='q'
        ;
        ''')
    answer = c.fetchone()[0]
    print answer
    return str(answer)


if __name__ == '__main__':
    import sqlite3

    reuters_conn = sqlite3.connect('reuters.db')
    matrix_conn = sqlite3.connect('matrix.db')

    write_answer('1a', problem_1a(reuters_conn))
    write_answer('1b', problem_1b(reuters_conn))
    write_answer('1c', problem_1c(reuters_conn))
    write_answer('1d', problem_1d(reuters_conn))
    write_answer('1e', problem_1e(reuters_conn))
    write_answer('1f', problem_1f(reuters_conn))
    write_answer('1f_alt', problem_1f_alt(reuters_conn))
    write_answer('2', problem_2(matrix_conn))
    write_answer('3h', problem_3h(reuters_conn))
    write_answer('3i', problem_3i(reuters_conn))
