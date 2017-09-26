# ************************************************************************
# ** Name:          StolenWebScraper.py
# ** Version:       1.0 IN DEVELOPMENT
# ** Purpose:       To take a list of values and to scrape websites for items as
# **                 specified. Examples include GumTree.com bike, within radius 
# **                 of a postcode.
# ** Creation date: September 2017 (from March 2017)
# ** Modules:       bs4 - beautiful soap
# **                urllib  - URL library
# **                json - json files import and export
# ** Author:        Matthew KELLY
# ** Inputs:        None at present
# ** Returns:       Creates report detailing results
# ** Amendments:    1.0 - Removed previous inout file format and amended to list of dictionaries readable as json
# ** Wishlist:      Amend hard coding to include spec files for different website to examine
# *                 Allows users to add websearch data (and save)?
# *                 Amend carving class to incorporate different website to GumTree...
# **                Error logging, raising and catching
# **                Central Try/Except
# ************************************************************************

import os
import sys
import json
import bs4 # beautiful soup
import urllib.request # url library to request an url
import urllib.parse # url library to parse htmk queries
from HTMLWriter import HTMLWriter

# ************************************************************************
# ** Name:          main()
# ** Purpose:       To take a list of values and to scrape websites for items as
# **                 specified. Examples include GumTree.com bike, within radius 
# **                 of a postcode.
# ** Process.       Read websites, specify search terms, conduct search, separate results, report.
# ** Creation date: March 2017
# ** Author:        Matthew KELLY
# ** Inputs:        None at present
# ** Returns:       None at present
# ** Amendments:    Changed URL and SOUP code to classes
# **                Amended report writing section for separatoin of reports
# ** WishList:      Needs to accept command line arguments
# ************************************************************************
def main():

    # mtk? get command line arguments
    #Change this to a functions
    InputFileNameElements = [ "WebsiteSearchDetails.txt" ]
    OutputFileNameElements = [ "Reports", "Report.json" ]

    # read each line in input file and store
    # get_stolen_website_details() returns a list including string or URL and further list of Search Terms
    for WebsiteUrl, SearchItems in  get_auction_website_details(InputFileNameElements):

        print("Getting search items for " + WebsiteUrl)        
        
        # mtk - insert logic here for different website details...
        
        # class StolenAuctionSoup takes SearchItems and locates results accordingly 
        GumTreeSoup = StolenAuctionSoup()
        # from each stored line in WebsiteSearchDetails.txt get specific URL  
        MyUrl = GumTreeSoup.create_url_request(WebsiteUrl, SearchItems)
        # send URl request to specific website using Beautiful Soup
        MySoup = GumTreeSoup.get_soup(MyUrl)
        # mtk 07.17 - added code to save each report to a Unique folder with name made up from search details        
        UniqueOutputFileNameElements = create_unique_report_file_name(OutputFileNameElements, SearchItems)
        # use this same information for SubHeading in HTML report
        SubHeading = return_string_with_each_search_term(SearchItems)
        
        # Create instance of HTML (Report) Writer
        HTMLReport = HTMLWriter()
        HTMLReport.create_html_file(UniqueOutputFileNameElements)
        HTMLReport.add_main_heading(WebsiteUrl)
        HTMLReport.add_sub_heading(SubHeading)
        HTMLReport.add_table_by_id(WebsiteUrl)
        
        # examine the specific results from GumTree.com (function contains yield)
        for CurrentItem in GumTreeSoup.get_website_items(MySoup, os.path.dirname(os.path.join(*UniqueOutputFileNameElements))):
            
            print ("Reporting current item..." + CurrentItem[0])
            
            # ..and add details to report,
            HTMLReport.add_table_data_by_id(WebsiteUrl, CurrentItem)
            # along with any related images
            HTMLReport.add_table_data_image_by_id(WebsiteUrl, GumTreeSoup.CurrentDownloadedImageFileName)
        
        # create report with specified imputs
        HTMLReport.write_html_report_and_close(2)

# end of main()

# ************************************************************************
# ** Name:          get_auction_website_details()
# ** Purpose:       Function to read InputFile as specified and to yield results until EOF.
# ** Creation date: June 2017
# ** Author:        Matthew KELLY
# ** Inputs:        InputFileNameElements - tuple or list UrlLinkToListinging to file containing specified search terms
# ** Returns:       URL string and dictionary of search terms
# ** Amendments:    July 2017 - added .strip() call to remove whitespace from search terms
# **                 as causing strange results.
# ************************************************************************
def get_auction_website_details(InputFileNameElements):

    # ensure folder exists and that file opens before proceeding
    FullFilePathName = os.path.join(*InputFileNameElements)
    if os.path.exists(FullFilePathName):
        try:
            InputFileStream = open(FullFilePathName, "r")
        except:
            print ("Error opening: " + FullFilePathName)
            return {}
    else:
        return {}
    
    # initialise SearchItems dictionary to be returned by function based on content of file
    DictSearch = json.load(InputFileStream)
    for eachSearchTerm in DictSearch:
        UrlString = eachSearchTerm['url']
        SearchItems = eachSearchTerm['search_terms']
        yield [UrlString, SearchItems]


# ************************************************************************
# ** Name:          function create_unique_report_file_name()
# ** Purpose:       To Change specified report name to include Unique details 
# **                 relating to specified search terms. This will stipulate that
# **                 each report is saved in a separate folder location
# ** Creation date: July 2017
# ** Author:        Matthew KELLY
# ** Inputs:        OutputFileNameElements - List of Output location
# **                CurrentSearchTerms - Dictionary of current search terms
# ** Returns:       New List for Output location
# ** Amendments:    None
# ************************************************************************
def create_unique_report_file_name(OutputFileNameElements, CurrentSearchItems):

    # Set intended return list shallow copy of current. THis can be amended within the function
    #  without changing the original that is used elsewhere
    ReturnList = list (OutputFileNameElements)
    # get count of number of list elements
    NoElements = len(ReturnList)
    # last element is file name. Store
    TempFileName = ReturnList[NoElements-1]
    # get a Unique ReportNameId from CurrentSearchTerms
    UniqueReportNameId = return_string_with_each_search_term(CurrentSearchItems)
    # change temporary file name to include unique ReportNameID
    TempFileName = TempFileName.replace(".html", "", 1) + UniqueReportNameId + ".html"
    # then add this UniqueReportName to the end of ReturnList (replacing filename)
    ReturnList[NoElements-1] = UniqueReportNameId.strip()
    # then add new file name to end.
    ReturnList.append(TempFileName)

    # ReturnList is now one item longer with original filename being replaced with unique folder
    #  to avoid images being overwritten and new unique filename appended to end

    return ReturnList


# ************************************************************************
# ** Name:          function return_string_with_each_search_term()
# ** Purpose:       Returns string containing Keys and Values from passed dictionary
# **                 This will be used to create a Unique directory name for reports
# ** Creation date: July 2017
# ** Author:        Matthew KELLY
# ** Inputs:        Dictionary of CurrentSearchTerms
# ** Returns:       String contains Keys and related Values
# ** Amendments:    None
# ************************************************************************
def return_string_with_each_search_term(CurrentSearchTerms):
    # initialise string to return
    ReturnString = ""
    # want keys and matching value strings
    for eachKey in CurrentSearchTerms:
        # Return string will be made up of each Key value and its corresponding data
        ReturnString += " " + eachKey + " " + CurrentSearchTerms[eachKey]

    return ReturnString


# ************************************************************************
# ** Name:          Class StolenAuctionSoup()
# ** Purpose:       To take a list of values and to scrape websites for items as
# **                 specified. Examples include GumTree.com bike, within radius 
# **                 of a postcode.
# ****          This class will currently only handle GumTree searches.         ****
# ****          Use Inheritance for further websites such as eBay, Preloved?    ****    
# ** Creation date: March 2017
# ** Author:        Matthew KELLY
# ** Inputs:        None at present
# ** Returns:       None at present
# ** Amendments:    June 2017 - changed code for BS4 and URL request into Class...
# ************************************************************************
class StolenAuctionSoup():

    # when an image is downloaded, this will be temporarily saved in the following
    #  variable until a further download is successfully completed
    CurrentDownloadedImageFileName = ""

    # ********************************************************************
    # ** Name:      create_url_request
    # ** Purpose:   Takes Website URL and Specified SearchItems
    # ** Inputs:    WebsiteUrl website for search, and
    # **            dictionary of SearchTerms
    # ** Returns:   URL search term
    # ** Amendments:None
    # ********************************************************************
    def create_url_request(self, WebsiteUrl, SearchItems):

        # using urlib.parse create query instruction from dictionary of search terms
        Query = urllib.parse.urlencode(SearchItems)

        # create list of items for full url creation
        WebsiteUrl =("https", WebsiteUrl, "search", Query, "")

        # create full url request from specified terms as above
        UrlRequest = urllib.parse.urlunsplit(WebsiteUrl)

        return UrlRequest


    # ********************************************************************
    # ** Name:      function get_website_items
    # ** Purpose:   Queries the Soup item to return specific items
    # **            This is the class function that would mainly need amending 
    # **             if other websites were incorporated
    # ** Inputs:    soup - current soup item
    # **            RelativeFolderToDownload - optional folder location to save images
    # ** Returns:   List of items located
    # ** Amendments:None at present
    # ********************************************************************
    def get_website_items(self, soup, RelativeFolderToDownload = ""):

        # find all natural soup items
        NaturalItems = soup.find_all(class_="natural")

        # iterate through each 'natural' item pulling specified data and storing this in variables
        for Index, CurrentNaturalItem in enumerate (NaturalItems):

            # The Listing title
            ListingTitle = CurrentNaturalItem.find(class_="listing-title").get_text()
            ListingTitle = ListingTitle.strip()

            # The Listing Description
            ListingDescription = CurrentNaturalItem.find(itemprop="description").get_text()
            ListingDescription = ListingDescription.strip()

            # The URL of the Listing (for future reference)
            UrlLinkToListing = CurrentNaturalItem.find("a", class_="listing-link").get("href")
            UrlLinkToListing = urllib.parse.urljoin("http://www.gumtree.com", UrlLinkToListing)

            # ...and attmept to download the Listing Thumbnail for inclusion in the report
            ImgUrl = CurrentNaturalItem.find(class_="listing-thumbnail").img.get("data-lazy")

            # set current downloaded image to ""
            CurrentDownloadedImageFullFileName = ""
            # don't try to download image if there isn't one...
            if ImgUrl is not None:
                # mtk 07.17 - set download location to RelativeFolder and Index 
                ImgFileName = os.path.join(RelativeFolderToDownload, str(Index)+".jpg")
                # mtk 22/07/17. if the path doesn't exist, create it...
                if not os.path.exists(RelativeFolderToDownload):
                    # mtk 26/09/17 - changed to makedirs as may request multiple levels
                    os.makedirs(RelativeFolderToDownload)
                # ..and try to download image to location in function
                self.__download_resource(ImgUrl, ImgFileName)
                # set current downloaded image to name
                self.CurrentDownloadedImageFileName = str(Index)+".jpg"

            # yield for each natural item
            yield(ListingTitle, ListingDescription, UrlLinkToListing)

    # ********************************************************************
    # ** Name:      function get_soup
    # ** Purpose:   To get SOUP for specicifed URL
    # ** Inputs:    URL for web address to return
    # ** Returns:   Returns Soup
    # ** Amendments:None
    # ********************************************************************
    def get_soup(self, Url):
        # Get request URL
        Req = urllib.request.urlopen(Url)
        # Submit to Beautiful Soup
        Soup = bs4.BeautifulSoup(Req, "html.parser")
        # and return soup
        return Soup

    # ********************************************************************
    # ** Name:      (private) function __download_resource
    # ** Purpose:   To download image from web address
    # ** Inputs:    - UrlToImg - URL to Image we want to download
    # **            - Location path to download image to
    # ** Returns:   None
    # ** Amendments:July 2017 - amended to accept DestinationPathForImg
    # ********************************************************************
    def __download_resource(self, UrlToImg, DestinationPathForImg):
        # open a binary stream for image
        ImgSaveStream = open(DestinationPathForImg, "wb")
        # an try to request image url
        try:
            req = urllib.request.urlopen(UrlToImg)
        except urllib.request.HTTPError as error:
            print(error.code)

        # save this request to the (image) filestream
        ImgSaveStream.write(req.read())

        # tidy up, close both stream and request
        ImgSaveStream.close()
        req.close()

# Call to main
print("Starting script...")
main()
print("Script completed...")
