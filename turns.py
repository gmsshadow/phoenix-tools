import positions as pos
import urllib2  # the lib that handles the url stuff
import os 
import json

current_path = os.path.dirname(os.path.realpath(__file__))
target_path=current_path+'/data/'
if not os.path.exists(target_path):
    os.makedirs(target_path)
position_path=target_path+'positions/'
if not os.path.exists(position_path):
    os.makedirs(position_path)
config_name=target_path+'config.json'
read_data=''
config={}
if os.path.exists(config_name):
    with open(config_name) as f:
        read_data = f.read()
        config=json.loads(read_data)
    f.closed

if config.has_key('positions')==False:
    config['positions']={}

for p in pos.pos_list:
    last_turn=0
    if config['positions'].has_key(p.data['num']):
        last_turn=int(config['positions'][p.data['num']])
    turn_day=0
    if p.data.has_key('turns') and p.data['turns'][0]:
         turn_day=p.data['turns'][0]
    ## download file if there is a new one
    if turn_day>last_turn:
        response = urllib2.urlopen('https://www.phoenixbse.com/index.php?a=xml&sa=turn_data&tid='+p.data['num']+'&uid=xxx&code=yyyy')
        data = response.read()
        day=p.data['turns'][0]
        if data!="":
            ## create directory tree
            day_path=position_path+str(turn_day)+'/'
            if not os.path.exists(day_path):
                os.makedirs(day_path)
            f = open(day_path+p.data['num']+'.html', 'w')
            ## save downloaded file info
            config['positions'].update({p.data['num']:turn_day})
            f.write(data)
            f.close()


f = open(config_name, 'w')
f.write(json.dumps(config))
f.close()
