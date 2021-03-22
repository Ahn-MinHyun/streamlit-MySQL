import streamlit as st
import mysql.connector
from mysql.connector import Error
import json
import pandas as pd

def delete():

    book_title_list =[]
    book_ID_list = []
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
            # st.write(json_result)
            df=pd.read_json(json_result)

            # print('--------------------------')
            # print(df['title'])

            for row in results:
                book_title_list.append( row['title'])

    except Error as e :
            print('디비관련 에러 발생',e)
        
    finally :
        cursor.close()
        connection.close()


# book_ID_list.append( row['book_id'] )
# print(book_ID_list)

    
    #----------- 지우는 문장-------------

    selected_lang= st.selectbox('지우고 싶은 책 이름을 선택하세요.',book_title_list)

    st.write('선택한 책은 {}입니다.'.format(selected_lang))
    # print(type(selected_lang))

    book_title_df= df.loc[df['title'] == selected_lang] 
    st.dataframe(book_title_df)
    for id in book_title_df['book_id']:
        book_ID_list.append(id)
    
# 만약 선택한 것이 여러개라면? 어떻하지??---------------------------------------------
    if len(df.loc[df['title'] == selected_lang]) != 1:
        print('1')
        selected_id_list= st.multiselect('지우고 싶은 book_id를 선태하세요 .',book_ID_list)

        st.warning('데이터가 영구 삭제 됩니다. 정말 지우시겠습니까?')

        if st.button('YES'):
            try :
                connection = mysql.connector.connect(
                            host ='database-2.cumcickeiqsl.ap-northeast-2.rds.amazonaws.com', #Hostname = RDS엔드포인트
                            user = 'streamlit',
                            password = 'yh1234',
                            database = 'yhdb'
                        )
                if connection.is_connected() :
                    cursor = connection.cursor(dictionary= True)
                    print('2')
    
                    
                    query = """delete from books 
                                where title = %s and book_id = %s;"""
                    data =[]
                    for id in selected_id_list:
                        data.append((selected_lang, id))

                    cursor.executemany(query, data)
                    connection.commit()  
            except Error as e :
                print('디비관련 에러 발생',e)
                
            finally :
                cursor.close()
                connection.close()
                st.subheader('삭제 되었습니다.')
# 데이터가 한개일 떄 ----------------------------------------------
                    
    else :
        st.warning('데이터가 영구 삭제 됩니다. 정말 지우시겠습니까?')

        if st.button('YES'):
            try :
                connection = mysql.connector.connect(
                            host ='database-2.cumcickeiqsl.ap-northeast-2.rds.amazonaws.com', #Hostname = RDS엔드포인트
                            user = 'streamlit',
                            password = 'yh1234',
                            database = 'yhdb'
                        )
                if connection.is_connected() :
                    cursor = connection.cursor(dictionary= True)
                    query = """delete from books 
                                where title = %s;"""
                    data = (selected_lang,)
                    cursor.execute(query, data)
                    connection.commit()  
            except Error as e :
                print('디비관련 에러 발생',e)
            
            finally :
                cursor.close()
                connection.close()
                st.success('삭제 되었습니다.')
