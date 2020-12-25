from PIL import Image

img = Image.open('apple.png')
img = img.convert("RGB")
datas = img.getdata()

newData = []
for item in datas:
    if item[0] == 255 and item[1] == 255 and item[2] == 255:
        newData.append((255, 255, 255))
    else:
        if item[0] > 150:
            newData.append((100, 200, 100))
        else:
            newData.append(item)
            print(item)


img.putdata(newData)
img.save("converted_apple.png", "PNG")
