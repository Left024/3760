#!/bin/bash

:'
#测试用例
sonarr_eventtype="Grab"
sonarr_release_size="510205632"
sonarr_release_seasonnumber="1"
sonarr_release_title="The 100 Girlfriends Who Really, Really, Really, Really, REALLY Love You S1E7 [简繁日][内封][1080P][WEBRip][-喵萌奶茶屋&LoliHouse]"
sonarr_release_episodenumbers="7"
sonarr_release_episodetitles="Saying Hello to the Chemistry Girl"
sonarr_release_indexer="mikan_jproxy"
sonarr_release_customformatscore="500"
sonarr_series_title="The 100 Girlfriends Who Really, Really, Really, Really, REALLY Love You"
sonarr_series_year="2023"
sonarr_release_quality="WEBRip-1080p"
sonarr_series_imdbid="tt28919914"
sonarr_release_episodecount="1"
sonarr_release_customformat="Chinese|LoliHouse|喵萌奶茶屋|简|简繁|简繁日"
'

if [ "${sonarr_eventtype}" = "Grab" ]; then
    json="{
        \"sonarr_eventtype\":\"Grab\",
        \"sonarr_release_size\":\""${sonarr_release_size}"\",
        \"sonarr_release_seasonnumber\":\""${sonarr_release_seasonnumber}"\",
        \"sonarr_release_title\":\""${sonarr_release_title}"\",
        \"sonarr_release_episodenumbers\":\""${sonarr_release_episodenumbers}"\",
        \"sonarr_release_episodetitles\":\""${sonarr_release_episodetitles}"\",
        \"sonarr_release_indexer\":\""${sonarr_release_indexer}"\",
        \"sonarr_release_customformatscore\":\""${sonarr_release_customformatscore}"\",
        \"sonarr_series_title\":\""${sonarr_series_title}"\",
        \"sonarr_series_year\":\""${sonarr_series_year}"\",
        \"sonarr_release_quality\":\""${sonarr_release_quality}"\",
        \"sonarr_series_imdbid\":\""${sonarr_series_imdbid}"\",
        \"sonarr_release_episodecount\":\""${sonarr_release_episodecount}"\",
        \"sonarr_release_customformat\":\""${sonarr_release_customformat}"\",
        \"sonarr_series_id\":\""${sonarr_series_id}"\"
        }"
elif [ "${sonarr_eventtype}" = "SeriesDelete" ]; then
    json="{
        \"sonarr_eventtype\":\"SeriesDelete\",
        \"sonarr_series_path\":\""${sonarr_series_path}"\",
        \"sonarr_series_title\":\""${sonarr_series_title}"\",
        \"sonarr_series_imdbid\":\""${sonarr_series_imdbid}"\"
        }"
elif [ "${sonarr_eventtype}" = "EpisodeFileDelete" ]; then
    json="{
        \"sonarr_eventtype\":\"EpisodeFileDelete\",
        \"sonarr_episodefile_path\":\""${sonarr_episodefile_path}"\",
        \"sonarr_episodefile_seasonnumber\":\""${sonarr_episodefile_seasonnumber}"\",
        \"sonarr_episodefile_episodecount\":\""${sonarr_episodefile_episodecount}"\",
        \"sonarr_series_title\":\""${sonarr_series_title}"\",
        \"sonarr_series_year\":\""${sonarr_series_year}"\",
        \"sonarr_episodefile_episodenumbers\":\""${sonarr_episodefile_episodenumbers}"\",
        \"sonarr_series_imdbid\":\""${sonarr_series_imdbid}"\",
        \"sonarr_episodefile_episodetitles\":\""${sonarr_episodefile_episodetitles}"\",
        \"sonarr_episodefile_relativepath\":\""${sonarr_episodefile_relativepath}"\",
        \"sonarr_series_path\":\""${sonarr_series_path}"\",
        \"sonarr_series_id\":\""${sonarr_series_id}"\"
        }"
elif [ "${sonarr_eventtype}" = "Download" ]; then
    json="{
        \"sonarr_eventtype\":\"Download\",
        \"sonarr_isupgrade\":\""${sonarr_isupgrade}"\",
        \"sonarr_release_title\":\""${sonarr_release_title}"\",
        \"sonarr_episodefile_path\":\""${sonarr_episodefile_path}"\",
        \"sonarr_release_indexer\":\""${sonarr_release_indexer}"\",
        \"sonarr_episodefile_seasonnumber\":\""${sonarr_episodefile_seasonnumber}"\",
        \"sonarr_episodefile_episodecount\":\""${sonarr_episodefile_episodecount}"\",
        \"sonarr_series_title\":\""${sonarr_series_title}"\",
        \"sonarr_series_year\":\""${sonarr_series_year}"\",
        \"sonarr_episodefile_episodetitles\":\""${sonarr_episodefile_episodetitles}"\",
        \"sonarr_episodefile_episodenumbers\":\""${sonarr_episodefile_episodenumbers}"\",
        \"sonarr_series_imdbid\":\""${sonarr_series_imdbid}"\",
        \"sonarr_episodefile_customformat\":\""${sonarr_episodefile_customformat}"\",
        \"sonarr_episodefile_customformatscore\":\""${sonarr_episodefile_customformatscore}"\",
        \"sonarr_release_size\":\""${sonarr_release_size}"\",
        \"sonarr_series_id\":\""${sonarr_series_id}"\"
        }"
fi

/usr/bin/python3 /root/Sonarr/run.py "${json}" & #将 python 脚本地址修改为你的

exit
