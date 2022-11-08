#!/usr/bin/env python
# coding: utf-8

# In[1]:


# coding: utf-8

# In[ ]:


#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__)
model = pickle.load(open('SVR_model.pkl', 'rb'))
model2 = pickle.load(open('KNN_model.pkl', 'rb'))
modelBIG = pickle.load(open('SVR_model_BIG.pkl', 'rb'))
modelBIG2 = pickle.load(open('KNN_model_BIG.pkl', 'rb'))
modellittle = pickle.load(open('SVR_model_little.pkl', 'rb'))
modellittle2 = pickle.load(open('KNN_model_little.pkl', 'rb'))
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    l=[]
    m=[]
#     今天幾月份?
    l.append(request.form['value1']) 
#     今天星期幾?
    l.append(request.form['value2'])
#     明日工地數量?
    l.append(request.form['value3'])
#     明日所有工地車次總數量?
    l.append(request.form['value4'])
#     明日遠距車次?
    l.append(request.form['value5'])
#     明日超遠距車次?
    l.append(request.form['value52'])
#     今日在職司機人數?
    l.append(request.form['value6'])
#     今日臨時司機人數?
    l.append(request.form['value7'])
#     明日天氣(好天氣填入0、下雨天填入1)
    l.append(request.form['value8'])
#     環山以上車次數量
    m.append(request.form['value9'])
    
    l_final = np.array(l).reshape((1,-1))
    ans = model.predict(l_final)
    ans2 = model2.predict(l_final)
    prediction=((ans+ans2)/2)
    final_Price = np.round(prediction.astype(int),0)   

    sites = request.form['value3']
    QTY = request.form['value4']
    weather = request.form['value8']
    farway = request.form['value5']
    superfar = request.form['value52']     
    superfarfar = request.form['value9']
    OVER_LOAD = (int(superfar)/int(QTY))
    
    str_sites = str(sites)
    str_QTY = str(QTY) 
    str_farway = str(farway)
    str_superfar = str(superfar)
    str_superfarfar = int(superfarfar)
    str2_superfarfar = str(superfarfar)
    str2_OVER_LOAD =OVER_LOAD
    
    if final_Price >10:
        l_final = np.array(l).reshape((1,-1))
        ans = modelBIG.predict(l_final)
        ans2 = modelBIG2.predict(l_final)
        prediction=((ans+ans2)/2)
        final_Price2 = np.round(prediction.astype(int),0)
    if final_Price <=10:
        l_final = np.array(l).reshape((1,-1))
        ans = modellittle.predict(l_final)
        ans2 = modellittle2.predict(l_final)
        prediction=((ans+ans2)/2)
        final_Price2 = np.round(prediction.astype(int),0)   
        if final_Price>final_Price2:
            final_Price2 = final_Price
    if str_superfarfar >4:
        final_note = "環山以上 極遠車次過多"
        str_yuan = "需人工判斷"
        return render_template('index.html',note=final_note,yuan=str_yuan)

    if str_superfarfar <5 and str2_OVER_LOAD <0.5 :
        final_note = "明天有"+str_sites+"個工地\n"+"預約 "+str_QTY+"車次\n"+"遠距 "+str_farway+"車次\n"+"超遠 "+str_superfar+"車次\n"+"環山以上 "+str2_superfarfar+"車次\n"+"\n"+"總共需要\n"
        str_yuan = "台預拌車"
        return render_template('index.html',prediction=final_Price2,note=final_note,yuan=str_yuan)
     
    elif str2_OVER_LOAD >=0.5:
        final_note = "超遠車次 超過半數"
        str_yuan = "需人工判斷"
        return render_template('index.html',note=final_note,yuan=str_yuan)
       

if __name__ == "__main__":
    app.run(debug=True)

