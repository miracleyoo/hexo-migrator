import os
import re
import requests
import codecs

root = "./_posts"

def main():
    names=os.listdir(root)
    files=[i for i in names if i.endswith('.md') and not os.path.isdir(os.path.join(root, i)) and not i.startswith('.')]
    file_paths = [os.path.join(root, i) for i in files]
    dirs=[i for i in names if os.path.isdir(os.path.join(root, i)) and not i.startswith('.')]
    dir_paths = [os.path.join(root, i) for i in dirs]
    print(files)
    for file_iter in files:
        name_temp = os.path.splitext(os.path.split(file_iter)[-1])[0]
        if name_temp not in dirs:
            dir_temp = os.path.join(root, name_temp)
            os.mkdir(dir_temp)
        download(os.path.join(root,file_iter))

def download(file_path):
    print("==> Now dealing with file:", file_path)
    dir_name = os.path.splitext(os.path.split(file_path)[-1])[0]
    # filename = "test"
    name = file_path.split(u"/")
    filename = name[-1]
    with codecs.open(file_path, encoding="UTF-8") as f:
        text = f.read()
    # regex
    result = re.findall('!\[(.*)\]\((.*)\)', text)

    for i, content in enumerate(result):
        image_quote = content[0]
        image_url = content[1]
        try:
            # download img
            img_data = requests.get(image_url).content
            # img name spell
            image_name = image_url.strip("/").split("/")[-1]
            image_path = os.path.join(root, dir_name, image_name)
            print("==>", image_path, '~~~', image_url)
            # write to file
            with open(image_path, 'wb') as handler:
                handler.write(img_data)

            text=text.replace("!["+image_quote+"]("+image_url+")", "!["+image_quote+"]("+image_name+')')
        except:
            continue
    with codecs.open(file_path, mode="w+", encoding="UTF-8") as f:
        f.write(text)

if __name__ == "__main__":
    main()

