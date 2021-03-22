import streamlit as st
import mysql.connector
from mysql.connector import Error
import pandas as pd
import numpy as np
import json

import streamlit as st
import mysql.connector
from mysql.connector import Error

def update():
    # column_list = ['title','author_fname','author_lname','released_year','stock_quantity','pages']
    # selected_column_list = st.multiselect('컬럼을 선택하세요', column_list)


    # 타이틀을 기준으로 잡고 업데이트하는 방식으로 가자 음.. 가능하다면 ID or 타이틀로 잡을 수 있도록

    st.title('Update 할 책을 선택하세요')
    update_book_df= None

    try :
        connection = mysql.connector.connect(
                    host ='database-2.cumcickeiqsl.ap-northeast-2.rds.amazonaws.com', #Hostname = RDS엔드포인트
                    user = 'streamlit',
                    password = 'yh1234',
                    database = 'yhdb'
                )
        if connection.is_connected() :
            cursor = connection.cursor(dictionary= True)
            query = """select * 
                        from books;"""
            cursor.execute(query)
            results = cursor.fetchall()
            json_result = json.dumps(results)
            df = pd.read_json(json_result)
            st.dataframe(df)
                # st.write(json_result)

            select_book=st.selectbox('선택하세요',df['title'])
            select_book_df=df.loc[df['title']==select_book]
            books_ID=[]
            for id in select_book_df['book_id']:
                books_ID.append(id)
            select_book_id= st.selectbox('선택하세요', books_ID)
            st.table(df.loc[df['book_id']== select_book_id])
            update_book_df = df.loc[df['book_id']== select_book_id].copy()
            
            
#------------------ update할 책 찾기(end)------------------------



            # for row in results:
            #     # st.write(row)
            #     book_id_list.append( row['book_id'])
            
    except Error as e :
            print('디비관련 에러 발생',e)
        
    finally :
        cursor.close()
        connection.close()
        st.write('MySQL 커넥션 종료')

#------------------------업데이트할 문장---------------------------
    print(['title'])
    print(int(update_book_df.loc[ : ,'pages'].values))
    
    title = st.text_input('책 제목 입력', value = ''.join(update_book_df.loc[ : ,'title'].values))
    author_fname = st.text_input('작가의 이름입력',value = ''.join(update_book_df.loc[ : ,'author_fname'].values))
    author_lname = st.text_input('작가의 성입력', value =''.join(update_book_df.loc[ : ,'author_lname'].values))
    pages = st.number_input('페이지 수 입력', value= int(update_book_df.loc[ : ,'pages'].values))
    released_year = st.number_input('출판년도 입력',value= int(update_book_df.loc[ : ,'released_year'].values))
    stock_quantity = st.number_input('수량 입력',value= int(update_book_df.loc[ : ,'stock_quantity'].values))

    st.warning('책의 정보가 영구적으로 바뀌게 됩니다. 업데이트 하시겠습니까?')
    
    if st.button('Update'):
        try:
            connection = mysql.connector.connect(
                    host ='database-2.cumcickeiqsl.ap-northeast-2.rds.amazonaws.com', #Hostname = RDS엔드포인트
                    user = 'streamlit',
                    password = 'yh1234',
                    database = 'yhdb'
                )

            if connection.is_connected() :
                cursor = connection.cursor(dictionary= True)
                print(type(author_fname))
                print(type(title))
                query ="""update books
                            set
                            title = %s,
                            author_fname = %s, 
                            author_lname = %s,
                            pages = %s, 
                            stock_quantity = %s, 
                            released_year = %s
                            where book_id = %s;"""

                data = (title, author_fname,author_lname, pages,stock_quantity,released_year,select_book_id)
                
                cursor.execute(query,data)
                
                connection.commit()
                st.table(update_book_df.loc[update_book_df['book_id']== select_book_id])
                st.success('완료하였습니다.')
                    

        except Error as e :
            print('디비관련 에러 발생',e)
        
        finally :
            cursor.close()
            connection.close()
            st.write('MySQL 커넥션 종료')
