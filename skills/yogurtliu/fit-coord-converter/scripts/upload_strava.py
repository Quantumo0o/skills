#!/usr/bin/env python3
"""
上传转换后的FIT文件到Strava
"""
import sys
import requests

STRAVA_UPLOAD_URL = "https://www.strava.com/api/v3/uploads"
ACCESS_TOKEN = "98f4da29b5cbe0ea8acd1596b41424621cc9a8d0"

def upload_to_strava(file_path, activity_name=None, description=""):
    """上传FIT文件到Strava"""
    
    if not activity_name:
        # 从文件名提取活动名
        import os
        activity_name = os.path.splitext(os.path.basename(file_path))[0]
    
    with open(file_path, 'rb') as f:
        files = {'file': f}
        data = {
            'data_type': 'fit',
            'name': activity_name,
            'description': description,
            'external_identifier': f'openclaw_{int(__import__("time").time())}'
        }
        headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}
        
        response = requests.post(
            STRAVA_UPLOAD_URL,
            files=files,
            data=data,
            headers=headers
        )
        
        if response.status_code == 201:
            result = response.json()
            print(f"上传成功！活动ID: {result.get('id')}")
            print(f"活动链接: https://www.strava.com/activities/{result.get('id')}")
            return result
        else:
            print(f"上传失败: {response.status_code}")
            print(response.text)
            return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python upload_strava.py <file.fit> [活动名称]")
        sys.exit(1)
    
    file_path = sys.argv[1]
    activity_name = sys.argv[2] if len(sys.argv) > 2 else None
    
    upload_to_strava(file_path, activity_name)