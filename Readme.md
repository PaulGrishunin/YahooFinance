REST API, returns JSON which contains historical
information about the value of shares of companies
for the entire period of their existence, according
to Yahoo. Finance.

1. endpoint 
   '/prices/Company_name1,Company_name2,...,Company_nameN'

returns JSON with the data of the listed companies. 
   The number of companies can be 1 or several.

Example:
    http://127.0.0.1:8000/prices/ZM
returns
    [{"company":"ZM","date":"2019-04-18","open":65.0,"high":66.0,
"low":60.320999,"close":62.0,"adj_close":62.0,"volume":25764700},{"company":"ZM",
"date":"2019-04-22","open":61.0,"high":68.900002,
"low":59.939999,"close":65.699997,"adj_close":65.699997,"volume":9949700},...


    http://127.0.0.1:8000/prices/RUN,ZUO
returns
    [{"company":"RUN","date":"2019-07-19","open":20.09,"high":20.459999,
"low":19.709999,"close":19.77,"adj_close":19.77,"volume":1668300},...
{"company":"ZUO","date":"2019-05-23","open":22.1,"high":22.17,
"low":20.32,"close":20.799999,"adj_close":20.799999,"volume":3787300}]
