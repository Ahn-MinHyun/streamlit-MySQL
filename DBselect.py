import streamlit as st
import mysql.connector
from mysql.connector import Error
import pandas as pd
import numpy as np
import json


def select():
    column_list = ['title','author_fname','author_lname','released_year','stock_quantity','pages']
    selected_column_list = st.multiselect('컬럼을 선택하세요', column_list)
    
    if len(selected_column_list) == 0:
        query = """ select * from books; """
    else:
        column_str = ', '.join(selected_column_list)
        query =  "select book_id, "+ column_str + " from books;"

    try :
        # 1. 커넥터로부터 커넥션을 받는다.
        connection = mysql.connector.connect(
            host ='database-2.cumcickeiqsl.ap-northeast-2.rds.amazonaws.com', #Hostname = RDS엔드포인트
            user = 'streamlit',
            password = 'yh1234',
            database = 'yhdb'
        )

        if connection.is_connected():

            cursor = connection.cursor(dictionary= True) #   하이퍼파라미터 dictionary=True 딕셔너리형태 
            
            cursor.execute(query)
            result = cursor.fetchall()
            
            #파이썬의 리스트+ 딕셔너리 조합을 => JSON형식으로 바꾼것
            json_result = json.dumps(result)
            # st.write(json_result)
            df=pd.read_json(json_result)

            st.dataframe(df)

    except Error as e : 
        print('디비관련 에러 발생', e)
        
    finally :

        cursor.close()
        connection.close()
        print('MySQL 커넥션 종료')

