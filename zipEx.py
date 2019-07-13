import zipfile
zip_ref = zipfile.ZipFile("C://Users//dell//Downloads//test.zip", 'r')
zip_ref.extractall("C://Users//dell//Desktop//keyphrase_extraction-master//keyphrase_extraction-master")
zip_ref.close()