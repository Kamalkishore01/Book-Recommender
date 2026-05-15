
from flask import Flask, render_template, request
import pickle
import numpy as np
popular_df=pickle.load(open('popular.pkl','rb'))
pt=pickle.load(open('pt.pkl','rb'))
books=pickle.load(open('books.pkl','rb'))
similarity_score=pickle.load(open('similarity_score.pkl','rb'))

app = Flask(__name__)

@app.route('/')

def index():

    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values),
                           Author=list(popular_df['Book-Author'].values),
                           Image=list(popular_df['Image-URL-S'].values),
                           Votes=list(popular_df['num_rating'].values),
                           rating=list(popular_df['avg_rating'].values),
    )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')





@app.route('/recommend_books', methods=['POST'] )

def recommend():
    User_input= request.form.get('User_input')
    index = np.where(pt.index == User_input)[0][0]
    similarties_items = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[
        1:6]  # List allt  5  items similar book in decesending order
    # doing sorting based on similarty score and enumerate we can get distance as well as index of book
    # After finding similar items start loop
    data = []
    for i in similarties_items:
        item = []
        # print(pt.index[i[0]]) #Print names and index
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-S'].values))
        data.append(item)

        print(data)

    return render_template('recommend.html',data=data)
if __name__ == '__main__':

    app.run(debug=True)

    #We Create 2 link one is for popular book 2nd one is recommendation page
    #First Create GUI