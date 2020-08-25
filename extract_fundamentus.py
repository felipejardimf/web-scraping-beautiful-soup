#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import re 
import pandas as pd
from urllib.request import urlopen
import time
import os

# In[2]:


# Extraindo dados do site Fundamentos


# In[3]:


header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}


# In[4]:


html = requests.get("https://www.fundamentus.com.br/detalhes.php?papel=",headers=header)


# In[5]:


soup = BeautifulSoup(html.text , 'html.parser')


# In[6]:


tabela = soup.find(id='test1')


# In[7]:


cols = [x.text for x in tabela.findAll('th') ]


# In[8]:


rows = tabela.findAll('tr')


# In[9]:


data = []

for row in rows:
    data_rows = row.findAll('td')
    papel = [x.text.strip() for x in data_rows]
    data.append([ele for ele in papel])
    


# In[10]:


acoes_df = pd.DataFrame(data=data , columns=cols)

papeis= list(acoes_df['Papel'])


error_list = []
success_list = []

for papel in papeis:

    html = requests.get('https://www.fundamentus.com.br/detalhes.php?papel={}'.format(papel),headers=header)



    bs = BeautifulSoup(html.text, 'html.parser')


    try:
        tabela1 = bs.findAll('table', class_='w728')[0]
        tabela2 = bs.findAll('table', class_='w728')[1]
        tabela3 = bs.findAll('table', class_='w728')[2]
        #tabela4 = bs.findAll('table', class_='w728')[3]
        tabela5 = bs.findAll('table', class_='w728')[4]


    # In[16]:

    
        data= []
        colunas=[]

        rows = tabela1.findAll('tr')

        for row in rows:
            data_rows = row.findAll(class_='txt')
            data_rows = [ele.text.strip() for ele in data_rows]
            data.append([ele for ele in data_rows])



        colunas = []
        valores = []

        for i in range(0,len(data)-1):
            for j in range(0,len(data[0])):
                if i%2 == 0:
                    colunas.append(data[j][i])
                else:
                    valores.append(data[j][i])
                




        data2= []


        rows = tabela2.findAll('tr')

        for row in rows:
            data_rows = row.findAll(class_='txt')
            data_rows = [ele.text.strip() for ele in data_rows]
            data2.append([ele for ele in data_rows])




        for i in range(0,len(data2)):
            for j in range(0,len(data2[0])):
                if j%2 == 0:
                    colunas.append(data2[i][j])
                else:
                    valores.append(data2[i][j])



        data3 = []

        rows = tabela3.findAll('tr')

        for row in rows:
            data_r = row.find_all(class_=['txt','oscil'])
            data_r = [ele.text.strip() for ele in data_r]
            data3.append([ele for ele in data_r ]) 
          



        for i in range(1,len(data3)):
            for j in range(0,2):
                if j%2 == 0:
                    colunas.append('oscilacoes_'+data3[i][j])
                else:    
                    valores.append(data3[i][j])
                



        for i in range(1,len(data3)):
            for j in range(2,6):
                if j%2 == 0:
                    colunas.append('ind_fund_'+data3[i][j])
                else:    
                    valores.append(data3[i][j])
                



        #data4 = []

        #rows = tabela4.findAll('tr')

        #for row in rows:
            #data_r = row.find_all(class_=['txt','oscil'])
            #data_r = [ele.text.strip() for ele in data_r]
            #data4.append([ele for ele in data_r ]) 
          
            



        #for i in range(1,len(data4)):
            #for j in range(0,4):
                #if j%2 == 0:
                    #colunas.append('dados_b_patr_'+data4[i][j])
                #else:    
                    #valores.append(data4[i][j])
                


        data5 = []

        rows = tabela5.findAll('tr')

        for row in rows:
            data_r = row.find_all(class_=['txt','oscil'])
            data_r = [ele.text.strip() for ele in data_r]
            data5.append([ele for ele in data_r ]) 
          
            

        colunas_ = []
        valores_ = []
        for i in range(2,len(data5)):
            for j in range(0,2):
                if j%2 == 0:
                    colunas.append('ult_12_m_'+data5[i][j])
                else:    
                    valores.append(data5[i][j])
                



        for i in range(2,len(data5)):
            for j in range(2,4):
                if j%2 == 0:
                    colunas.append('ult_3_m_'+data5[i][j])
                else:    
                    valores.append(data5[i][j])
                



        tabela_ok = pd.DataFrame(data=[valores] , columns=colunas)


        from time import gmtime, strftime
        actual_date= strftime("%Y%m%d", gmtime())


        tabela_ok['data_proc'] = actual_date
        
        filename = 'C:/Users/Felipe/Desktop/acoes.csv'
        tabela_ok.to_csv(filename,sep=';',mode='a',index=False,encoding='latin1',header=(not os.path.exists(filename)))

        print('Papel extraído com sucesso  > ',papel)
        success_list.append(papel)
    except IndexError:
        print("Erro ao extrair >" ,papel)
        error_list.append(papel)
    except Exception as e:
        print("Erro no Servidor :",e)
        time.sleep(10)

