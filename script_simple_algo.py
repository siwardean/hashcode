class Library():
    def __init__(self, id, data, books, book_values):
        self.id = id
        self.nb_book = int(data[0])
        self.nb_day = int(data[1])
        self.nb_book_by_day = int(data[2])
        self.books = [Book(int(book),book_values) for book in books]
        self.books.sort(key=lambda x: x.value, reverse=True)
        
    def total_value(self):
        return sum(int(book.value) for book in self.books)
    
    def show_books(self):
        print()
        for book in self.books:
            print(book)
            
    def nb_book_readable(self, nb_day_max):
        return min(nb_day_max * self.nb_book_by_day, self.nb_book)
    
    def nb_book_read_with_sign(self, nb_day_max):
        return min((nb_day_max-self.nb_day) * self.nb_book_by_day, self.nb_book)
    
    def books_scan(self, day):
        return self.books[:max(0,self.nb_book_read_with_sign(day))]
    
    def score_max_actual(self, nb_day_max):
        return sum([book.value for book in self.books[:max(0,self.nb_book_read_with_sign(nb_day_max))]])
            
    def __str__(self):
        return "Librairie id : "+ str(self.id) + "\n NB Books : " + str(self.nb_book) + "\n NB Days : " + str(self.nb_day) + "\n NB books/day : " + str(self.nb_book_by_day)+ "\n Total value : " + str(self.total_value())
            
        
        
class Environement():
    def __init__(self, data):
        self.nb_book = int(data[0])
        self.nb_lib = int(data[1])
        self.nb_day_scan = int(data[2])
        
    def show_lib(self):
        for lib in self.libraries:
            print(lib)
            lib.show_books()
            print("---")
            print()
            
    def best_output(self):
        
        list_best_lib = []
        
        rest_lib = self.libraries
        days = self.nb_day_scan
        while days > 0 and len(rest_lib) != 0:  
            rest_lib.sort(key=lambda x: x.score_max_actual(days), reverse=True)
            best_lib = rest_lib[0]
            if (len(rest_lib) == 1):
                rest_lib = []
            else : 
                rest_lib = rest_lib[1:]
            list_best_lib.append((best_lib,days))
            
            days = days - best_lib.nb_day
                                 
        
        return list_best_lib
        
class Book():
    def __init__(self, _id, book_values):
        self.id = _id
        self.value = int(book_values[_id])
    def __str__(self):
        return "Book id : " + str(self.id) +" value : " + str(self.value)
    
    
def load(input_path):
    input_file = open(input_path,"r") 
    lines = input_file.read().split("\n")
    lines = [line.split(" ") for line in lines if line != ""]
    
    env = Environement(lines[0])
    i = 2
    libraries = []
    book_values = [val for val in lines[1]]
    while (i< len(lines)):
        data = lines[i] 
        i+=1
        books = lines[i]
        i+=1
        _id = int(i/2-1)
        libraries.append(Library(_id,data, books, book_values))
    libraries.sort(key=lambda x: x.total_value(), reverse=True)
    env.libraries = libraries
    return env, libraries

path_file = "./data/d_tough_choices"
print("_0_")
env, libraries = load(path_file + ".txt")
best_libs = env.best_output()
print("_1_")

def create_output(best_libs):
    output = ""
    output += str(len(best_libs)) 
    for lib, days in best_libs:
        books = lib.books_scan(days)
        if(len(books)>0):
            output +=" \n"
            output += str(lib.id-1) + " " + str(len(books)) +" \n"
            output += " ".join([str(book.id) for book in books])
        else :
            output +=" \n"
            output += str(lib.id-1) + " " + str(len(books)+1) +" \n"
            output += str(lib.books[0].id)
    return output  

print("-2-")
output = create_output(best_libs)

with open(path_file + '_output.txt', 'w') as the_file:
    the_file.write(output)