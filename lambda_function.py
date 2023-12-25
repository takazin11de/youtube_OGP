import json
import urllib.request
import re

def lambda_handler(event, context):
    
    v_id=json.dumps(event["pathParameters"]["v_id"]).replace('"','')

    if len(v_id)==0:
        return make()
    v_id=v_id.replace('_c_', '-')
    v_id=v_id.replace('_b_', '/')
    v_id=v_id.replace('_a_', '_')

    url='https://www.youtube.com/watch?v='+v_id
    site_name='YouTube'
    content_type='video.movie'
    if re.match("sm\w*",v_id):
        url='https://www.nicovideo.jp/watch/'+v_id
        site_name='ニコニコ動画'
        content_type='video.other'
    if re.match("lv\w*",v_id):
        url='https://live.nicovideo.jp/watch/'+v_id
        site_name='ニコニコ生放送'
        content_type='website'
    if re.match("im\w*",v_id):
        url='https://seiga.nicovideo.jp/seiga/'+v_id
        site_name='ニコニコ静画（イラスト）'
        content_type='article'
    if re.search("/",v_id):
        url='https://note.com/'+v_id
        site_name='note（ノート）'
        content_type='article'

    response = urllib.request.urlopen(url)
    content=response.read().decode()
    title_list=re.findall('"og:title"\s*content="(.*?)"', content)
    img_list=re.findall('"og:image"\s*content="(.*?)"', content)
    if len(title_list)==1:
        title=title_list[0]
    else:
        return {
            'statusCode': 200,
            "headers": {"Content-Type": "text/html"},
            'body': '<!DOCTYPE html><html lang="ja"><head><meta charset="utf-8"><link rel="icon" href="data:image/x-icon;,">'\
                    '<title></title></head><body></body></html>'
        }
    return {
        'statusCode': 200,
        "headers": {"Content-Type": "text/html"},
        'body': '<!DOCTYPE html><html lang="ja"><head><meta charset="utf-8"><link rel="icon" href="data:image/x-icon;,">'\
                '<meta http-equiv="refresh" content="0;URL='+url+'">'\
                '<meta property="og:type" content="'+content_type+'">'\
                '<meta property="og:url" content="'+url+'">'\
                '<meta property="og:title" content="['+site_name+']'+title+'">'\
                '<meta property="og:image" content="'+img_list[0]+'">'\
                '<meta name="twitter:card" content="summary_large_image"><title></title></head><body></body></html>'
    }

def make():
    return{'statusCode': 200,
            "headers": {"Content-Type": "text/html"},
            'body':"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width">
<link rel="icon" href="data:image/x-icon;,">
<title></title>
<script>
function conv(){
  document.getElementById('input2').value= "";
  input1=document.getElementById('input1').value;

  input11 =input1.match(/youtube\.com\/watch\?v=((\w|-)*)/)
  input12 =input1.match(/youtu\.be\/((\w|-)*)/)
  input13 =input1.match(/youtube\.com\/live\/((\w|-)*)/)
  input14 =input1.match(/nicovideo\.jp\/watch\/(\w*)/) //movie,live
  input15 =input1.match(/nicovideo\.jp\/seiga\/(\w*)/) //seiga
  input16 =input1.match(/note\.com\/((\w|\/)*)/) //note.com


  if(input11!=null){
    input1_=input11[1];
  }
  if(input12!=null){
    input1_=input12[1];
  }
  if(input13!=null){
    input1_=input13[1];
  }
  if(input14!=null){
    input1_=input14[1];
  }
  if(input15!=null){
    input1_=input15[1];
  }
  if(input16!=null){
    input1_=input16[1];
  }
  if(input1_!=null){
    input1_=input1_.split(`_`).join(`_a_`);
    input1_=input1_.split(`\/`).join(`_b_`);
    input1_=input1_.split(`-`).join(`_c_`);
  }
  document.getElementById('input2').value= "https://videotmb.net/" + input1_;
  copy();

}
function copy(){
  var input2 = document.getElementById("input2");
  input2.select();
  document.execCommand("Copy");
}
</script>
<style>
  abbr,address,article,aside,audio,b,blockquote,body,canvas,caption,cite,code,dd,
  del,details,dfn,div,dl,dt,em,fieldset,figcaption,figure,footer,form,h1,h2,h3,h4,
  h5,h6,header,hgroup,html,i,iframe,img,ins,kbd,label,legend,li,mark,menu,nav,
  object,ol,p,pre,q,samp,section,small,span,strong,sub,summary,sup,table,tbody,td,
  tfoot,th,thead,time,tr,ul,var,video{margin:0;padding:0;border:0;outline:0;
  font-size:100%;vertical-align:baseline;background:transparent}body{line-height:1
  }article,aside,details,figcaption,figure,footer,header,hgroup,menu,nav,section{
  display:block}nav ul{list-style:none}blockquote,q{quotes:none}blockquote:after,
  blockquote:before,q:after,q:before{content:'';content:none}a{margin:0;padding:0;
  font-size:100%;vertical-align:baseline;background:transparent}ins{
  text-decoration:none}ins,mark{background-color:#ff9;color:#000}mark{font-style:
  italic;font-weight:700}del{text-decoration:line-through}abbr[title],dfn[title]{
  border-bottom:1px dotted;cursor:help}table{border-collapse:collapse;
  border-spacing:0}hr{display:block;height:1px;border:0;border-top:1px solid #ccc;
  margin:1em 0;padding:0}input,select{vertical-align:middle}*,:after,:before{
  box-sizing:border-box}
  body{
    font-family: arial,sans-serif;
    font-size: 14px;
  }
  body{
    padding: 10px;
  }
  h1{
    font-size: 20px;
  }
  p{
    padding: 3px
  }
  #input1{
    width:100%
  }
  #input2{
    width:100%
  }
  </style>
</head>
<body>
<h1>サムネアドレス変換器</h1>
<p>下記形式のURLを入力してください。</p>
<p>YouTube</p>
<p>「https://www.youtube.com/watch?v=******」</p>
<p>「https://youtu.be/******」等</p>
<p>YouTubeライブ配信</p>
<p>「https://www.youtube.com/live/******」</p>
<p>note.com</p>
<p>「https://note.com/******/*/******」</p>
<p>ニコニコ動画</p>
<p>「https://www.nicovideo.jp/watch/sm******」</p>
<p>ニコニコ生放送</p>
<p>「https://live.nicovideo.jp/watch/lv******」</p>
<p>ニコニコ静画</p>
<p>「https://seiga.nicovideo.jp/seiga/im******」</p><br>
<input type="text" id="input1" maxlength="50"><br><br>
<input type="button" value="サムネイルURL作成" onclick="conv()"><br><br>
<input type="text" id="input2"><br><br>
<input type="button" value="コピー" onclick="copy()"><br><br>
</body>
</html>
"""
    }
