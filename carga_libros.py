import json

with open("books_to_clean.json",encoding="utf-8") as libros:
    data= json.load(libros)

    diccionario={}
    lista=[]

    for x in range(0,11127):
        if len(str(data[x]['publication_date'])) == 1:
            continue
        
        month, day, year = str(data[x]['publication_date']).split('/')
        if (month == "11" and day == "31") or (month == "6" and day == "31"):
            day = "30"
        testeddate = '-'.join([year, month, day])
        
        diccionario ={

        "model":"myapp.libro",
        "pk": x+1,
        "fields":{
            "title": data[x]["title"],
            "authors": data[x]["authors"],
            "average_rating": float(data[x]["average_rating"]),
            "isbn": data[x]["isbn"],
            "isbn13": data[x]["isbn13"],
            "language_code": data[x]["language_code"],
            "num_pages": int(data[x]["num_pages"]),
            "ratings_count": int(data[x]["ratings_count"]),
            "text_reviews_count": int(data[x]["text_reviews_count"]),
            "publication_date": testeddate,
            "publisher": data[x]["publisher"]    

            }
        }
        lista.append(diccionario)

with open("books.json",'w') as nuevo:
    json.dump(lista, nuevo)
