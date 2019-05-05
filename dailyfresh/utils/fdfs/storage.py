from django.core.files.storage import Storage
from fdfs_client.client import Fdfs_client
from django.conf import settings

class FDFSStorage(Storage):

    def __init__(self, client_conf=None, base_url=None):
        if client_conf is None:
            client_conf = settings.FDFS_CLIENT_CONF

        if base_url is None:
            base_url = settings.FDFS_URL

        self.client_conf = client_conf
        self.base_url = base_url

    def save(self, name, content, max_length=None):
        client = Fdfs_client(self.client_conf)
        res = client.upload_by_buffer(content.read())

        '''
        @return dict {
            'Group name'      : group_name,
            'Remote file_id'  : remote_file_id,
            'Status'          : 'Upload successed.',
            'Local file name' : '',
            'Uploaded size'   : upload_size,
            'Storage IP'      : storage_ip
        } if success else None
        '''

        if res.get('Status') != 'Upload successed.':
            raise Exception('upload file to fast dfs failed.')

        file_name = res.get('Remote file_id')
        return file_name

    def exists(self, name):

        return False

    def url(self, name):

        return self.base_url + name
