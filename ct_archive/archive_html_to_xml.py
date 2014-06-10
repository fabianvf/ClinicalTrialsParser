## parsing HTML files to pull out the xml data


from bs4 import BeautifulSoup
import glob
import os

''' turns an HTML file from the study archive into XML '''
def archive_html_to_xml(input_file, output_directory):

    xml_name = str(input_file).replace('.html','')
    xml_name = xml_name.replace('./ct_changes/', '')

    # testing on the first change file for NCT00000122
    soup = BeautifulSoup(open(input_file)) 

    # this is a bs4 Tag object of just the sdiff-full stuff
    sdiff_full = soup.find(id="sdiff-full")

    # and these are the <tr> tags in that object with the xml we want
    sdiff_xml = sdiff_full.find_all("tr", {"class" : 
                                    ["sdiff-unc", "sdiff-add","sdiff-chg"]})

    ### td class sdiff-a: all of the "before" xml ###
    all_before = []
    for result in sdiff_xml:
        all_before.append(result.find("td", {"class" : "sdiff-a"}))

    before_file = open(output_directory + xml_name + '-before.xml', 'w')
    for item in all_before:
        before_file.write("%s\n" % item.text)

    # td class sdiff-b: all of the "after" xml
    all_after = []
    for result in sdiff_xml:
        all_after.append(result.find("td", {"class" : "sdiff-b"}))

    after_file = open(output_directory + xml_name + '-after.xml', 'w')
    for item in all_after:
        after_file.write("%s\n" % item.text)

''' returns a list of directories in the archive -> changes directory '''
def get_directory_list():
    archive_directory = './ct_changes/'
    directory_names = os.walk(archive_directory).next()[1]
    return directory_names

''' saves XML files for each archive HTML change file '''
def get_archive_xml():
    archive_directories = get_directory_list()
    directory_of_html = './ct_changes/'
    directory_for_xml = './ct_changes_xml/'

    # create new directory to store the arcive xml if it dosen't exist
    # directory: 'NCT00000122'
    for directory in archive_directories:
        if not os.path.exists(directory_for_xml + '/' + directory):
            os.makedirs(directory_for_xml + directory)

        # get a list of all HTML files in each HTML study directory
        html_files = glob.glob(directory_of_html + directory + '/*.html')
        
        # iterate through filenames in html_files and write XML in right folder
        for filename in html_files:
            xml_filename = filename.replace('./ct_changes/' + directory + '/', '')
            archive_html_to_xml(directory_of_html + directory + '/' +
                                xml_filename , directory_for_xml)

get_archive_xml()


