import calendar
from queries_db_script import *
from create_db_script import *
import matplotlib.pyplot as plt
from api_data_retrieve import *

con = mysql.connector.connect(
    host="localhost",
    port=3305,
    user="milanay1",
    database="milanay1",
    password="mila82183",
)
cursor = con.cursor()


def execute_query_genre(input_genre):
    if input_genre is None:
        # find all the genres to display to the user
        query = "SELECT name " \
                "FROM genres"
        cursor.execute(query)
        genres = [genre[0] for genre in cursor.fetchall()]
        genres_display_table = prettytable.PrettyTable(header=False)
        genres_display_table.add_rows([[genre] for genre in genres])
        print(genres_display_table)

        input_genre = input("Choose a genre from the above list: ")
        if input_genre not in genres:
            print("'{}' is not a valid genre.".format(input_genre))
            return
    results_table = query_1(input_genre, cursor)
    print("The top 5 profitable movies from the genre '{}' and their profits are:".format(input_genre))
    print(results_table)


def execute_query_actor(actor):
    if actor is None:
        print("Actor Helper - Find the best actor based on average movies popularity")
        actor = input("Enter the name of the actor you want to search for: ")
        if actor == "":
            print("Invalid input. Please enter a non-empty actor name.")
            return          
    result = query_2(actor, cursor)
    print("The average populairty of movies including '{}' is:".format(actor))
    print(result)
    
def execute_query_title(keyword):
    if keyword is None:
        print("Movie Title Helper - Find the best name for a movie")
        keyword = input("Enter a keyword to find the average revenue of movies containing your keyword in their title: ")
        if keyword == "":
            print("Invalid input. Please enter a non-empty keyword.")
            return        
    result = query_3(keyword, cursor)
    print("The average revenue of movies containing '{}' in their title is:".format(keyword))
    print(result)
    
def execute_query_runtime(budget):
    if budget is None:
        print("Runtime Helper - Find the best runtime for a movie with a given budget")
        try:
            budget = float(input("Enter the desired budget for the movie: "))
        except ValueError:
            print("Invalid input. Please enter a numeric value for the budget.")
            return
        if budget == 0:
            print("Invalid input. Please enter a non-zero value for the budget.")
            return
    print("The best runtime for a movie with a budget of ${} is:".format(budget))
    result = query_4(budget, cursor)
    print(result)

def execute_query_month(input_month):
    if input_month is None:
        # display all months to the user
        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                  "November", "December"]
        months_display = prettytable.PrettyTable(header=False)
        months_display.add_rows([[month] for month in months])
        print(months_display)
        input_month = input("Choose a month from the above list: ")
        if input_month not in months:
            print("'{}' is not a valid month.".format(input_month))
            return

    month_number = list(calendar.month_name).index(input_month)
    results_table = query_5(month_number, cursor).rows
    # display a graph with the average popularity of movies released on each day of the month
    days = [int(row[0]) for row in results_table]
    average_popularity = [float(row[1]) for row in results_table]
    print("Here is the average popularity of movies released on each day of the month you selected:")
    plt.figure(figsize=(10, 5))
    plt.bar(days, average_popularity)
    plt.title(f'Average Popularity of Movies Released Each Day in {input_month}')
    plt.xlabel('Day')
    plt.ylabel('Average Popularity')
    plt.grid(True)
    plt.show()


def run_examples():
    print("----------------Query Genre----------------")
    print(execute_query_genre('Action'))
    print("----------------Query Actor----------------")
    print(execute_query_actor('Tom Hanks'))
    print("----------------Query Title----------------")
    print(execute_query_title('Star'))
    print("----------------Query Runtime----------------")
    print(execute_query_runtime(150000000))
    print("----------------Query Date----------------")
    print(execute_query_month('January'))
    print()


def run_real():
    print("Choose a query to execute from the following options:")
    print("1: find the top 5 profitable movies from a selected genre")
    print("2: get the average popularity of movies with a selected actor")
    print("3: get the average popularity of movies with a keyword in the title")
    print("4: get the best runtime for a movie with a given budget")
    print("5: for each day of the selected month, find the average popularity of movies released on that day")
    query_num = input("Enter the query number you wish to execute: ")
    if query_num == '1':
        execute_query_genre(None)
    elif query_num == '2':
        execute_query_actor(None)
    elif query_num == '3':
        execute_query_title(None)
    elif query_num == '4':
        execute_query_runtime(None)
    elif query_num == '5':
        execute_query_month(None)
    else:
        print("Invalid query number.")


def main():
    while True:
        option = input(
            "Enter delete to delete all tables\n"
            "Enter create to create all Tables\n"
            "Enter initialize to insert data to the DB\n"
            "Enter run to run queries\n"
            "Enter example to run examples\n"
            "Enter exit to exit the program\n"
        )
        if option == 'delete':
            input("Are you sure you want to delete all tables? populating the db takes around 2hrs. (Y/N)")
            if input() == 'Y':
                delete_tables(cursor)
                print("All tables deleted.")
            else:
                print("Tables were not deleted.")
                return
            
        elif option == 'create':
            create_tables(cursor)
            print("All tables were created.")
            
        elif option == 'initialize':
            insert_data(cursor, con)
            print("All data was inserted.")
            
        elif option == 'run':
            run_real()
            
        elif option == 'example':
            run_examples()
        elif option == 'exit':
            break
        else:
            print("Invalid choice.")    

if __name__ == "__main__":
    main()
    
con.close()