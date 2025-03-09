# Stock App
Application for viewing stocks, stock news, stock graphs, developed with KivyMD and connect with yfinance API.

## Contributor
[@Worachat-Songmuangnu](https://github.com/Worachat-Songmuangnu) - Worachat Songmuangnu 6710110370 <br>
[@Pyneola](https://github.com/Pyneola) - Weera Arsasutcharit 6710110393 <br>
[@Jackyzaz](https://github.com/Jackyzaz) - Soravit Sukkarn 6710110428 <br>

## Overview


## Application Materials
### Widgets (47 totals)
```
main.kv (11)
  MDBoxLayout x1
  | MDNavigationRail x1
  |   |-MDNavigationRailFabButton x1
  |   |-MDNavigationRailItem x4
  |-MDScreenManager x1
      |-HomeScreen x1
      |-SearchScreen x1
      |-NewsScreen x1
      |-FavoriteScreen x1
```
```
HomeScreen.kv (9)
  HomeScreen
    |-MDBoxLayout x1
      |-MDBoxLayout x1
      |  |-MDBoxLayout x3  
      |  |-MDLabel x2
      |  |-MDRaisedButton x1
      |-ScrollView X1
```
```
NewsScreen.kv (24)
  <NewsScreen>
    |-MDBoxLayout x1
      |-MDBoxLayout x1
        |-MDBoxLayout x1
        |  |-MDBoxLayout x1
        |  | |-MDLabel x2 # Stock Info Section
        |  |-MDBoxLayout x1
        |    |-MDTextField x1
        |-MDBoxLayout x1
        |-MDBoxLayout x1
        |-MDBoxLayout x1
          |-MDScrollView x1
          |-MDGridLayout x1 # News Section
  <StockInfo>
    |-MDBoxLayout x1
    |  |-MDLabel x2
    |-MDBoxLayout x1
    |  |-MDLabel x2
    |-MDLabel x1

  <NewCard>
    |-MDLabel x4
```
```
SearchScreen.kv (3)
  <SearchScreen>
    |-MDTextField x1
    |-MDRaisedButton x1
    |-Widget x1 # Plot Graph Section

```
### Callbacks (totals)



## For Developer
### Start

```sh
python -m venv venv
```

### Window

```sh
venv\Scripts\activate
```

### Mac / Linux

```sh
source venv/bin/activate
```

### Install requirement

```sh
pip install -r requirements.txt
```

### Start App
```sh
python src/screens/main.py
```
