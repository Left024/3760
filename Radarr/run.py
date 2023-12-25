import json,os,sys,requests,re
from urllib.parse import urlparse

settingSaveLocation=os.path.realpath(__file__)[0:os.path.realpath(__file__).rfind("/")+1]+"settings.json"

#将文件内容转为 Json
def get_json_data(json_path):
    try:
        with open(json_path,'rb') as f:
            params = json.load(f)
        f.close()
    except FileNotFoundError:
        os.mknod(json_path)
        params={}
    except ValueError:
        params={}
    return params

settings=get_json_data(settingSaveLocation)

def sendMessageOnly(caption):
    url = 'https://api.telegram.org/bot'+settings['bot_token']+'/sendMessage'
    d = {'chat_id':settings['userid'], 'parse_mode': 'html', 'text': caption}
    retries = 0
    max_retries = 5
    retry_delay = 5
    while retries < max_retries:
        try:
            r = requests.post(url, json=d, timeout=30)
            # 如果响应码为200，表示成功发送消息
            #if r.status_code == 200:
            print(r.json())
            break  # 退出循环，不再重试
        except Exception as e:
            print(f"尝试失败，重试中 ({retries + 1}/{max_retries})...")
            time.sleep(retry_delay)
            retries += 1
    else:
        print(f"发送失败，达到最大重试次数 ({max_retries})，停止重试。")
        sys.exit()

def send_image_with_caption(image_path, caption):
    url = f"https://api.telegram.org/bot"+settings['bot_token']+"/sendPhoto"

    # 打开图片文件
    with open(image_path, 'rb') as photo:
        files = {'photo': photo}
        params = {'chat_id': settings['userid'], 'caption': caption, 'parse_mode': 'html'}

        retries = 0
        max_retries = 5
        retry_delay = 5
        while retries < max_retries:
            try:
                # 发送 POST 请求
                response = requests.post(url, files=files, params=params)
                # 打印响应
                #print(response.json())
                
                #if response.status_code == 200:
                print("\nsend_image_with_caption\n\n")
                result=response.json()
                print(response.json())
                if result['ok']:
                    break  # 退出循环，不再重试
                else:
                    print(f"send_image_with_caption失败，重试中 ({retries + 1}/{max_retries})...")
                    time.sleep(retry_delay)
                    retries += 1
            except Exception as e:
                print(f"尝试失败，重试中 ({retries + 1}/{max_retries})...")
                time.sleep(retry_delay)
                retries += 1
        else:
            print(f"发送图片文字失败，达到最大重试次数 ({max_retries})，停止重试。")
            sys.exit()

def download_image(url, folder_path, file_name=None):
    # 确保文件夹存在
    os.makedirs(folder_path, exist_ok=True)

    # 获取文件名和后缀
    if not file_name:
        file_name = os.path.basename(urlparse(url).path)
    base_name, file_extension = os.path.splitext(file_name)

    retries = 0
    max_retries = 5
    retry_delay = 5
    while retries < max_retries:
        try:
            # 下载图片
            response = requests.get(url)
            
            # 检查响应状态码
            if response.status_code == 200:
                # 拼接文件路径
                file_path = os.path.join(folder_path, file_name)

                # 保存图片
                with open(file_path, 'wb') as file:
                    file.write(response.content)

                return True
                #break
            else:
                return False
                #break
        except Exception as e:
            print(f"尝试下载图片失败，重试中 ({retries + 1}/{max_retries})...")
            time.sleep(retry_delay)
            retries += 1
    else:
        print(f"下载图片失败，达到最大重试次数 ({max_retries})，停止重试。")
        sys.exit()

def sendMessage(tmdbid,caption,imdbid):
    retries = 0
    max_retries = 5
    retry_delay = 5
    while retries < max_retries:
        try:
            movieImageDetail=json.loads(requests.get('https://api.themoviedb.org/3/movie/'+str(tmdbid)+'/images?api_key='+settings['themoviedb_api_key']).text)
            break
        except Exception as e:
            print(f"尝试获取imdb图片失败，重试中 ({retries + 1}/{max_retries})...")
            time.sleep(retry_delay)
            retries += 1
    else:
        print(f"获取imdb图片失败，达到最大重试次数 ({max_retries})，停止重试。")
        sys.exit()
    if 'backdrops' in movieImageDetail:
        if os.path.exists(settings['image_folder']+movieImageDetail['backdrops'][0]['file_path']):
            send_image_with_caption(settings['image_folder']+movieImageDetail['backdrops'][0]['file_path'],caption)
        else:
            result=download_image("https://image.tmdb.org/t/p/original"+movieImageDetail['backdrops'][0]['file_path'],settings['image_folder'])
            if result:
                send_image_with_caption(settings['image_folder']+movieImageDetail['backdrops'][0]['file_path'],caption)
            else:
                caption=caption+"\nhttps://www.imdb.com/title/"+imdbid
                sendMessageOnly(caption)
    else:
        caption=caption+"\nhttps://www.imdb.com/title/"+imdbid
        sendMessageOnly(caption)
    
def generateFormatedName(tmdbID):
    result=""
    for x in range(5):
        movieDetail=json.loads(requests.get('https://api.themoviedb.org/3/movie/'+str(tmdbID)+'?api_key='+settings['themoviedb_api_key']+'&language=zh-CN', timeout=10).text)
        if "\"success\":false" not in movieDetail:
            break
    if "\"success\":false" in movieDetail:
        result="error"
    else:
        for x in range(5):
            imdbDetail=json.loads(requests.get('https://www.omdbapi.com/?i='+movieDetail['imdb_id']+'&apikey='+settings['omdb_apikey'], timeout=10).text)
            if "\"Response\":\"False\"" not in imdbDetail:
                break
        if "\"Response\":\"False\"" in imdbDetail:
            result="error"
        else:
            result=movieDetail['title']+"."+imdbDetail['Title']+"."+imdbDetail['Year']
            result=re.sub('(,)|(，)|(：)|(:)|(\s)|(!)|(！)|(\?)|(？)|(\()|(（)|(\))|(）)|({)|(})|(;)|(；)|(\[)|(【)|(\])|(】)','.',result)
            result=re.sub('\.+','.',result)
    return result.title()

def list_files(folder_path):
    # 初始化文件列表
    files = []

    # 遍历文件夹下的所有文件
    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)

        # 检查文件是否为普通文件（不是文件夹）
        if os.path.isfile(filepath):
            # 提取文件名并添加到列表
            files.append(os.path.basename(filepath))

    return files

query=json.loads(sys.argv[1])

if query['radarr_movie_tmdbid']!="":
    movieName=generateFormatedName(query['radarr_movie_tmdbid'])
    if movieName == "error":
        movieName=query['radarr_movie_title']+" ("+query['radarr_movie_year']+")"
else:
    movieName=query['radarr_movie_title']+" ("+query['radarr_movie_year']+")"

if query['radarr_eventtype'] == "Grab":
    caption="<b>下载已添加</b>\n\n"
    
    caption=caption+"<b>电影：</b>"+movieName+"\n<b>种子：</b>"+query['radarr_release_title']+"\n"
    
    size = "{:.2f}".format(int(query['radarr_release_size'])/1073741824)
    
    caption=caption+"<b>大小：</b>"+str(size)+" GB\n<b>来源：</b>"+query['radarr_release_indexer']
    
    sendMessage(query['radarr_movie_tmdbid'],caption,query['radarr_movie_imdbid'])

elif query['radarr_eventtype'] == "MovieFileDelete":
    caption="<b>文件被删除</b>\n\n<b>电影：</b>"+movieName+"\n<b>文件路径：</b>"+query['radarr_moviefile_path']
    
    size = "{:.2f}".format(int(query['radarr_moviefile_size'])/1073741824)
    
    caption=caption+"\n<b>大小：</b>"+str(size)+" GB"
    
    sendMessage(query['radarr_movie_tmdbid'],caption,query['radarr_movie_imdbid'])
    
elif query['radarr_eventtype'] == "Download":
    if query['radarr_isupgrade']=="True":
        deleteFileName, file_extension = os.path.splitext(query['radarr_deletedrelativepaths'])
        newFileName, file_extension = os.path.splitext(query['radarr_moviefile_relativepath'])
        
        deleteFolder=settings['radarr_delete_folder']+"/"+os.path.basename(query['radarr_movie_path'])
        deleteFiles=list_files(deleteFolder)
        banExtension=['.mkv','.mp4']
        for files in deleteFiles:
            filesName, filesExtension = os.path.splitext(files)
            #print(filesExtension)
            if filesExtension not in banExtension:
                if deleteFileName in filesName:
                    newName=filesName.replace(deleteFileName, newFileName)+filesExtension
                else:
                    newName=files
                rr=os.popen('/usr/bin/mv "%s" "%s"' % (deleteFolder+"/"+files,query['radarr_movie_path']+"/"+newName)).readlines()
                
        caption="<b>升级完成</b>\n\n<b>电影：</b>"+movieName+"\n<b>文件路径：</b>"+query['radarr_moviefile_path']
        
        size = "{:.2f}".format(int(query['radarr_release_size'])/1073741824)
        caption=caption+"\n<b>大小：</b>"+str(size)+" GB\n<b>来源：</b>"+query['radarr_release_indexer']
    else:
        caption="<b>下载完成</b>\n\n<b>电影：</b>"+movieName+"\n<b>文件路径：</b>"+query['radarr_moviefile_path']
        
        size = "{:.2f}".format(int(query['radarr_release_size'])/1073741824)
        caption=caption+"\n<b>大小：</b>"+str(size)+" GB\n<b>来源：</b>"+query['radarr_release_indexer']
    
    sendMessage(query['radarr_movie_tmdbid'],caption,query['radarr_movie_imdbid'])
