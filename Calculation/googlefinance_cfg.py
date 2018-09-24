def _generate_cfg(namelist,tickerlist,tickercolumn,fieldnames,outputfile):

    '''
    tickercolumn='B'
    fieldnames=['tradtime','price']
    =GOOGLEFINANCE(B2,"tradetime")

    '''  
    import pandas as pd
    df=pd.DataFrame()
    df['Name']=namelist
    df['Ticker']=tickerlist
    length=len(tickerlist)
    for name in fieldnames:
        df[name]=['=GOOGLEFINANCE({column}{index},"{field}")'.format(column=tickercolumn,index=i,field=name) for i in range(2,length+2)]
    df.to_csv(outputfile,index=False)
    return None

def generate_cfg(inputfile,outputfile,tickertype=''):

    import pandas as pd 

    if tickertype=='Fund':
        fieldnames=['morningstarrating','closeyest','date','returnytd','netassets','change','yieldpct','return1','return4','return13','return52','return156','return260','incomedividenddate','incomedividend','capitalgain','expenseratio']

    if tickertype=='Equity':
        fieldnames=['tradetime','price','priceopen','high','low','volume','high52','low52','volumeavg','pe','marketcap','beta','change','shares','currency']
    else:
        fieldnames=['tradetime','price','priceopen','high','low','volume','high52','low52']

    input=pd.read_csv(inputfile)
    namelist=input['Name']
    tickerlist=input['Ticker']
    _generate_cfg(namelist,tickerlist,'B',fieldnames,outputfile)


if __name__ == '__main__':
    generate_cfg('Vanguard.csv','Vanguardcfg.csv')
    generate_cfg('LSE_equities.csv','LSE_equitiescfg.csv')
    generate_cfg('LSE_ETF.csv','LSE_ETFcfg.csv')
    
