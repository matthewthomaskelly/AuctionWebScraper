import os

# ************************************************************************
# ** Name:          HTMLWriter()
# ** Purpose:       A class incorporating code to create and write and write a
# **                 simple report containing Heading, sub-heading, tables with 
# **                 table data. Report is written with number of columns per
# **                 row being specified.
# ** Creation date: June 2017
# ** Author:        Matthew KELLY
# ** Amendments:    July 2017 - added function add_table_data_image_by_id()
# **                had to amend WriteHTMLReportAndClose() to not list index for <IMG
# ** Wishlist:      -
# ************************************************************************
class HTMLWriter():

    # __init__ specify and declare initial values for MainHeading, SubHeading
    #  and dictionary containing Tables
    def __init__(self):
        self.__MainHeading = ""
        self.__SubHeading = ""
        self.__Tables = {}

    # Creates HTML (text) file as specified. ...
    def create_html_file(self, FullFileNameElements):

        FullReportPathName = os.path.join(*FullFileNameElements)

        FullReportDirectory = os.path.dirname(FullReportPathName)
        try:
            if not os.path.exists(FullReportDirectory):
                os.makedirs(FullReportDirectory)
            self.__FileStream = open(FullReportPathName, "w")
        except:
            print ("Unable to open file: " + FullReportPathName)
            # mtk raise an error?!

    # Changes __MainHeading
    def add_main_heading(self, MainHeadingListingTitle):
        self.__MainHeading = "<H1>" + MainHeadingListingTitle + "</H1>"

    # Changes __SubHeading
    def add_sub_heading(self, SubHeading):
        self.__SubHeading = "<H2>" + SubHeading + "</H2>"

    # Adds a dictionary entry to Tables with specified key. 
    # Dictionary will containt an list of lists for each element;
    # Starting with the <TABLE> element and one for each added <TD>
    def add_table_by_id(self, TableName):
        self.__Tables[TableName] = [ ["<TABLE id=" + TableName + ">"] ]  

    # Adds a <TD> element to List of Lists under specified key.
    # accepts a list of element tat will be separated to a newline <BR>
    # This allows multiple report details to be passed and makes mental imagery easier.
    def add_table_data_by_id(self, TableName, lstData):
        HTMLString = "<TD>"
        for eachTD in lstData:
            HTMLString += eachTD + "<BR>"
        HTMLString += "</TD>"

        self.__Tables [TableName] += [ [ HTMLString ] ] 

    # Adds a <TD> element in the form of an IMG to List of Lists under specified key.
    # accepts a RelativeImageLocation for specified <IMG> element
    def add_table_data_image_by_id(self, TableName, ImageFileName):
        HTMLString = "<TD>"
        HTMLString += "<IMG SRC=" + ImageFileName + " />"
        HTMLString += "</TD>"

        self.__Tables [ TableName ] += [ [HTMLString] ]

    # Writes report HTML string and saves this to the filestream specified
    def write_html_report_and_close(self, MaxColumnNumber, InsertIndexCount=True):

        HTMLString = ""
        HTMLString += "<HTML>"
        HTMLString += self.__MainHeading
        HTMLString += self.__SubHeading

        # want to iterate through each Table key i.e - each TABLE
        for eachTableKey in self.__Tables:
                        
            # each TABLE contains a two dimensional list of TD values.
            # want to iterate through each sepatate list for each TABLE  
            ColumnCounter = 1          
            for Index, eachTable in enumerate(self.__Tables[eachTableKey]):

                # each   
                for eachTableData in eachTable:

                    # first list value contains <TABLE> element.
                    # Need to add first row <TR>            
                    if Index == 0:
                        HTMLString += eachTableData
                        HTMLString += "<TR>"
                    else:
                        # for every other data element <TD> add to HTML string
                        # mtk 20/07/17 - added logic for if TD containts <IMG for no index
                        if InsertIndexCount and eachTableData.find("<IMG") < 0:
                            HTMLString += eachTableData.replace("<TD>", "<TD>" + str(ColumnCounter) + "<BR></TD><TD>", 1)
                            ColumnCounter += 1
                        else:
                            HTMLString += eachTableData
                        
                        # When the specified number of rows is reached, create a new one:
                        if Index % MaxColumnNumber == 0:
                            HTMLString += "</TR><TR>"

            # Add final closing table row and closing table elements
            HTMLString += "</TR>"
            HTMLString += "</TABLE>"

        # ... and closing HTML element
        HTMLString += "</HTML>"

        # write HTML string to FileStream
        self.__FileStream.write(HTMLString)

        # and close FileStream
        self.__FileStream.close()
