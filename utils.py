#coding=utf-8
import json
from qcloud_cos import CosClient
from qcloud_cos import UploadFileRequest, DelFileRequest,CreateFolderRequest,ListFolderRequest,StatFolderRequest,StatFileRequest,DelFolderRequest
from qcloud_image import Client
from qcloud_image import CIUrl, CIFile, CIBuffer, CIUrls, CIFiles, CIBuffers

appid = 100000000  # 替换为用户的appid
secret_id = u''  # 替换为用户的secret_id
secret_key = u''  # 替换为用户的secret_key
region_info = u"sh"  # 替换为用户的region，例如 sh 表示华东园区, gz 表示华南园区, tj 表示华北园区
bucket = u'test'
cos_client = CosClient(appid, secret_id, secret_key, region=region_info)

#查看文件属性
def stat_file_ret():
    request = StatFileRequest(bucket, u'/meizitu/meizitu/0067Dm70gy1fj4j5dexhbj30u011hwjl.jpg')
    stat_file_ret = cos_client.stat_file(request)
    print stat_file_ret

#上传文件
def upload_file(filename):
    request = UploadFileRequest(bucket, u'/sample_file.txt', u'local_file_1.txt')
    upload_file_ret = cos_client.upload_file(request)
#删除文件
def del_file(filename):
    request = DelFileRequest(bucket, u'%s'%filename)
    del_ret = cos_client.del_file(request)
    return  del_ret

#删除目录
def del_folder(path):
    request = DelFolderRequest(bucket, u'%s'%path)
    delete_folder_ret = cos_client.del_folder(request)
    return delete_folder_ret

#创建文件夹
def create_folder(path):
    request = CreateFolderRequest(bucket, u'%s'%path)
    create_folder_ret = cos_client.create_folder(request)
    print create_folder_ret

#查看文件夹列表
def list_folder_ret(path):
    request = ListFolderRequest(bucket, u'%s'%path)
    list_folder_ret = cos_client.list_folder(request)
    # print list_folder_ret['data']['infos'][0]
    print list_folder_ret
    source_url_list=[]
    # print list_folder_ret
    # print list_folder_ret['data']['infos']
    # print len(list_folder_ret['data']['infos'])
    for picture in list_folder_ret['data']['infos']:
        print picture
        picture_url = picture['name']
        source_url_list.append(picture_url)
    print len(source_url_list)
    return source_url_list


#查看文件夹属性
def stat_folder():
    request = StatFolderRequest(bucket, u'/meizitu/meizitu/')
    stat_folder_ret = cos_client.stat_folder(request)
    print stat_folder_ret

#鉴定图片
def porn_detect(data):
    print data
    client = Client(appid, secret_id, secret_key, bucket)
    client.use_http()
    client.set_timeout(30)
    a=client.porn_detect(CIUrls(data[0:5]))
    print a

if __name__=='__main__':
    # create_folder('/mztu/mztu01/')
    data= list_folder_ret('/meizitu/meizitu/')
    porn_detect(data)
    # stat_folder()