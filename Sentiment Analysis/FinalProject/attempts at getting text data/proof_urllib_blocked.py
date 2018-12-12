import wget

tid = 2220054
url = "http://www.ratemyprofessors.com/paginate/professors/ratings?tid=" + str(tid)

filename = wget.download(url)

print(filename)