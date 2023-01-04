import streamlit as st
import pandas as pd
import math
import xlsxwriter
import yfinance as yf
from GoogleNews import GoogleNews



#for adding title
st.title("five:blue[&]dime")


st.image("markus-winkler-IrRbSND5EUc-unsplash.jpg",caption =None, clamp=False, channels="RGB", output_format="auto")
symbol=""
symbol = st.text_input('Stock name :', 'ex .. AAPL , FB , etc ')
#symbol = 'AAPL'
if symbol != '':
    stock = yf.Ticker(symbol)
    stock_df = stock.history(period="5y")
    line_graph =stock_df['Close'].plot(title=symbol +" stock price")
    st.line_chart(stock_df, y="Close")

    #vote variable for voting for buying
    vote =0
    #major holders


    with st.container():
        #basic details
        try:
            sector = stock.info['sector']
            st.write("Sector : "+  sector)
        except:
            st.write("Sector : " + "NA")

        try:
            headquarter = stock.info['country']
            st.write("Headquarter : "+  headquarter)
        except:
            st.write("Headquarter : "+ "NA")


        try:
            pe = stock.info['trailingPE']
            if pe <25 :
                st.success( "PE ratio : "+  str(pe))
                vote=vote + 1
            else :
                st.error("PE ratio : "+str(pe))
        except:
            st.warning("PE ratio : " + "NA")

        try:
            peg = stock.info['pegRatio']
            if peg <1 :
                st.success( "PEG ratio : "+  str(peg))
                vote=vote + 1
            else :
                st.error("PEG ratio : "+str(peg))
        except:
            st.warning("PEG ratio : "+ "NA")
    
        try:
            high_low =stock.info['52WeekChange']

            if high_low < -0.10 :
                    st.success( "from 52 week high : "+  str(high_low))
                    vote=vote+1
            else :
                st.error("from 52 week high : "+str(high_low))
        except:
            st.warning("52 week high : "+ "NA")

        





    #total shares
    st.markdown('**Total Number of shares**')
    total_shares = stock.shares
    st.bar_chart(total_shares)
    #st.dataframe(total_shares)


    #print share holders
    st.markdown('**Major share holders**')
    maj_holders = stock.major_holders
    st.table(maj_holders)




    major_holder = stock.major_holders
    type(major_holder[0][0])
    maj_hold_insider = major_holder[0][0]
    maj_hold_insider = float(maj_hold_insider.rstrip('%'))

    maj_holder_inst=int(major_holder[0][3])

    if maj_hold_insider > 40 or maj_holder_inst >1000:
        vote= vote+1

    with st.container():
        st.markdown("**Buying status :**")
        if vote > 2 :
            st.success("Right time to buy "+symbol +" stocks")
            st.balloons()
        else :
            st.error("Don't buy "  + symbol + "stocks")



    st.subheader("")
    st.subheader("Latest NEWS : "+symbol)




    #NEWS Part
    with st.container():
        gNews = GoogleNews(period = '5d')
        gNews.search(symbol + ' stock ' + ' market ')
        result = gNews.result()
        data = pd.DataFrame.from_dict(result)
        data = data.drop(columns=['img'])

        for res in result:
            st.write('Title :',res['title'])
            st.write('Discription :',res['desc'])
            st.write('Details : ', res['link'])
            word =res['title'].lower()
            sentiment = 'Neutral'
            if word.find('down')!=-1 or word.find('fall')!=-1 :
                sentiment = 'Bad'
            elif word.find('rise')!=-1 or word.find('up')!=-1 :
                sentiment ='Good'
            if sentiment=='Good':
                st.markdown(":green[Good]")
            elif sentiment =='Bad':
                st.markdown(":red[Bad]")
            else :
                st.markdown("Neutral")
            st.write("-----------------------------")
  
        
        





