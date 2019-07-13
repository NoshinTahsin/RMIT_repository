import os
import win32com.client

DOC_FILEPATH = "C://Users//dell//Desktop//keyphrase_extraction-master//keyphrase_extraction-master//qu.docx"
doc = win32com.client.GetObject(DOC_FILEPATH)
text = doc.Range().Text

#
# do something with the text...
#
with open("something.txt", "wb") as f:
	f.write(text.encode("utf-8"))
os.startfile("something.txt")
