import re, yaml

from sub_convert import sub_convert
from list_merge import sub_merge

Eterniy_file = './Subscription/GreenFishPool'
Eternity_yml_file = './Subscription/Clash/GreenFishPool'
readme = './README.md'


sub_list_json = './sub/sub_list.json'


class NoAliasDumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True

def eternity_convert(content, config, output, provider_file_enabled=False):
    try:
        file_eternity = open(content, 'r', encoding='utf-8')
        sub_content = file_eternity.read()
        file_eternity.close()
    except Exception as err:
        print(err)
        sub_content = content
    all_provider = sub_convert.convert(sub_content,'content','YAML',custom_set={ 'dup_rm_enabled': False,'format_name_enabled': True})


    config_f = open(config_file, 'r', encoding='utf-8')
    config_raw = config_f.read()
    config_f.close()
    
    config = yaml.safe_load(config_raw)

    all_provider_dic = {'proxies': []}
    others_provider_dic = {'proxies': []}
    us_provider_dic = {'proxies': []}
    hk_provider_dic = {'proxies': []}
    sg_provider_dic = {'proxies': []}
    provider_dic = {
        'all': all_provider_dic,
        'others': others_provider_dic,
        'us': us_provider_dic,
        'hk': hk_provider_dic,
        'sg': sg_provider_dic
    }
    for key in eternity_providers.keys():
        provider_load = yaml.safe_load(eternity_providers[key])
        provider_dic[key].update(provider_load)

    all_name = []
    others_name = []
    us_name = []
    hk_name = []
    sg_name = [] 
    name_dict = {
        'all': all_name,
        'others': others_name,
        'us': us_name,
        'hk': hk_name,
        'sg': sg_name
    }
    for key in provider_dic.keys():
        if not provider_dic[key]['proxies'] is None:
            for proxy in provider_dic[key]['proxies']:
                name_dict[key].append(proxy['name'])
        if provider_dic[key]['proxies'] is None:
            name_dict[key].append('DIRECT')
    proxy_groups = config['proxy-groups']
    proxy_group_fill = []
    for rule in proxy_groups:
        if rule['proxies'] is None:
            proxy_group_fill.append(rule['name'])
    for rule_name in proxy_group_fill:
        for rule in proxy_groups:
            if rule['name'] == rule_name:
                if '美国' in rule_name:
                    rule.update({'proxies': us_name})
                elif '香港' in rule_name:
                    rule.update({'proxies': hk_name})
                elif '狮城' in rule_name or '新加坡' in rule_name:
                    rule.update({'proxies': sg_name})
                elif '其他' in rule_name:
                    rule.update({'proxies': others_name})
                else:
                    rule.update({'proxies': all_name})
    config.update(all_provider_dic)
    config.update({'proxy-groups': proxy_groups})

    """
    yaml_format = ruamel.yaml.YAML() # https://www.coder.work/article/4975478
    yaml_format.indent(mapping=2, sequence=4, offset=2)
    config_yaml = yaml_format.dump(config, sys.stdout)
    """
    config_yaml = yaml.dump(config, default_flow_style=False, sort_keys=False, allow_unicode=True, width=750, indent=2, Dumper=NoAliasDumper)
    
    Eternity_yml = open(output, 'w', encoding='utf-8')
    Eternity_yml.write(config_yaml)
    Eternity_yml.close()

if __name__ == '__main__':
    convert = eternity_convert(Eterniy_file, config_file, output=Eternity_yml_file)
    sub_merge.readme_update(readme,sub_merge.read_list(sub_list_json))