#uv run main.py -i colortest.png -p '255 0 0 , #00ff00 , #777777'
#uv run main.py -i test.png -p '#ffffff , #000000 , 200 130 60' 
#uv run main.py -i test.png -p '#ffffff , #000000 , 200 130 60 , #444444' -o test2_q.png --AddPalette --Image
#uv run main.py -i test.png -p '#ffffff , #000000 , 200 130 60 ,#333333' -o test_q_pal.png --AddPalette --Image
#uv run main.py -i test.png -p '#ffffff , #000000 , 200 130 60 ,#333333' -o test_q.png --Image
#uv run main.py -i test.png -p '#ffffff , #000000 , 200 130 60 ,#333333' -o test_q.png
#uv run main.py -i comicbook.png  -o spiderman.png --Image --AddPalette
#uv run main.py -i comicbook.png  -o spiderman.png --Image --AddPalette


#uv run main.py -i test.png  -o bo2.png --Extrude bitmap -p '191 131 73 , #ffffff , #000000 ,51 51 51 ' 

uv run main.py -i album.png  -o x.png --Image -p '#000000 , #ffffff , #888888 , #ff0000  ' 
uv run main.py -i album.png  -o xp.png --Image -p '#000000 , #ffffff , #888888 , #ff0000  ' --AddPalette 
