# PEC 4 Ana Blanco - twtter_nlp_uoc


## How to run the code
1. Unzip file
2. `cd ./twitter_nlp_uoc`
3. Copy `twitter_reduced.csv` file data inside `data` folder
4. You can create a new virtual enviroment and activate it:
   ```shell
   virtualenv venv
   source venv/bin/activate
   ``` 
5. Install the required modules:
   ```shell
   pip install -r requirements.txt
   ``` 
6. Finally execute the code:
   ```shell
   python3 main.py
   ```
   
NOTE: In case you get this error in the execution:
`UserWarning: Matplotlib is currently using agg, which is a non-GUI backend,
so cannot show the figure.`, the problem is that you are trying to display a
plot in a GUI window but you do not have a python module for GUI display.
In this case you can solve the problem intalling `tkinter`:
```shell
sudo apt-get install python3-tk
```

## *linter*
We are going to use `pylint` *linter*
### How to run *linter*
1. First install `pylint` library:
    ```bash
    sudo apt install pylint
    ```
2. Run the following command from the root folder:
    ```bash
    pylint *.py
    ```
### *linter* results  
```commandline
Your code has been rated at 10.00/10
```



## Tests
The tests are in located in the `test` folder.  
The code have been tested for the package `sentiment_analyzer`.
This package contains two modules:
- `menu.py`
- `utils.py`

All functions of these two modules have been tested except for the graphical ones:
`paint_2word_clouds` and `paint_2bars`.

### How to run the tests
Run the following command from the root folder:
```bash
python3 -m test.test_sentiment_analyzer
```

These are the test results:
```commandline
ok test_file_exists (__main__.TestMenu)
ok test_stop_between_steps (__main__.TestMenu)
ok test_create_bows_vocab (__main__.TestUtils)
ok test_create_cluster_bow (__main__.TestUtils)
ok test_join_dicts_bows (__main__.TestUtils)
ok test_preprocess_data (__main__.TestUtils)
ok test_preprocess_text (__main__.TestUtils)
ok test_remove_stop_words (__main__.TestUtils)
```

### Tests coverage

#### How to run the tests coverage
1. First install Coverage.py library:
    ```bash
    pip install coverage
    ```
2. Run the following commands from the root folder:
   ```bash
   coverage run -m test.test_sentiment_analyzer
   coverage report
   ```
3. We can obtain a more detailed html report with these commands:
   ```bash
   coverage run -m test.test_sentiment_analyzer
   coverage html
   ```
   Follow this link, after executing above commands, to open the html report:
   [Coverage HTML report](/htmlcov/index.html)

#### Tests coverage result
This is the tests coverage result for the package `sentiment_analyzer`:
```commandline
Name                          Stmts   Miss  Cover
-------------------------------------------------
sentiment_analyzer/menu.py       14      1    93%
sentiment_analyzer/utils.py      72     26    64%
-------------------------------------------------
TOTAL                            86     27    69%
```
