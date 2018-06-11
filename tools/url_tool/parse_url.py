# encoding:utf-8
import json
from file_utils import write_log
from business_url import get_url_params_dict, get_url_dict_params

SET_CHECK_NAME = {r"data.only_impression_url", r"data.ads.*.impression_url", r"data.ads.*.notice_url", "data.ads.*.click_url", r"data.ads.*.ad_tracking.*"}


def run(action_type):
    if action_type == "1":
        url = raw_input("input the url: ").strip()
        d = get_url_params_dict(url, "url")
        c_list_param = ["p", "mp", "q", "csp", "r"]
        for c_param in c_list_param:
            write_log(c_param.center(20, "-"))
            c_value = d.get(c_param)
            if c_value and isinstance(c_value, dict):
                c_value = json.dumps(c_value, indent=4)
            write_log(c_value)
    else:
        param_name = raw_input("p | q | mp | csp |r, choose param name: ").strip()
        param_value = raw_input("input param value: ").strip()
        c_value = get_url_dict_params(param_name, param_value, "test")
        if c_value and isinstance(c_value, dict):
            c_value = json.dumps(c_value, indent=4)
        write_log(c_value)


if __name__ == "__main__":
    # url = "https://test-net.rayjump.com/impression?k=5ab886db4e52423c76089edb&p=fHx8fHx8fG5hdGl2ZXwxMjAweDYyN3x8aW9zfDkuMy41fG1pXzMuMS4wfGlwaG9uZTYyYzJ8MzIweDU2OHwxfHx6aC1IYW5zLUFTfDJnfHx8fE1Ob3JtYWxBbHBoYU1vZGVsUlRlc3RSYW5rZXJfb2xkXzEuMC4wOzEwOzY5MTsxMTswOzExOzA7fDVhYjg4NmRiNGU1MjQyM2M3NjA4OWVkYnx8fHx8fHx8MzkuMTA5LjEyNC45M3x8fHx8fHx8fDM1OTUxRDZBLURCNjYtNDdBMS04Q0QwLURCMUU5RTBEMzNDQ3x8YXBwbGV8MTkyLjE2OC4xLjE3OXw1YWI4ODZkYjRlNTI0MjNjNzY3MDg5ZWJ8NWFiODg2ZGI0ZTUyNDIzYzc2NzA4OWVjfHx8fHwxfHxCNzQ5QjQ2Ni0yRjQ2LTRFNkEtQURCQS04ODAxNTdDRTI5MkEsfHx8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fDV8fA%3D%3D&q=a_i09M6dxQhbNwYr5TWgzt4ku2Y%2Bv%2FDFKw6a5tDUl9frx0f7V2iUNBiFibfUv9Gk5QDgM2DkR9GaH3DUxQfnRTiUfUfADMGaQQH7zIfUiAf%2BMBiANeG%2BMeiUieibMTfnJIinhbfniFfni96ai26ai267csHFKIfbeRZbMwi%2BMM6acIiUiTinQIiA3M6aR%2FGZ9M67KMHkPth7QIigeIW%2BeSi%2BeIiUiTinQI6dMM6acIidMT6aSI6dMB6aRMiavBiaNAiUtIidMM6acI6acI6dMe6acIkBRAfZRsRUi2R0MeWacJ6aj%3D&x=0&r=eyJnaWQiOiI2MThiNjI2MDliNmJkMzhjOTBkOTM4MGI0NGMyY2E5ZiIsInRwaWQiOjQwMiwiY3JhdCI6MywiYWR2X2NyaWQiOjAsImljYyI6MCwiZ2xpc3QiOiIxMDYsMjAwMDIwNDMyOCwwLDB8NDAxLDIwMDAyMDQwODMsMCwwfDQwMiwyMDAwMTM4NDY5LDAsMHw0MDMsMjAwMDIwNDE4NywwLDB8NDA0LDIwMDAyMDQyMzYsMCwwfDQwNSwyMDAwMjA0Mjg0LDAsMCIsInBpIjozNSwicG8iOjM1fQ%3D%3D&al=&csp=i%2BMeGUjbfAVAfUVAGaEe6acIfAhPG%2BMeGUEB6acIiN%3D%3D"
    c_action_type = raw_input("1-parse whole url|2-parse singal param; choose parse type index: ").strip()
    run(c_action_type)
    # write_log decode_p("eyJnaWQiOiI2MThiNjI2MDliNmJkMzhjOTBkOTM4MGI0NGMyY2E5ZiIsInRwaWQiOjQwMiwiY3JhdCI6MywiYWR2X2NyaWQiOjAsImljYyI6MCwiZ2xpc3QiOiIxMDYsMjAwMDIwNDMyOCwwLDB8NDAxLDIwMDAyMDQwODMsMCwwfDQwMiwyMDAwMTM4NDY5LDAsMHw0MDMsMjAwMDIwNDE4NywwLDB8NDA0LDIwMDAyMDQyMzYsMCwwfDQwNSwyMDAwMjA0Mjg0LDAsMCIsInBpIjozNSwicG8iOjM1fQ%3D%3D")


