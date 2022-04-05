import os
from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split

PATH = Path(__file__).parent.absolute()
DIR_NAME = "ml-1m"


def load_movie_data():
    movies_file = os.path.join(PATH, DIR_NAME, "movies.dat")
    col_names = ["movie_id", "Title", "Genere"]
    df_movie = pd.read_csv(movies_file, sep="::", engine="python",
                           encoding='latin-1', names=col_names)
    df_movie["Genere"] = df_movie["Genere"].str.split('|')
    return df_movie


def load_user_data():
    users_file = os.path.join(PATH, DIR_NAME, "users.dat")
    col_names = ["user_id", "gender", "age", "occupation", "Zip-code"]
    df_user = pd.read_csv(users_file, encoding="utf-8",
                          sep="::", names=col_names, engine="python")
    return df_user


def load_rating_data():
    ratings_file = os.path.join(PATH, DIR_NAME, "ratings.dat")
    col_names = [
        "user_id", "movie_id", "rating", "timestamp"]
    df_rating = pd.read_csv(ratings_file, sep="::",
                            engine="python", names=col_names)
    return df_rating


def load_data():

    def get_col_num(col_name: str):
        return {col_name: x[col_name].unique().shape[0]+1}
    df_user = load_user_data()
    df_rating = load_rating_data()

    ID_col = 'user_id'
    item_cols = ['age', 'gender', 'occupation']
    context_cols = ['movie_id']
    columns = [ID_col] + context_cols + item_cols

    result = df_rating.set_index("user_id").join(df_user.set_index("user_id"))
    result["user_id"] = result.index
    result["gender"] = result["gender"].apply(lambda x: 0 if x == "M" else 1)
    x = result[columns].astype(float)

    y = result[["rating"]].apply(lambda x: x/5).to_numpy().astype(float)

    num_item_cols = [get_col_num(item_col) for item_col in item_cols]
    # num_context_cols = [get_col_num(context_col) for context_col in context_cols]

    # some pre-processing
    num_words_dict = {
        **get_col_num(ID_col),
        'movie_id': 4001
    }

    for num_item_col in num_item_cols:
        num_words_dict.update(num_item_col)

    # for num_context_col in num_context_cols:
    #     num_words_dict.update(num_context_col)
    return x, y, num_words_dict, columns


if __name__ == "__main__":

    x, y, num_words_dict, columns = load_data()
    print(num_words_dict)
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=42)
    print(x_train)
    print(x_test)