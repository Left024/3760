#!/bin/bash

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

current_time=$(date +"%Y-%m-%d %H:%M:%S")

/usr/bin/python3 /root/radarr/run.py "${json}" #将 python 脚本地址修改为你的

exit
