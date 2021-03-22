import streamlit as st
import mysql.connector
from mysql.connector import Error

def main():
    
    book_id_list =[]

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
                        from books
                        limit 5;"""
            cursor.execute(query)
            results = cursor.fetchall()

            for row in results:
                st.write(row)
                book_id_list.append( row['book_id'])
            
    except Error as e :
            print('디비관련 에러 발생',e)
        
    finally :
        cursor.close()
        connection.close()
        st.write('MySQL 커넥션 종료')


    book_id = st.number_input('책ID 입력', book_id_list[0],book_id_list[-1])
    pages = st.number_input('페이지 수 입력',0,500)
    stock = st.number_input('수량 입력',0,200)


    if st.button('실행'):
        try:
            connection = mysql.connector.connect(
                    host ='database-2.cumcickeiqsl.ap-northeast-2.rds.amazonaws.com', #Hostname = RDS엔드포인트
                    user = 'streamlit',
                    password = 'yh1234',
                    database = 'yhdb'
                )

            if connection.is_connected():

                cursor = connection.cursor()
                query ="""update books
                            set pages = %s, stock_quantity = %s
                            where book_id = %s;"""
                
                data = (pages, stock, book_id)
                cursor.execute(query, data)
                connection.commit()
                    

        except Error as e :
            print('디비관련 에러 발생',e)
        
        finally :
            cursor.close()
            connection.close()
            st.write('MySQL 커넥션 종료')
if __name__ == '__main__':
    main()