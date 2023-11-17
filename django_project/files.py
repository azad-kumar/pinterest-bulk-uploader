#header files
import os




def get_video_dir():
    # video_dir_path = os.getcwd() + "/" +constants.VIDEO_FOLDER_NAME
    video_dir_path = "django_project/videos"
    if video_dir_path:
        return video_dir_path
    else:
        print("video directory not found")
        return False

def get_next_file_number(path) -> str:
    file_list = os.listdir(path)
    if len(file_list) == 0:
        return "0"
    elif len(file_list) >= 0:
        return len(file_list)
    else:
        return False

