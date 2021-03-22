import streamlit as st
import mysql.connector
from mysql.connector import Error

from datetime import datetime

def main():
    # title = st.text_input('book title') # 입력행 수 제한
    # st.write(title)

    # author_fname =st.text_input('author frist name') # 입력행 수 제한
    # st.write(author_fname)

    # author_lname = st.text_input('author last name') # 입력행 수 제한
    # st.write(author_lname)

    # released_year = st.number_input('released year',1)
    # st.write(released_year)

    # stock_quantity = st.number_input('stock quantity',1)
    # st.write(stock_quantity)

    # pages = st.number_input('page',1)
    # st.write(pages)

    # name = st.text_input(' Name ')
    # birthdate = st.date_input('birth day')
    # birthtime = st.time_input('birth time')
    # birthdt = datetime.combine(birthdate, birthtime)
    # print(type(birthdate))
    # print(type(birthtime))

    released_year = st.number_input('년도 입력', 1800, 2050)
    pages = st.number_input('페이지 수 입력',1,500)
   
    if st.button('조회'):
        try :
            # 1. 커넥터로부터 커넥션을 받는다.
            connection = mysql.connector.connect(
                host ='database-2.cumcickeiqsl.ap-northeast-2.rds.amazonaws.com', #Hostname = RDS엔드포인트
                user = 'streamlit',
                password = 'yh1234',
                database = 'yhdb'
            )

            if connection.is_connected():
                print('connection 완료')
                db_info = connection.get_server_info()
                print('MySQL server version : ', db_info)
            
                # 2. 커서를 가져온다.
                cursor = connection.cursor() #   하이퍼파라미터 dictionary=True 딕셔너리형태 
                # 3. 우리가 원하는거 실행 가능 !!!!!!!!!!!!
                
                query = '''select * from books;'''
                cursor.execute(query)

                # 입력할 때
                # record =[('냐옹이', 1), ('나비', 3),('단비', 5)] #튜플로 묶어 줌
                # cursor.execute(query, record) 
                # cursor.executemany(query, record) # 파이선에서  sql로 입력할때
                # connection.commit()  #  데이터베이스에 영구저장하라

                print('{}개 적용됨'.format(cursor.rowcount))

                # 4. 실행 후 커서에서 결과를 빼낸다.
                results = cursor.fetchall()
                print(results)

                for data in results :
                    print(data[1], data[4])                 
                # record = cursor.fetchone()
                # print('connected to DB : ',record)

                cursor = connection.cursor(dictionary=True)
                query = ''' select title, released_year, pages
                            from books
                            where released_year > %s and pages > %s 
                            order by released_year desc'''
                # released_year = 2005
                # pages = 400
                    
                param = (released_year, pages) 
                cursor.execute(query, param)
                result = cursor.fetchall()
                
                
                for data in result :
                    print(data)
                    st.write(data)

        except Error as e : 
            print('디비관련 에러 발생', e)
            
        finally :
            # 5. 모든 데이터베이스 실행 명령을 전부 끝냈으면, 
            #   커서와 커넥션을 모두 닫아준다. 
            cursor.close()
            connection.close()
            print('MySQL 커넥션 종료')
        st.write('완료.')


if __name__ =='__main__':
    main()
