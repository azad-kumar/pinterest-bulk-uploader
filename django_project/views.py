from django.http import JsonResponse
from rest_framework.decorators import api_view
import requests
import os
from typing import IO
from django.http import FileResponse
from . import constants
from . import files


def Download(VideoUrl: str) -> bool:
    response = requests.get(VideoUrl)
    if response.status_code == 200:
        # folder_path = files.get_video_dir()
        file_name = constants.PINTEREST
        folder_path = constants.VIDEO
        unique_file_number = str(files.get_next_file_number(folder_path))
        extention = ".mp4"
        video_file_name = folder_path + "/" + file_name + unique_file_number + extention
        with open(video_file_name, "wb") as f:
            f.write(response.content)
        return True
    else:
        return False


@api_view(["GET", "POST"])
def DownloadVideo(request):
    if request.method == 'POST':
        link = request.data.get('VideoLink')
        if Download(link):
            DataResponse = {
                'status': True,
            }
            return JsonResponse(DataResponse)
        else:
            DataResponse = {
                'status': False,
            }
            return JsonResponse(DataResponse)
    else:
        DataResponse = {
            'status': False,
            'error': 'This endpoint only accepts POST requests',
        }
        return JsonResponse(DataResponse)


def ReturnVideoByIndex(self, index: int, random_str: str) -> IO:

    video_files = os.listdir(constants.VIDEO_DIR)
    if video_files:
        if len(video_files) < index:
            response = {'status': False, 'error': "video index out of range"}
            return JsonResponse(response)

        file_name = video_files[index]
        video_path = os.path.join(constants.VIDEO_DIR, file_name)
        try:
            file = open(video_path, 'rb')
            response = FileResponse(file, content_type='video/mp4')
            response[
                'Content-Disposition'] = f'attachment; filename="{file_name}"'.format(
                    file_name)
            return response
        except FileNotFoundError:
            response = {'status': False, 'error': 'video not found'}
    else:
        response = {'status': False, 'error': 'video directory not found'}
        return JsonResponse(response)


def Get_Remaining_Count(request=None):
    video_files = os.listdir(constants.VIDEO_DIR)
    Remaining_Count = 10 - len(video_files)
    if request != None:
        data = {
            'status': True,
            'Reamining_Count': Remaining_Count,
        }
        return JsonResponse(data)
    else:
        return Remaining_Count


def Download_Remaining(request) -> dict:
    Remaining_count = Get_Remaining_Count()
    if Remaining_count > 0:
        for i in range(Remaining_count):
            link_dict_response = requests.get("PRIVATE URL : NOT FOR PUBLIC")
            if link_dict_response.status_code == 200:
                if link_dict_response.json()['status'] is not False:
                    link = link_dict_response.json()['response']
                    payload = {'url': link}
                    try:
                        response = requests.post(
                            'PRIVATE URL : NOT FOR PUBLIC', data=payload)
                        if response.status_code == 200:
                            Download(response.json()['video_url'])
                            print(f"video no {i+1} downloaded")
                        else:
                            pass
                    except Exception as E:
                        print(E)
                        pass
                else:
                    response = {
                        'status': False,
                        'error': 'no video url in the Database'
                    }
                    return JsonResponse(response)
    response = {
        'status': True,
        'message': 'Remaining Videos Downloaded Succesfully'
    }
    return JsonResponse(response)
