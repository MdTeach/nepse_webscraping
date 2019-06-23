"""
 Geting the stcoks data from the NEPSE
 Data geting today's data: name,max,min,closing

 Url = http://www.nepalstock.com/todays_price/index/1
 Url = http://www.nepalstock.com/todays_price/index/2
 Url = http://www.nepalstock.com/todays_price/index/3
 And so on......


"""

import requests as req
import bs4
import json

class NepseData():
    URL = "http://www.nepalstock.com/main/todays_price/index/"
    NUM_INDEX = 8

    data_label = []
    final_data = []

    ##From the NEPSE website get the getting the headers of the data
    def getDataHeaders(self):
        res = req.get(self.NUM_INDEX)
        content = bs4.BeautifulSoup(res.text, features="lxml")
        
        headers = content.select(".unique")[0]
        
        headers_list = headers.select("td")

        data = []
        for head in headers_list:
            data.append(head.text)
        return data


    ##From the NEPSE website from page 1-9 get all the data
    def getAllData(self):

        final_data = []
        for i in range(self.NUM_INDEX):
            index = self.NUM_INDEX +1
            res  = req.get(self.URL+str(index))
            content = bs4.BeautifulSoup(res.text,features="lxml")
            #data is given in html table
            table_content = content.select('.table-condensed')[0]

            #remove forms field
            selects = table_content.findAll('form')
            for match in selects:
                match.decompose()

            #removing image links
            selects = table_content.findAll('img')
            for match in selects:
                match.decompose()

            #remove other unnecessary fields class    
            data_fields = table_content.select('tr')
            data_fields.pop(0)
            data_fields.pop(0)
            data_fields.pop(-1)
            data_fields.pop(-1)
            data_fields.pop(-1)
            data_fields.pop(-1)

            #List containg all datas
            data = []


            for data_field in data_fields:
                table_datas = data_field.select("td")
                
                #Temp list containg the datas
                data_lists = []
                
                for table_data in table_datas:
                    #print(table_data.text)
                    data_lists.append(table_data.text)
                data.append(data_lists)
            
            final_data.append(data)
        return final_data

    def export_json(self):
        headers = self.getDataHeaders()
        final_data = self.getAllData()
        headers.append(final_data)
        with open('data.json', 'w') as outfile:
            json.dump(headers, outfile)