# encoding:utf-8
import base64
from string import maketrans
from urlparse import unquote
from urllib import urlencode

OLD_STR = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
NEW_STR = "vSoajc7dRzpWifGyNxZnV5k+DHLYhJ46lt0U3QrgEuq8sw/XMeBAT2Fb9P1OIKmC"


def encode_demo(str_data):
    str_data = base64.b64encode(str_data)
    encode_tab = maketrans(OLD_STR, NEW_STR)
    return str_data.translate(encode_tab)


def decode_demo(str_data):
    decode_tab = maketrans(NEW_STR, OLD_STR)
    str_data = str_data.translate(decode_tab)
    return base64.b64decode(str_data)

def base64decodeForClickID(str_data):
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
    chars1 = "vSoajc7dRzpWifGyNxZnV5k+DHLYhJ46lt0U3QrgEuq8sw/XMeBAT2Fb9P1OIKmC";
    chars_combine = maketrans(chars1, chars)
    str_data = str_data.translate(chars_combine)
    return base64.b64decode(str_data)

if __name__ == '__main__':
    # key_name = "ad_backend|ad_backend_data|flow_tag_id|rand_value|backend_config|MW_adnum|MW_tnum"
    # set_key = set(key_name.split("|"))
    # pv
    expect = "NjAyOHwyODAwMHwwfDkwM3wxODA0NTc4MTJ8MjIzMDQ2MTE0N3xub3JtYWx8ZG91YmxlY2xpY2t8MzIweDUwfDh8YW5kcm9pZHw2LjAuMHx8c20tajUwMG18fHxCUnx8Mnx8anVzdGNvbnN8fGNvbS5vdXRmaXQ3Lm15dGFsa2luZ2FuZ2VsYWZyZWV8fDVhN2JjZGM2MzMzZjdmNDdlNWE2YzBlYXx8fHx8fDVhN2JjZGM2MzMzZjdmNDdlNWE2YzBlYXwxNzcuMS43MC4wfHx8fHx8MHwwfDZlOTlhODBhLTgyZWMtNDA1Ny1iNGZkLWE3OWFhMTAxNmZhM3x8fHNhbXN1bmd8fHxyYW5rX21vZGVsX2NhbXB8fDF8fHwsdGEsZm58eyJjYXJyaWVyIjoiIiwiY2l0eSI6ImFyYWd1YWluYSIsImN0eXBlIjoiMSIsInBhcnNlIjoiMCIsInJlcXR5cGUiOiJiIiwidHJhZmZpY190eXBlIjoiYXBwIn18MTUxODA2MzA0Nnx8MXxwdWItNDA2NzMxMzE5ODgwNTIwMHx8fHx8fGNvbS5vdXRmaXQ3Lm15dGFsa2luZ2FuZ2VsYWZyZWV8fHx8fHwxMzYxMDcwNDE1NTMyMjU2fHx8fHx8fHx8fDB8fHx8fHx8fHxbMC44LDAuOCwxLDFd"
    fact = "LdxThdi1WBKFiB2TJoPu47QgJkj/DFKwWAQ0HaiFH7Vefr5tiai2iFxQfnzrHaQriAvbDAlPfUDAWA5tfFNFHnx0WbHuH75XWFTXiURMDFDFiah9DFjbHaJ3f7cUH7zUHncrinH0fFDPfFiTHaheinVBHkjAGavMiavPfrVBiUh2iaJtfaRX"
    # imp
    # expect = "i%2BMM6ajBGdMbiAN26aj1YkK0JrQAJ7c6LF5P%2BAj1i%2BMe6ai%3D"
    # fact = "i%2BMeGUv1i%2BMeiUtIfAiTf%2BMeGUv1idMe6ai%3D"
    expect = base64.b64decode(unquote(expect).replace(" ", "+"))
    fact = base64decodeForClickID(unquote(fact).replace(" ", "+"))
    # fact = base64decodeForClickID(urlencode(fact))
    # print("mv")
    # print( expect)
    print("q",fact)
    # x = "|||||||doubleclick|VIDEO||ios|10.3.1|mi_2.7.9|iphone82c1|375x667|1||en-JP|wifi|44050|||MNormalAlphaModelRanker_old_1.0.0;10;497;26;0;26;1;1_filt_advertiser-2_fr_base|5a791c280ec1bc31c327e1a6||||||||66.102.0.103|||||||||C98B99BB-1B2F-434E-BE53-FD651B03FB6A||apple|66.102.0.103|59351bcfbf6949550d92a50c|5a791c280ec1bc31c3727e19|||||1||2603D94D-7465-4388-B0C3-BDFA40DCBE32,74C87BBD-C675-EE2A-7651-6EBAC72835EA|||||||||||||||||||||||||||||||||||||||||"
    # x = base64.b64encode(x)
    # # x = urlencode(x)
    # print(x)
    y = 'http://v11-tt.ixigua.com/58fbc2a9f3ef1f159f31dc1014cc488c/5a7c02e8/video/m/220cf6078ca7d7d4acdbce1f16b7f97c4d71152ea38000096e227507a42/'
    y = encode_demo(y)
    print(y)
