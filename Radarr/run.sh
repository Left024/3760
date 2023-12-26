#!/bin/bash

: '
radarr_eventtype="Grab"
radarr_movie_imdbid="tt1670345"
radarr_movie_title="Now You See Me"
radarr_movie_year="2013"
radarr_release_quality="Remux-2160p"
radarr_release_size="56144584704"
radarr_release_title="Now You See Me 2013 Theatrical 2160p UHD BluRay REMUX HDR HEVC Atmos-EPSiLON"
radarr_release_indexer="TorrentLeech"
radarr_movie_tmdbid="75656"
'

if [ "${radarr_eventtype}" = "Grab" ]; then
    json="{
        \"radarr_eventtype\":\"Grab\",
        \"radarr_movie_imdbid\":\""${radarr_movie_imdbid}"\",
        \"radarr_movie_title\":\""${radarr_movie_title}"\",
        \"radarr_movie_year\":\""${radarr_movie_year}"\",
        \"radarr_release_quality\":\""${radarr_release_quality}"\",
        \"radarr_release_size\":\""${radarr_release_size}"\",
        \"radarr_release_title\":\""${radarr_release_title}"\",
        \"radarr_release_indexer\":\""${radarr_release_indexer}"\",
        \"radarr_movie_tmdbid\":\""${radarr_movie_tmdbid}"\"
        }"
elif [ "${radarr_eventtype}" = "MovieFileDelete" ]; then
    json="{
        \"radarr_eventtype\":\"MovieFileDelete\",
        \"radarr_movie_imdbid\":\""${radarr_movie_imdbid}"\",
        \"radarr_movie_title\":\""${radarr_movie_title}"\",
        \"radarr_movie_year\":\""${radarr_movie_year}"\",
        \"radarr_moviefile_path\":\""${radarr_moviefile_path}"\",
        \"radarr_moviefile_size\":\""${radarr_moviefile_size}"\",
        \"radarr_moviefile_quality\":\""${radarr_moviefile_quality}"\",
        \"radarr_movie_tmdbid\":\""${radarr_movie_tmdbid}"\"
        }"
elif [ "${radarr_eventtype}" = "Download" ]; then
    if [ "${radarr_isupgrade}" = "True" ]; then
        json="{
        \"radarr_eventtype\":\"Download\",
        \"radarr_isupgrade\":\""${radarr_isupgrade}"\",
        \"radarr_movie_imdbid\":\""${radarr_movie_imdbid}"\",
        \"radarr_movie_title\":\""${radarr_movie_title}"\",
        \"radarr_movie_year\":\""${radarr_movie_year}"\",
        \"radarr_moviefile_relativepath\":\""${radarr_moviefile_relativepath}"\",
        \"radarr_release_size\":\""${radarr_release_size}"\",
        \"radarr_moviefile_quality\":\""${radarr_moviefile_quality}"\",
        \"radarr_release_title\":\""${radarr_release_title}"\",
        \"radarr_movie_path\":\""${radarr_movie_path}"\",
        \"radarr_deletedrelativepaths\":\""${radarr_deletedrelativepaths}"\",
        \"radarr_release_indexer\":\""${radarr_release_indexer}"\",
        \"radarr_movie_tmdbid\":\""${radarr_movie_tmdbid}"\",
        \"radarr_moviefile_path\":\""${radarr_moviefile_path}"\"
        }"
    else
        json="{
        \"radarr_eventtype\":\"Download\",
        \"radarr_isupgrade\":\""${radarr_isupgrade}"\",
        \"radarr_movie_imdbid\":\""${radarr_movie_imdbid}"\",
        \"radarr_movie_title\":\""${radarr_movie_title}"\",
        \"radarr_movie_year\":\""${radarr_movie_year}"\",
        \"radarr_moviefile_relativepath\":\""${radarr_moviefile_relativepath}"\",
        \"radarr_release_size\":\""${radarr_release_size}"\",
        \"radarr_moviefile_quality\":\""${radarr_moviefile_quality}"\",
        \"radarr_release_title\":\""${radarr_release_title}"\",
        \"radarr_movie_path\":\""${radarr_movie_path}"\",
        \"radarr_deletedrelativepaths\":\""${radarr_deletedrelativepaths}"\",
        \"radarr_release_indexer\":\""${radarr_release_indexer}"\",
        \"radarr_moviefile_path\":\""${radarr_moviefile_path}"\",
        \"radarr_movie_tmdbid\":\""${radarr_movie_tmdbid}"\"
        }"
    fi
fi

/usr/bin/python3 /root/Radarr/run.py "${json}" & #将 python 脚本地址修改为你的

exit
