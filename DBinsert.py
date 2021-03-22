import streamlit as st
import mysql.connector
from mysql.connector import Error
import json
import pandas as pd

def insert():
    
    query = '''insert into books(title, author_fname, author_lname, released_year, stock_quantity, pages)
	            values(%s, %s, %s, %s, %s, %s);'''
    

    title = st.text_input('book title') 
    st.write(title)

    author_fname =st.text_input('author frist name')
    st.write(author_fname)

    author_lname = st.text_input('author last name') 
    st.write(author_lname)

    released_year = st.number_input('released year',1)
    st.write(released_year)

    stock_quantity = st.number_input('stock quantity',1)
    st.write(stock_quantity)

    pages = st.number_input('page',1)
    st.write(pages)

    data = (title, author_fname, author_lname, released_year, stock_quantity, pages)

    if st.button('SAVE'):
        try :
            connection = mysql.connector.connect(
                        host ='database-2.cumcickeiqsl.ap-northeast-2.rds.amazonaws.com', #Hostname = RDS엔드포인트
                        user = 'streamlit',
                        password = 'yh1234',
                        database = 'yhdb'
                    )
            if connection.is_connected() :
                cursor = connection.cursor(dictionary= True)
                cursor.execute(query, data) # 파이선에서  sql로 입력할때
                connection.commit()  #  데이터베이스에 영구저장하라
                


                cursor.execute("""select * from books""")
                result = cursor.fetchall()
            
                #파이썬의 리스트+ 딕셔너리 조합을 => JSON형식으로 바꾼것
                json_result = json.dumps(result)
                # st.write(json_result)
                df=pd.read_json(json_result)

                st.dataframe(df.tail(1))
                
        except Error as e :
                print('디비관련 에러 발생',e)
            
        finally :
            cursor.close()
            connection.close()
            # st.write('MySQL 커넥션 종료')
            st.success('저장되었습니다.')