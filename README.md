# phy1
## this is a repository for not using excel as data base, since it's file size is too large. It's not a good thing to use it as a repo. 
[old repository](https://github.com/chemmy-jack/phy)
[目前最新的資料整理](https://docs.google.com/spreadsheets/d/1CANEBRG2YRJyrXlpOOC52pnUBJTdqH6G90x_D38qdVU/edit?usp=sharing)
[目前蝴蝶資料](https://docs.google.com/spreadsheets/d/1zfbFTa0ONDA5KLNcvF6RCnSnSxjnCh9jZJ9CPZcXeJA/edit?usp=sharing)
[目前蝴蝶front資料](https://docs.google.com/spreadsheets/d/1cpXIM-xyUM_NZUEXTr3m5iaQ-iiMJKjRhuRAytge0l8/edit?usp=sharing)
[我的雲端硬碟公開在github之資料夾](https://drive.google.com/drive/folders/17HDjfx5OjlZcMptYHOPJgpGvJKZ_gNSd?usp=sharing)

## reminder for myself
- butterfly and ornithopter database should be seperated

## a simple guide
check required python package:
	- xlwings
	- vpython
	- matplotlib
	- tkinter
	- gitpython
	- json
	- sys
	- numpy
	- math
	- statistics

then in command line : 
	` git clone https://github.com/chemmy-jack/phy1.git ` 
	` cd phy1 ` 
	` python3 src/main.py ` 
	` type 1 <Enter> 2 <Enter> 2~14 <Enter> 2 <Enter> `


## required python extensions :
- json
- xlwings
- vpython
- matplotlib
- tkinter
- gitpython
- numpy

# new main structure
main structure :
main.py
	read and save to json database (visualize then save)
		from csv
		from xls
	visualization of data in json database
	export analysed json database in csv form

# new export analyse data include :
| title | abdomen angle | flapping angle | pitching angle | angle of attack | shift angle | x | y | | |
|-|-|-|-|-|-|-|-|-|-|
|1|
|2|
|3|
|...|

## to do list 
- read csv file 
	- store data button
	- degree on screen
	- inner coordinate show 
	- 3 analysing methods
		- seniors analyse1
		- my analyse1
		- my analyse2
- optimize vpython show
- analysed json
	- name ( same as file )
		- origin coordinate
		- analyse1
			- flapping
			- pitching
			- rotate
			- abdomen
		- analyse2
		- information
			- unit
			- filming date 
			- number of butterfly
			- number of filming
- information number of butterfly json
	- span
	- wing area
	- weight
	- breed
- write discription to readme
	- progress
		- film
		- mark feature points
		- analyse
			- definition of angles
	- time table(schedule) of contests

## some information for this project
- 目的：探討蝴蝶獨特的飛行
	- 目前從拍翼動態來研究
	- 製作拍翼機使變因可控，再透過改變拍翼機之參數觀察其不同
	- 正在嘗試以PIV將流場可視化, 從流場的角度探討,
- progress
	- butterfly
		- dynamic motion filming
		- use imagej(mtrack) manualy get cooradinate data
		- write python analyse script
		- copy data to excel and analyse with code
		- discuss on the analysed data
	- DIY butterfly ornithopter
- reference

