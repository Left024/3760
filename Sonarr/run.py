import json,os,sys,requests,re,time
from urllib.parse import urlparse

settingSaveLocation=os.path.realpath(__file__)[0:os.path.realpath(__file__).rfind("/")+1]+"settings.json"
cacheSaveLocation=os.path.realpath(__file__)[0:os.path.realpath(__file__).rfind("/")+1]+"cache.json"

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

def write_json_data(dict,path):
    with open(path,'w') as r:
        json.dump(dict,r,indent=4)
    r.close()

def sendMessageOnly(caption):
    retries = 0
    max_retries = 5
    retry_delay = 5
    while retries < max_retries:
        try:
            url = 'https://api.telegram.org/bot'+settings['bot_token']+'/sendMessage'
            d = {'chat_id':settings['userid'], 'parse_mode': 'html', 'text': caption}
            r = requests.post(url, json=d, timeout=10)
            
            # 如果响应码为200，表示成功发送消息
            #if r.status_code == 200:
            print("\n\nsendMessageOnly\n\n")
            print(r.json())
            break  # 退出循环，不再重试
        except Exception as e:
            print(f"nsendMessageOnly失败，重试中 ({retries + 1}/{max_retries})...")
            time.sleep(retry_delay)
            retries += 1
    else:
        print(f"sendMessageOnly，达到最大重试次数 ({max_retries})，停止重试。")
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
                response = requests.post(url, files=files, params=params, timeout=10)
                # 如果响应码为200，表示成功发送消息
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
                print(f"send_image_with_caption失败，重试中 ({retries + 1}/{max_retries})...")
                time.sleep(retry_delay)
                retries += 1
        else:
            print(f"send_image_with_caption，达到最大重试次数 ({max_retries})，停止重试。")
            sys.exit()

def download_image(url, folder_path, file_name=None):
    # 确保文件夹存在
    os.makedirs(folder_path, exist_ok=True)

    # 获取文件名和后缀
    if not file_name:
        file_name = os.path.basename(urlparse(url).path)
    base_name, file_extension = os.path.splitext(file_name)

    # 下载图片
    retries = 0
    max_retries = 5
    retry_delay = 5
    while retries < max_retries:
        try:
            response = requests.get(url, timeout=10)
    
            # 检查响应状态码
            #if response.status_code == 200:
            # 拼接文件路径
            file_path = os.path.join(folder_path, file_name)

            # 保存图片
            with open(file_path, 'wb') as file:
                file.write(response.content)

            return True
        except Exception as e:
            print(f"下载图片失败，重试中 ({retries + 1}/{max_retries})...")
            time.sleep(retry_delay)
            retries += 1
    else:
        print(f"下载图片失败，达到最大重试次数 ({max_retries})，停止重试。")
        sys.exit()

def sendMessage(tmdbid,caption,season,episode,imdbid,isSingleEpisode):
    filePath=None
    retries = 0
    max_retries = 5
    retry_delay = 5
    while retries < max_retries:
        try:
            if isSingleEpisode:
                tvImage=json.loads(requests.get('https://api.themoviedb.org/3/tv/'+str(tmdbid)+'/season/'+season+'/episode/'+episode+'/images?api_key='+settings['themoviedb_api_key'], timeout=10).text)
                if 'stills' in tvImage and len(tvImage['stills'])>0 :
                    filePath=tvImage['stills'][0]['file_path']
                else:
                    tvImage=json.loads(requests.get('https://api.themoviedb.org/3/tv/'+str(tmdbid)+'/images?api_key='+settings['themoviedb_api_key'], timeout=10).text)
                    if 'backdrops' in tvImage and len(tvImage['backdrops'])>0:
                        filePath=tvImage['backdrops'][0]['file_path']
                    else:
                        filePath=None
            else:
                tvImage=json.loads(requests.get('https://api.themoviedb.org/3/tv/'+str(tmdbid)+'/images?api_key='+settings['themoviedb_api_key'], timeout=10).text)
                if 'backdrops' in tvImage and len(tvImage['backdrops'])>0:
                    filePath=tvImage['backdrops'][0]['file_path']
                else:
                    filePath=None
            break
        except Exception as e:
            print(f"sendMessage失败，重试中 ({retries + 1}/{max_retries})...")
            time.sleep(retry_delay)
            retries += 1
    else:
        print(f"sendMessage，达到最大重试次数 ({max_retries})，停止重试。")
        sys.exit()
    
    if filePath != None:
        if os.path.exists(settings['image_folder']+filePath):
            send_image_with_caption(settings['image_folder']+filePath,caption)
        else:
            result=download_image("https://image.tmdb.org/t/p/original"+filePath,settings['image_folder'])
            if result:
                send_image_with_caption(settings['image_folder']+filePath,caption)
            else:
                caption=caption+"\nhttps://www.imdb.com/title/"+imdbid
                sendMessageOnly(caption)
    else:
        caption=caption+"\nhttps://www.imdb.com/title/"+imdbid
        sendMessageOnly(caption)
    
def generateFormatedName(name,year):
    retries = 0
    max_retries = 5
    retry_delay = 5
    while retries < max_retries:
        try:
            result=""
            tvSearch=json.loads(requests.get("https://api.themoviedb.org/3/search/tv?api_key="+settings['themoviedb_api_key']+"&page=1&include_adult=false&query="+name+"&language=zh-CN&year="+year, timeout=10).text)
            if len(tvSearch['results'])>0:
                tvDetailEng=json.loads(requests.get('https://api.themoviedb.org/3/tv/'+str(tvSearch['results'][0]['id'])+'?api_key='+settings['themoviedb_api_key']+'&language=en-US', timeout=10).text)
                
                result=tvSearch['results'][0]['name']+"."+tvDetailEng['name']+"."+tvDetailEng['first_air_date'][0:4]
                result=re.sub('(,)|(，)|(：)|(:)|(\s)|(!)|(！)|(\?)|(？)|(\()|(（)|(\))|(）)|({)|(})|(;)|(；)|(\[)|(【)|(\])|(】)','.',result)
                result=re.sub('\.+','.',result)
                return result.title(),tvDetailEng['id']
            else:
                return "error","error"
            #break
        except Exception as e:
            print(f"generateFormatedName失败，重试中 ({retries + 1}/{max_retries})...")
            time.sleep(retry_delay)
            retries += 1
    else:
        print(f"generateFormatedName，达到最大重试次数 ({max_retries})，停止重试。")
        return "error","error"

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

def getSeriesYear(imdbID):
    retries = 0
    max_retries = 5
    retry_delay = 5
    while retries < max_retries:
        try:
            omdb=json.loads(requests.get("https://www.omdbapi.com/?i="+imdbID+"&apikey="+settings['omdb_apikey'], timeout=10).text)
            return omdb['Year']
            #break
        except Exception as e:
            print(f"getSeriesYear失败，重试中 ({retries + 1}/{max_retries})...")
            time.sleep(retry_delay)
            retries += 1
    else:
        print(f"omdb失败，达到最大重试次数 ({max_retries})，停止重试。")
        return ""

def getFolderSize(folder_path):
    total_size = 0
    
    # 使用 os.walk 遍历文件夹内的所有文件和子文件夹
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            # 获取文件的完整路径
            file_path = os.path.join(dirpath, filename)
            
            # 累加文件大小
            total_size += os.path.getsize(file_path)
    
    # 将字节数转换为更容易理解的单位（MB 或 GB）
    if total_size < 1024 * 1024 * 1024:  # 小于1GB
        size_str = f"{total_size / (1024 * 1024):.2f} MB"
    else:
        size_str = f"{total_size / (1024 * 1024 * 1024):.2f} GB"
    
    return size_str

def getFileSize(file_path):
    try:
        # 使用 os.path.getsize 获取文件大小（字节数）
        size_bytes = os.path.getsize(file_path)

        # 将字节数转换为更容易理解的单位（KB、MB、GB等）
        if size_bytes < 1024:
            size_str = f"{size_bytes} bytes"
        elif size_bytes < 1024 * 1024:
            size_str = f"{size_bytes / 1024:.2f} KB"
        elif size_bytes < 1024 * 1024 * 1024:
            size_str = f"{size_bytes / (1024 * 1024):.2f} MB"
        else:
            size_str = f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"

        return size_str
    except Exception as e:
        return "getFileSize error"

def get_last_part_after_slash(input_string):
    # 使用 rfind 方法找到最后一个 "/" 的索引
    last_slash_index = input_string.rfind("/")

    # 判断是否找到了 "/"
    if last_slash_index != -1:
        # 使用切片获取最后一个 "/" 之后的部分
        result = input_string[last_slash_index + 1:]
        return result
    else:
        # 如果没有找到 "/", 返回整个字符串
        return input_string

def getTagBySize(size):
    if size>5*1073741824 and size<=10*1073741824:
        return "SP_5"
    elif size>10*1073741824 and size<=15*1073741824:
        return "SP_10"
    elif size>15*1073741824 and size<=20*1073741824:
        return "SP_15"
    elif size>20*1073741824 and size<=30*1073741824:
        return "SP_20"
    elif size>30*1073741824 and size<=40*1073741824:
        return "SP_30"
    elif size>40*1073741824 and size<=50*1073741824:
        return "SP_40"
    elif size>50*1073741824 and size<=60*1073741824:
        return "SP_50"
    elif size>60*1073741824 and size<=70*1073741824:
        return "SP_60"
    elif size>70*1073741824 and size<=80*1073741824:
        return "SP_70"
    elif size>80*1073741824 and size<=90*1073741824:
        return "SP_80"
    elif size>100*1073741824 and size<=110*1073741824:
        return "SP_100"
    elif size>110*1073741824 and size<=120*1073741824:
        return "SP_110"
    else:
        return ""
    
def addTagToFileName(fileName,tag):
    cache=get_json_data(cacheSaveLocation)
    try:
        # 获取旧文件名
        old_name = os.path.basename(fileName)
        if " - " in old_name:
            new_name=old_name.replace(" - "," - "+tag+".")
        else:
            new_name=old_name+"."+tag
            
        # 构建新的完整路径
        new_path = os.path.join(os.path.dirname(fileName), new_name)
        
        os.rename(fileName, new_path)
        cache['rename'][fileName]=new_path
        write_json_data(cache,cacheSaveLocation)
        return new_path
        #print(f"File '{old_name}' has been renamed to '{new_name}'.")
    except Exception as e:
        print(f"重命名错误: {e}")
        return False

def refreshSeries(id):
    payload = json.dumps({
        "name": "RefreshSeries",
        "seriesId": id
    })
    headers = {
        'X-Api-Key': settings['sonarr_api_key'],
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", settings['sonarr_adress']+"/api/v3/command", headers=headers, data=payload, timeout=10)

query=json.loads(sys.argv[1])
print(sys.argv[1])
#query=json.loads('{"sonarr_eventtype": "Grab", "sonarr_release_size": "653493504", "sonarr_release_seasonnumber": "1", "sonarr_release_title": "Undead Unluck - S01E09 -  [1080P][Baha][WEB-DL][AAC AVC][CHT][MP4][ANi]", "sonarr_release_episodenumbers": "9", "sonarr_release_episodetitles": "Return", "sonarr_release_indexer": "mikan_ani", "sonarr_release_customformatscore": "115", "sonarr_series_title": "Undead Unluck", "sonarr_series_year": "2023", "sonarr_release_quality": "WEBDL-1080p", "sonarr_series_imdbid": "tt21927720", "sonarr_release_episodecount": "1", "sonarr_release_customformat": "ANI|Chinese|CHT"}')

if query['sonarr_eventtype'] == "SeriesDelete":
    year=getSeriesYear(query['sonarr_series_imdbid'])
else:
    year=query['sonarr_series_year']

tvName,tmdbID=generateFormatedName(query['sonarr_series_title'],year)

if query['sonarr_eventtype'] == "Grab" or query['sonarr_eventtype'] == "EpisodeFileDelete" or query['sonarr_eventtype'] == "Download":
    if query['sonarr_eventtype'] == "Grab":
        seasonnumber=query['sonarr_release_seasonnumber']
        episodecount=query['sonarr_release_episodecount']
        episodenumbers=query['sonarr_release_episodenumbers']
        episodetitles=query['sonarr_release_episodetitles']
    elif query['sonarr_eventtype'] == "EpisodeFileDelete" or query['sonarr_eventtype'] == "Download":
        seasonnumber=query['sonarr_episodefile_seasonnumber']
        episodecount=query['sonarr_episodefile_episodecount']
        episodenumbers=query['sonarr_episodefile_episodenumbers']
        episodetitles=query['sonarr_episodefile_episodetitles']
        
    if int(seasonnumber)<10:
        season="0"+seasonnumber
    else:
        season=str(seasonnumber)

    if int(episodecount)>1:
        episodeList=episodenumbers.split(',')
        if int(episodeList[0])<10:
            episodeStart="0"+episodeList[0]
        else:
            episodeStart=episodeList[0]
        
        if int(episodeList[len(episodeList)-1])<10:
            episodeEnd="0"+episodeList[len(episodeList)-1]
        else:
            episodeEnd=episodeList[len(episodeList)-1]
        
        episode=episodeStart+"-E"+episodeEnd
        fullEpisode="S"+season+"E"+episode
    else:
        if int(episodenumbers)<10:
            episode="0"+episodenumbers
        else:
            episode=str(episodenumbers)
        
        fullEpisode="S"+season+"E"+episode+" - "+episodetitles

if tvName=="error":
    tvName=query['sonarr_series_title']+" ("+year+")"

if query['sonarr_eventtype'] == "Grab":
    caption="<b>下载已添加</b>\n\n"
    
    caption=caption+"<b>剧集：</b>"+tvName+"\n<b>集：</b>"+fullEpisode+"\n<b>种子：</b>"+query['sonarr_release_title']+"\n"
    
    if int(query['sonarr_release_size'])<1073741824:
        size = "{:.2f}".format(int(query['sonarr_release_size'])/1048576)+" MB"
    else:
        size = "{:.2f}".format(int(query['sonarr_release_size'])/1073741824)+" GB"
    
    caption=caption+"<b>大小：</b>"+str(size)+"\n<b>来源：</b>"+query['sonarr_release_indexer']+"\n<b>自定义格式：</b>"+query['sonarr_release_customformat']+"\n<b>自定义格式评分：</b>"+query['sonarr_release_customformatscore']
    
    if tvName==query['sonarr_series_title']+" ("+year+")":
        caption=caption+"\nhttps://www.imdb.com/title/"+query['sonarr_series_imdbid']
        sendMessageOnly(caption)
    else:
        if int(query['sonarr_release_episodecount'])>1:
            sendMessage(tmdbID,caption,query['sonarr_release_seasonnumber'],query['sonarr_release_episodenumbers'],query['sonarr_series_imdbid'],False)
        else:
            sendMessage(tmdbID,caption,query['sonarr_release_seasonnumber'],query['sonarr_release_episodenumbers'],query['sonarr_series_imdbid'],True)

elif query['sonarr_eventtype'] == "SeriesDelete":
    caption="<b>剧集文件夹被删除</b>\n\n<b>剧集：</b>"+tvName+"\n<b>文件夹路径：</b>"+query['sonarr_series_path']
    
    caption=caption+"\n<b>大小：</b>"+getFolderSize(settings['sonarr_delete_folder']+"/"+get_last_part_after_slash(query['sonarr_series_path']))
    
    if tvName==query['sonarr_series_title']+" ("+year+")":
        caption=caption+"\nhttps://www.imdb.com/title/"+query['sonarr_series_imdbid']
        sendMessageOnly(caption)
    else:
        sendMessage(tmdbID,caption,"1","1",query['sonarr_series_imdbid'],False)

elif query['sonarr_eventtype'] == "EpisodeFileDelete":
    cache=get_json_data(cacheSaveLocation)
    if query['sonarr_episodefile_path'] in cache['rename']:
        caption="<b>剧集被重命名</b>\n\n"
        fileLocation=cache['rename'][query['sonarr_episodefile_path']]
        fileSize=getFileSize(cache['rename'][query['sonarr_episodefile_path']])
    else:
        caption="<b>剧集被删除</b>\n\n"
        fileLocation=query['sonarr_episodefile_path']
        fileSize=getFileSize(settings['sonarr_delete_folder']+"/"+get_last_part_after_slash(query['sonarr_series_path'])+"/"+query['sonarr_episodefile_relativepath'])
    
    caption=caption+"<b>剧集：</b>"+tvName+"\n<b>文件路径：</b>"+fileLocation
    
    caption=caption+"\n<b>大小：</b>"+fileSize
    
    refreshSeries(int(query['sonarr_series_id']))
    
    if tvName==query['sonarr_series_title']+" ("+year+")":
        caption=caption+"\nhttps://www.imdb.com/title/"+query['sonarr_series_imdbid']
        sendMessageOnly(caption)
    else:
        if int(query['sonarr_episodefile_episodecount'])>1:
            sendMessage(tmdbID,caption,query['sonarr_episodefile_seasonnumber'],query['sonarr_episodefile_episodenumbers'],query['sonarr_series_imdbid'],False)
        else:
            sendMessage(tmdbID,caption,query['sonarr_episodefile_seasonnumber'],query['sonarr_episodefile_episodenumbers'],query['sonarr_series_imdbid'],True)

elif query['sonarr_eventtype'] == "Download":
    if query['sonarr_isupgrade'] == "True":
        caption="<b>剧集质量已升级</b>\n\n"
    else:
        caption="<b>剧集已下载</b>\n\n"
        
    caption=caption+"<b>剧集：</b>"+tvName+"\n<b>集：</b>"+fullEpisode+"\n<b>种子：</b>"+query['sonarr_release_title']+"\n"
        
    localPath=query['sonarr_episodefile_path']
    
    isSeasonPack = re.search( r'(\.S\d+\.)|(\sS\d+\s)|(\.S\d+E\d+-E?\d+\.)|(\.S\d+E\d+–E?\d+\.)|(\sS\d+E\d+-E?\d+\s)|(\sS\d+E\d+–E?\d+\s)|(\.S\d+E\d+~E?\d+\.)|(\sS\d+E\d+~E?\d+\s)', query['sonarr_release_title'], re.I)

    fileSize=getFileSize(query['sonarr_episodefile_path'])
    if isSeasonPack:
        tag=getTagBySize(int(query['sonarr_release_size']))
        if tag not in query['sonarr_episodefile_path']:
            rename=addTagToFileName(query['sonarr_episodefile_path'],tag)
            if rename:
                localPath=rename
                fileSize=getFileSize(localPath)
            refreshSeries(int(query['sonarr_series_id']))
        
    caption=caption+"<b>本地路径：</b>"+localPath+"\n"+"<b>大小：</b>"+fileSize+"\n<b>来源：</b>"+query['sonarr_release_indexer']+"\n<b>自定义格式：</b>"+query['sonarr_episodefile_customformat']+"\n<b>自定义格式评分：</b>"+query['sonarr_episodefile_customformatscore']
    
    if tvName==query['sonarr_series_title']+" ("+year+")":
        caption=caption+"\nhttps://www.imdb.com/title/"+query['sonarr_series_imdbid']
        sendMessageOnly(caption)
    else:
        if int(query['sonarr_episodefile_episodecount'])>1:
            sendMessage(tmdbID,caption,query['sonarr_episodefile_seasonnumber'],query['sonarr_episodefile_episodenumbers'],query['sonarr_series_imdbid'],False)
        else:
            sendMessage(tmdbID,caption,query['sonarr_episodefile_seasonnumber'],query['sonarr_episodefile_episodenumbers'],query['sonarr_series_imdbid'],True)
