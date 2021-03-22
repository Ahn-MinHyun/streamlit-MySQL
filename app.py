import streamlit as st
import streamlit as st
import mysql.connector
from mysql.connector import Error

from DBselect import select
from DBinsert import insert
from DBdelete import delete
from DBupdate import update
def main():
    st.title('DB project')

    menu = ['Select','Insert','Delete','Update']

    choice = st.sidebar.selectbox('MENU',menu)

    if choice == 'Select':

        select()

    elif choice == 'Insert':
        
        insert()

    elif choice == 'Delete':

        delete()
    
    elif choice == 'Update':
        
        update()

    else: 
        st.subheader('Introduce project')
if __name__=='__main__' :
    main()
