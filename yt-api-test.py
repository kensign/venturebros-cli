# -*- coding: utf-8 -*-

# Sample Python code for youtube.playlistItems.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os

import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]


def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    season_ids = ["EL4xt8EwQHBj4",
                  "ELMaIaxi9tPdo",
                  "ELBCAjzvSjE1w",
                  "EL96eWPWDC9Z4",
                  "ELSmv3U1eh5iA",
                  "ELJfT_4NxevdI6lGVBGsTSdQ",
                  "EL3Lt5Is3LD5N9z7OVCnVxxg"]

    youtube = googleapiclient.discovery.build(
        api_service_name,
        api_version,
        developerKey="AIzaSyAkBY5Dv5Xh0BjO8psqEWZlqLrcdl6UIiw")

    season_count = 1

    for season in season_ids:
        ep_num = 0
        season_request = youtube.playlistItems().list(
            part="contentDetails",
            maxResults=20,
            playlistId=season
        )

        season_response = season_request.execute()
        season_videos = season_response['items']

        for video_item in season_videos:
            video_id = video_item['contentDetails']['videoId']
            video_request = youtube.videos().list(
                part="snippet, contentDetails",
                id=video_id
            )

            video_response = video_request.execute()

            for video in video_response['items']:
                duration = video['contentDetails']['duration']
                ep_id = str(season_count) + "-" + str(ep_num)
                print(ep_id + ',' + duration + ',"' + video['snippet']['title'] + '"')
                ep_num += 1

        season_count += 1


if __name__ == "__main__":
    main()
