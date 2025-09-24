import pandas as pd

def find_order_within_range(df,minValue,maxValue,SortType=True):
    order_totals=df.groupby('ProductID').apply(lambda x: (x['UnitPrice']* x['Quantity']*(1-x['Discount'])).sum())
    orders_within_range=order_totals[(order_totals>= minValue) & (order_totals <= maxValue)]
    #unique_orders=df[df['OrderID'].isin(orders_within_range.index)]['OrderID'].drop_duplicates().tolist()
    #return unique_orders
    result_df = pd.DataFrame({
        'ProductID': orders_within_range.index,
        'Sum': orders_within_range.values
    })

    if SortType:
        result_df = result_df.sort_values('Sum', ascending=True)
    else:
        result_df = result_df.sort_values('Sum', ascending=False)

    return result_df.head(3)

df=pd.read_csv('d:/Pycharm Projects/ML/Day 2/data/SalesTransactions.csv')

minValue=float(input("Nhap gia tri min: "))
maxValue=float(input("Nhap gia tri max: "))
sort_option = input("(True/False)?: ")
if sort_option.lower() == 'false':
    SortType = False
else:
    SortType = True
result=find_order_within_range(df,minValue,maxValue,SortType)
print(f'\nDanh sách các hóa đơn trong phạm vi từ {minValue} đến {maxValue}:')
print(result.reset_index(drop=True))