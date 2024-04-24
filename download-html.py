import requests

base_url = 'https://www.matweb.com/Search/MaterialGroupSearch.aspx?GroupID=178'  # group id

material_id = 'https://www.matweb.com/search/DataSheet.aspx?MatGUID=e5e92a1ae7f24e1b918bf4e65dbc7e52'# query_format = {"downloadformat": "iqy", "matguid": "915048dac2534185824edd1dfcc33b2b"}

# TODO this action matweb know that this is a download request, block by frequency enter
response = requests.get(material_id, auth=('zhenghuanhuan@zhejianglab.com', 'zhijiang2893'))
# response.xpath("//*[@id='lnkMatl_8971']/@href").get()
# '/search/DataSheet.aspx?MatGUID=f6d0bebbfc7248838243b7fa141431ba'

response = requests.get(material_id)
import time
time.sleep(20)
with open('matweb_data', 'wb') as file:
    file.write(response.content)

print('done.')