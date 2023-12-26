#!/bin/bash

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

/usr/bin/python3 /root/Sonarr/run.py "${json}" &

exit
