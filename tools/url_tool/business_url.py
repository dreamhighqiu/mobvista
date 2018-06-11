# encoding:utf-8
from base64_demo import decode_p, decode_q_mp
from config import DICT_PARAM_KEYS
from file_utils import write_log

SET_CHECK_NAME = {r"data.only_impression_url", r"data.ads.*.impression_url", r"data.ads.*.notice_url", "data.ads.*.click_url", r"data.ads.*.ad_tracking.*"}

def get_url_params_dict(url, url_name):
    # type: (object, object) -> object
    """将url转化为dict格式
    :rtype: object
    """
    dict_params = {}
    try:
        url_path, url_params = url.split("?")
        dict_params['url_path'] = url_path
        list_kv = url_params.split("&")
        for kv in list_kv:
            k, v = kv.split("=")
            if k in DICT_PARAM_KEYS.keys():
                v = get_url_dict_params(k, v, url_name)
            dict_params.setdefault(k, v)
    except StandardError, e:
        print(e)
        write_log("{0} is not correct: {1}".format(url_name, url), 'warn')
    return dict_params

def get_url_dict_params(param_name, param_value, url_name):
    """将特殊字段转化为dict格式
    :rtype: object
    """
    if not param_value:
        write_log("{1}: the value param {0} is empty"
                  .format(param_name, url_name), 'warn')
        return {param_name:param_value}
    param_k = DICT_PARAM_KEYS.get(param_name)
    if param_name in ("mp", "q", "csp"):
        param_v = decode_q_mp(param_value)
    else:
        param_v = decode_p(param_value)
    param_v = param_v.split("|")
    if len(param_v) < 2:
        write_log("build {0} faild:\n{2}: {1}"
                  .format(param_name, param_v, url_name), 'error')
        return {param_name: param_value}
    elif len(param_k) != len(param_v):
        write_log("{3}: build {0}, the size of key {1} is diff to size of value {2}"
                  .format(param_name, len(param_k), len(param_v), url_name), 'warn')

    return dict(zip(param_k, param_v))



if __name__ == "__main__":
    url = "https://test-net.rayjump.com/click?k=5ab477164e52423c75382ba1&p=fHx8fHx8fHJld2FyZGVkX3ZpZGVvfFZJREVPfHxpb3N8MTEuMS4yfG1pXzMuMy4yfGlwaG9uZTgyYzF8Mzc1eDgxMnwxfHxlbi1KUHx3aWZpfDQ0MDUwfHx8TU5vcm1hbEFscGhhTW9kZWxSYW5rZXJfbmV3XzEuMC4wOzEwOzQ5Nzs0OzA7NDs0OzFfYmFzZXw1YWI0NzcxNjRlNTI0MjNjNzUzODJiOTF8fHx8fHx8fDM5LjEwOS4xMjQuOTN8fHx8fHx8fHxDOThCOTlCQi0xQjJGLTQzNEUtQkU1My1GRDY1MUIwM0ZCNkF8fGFwcGxlfDE5Mi4xNjguMS4xNzl8NWFiNDc3MTY0ZTUyNDIzYzc1NzM4MmI3fDVhYjQ3NzE2NGU1MjQyM2M3NTczODJiOHx8fHx8NXx8MjYwM0Q5NEQtNzQ2NS00Mzg4LUIwQzMtQkRGQTQwRENCRTMyLDc0Qzg3QkJELUM2NzUtRUUyQS03NjUxLTZFQkFDNzI4MzVFQXx8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fA%3D%3D&q=a_i09M6dxQhbNwYr5TWgzt4ku2Y%2Bv%2FDFKw6a5tDUNbfAjFf7V2iUNBiFibfni9irzti%2BM2DkRTfAhefUxQfnRTiUfUfAVAGaz0GncIfnvPf%2BMBfnR2G%2BMeiANe6aN2fbMefavbiUNbfAcIio9ef%2BMMWUj267csHFKIfbeRZbMwi%2BMM6acIiUVBfnQIiA3M6al%2FiB9T67KMHkPth7QIG%2BeIW%2BeofdeIiUVBfnQI6dMM6acIideSinvAigMM6deIigMM6aSIidMe6dMe6deIidMe6cs0io9efZRsRUv%2FinV0Wajsi52IiN%3D%3D&r=&al=0.15%2C0.5%2C0.5%2C0&csp=i%2BMeGUjTiahBfahbinEe6acIGavFfdMeGUEB6a5IfN%3D%3D&notice=1"
    url = "https://test-net.rayjump.com/click?k=5ab477164e52422eb4492748&p=fHx8fHx8fGFwcHdhbGx8fHxpb3N8OS4zLjV8bWlfMi40LjB8aXBob25lNiwyfDMyMHg1Njh8MXx8emgtSGFucy1BU3wyZ3x8fHxNTm9ybWFsQWxwaGFNb2RlbFJUZXN0UmFua2VyX29sZF8xLjAuMDsxMDs2OTE7MTMxOzA7MTMxOzA7fDVhYjNjNTU5NGU1MjQyMmViNDk0OTEyM3x8fHx8fHx8NDIuMTk5LjU5LjE1M3x8fHx8fHx8fDM1OTUxRDZBLURCNjYtNDdBMS04Q0QwLURCMUU5RTBEMzNDQ3x8YXBwbGV8fDU5NjZkODkzYWMwZjRlNWUxYzQ4YjVmNnx8fHx8fDV8fDFENzEwREY5LTc1MEMtNDkyMy1BNENGLTMwNjI5RDFGOUM2Qix8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fA%3D%3D&q=a_i09M6dxQhbNwYr5TWgzt4ku2Y%2Bv%2FDFKw6a5tDUNbfAjFf7V2iUNBir50faNPiUhTGdM2DkRTfAhefUxQfnRTiUzQDUNPfa3BfrHIfnvPf%2BMBfnR2G%2BMeiANe6aN2fbMefavbiUNbfAcIio9ef%2BMMWUj267c3%2BbfQhgHQhgMb6jtW6oTe6aSIi%2BMBfnR2G%2BMAGnSIGo9AWUxIYbSQYrcML%2BMP6dMw6a5IidMBfnR2G%2BeIidMM6aSI6jReiaiB6dMM6dMB6aRMiavAinN2fUfIideIi%2BMM6dMM6deIideYRUv%2FinV0WoRMWUj2R0M0iZRsRUj0%2B%2BMM&r=eyJnaWQiOiI4Mjg5Y2RkMTAzYTkxNGVmY2UwNmViZDMyYzkxMmI3MyIsInRwaWQiOjUwMSwiY3JhdCI6OCwiYWR2X2NyaWQiOjAsImljYyI6MCwiZ2xpc3QiOiJDVEFfQlVUVE9OLO%2B%2FvSwsfElDT04s77%2B9LCx8U0laRV8xMjAweDYyNyzvv70sLHxWSURFTyzvv70sLHxBUFBfTkFNRSzvv70sLHxBUFBfREVTQyzvv70sLHxBUFBfUkFURSzvv70sLCIsInBpIjowLjE1LCJwbyI6MC4xNX0%3D&al=0.15%2C0.5%2C0.5%2C0&csp=&notice=1"

    d = get_url_params_dict(url, "imp")
    print(d.get('p'))
    print(d.get('q'))
