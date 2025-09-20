#uv run main.py -i colortest.png -p '255 0 0 , #00ff00 , #777777'
uv run main.py -i test.png -p '#ffffff , #000000 , 200 130 60' 
uv run main.py -i test.png -p '#ffffff , #000000 , 200 130 60 , #444444' -o test2_q.png --AddPalette --Image
uv run main.py -i test.png -p '#ffffff , #000000 , 200 130 60 ,#333333' -o test3_q.png --AddPalette --Image


#rm $(grep 'quantized.png')
