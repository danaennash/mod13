from SymbolInput import SymbolInput
from ChartTypeInput import ChartTypeInput
from UserInput import UserInput
from Constants import Constants
from StockModel import StockModel
import requests as rq
import datetime
import pygal
import lxml

class StockDataVisualizer:


    def __init__(self, inputData):

        self.inputData = inputData

    def queryStockData(self):

        series = "TIME_SERIES_" + Constants.TIMESERIES[self.inputData[Constants.SERIES]].upper()
        data = {
            "function": series,
            "symbol": self.inputData[Constants.SYMBOL],
            "outputsize":"full",
            "interval":"60min",
            "apikey":Constants.API_KEY
            }
        
        apiCall = rq.get(Constants.API_URL, params=data)

        response = apiCall.json()
        
        if series == "TIME_SERIES_DAILY":
                timeSeries = "Time Series (Daily)"
            elif series == "TIME_SERIES_WEEKLY":
                timeSeries = "Weekly Time Series"
            elif series == "TIME_SERIES_MONTHLY":
                timeSeries = "Monthly Time Series"
        
        dates = []
        opens = []
        highs = []
        lows = []
        closes = []

        startDate = datetime.date.fromisoformat(self.inputData[Constants.STARTDATE])
        endDate = datetime.date.fromisoformat(self.inputData[Constants.ENDDATE])

        for date, stockData in reversed(response[timeSeries].items()):

            entryDate = datetime.date.fromisoformat(date)

 
            if (entryDate >= startDate and entryDate <= endDate):
                model = StockModel(stockData)
                opens.append(model.open)
                highs.append(model.high)
                lows.append(model.low)
                closes.append(model.close)
                dates.append(date)

            if self.inputData[Constants.CHARTTYPE] == "2":
                chart = pygal.Line(x_label_rotation=45)
                chart.x_labels = dates
                chart.title = "Stock Date for " + self.inputData[Constants.SYMBOL] + ": " + self.inputData[Constants.STARTDATE] + " to " + self.inputData[Constants.ENDDATE]
                chart.add("Open",opens)
                chart.add("High",highs)
                chart.add("Low", lows)
                chart.add("Close",closes)
                chart.render_in_browser()
                
                    print("Success!")
        else:
            chart = pygal.Bar(x_label_rotation=45)
            chart.title = "Stock Date for " + self.inputData[Constants.SYMBOL] + ": " + self.inputData[Constants.STARTDATE] + " to " + self.inputData[Constants.ENDDATE]
            chart.x_labels = dates
            chart.add("Open",opens)
            chart.add("High",highs)
            chart.add("Low", lows)
            chart.add("Close",closes)
            chart.render_in_browser()
            
                    print("Success!")


class UserInput:
    def __init__(self, promptMsg, optionsTxt=""):

        self.promptMsg = promptMsg

        self.optionsTxt = optionsTxt

        self.value = None

    def trySetValue(self, input):

        if (self.isInputValid(input)):
            self.value = input
            return True
        else:
            return False

    def isInputValid(self, input):

        pass


class ChartTypeInput(UserInput):
        
        UserInput.__init__(self, "Please enter which chart type you want (1, 2)", exampletxt)

    def isInputValid(self, input):
            if (input == "1"):
                return True
                    elif (input == "2"):
                        return True
                    else:
                        print("Please enter 1 or 2")
                            return False


class TimeSeriesInput(UserInput):
    def __init__(self):

            

        exampletxt = ("Please select time frame you want chart to run for\r\n")
        
            for key, value in Constants.TIMESERIES.items():
                
                exampletxt += key + ". " + value + "\r\n"
            
        UserInput.__init__(self, "Please pick between the time series options (1, 2, 3, 4)",exampletxt)

        def isInputValid(self, timeSeries):
            try:
                selection = int(timeSeries)
                if(selection < 1 or selection > 4):
                    print("\nThis is not a valid option. Must be between one and four.\n")
                    return False
                
                    except ValueError:
                        print("\nNot a valid option. Please choose from one of the four options.\n")
                    return False

            return True

class StartDateInput(UserInput):

    def __init__(self):

        UserInput.__init__(self,"Enter the start date (YYYY-MM-DD)")

    def isInputValid(self, input):
        try:
            datetime.date.fromisoformat(input)
            return True

        except ValueError:
            return False

class EndDateInput(UserInput):
    
    #start date by user
    
    def __init__(self, startDateInput):
        self.startDateInput = startDateInput
        UserInput.__init__(self, "Please enter the end date (YYYY-MM-DD)")

    def isInputValid(self, endDate):
        
        try:
            
            d1 = self.startDateInput.split(('-'))
            d2 = endDate.split('-')
                      
            start = datetime.datetime(int(d1[0]),int(d1[1]),int(d1[2]))
            end = datetime.datetime(int(d2[0]),int(d2[1]),int(d2[2]))
            
            #error handling 
            
            if start == end:
                
                print("[ERROR] Start date and end date cannot be the same.\n")
                
            elif start > end:
                
                print("[ERROR] Start date must be before the end date.\n")
                
            else:
                
                return True
            
        except ValueError:
            
            print("[ERROR] Date entered not valid.\n")
        
        #if invalid
        return False

