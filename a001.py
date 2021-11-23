import json
import urllib.request
import re

def lambda_handler(event, context):
    # TODO implement
    print(json.dumps(event))
    v_id=json.dumps(event["pathParameters"]["v_id"]).replace('"','')
    print(v_id)
    response = urllib.request.urlopen('https://www.youtube.com/watch?v='+v_id)
    print('url:', response.geturl())
    print('code:', response.getcode())
    print('Content-Type:', response.info()['Content-Type'])
    content=response.read().decode()
    #print(content)
    title_list=re.findall('"og:title"\s*content="(.*?)"', content)
    img_list=re.findall('"og:image"\s*content="(.*?)"', content)
    print('len:', len(title_list))
    print('len:', len(img_list))
    
    if len(title_list)==1:
        title=title_list[0]
    else:
        return {
            'statusCode': 200,
            "headers": {"Content-Type": "text/html"},
            'body': '<!DOCTYPE html><html lang="ja"><head><meta charset="utf-8"><link rel="icon" href="data:image/x-icon;,">'\
                    '<title></title></head><body></body></html>'
        }
    print('aaaa:',len(title_list[0]))
    print('aaaa:',len(img_list[0]))
    
    return {
        'statusCode': 200,
        "headers": {"Content-Type": "text/html"},
        'body': '<!DOCTYPE html><html lang="ja"><head><meta charset="utf-8"><link rel="icon" href="data:image/x-icon;,">'\
                '<meta http-equiv="refresh" content="0;URL=https://www.youtube.com/watch?v='+v_id+'">'\
                '<meta property="og:type" content="video.movie">'\
                '<meta property="og:url" content="https://www.youtube.com/watch?v='+v_id+'">'\
                '<meta property="og:title" content="[YouTube]'+title+'">'\
                '<meta property="og:image" content="'+img_list[0]+'">'\
                '<meta name="twitter:card" content="summary_large_image"><title></title></head><body></body></html>'
    }
